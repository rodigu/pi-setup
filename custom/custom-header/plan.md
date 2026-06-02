# Plan: Custom Pi Header Extension

## Goal

Create a custom header extension for Pi that combines two ASCII art sources into a single side-by-side display. The left side shows a brain image, and the right side shows a text logo with runtime metadata. The extension will replace Pi's default startup header with this custom layout.

## Final Outcome

A single TypeScript file (`custom-header.ts`) that:
- Loads and parses two markdown files containing ASCII art
- Combines them side-by-side at render time
- Substitutes `{{ pi_version }}` with the actual Pi version dynamically
- Applies themed coloring (accent for art, muted for metadata)
- Gracefully handles narrow terminals
- Registers a `/builtin-header` command to restore the default header

---

## Reference Files

All files are in the current working directory (`/root/src`):

| File | Description |
|------|-------------|
| `perola-header.md` | Documentation explaining how Pi's custom header API works, including `ctx.ui.setHeader()`, the `render()`/`invalidate()` contract, color tokens, and installation paths. **Read this first for API reference.** |
| `perola-header.ts` | Working example extension that replaces the default header with a simple greeting. Use this as the structural template for `custom-header.ts`. |
| `image-header.md` | ASCII art of a brain/head (~26 chars wide, ~20 lines tall). This is the left column of the combined header. |
| `info-header.md` | ASCII art text logo ("CEJAM") plus metadata lines. Contains placeholder `{{ pi_version }}` that must be replaced at runtime. This is the right column. |
| `header.md` | Sample output showing the expected final result: brain art on the left, info text on the right, combined side-by-side. Use this to validate the output. |

---

## Implementation Details

### Step 1: Project Setup

Create `custom-header.ts` in the same directory. The file will follow the same structure as `perola-header.ts`:

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  // implementation here
}
```

### Step 2: Read and Parse ASCII Art Files

At module load time (or lazily on first render), read both markdown files and split them into line arrays:

```typescript
import { readFileSync } from "fs";
import { join, dirname } from "path";

// Resolve paths relative to this extension file's location
const __dirname = dirname(new URL(import.meta.url).pathname);

const brainLines = readFileSync(join(__dirname, "image-header.md"), "utf-8")
  .split("\n");

const infoLines = readFileSync(join(__dirname, "info-header.md"), "utf-8")
  .split("\n");
```

**Note:** The files must be in the same directory as `custom-header.ts` (i.e., `.pi/extensions/` or `~/.pi/agent/extensions/`).

### Step 3: Template Substitution

Create a helper function to replace placeholders in the info lines:

```typescript
function substituteTemplates(lines: string[], vars: Record<string, string>): string[] {
  return lines.map(line => {
    let result = line;
    for (const [key, value] of Object.entries(vars)) {
      result = result.replace(new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, "g"), value);
    }
    return result;
  });
}
```

At render time, call this with the actual Pi version:

```typescript
const processedInfo = substituteTemplates(infoLines, {
  pi_version: pi.version || "unknown",
});
```

**Determine how to get Pi version:** Check if `pi.version` exists on the `ExtensionAPI` object. If not, fall back to reading from `process.env` or parsing from `pi --version` output. If no version is available, use a placeholder like `"unknown"`.

### Step 4: Side-by-Side Layout Engine

Create a function that combines two arrays of lines horizontally:

```typescript
function combineColumns(left: string[], right: string[], gap: number = 3): string[] {
  const maxLeftWidth = Math.max(...left.map(l => l.length));
  const totalLines = Math.max(left.length, right.length);
  const separator = " ".repeat(gap);
  const result: string[] = [];

  for (let i = 0; i < totalLines; i++) {
    const leftLine = (left[i] || "").padEnd(maxLeftWidth);
    const rightLine = right[i] || "";
    result.push(leftLine + separator + rightLine);
  }

  return result;
}
```

### Step 5: Apply Theme Coloring

Apply colors to the combined output:

- **Brain art** (left column): `theme.fg("accent", line)` — makes it stand out
- **Text logo** (right column, top section): `theme.fg("text", line)` — default foreground
- **Metadata lines** (right column, `**ver**:` and `**pi version**:`): `theme.fg("muted", line)` — secondary color
- **Separator line** (`---...`): `theme.fg("dim", line)` — subtle divider

Implementation approach: Color each column *before* combining, so line lengths stay consistent:

```typescript
const coloredBrain = brainLines.map(line => theme.fg("accent", line));

