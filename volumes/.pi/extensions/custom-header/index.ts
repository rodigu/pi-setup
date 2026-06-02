/**
 * Custom Header Extension
 *
 * Combines two ASCII art markdown files side-by-side:
 *   - Left column:  an image (e.g. brain art)
 *   - Right column: a text logo with metadata (e.g. info-header.md)
 *
 * The info file may contain {{ pi_version }} placeholders that are
 * substituted at render time.
 *
 * INSTALLATION:
 *   1. Copy this file plus image-header.md and info-header.md to:
 *        - ~/.pi/agent/extensions/   (global, all projects)
 *        - .pi/extensions/           (project-local)
 *
 *   2. Restart pi (or run /reload to hot-load)
 *
 *   3. To restore the default header, run /builtin-header
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { VERSION } from "@earendil-works/pi-coding-agent";
import { readFileSync } from "fs";
import { join, dirname } from "path";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Strip ANSI escape sequences so we can measure visible character width. */
function stripAnsi(str: string): string {
  return str.replace(/\x1b\[[0-9;]*m/g, "");
}

/**
 * Parse lightweight markdown inline formatting and apply theme styles.
 * Supports: **bold**, *italic*, and bare text.
 */
function renderMarkdown(
  text: string,
  theme: { bold(s: string): string; italic(s: string): string },
): string {
  // Process bold first (**...**), then italic (*...*)
  // Use a single pass to avoid double-processing
  return text.replace(/\*\*(.+?)\*\*|\*(.+?)\*/g, (match, bold, italic) => {
    if (bold !== undefined) return theme.bold(bold);
    if (italic !== undefined) return theme.italic(italic);
    return match;
  });
}

/**
 * Replace `{{ key }}` placeholders in every line.
 * Keys are matched case-sensitively; surrounding whitespace is tolerated.
 */
function substituteTemplates(
  lines: string[],
  vars: Record<string, string>,
): string[] {
  return lines.map((line) => {
    let result = line;
    for (const [key, value] of Object.entries(vars)) {
      result = result.replace(
        new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, "g"),
        value,
      );
    }
    return result;
  });
}

/**
 * Combine two columns of text side-by-side.
 *
 * - Left lines are right-padded to the widest visual line so that the
 *   right column starts at a consistent horizontal position.
 * - A fixed-width gap separates the two columns.
 * - If one column has fewer lines than the other, the missing lines
 *   are treated as empty.
 */
function combineColumns(
  left: string[],
  right: string[],
  gap: number = 3,
): string[] {
  const maxLeftWidth = Math.max(0, ...left.map((l) => stripAnsi(l).length));
  const totalLines = Math.max(left.length, right.length);
  const separator = " ".repeat(gap);
  const result: string[] = [];

  for (let i = 0; i < totalLines; i++) {
    const rawLeft = left[i] ?? "";
    const visibleLeft = stripAnsi(rawLeft);
    const padding = " ".repeat(maxLeftWidth - visibleLeft.length);
    const rightLine = right[i] ?? "";
    result.push(rawLeft + padding + separator + rightLine);
  }

  return result;
}

// ---------------------------------------------------------------------------
// Extension entry point
// ---------------------------------------------------------------------------

export default function (pi: ExtensionAPI) {
  // Resolve paths relative to this extension file's location
  const __dirname = dirname(new URL(import.meta.url).pathname);

  // Load the two ASCII art sources
  const brainLines = readFileSync(join(__dirname, "image-header.md"), "utf-8")
    .split("\n")
    .map((l) => l.trimEnd()); // strip trailing whitespace (spaces / CR)

  const infoLines = readFileSync(join(__dirname, "info-header.md"), "utf-8")
    .split("\n")
    .map((l) => l.trimEnd());

  // Register a command to restore pi's built-in header
  pi.registerCommand("builtin-header", {
    description: "Restore pi's default startup header",
    handler: async (_args, ctx) => {
      ctx.ui.setHeader(undefined);
      ctx.ui.notify("Default header restored.", "info");
    },
  });

  // Set the custom header when a session starts
  pi.on("session_start", async (_event, ctx) => {
    if (!ctx.hasUI) return;

    ctx.ui.setHeader((_tui, theme) => {
      // --- Prepare themed columns ---

      // Left: brain art in accent color
      const coloredBrain = brainLines.map((line) =>
        theme.fg("accent", line),
      );

      // Right: substitute version placeholder, then apply per-line coloring
      const processedInfo = substituteTemplates(infoLines, {
        pi_version: `v${VERSION}`,
      });

      const coloredInfo = processedInfo.map((line) => {
        // Separator lines (all dashes) → dim
        if (/^-+$/.test(line)) {
          return theme.fg("dim", line);
        }
        // Parse inline markdown (**bold**, *italic*) using theme styles
        const rendered = renderMarkdown(line, theme);
        // Metadata lines (**key**: value) → muted color
        if (/^\*\*[^*]+\*\*:/.test(line)) {
          return theme.fg("muted", rendered);
        }
        // Everything else → default text color
        return theme.fg("text", rendered);
      });

      // --- Build the header object ---
      return {
        render(width: number): string[] {
          const gap = 3;
          const combined = combineColumns(coloredBrain, coloredInfo, gap);

          // If the combined output is wider than the terminal, fall back
          // to showing only the info column (typically narrower).
          const maxLineWidth = Math.max(
            0,
            ...combined.map((l) => stripAnsi(l).length),
          );
          if (maxLineWidth > width) {
            return coloredInfo;
          }

          return combined;
        },

        invalidate() {
          // Nothing cached — colours are recomputed on every render().
        },
      };
    });
  });
}
