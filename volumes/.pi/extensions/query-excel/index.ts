/**
 * Query Excel Extension
 *
 * Registers a tool for querying Excel files with SQL using Polars.
 * Spawns a Python subprocess that reads Excel sheets and executes SQL queries.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { spawn } from "node:child_process";
import { join, dirname } from "node:path";
import { existsSync } from "node:fs";

// Resolve Python script path relative to this extension
const __dirname = dirname(new URL(import.meta.url).pathname);
const PYTHON_SCRIPT = join(__dirname, "script.py");

// Tool parameters schema
const QUERY_EXCEL_PARAMS = Type.Object({
  filepath: Type.String({ description: "Full absolute path to the Excel file" }),
  query: Type.String({ description: "SQL query in Polars SQL dialect" }),
});

// Result types
interface QuerySuccess {
  data: Record<string, unknown>[];
  columns: string[];
  row_count: number;
  warnings?: string[];
}

interface QueryError {
  error: string;
}

type QueryResult = QuerySuccess | QueryError;

/**
 * Execute the Python query_excel script as a subprocess.
 */
function executeQueryExcel(
  filepath: string,
  query: string,
  signal?: AbortSignal,
): Promise<QueryResult> {
  return new Promise((resolve, reject) => {
    // Check Python script exists
    if (!existsSync(PYTHON_SCRIPT)) {
      reject(new Error(`Python script not found: ${PYTHON_SCRIPT}`));
      return;
    }

    const child = spawn("python3", [PYTHON_SCRIPT, "--filepath", filepath, "--query", query], {
      stdio: ["ignore", "pipe", "pipe"],
      detached: true,
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let timeoutHandle: NodeJS.Timeout | undefined;

    // 30-second timeout
    timeoutHandle = setTimeout(() => {
      timedOut = true;
      if (child.pid) {
        try {
          process.kill(-child.pid, "SIGKILL");
        } catch {
          child.kill("SIGKILL");
        }
      }
    }, 30_000);

    child.stdout?.on("data", (data: Buffer) => {
      stdout += data.toString();
    });

    child.stderr?.on("data", (data: Buffer) => {
      stderr += data.toString();
    });

    // Handle abort signal
    const onAbort = () => {
      if (child.pid) {
        try {
          process.kill(-child.pid, "SIGKILL");
        } catch {
          child.kill("SIGKILL");
        }
      }
    };

    signal?.addEventListener("abort", onAbort, { once: true });

    child.on("error", (err) => {
      if (timeoutHandle) clearTimeout(timeoutHandle);
      signal?.removeEventListener("abort", onAbort);
      reject(new Error(`Failed to spawn process: ${err.message}`));
    });

    child.on("close", (code) => {
      if (timeoutHandle) clearTimeout(timeoutHandle);
      signal?.removeEventListener("abort", onAbort);

      if (signal?.aborted) {
        reject(new Error("Query cancelled"));
        return;
      }

      if (timedOut) {
        reject(new Error("Query timed out after 30 seconds"));
        return;
      }

      // Try to parse stdout as JSON
      if (stdout.trim()) {
        try {
          const result = JSON.parse(stdout.trim()) as QueryResult;
          resolve(result);
          return;
        } catch {
          // Not valid JSON, fall through to error
        }
      }

      // Error cases
      if (code !== 0) {
        const errorMsg = stderr.trim() || stdout.trim() || "Unknown error";
        reject(new Error(`Query failed (exit ${code}): ${errorMsg.slice(0, 200)}`));
        return;
      }

      // Empty output with exit 0
      resolve({ data: [], columns: [], row_count: 0 });
    });
  });
}

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "query_excel",
    label: "Query Excel",
    description: "Query Excel files with SQL using Polars",
    promptSnippet: "Query Excel files with SQL",
    promptGuidelines: [
      "Use query_excel when the user wants to analyze or query Excel data.",
      "Provide `filepath` (full absolute path) and `query` (Polars SQL).",
      "Use query_excel in place of read or bash for Excel files — they are binary.",
      "Query SELECT * FROM _AVAILABLE_SHEETS to discover available tables.",
      "Use DESCRIBE table or SHOW COLUMNS FROM table to explore schema before querying.",
      "query_excel returns a sample of 5 rows and at most 5 columns.",
      "Use WHERE filters and aggregates (SUM, AVG, COUNT) to get exactly what you need.",
    ],
    parameters: QUERY_EXCEL_PARAMS,
    async execute(_toolCallId, params, signal) {
      const result = await executeQueryExcel(params.filepath, params.query, signal);

      if ("error" in result) {
        return {
          content: [{ type: "text", text: `Error: ${result.error}` }],
          details: { error: result.error },
          isError: true,
        };
      }

      // Format output
      const lines: string[] = [];

      if (result.warnings?.length) {
        for (const warning of result.warnings) {
          lines.push(`⚠️ ${warning}`);
        }
        lines.push("");
      }

      // Table output
      if (result.data.length === 0) {
        lines.push("No results.");
      } else {
        // Header
        lines.push(result.columns.join("\t"));
        lines.push("-".repeat(result.columns.join("\t").length));

        // Rows
        for (const row of result.data) {
          const values = result.columns.map((col) => {
            const val = row[col];
            return val === null ? "NULL" : String(val);
          });
          lines.push(values.join("\t"));
        }

        lines.push("");
        lines.push(`(${result.row_count} rows shown)`);
      }

      return {
        content: [{ type: "text", text: lines.join("\n") }],
        details: {
          columns: result.columns,
          row_count: result.row_count,
          warnings: result.warnings,
        },
      };
    },
  });
}