const coloredInfo = processedInfo.map(line => {
  if (line.match(/^\*\*ver\*\*:|^\*\*pi version\*\*:/)) {
    return theme.fg("muted", line);
  }
  if (line.match(/^-+$/)) {
    return theme.fg("dim", line);
  }
  return theme.fg("text", line);
});

const combined = combineColumns(coloredBrain, coloredInfo);
```

### Step 6: Render and Invalidate

Implement the `render()` and `invalidate()` methods:

```typescript
render(width: number): string[] {
  // If terminal is too narrow, fall back to info-only or brain-only
  const combined = combineColumns(coloredBrain, coloredInfo);
  const maxLineWidth = Math.max(...combined.map(l => stripAnsi(l).length));

  if (maxLineWidth > width) {
    // Narrow terminal fallback: show only the info column
    return coloredInfo;
  }

  return combined;
},

invalidate() {
  // Clear any cached themed strings if needed
  // For this implementation, we recompute each time, so no-op
},
```

**Note:** You'll need a `stripAnsi()` helper to measure actual visible width (ANSI codes don't take screen space). A simple regex works:

```typescript
function stripAnsi(str: string): string {
  return str.replace(/\x1b\[[0-9;]*m/g, "");
}
```

### Step 7: Register the Extension and Command

Hook into `session_start` and register the `/builtin-header` command:

```typescript
pi.on("session_start", async (_event, ctx) => {
  if (!ctx.hasUI) return;

  ctx.ui.setHeader((_tui, theme) => {
    // Build colored lines here using theme
    const coloredBrain = brainLines.map(line => theme.fg("accent", line));
    const coloredInfo = substituteTemplates(infoLines, {
      pi_version: pi.version || "unknown",
    }).map(line => {
      if (line.match(/^\*\*ver\*\*:|^\*\*pi version\*\*:/)) return theme.fg("muted", line);
      if (line.match(/^-+$/)) return theme.fg("dim", line);
      return theme.fg("text", line);
    });

    return {
      render(width: number): string[] {
        const combined = combineColumns(coloredBrain, coloredInfo, 3);
        const maxLineWidth = Math.max(...combined.map(l => stripAnsi(l).length));
        if (maxLineWidth > width) return coloredInfo; // fallback for narrow terminals
        return combined;
      },
      invalidate() {},
    };
  });
});

pi.registerCommand("builtin-header", {
  description: "Restore pi's default startup header",
  handler: async (_args, ctx) => {
    ctx.ui.setHeader(undefined);
    ctx.ui.notify("Default header restored.", "info");
  },
});
```

---

## File Placement

Copy `custom-header.ts` (along with `image-header.md` and `info-header.md`) to:

| Path | Scope |
|------|-------|
| `~/.pi/agent/extensions/` | Global — applies to every project |
| `.pi/extensions/` | Project-local — only for this repo |

All three files must be in the **same directory** since the extension reads the markdown files relative to its own location.

---

## Validation

After installation, run `/reload` in Pi and verify:

1. The header displays the brain art on the left and info text on the right
2. `{{ pi_version }}` is replaced with the actual version (e.g., `v0.76.0`)
3. Colors match the current theme (accent for brain, muted for metadata)
4. Narrowing the terminal falls back to info-only display
5. Running `/builtin-header` restores the default Pi header

Compare output against `header.md` for visual correctness.

---

## Potential Issues

| Issue | Mitigation |
|-------|------------|
| `pi.version` not available on `ExtensionAPI` | Fall back to `"unknown"` or parse from environment |
| Files not found at runtime | Throw clear error with path hint during `readFileSync` |
| ANSI strip regex incomplete | Test with actual theme output; expand regex if needed |
| Terminal width calculation off-by-one | Use `stripAnsi()` consistently; test at various widths |
