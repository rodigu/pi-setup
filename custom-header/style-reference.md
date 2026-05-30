# Pi TUI Style Reference

All styling in pi extensions uses the `theme` object passed to render callbacks. Styles are applied by wrapping text in method calls that inject ANSI escape codes into the string.

## Text Styles

| Method | Effect | Example |
|--------|--------|---------|
| `theme.bold(text)` | **Bold** | `theme.bold("Important")` |
| `theme.italic(text)` | *Italic* | `theme.italic("emphasis")` |
| `theme.strikethrough(text)` | ~~Strikethrough~~ | `theme.strikethrough("deleted")` |

Combine with colors by nesting:

```typescript
theme.fg("accent", theme.bold("bold and colored"))
```

## Foreground Colors

Apply with `theme.fg(token, text)`.

### General

| Token | Typical appearance | Use for |
|-------|-------------------|---------|
| `"text"` | Default foreground | Body text |
| `"accent"` | Bright highlight (logo, cursor, selected items) | Headings, emphasis |
| `"muted"` | Subdued | Secondary info, labels |
| `"dim"` | Very faint | Tertiary, timestamps, hints |

### Status

| Token | Typical appearance | Use for |
|-------|-------------------|---------|
| `"success"` | Green | Confirmations, completions |
| `"error"` | Red | Errors, failures |
| `"warning"` | Yellow | Caution, alerts |

### Borders

| Token | Typical appearance | Use for |
|-------|-------------------|---------|
| `"border"` | Normal | Standard borders |
| `"borderAccent"` | Bright | Highlighted/focused borders |
| `"borderMuted"` | Subtle | Editor borders |

### Messages

| Token | Use for |
|-------|---------|
| `"userMessageText"` | User message foreground |
| `"customMessageText"` | Extension message foreground |
| `"customMessageLabel"` | Extension message label/header |

### Tools

| Token | Use for |
|-------|---------|
| `"toolTitle"` | Tool name in tool call rows |
| `"toolOutput"` | Tool output text |

### Diffs

| Token | Typical appearance | Use for |
|-------|-------------------|---------|
| `"toolDiffAdded"` | Green | Added lines |
| `"toolDiffRemoved"` | Red | Removed lines |
| `"toolDiffContext"` | Neutral | Context lines |

### Markdown

| Token | Use for |
|-------|---------|
| `"mdHeading"` | `#` headings |
| `"mdLink"` | Link text |
| `"mdLinkUrl"` | Link URL |
| `"mdCode"` | Inline `` `code` `` |
| `"mdCodeBlock"` | Code block content |
| `"mdCodeBlockBorder"` | Code block fences |
| `"mdQuote"` | Blockquote text |
| `"mdQuoteBorder"` | Blockquote border |
| `"mdHr"` | Horizontal rule |
| `"mdListBullet"` | List bullets |

### Syntax Highlighting

| Token | Use for |
|-------|---------|
| `"syntaxComment"` | Comments |
| `"syntaxKeyword"` | Keywords (`if`, `return`, etc.) |
| `"syntaxFunction"` | Function names |
| `"syntaxVariable"` | Variable names |
| `"syntaxString"` | String literals |
| `"syntaxNumber"` | Numeric literals |
| `"syntaxType"` | Type names |
| `"syntaxOperator"` | Operators |
| `"syntaxPunctuation"` | Punctuation |

### Thinking Level

| Token | Use for |
|-------|---------|
| `"thinkingOff"` | Thinking off |
| `"thinkingMinimal"` | Minimal thinking |
| `"thinkingLow"` | Low thinking |
| `"thinkingMedium"` | Medium thinking |
| `"thinkingHigh"` | High thinking |
| `"thinkingXhigh"` | Extra high thinking |
| `"thinkingText"` | Thinking block text |

### Modes

| Token | Use for |
|-------|---------|
| `"bashMode"` | Editor border when in bash mode (`!` prefix) |

## Background Colors

Apply with `theme.bg(token, text)`.

### General

| Token | Use for |
|-------|---------|
| `"selectedBg"` | Selected line background |
| `"userMessageBg"` | User message background |
| `"customMessageBg"` | Extension message background |

### Tool States

| Token | Typical appearance | Use for |
|-------|-------------------|---------|
| `"toolPendingBg"` | Muted/dark | Tool running |
| `"toolSuccessBg"` | Green tint | Tool succeeded |
| `"toolErrorBg"` | Red tint | Tool failed |

## Combining Styles

Styles nest — the innermost call wraps the text, outer calls add more codes:

```typescript
// Bold + accent color
theme.fg("accent", theme.bold("Important!"))

// Italic + muted color
theme.fg("muted", theme.italic("footnote"))

// Strikethrough + dim color
theme.fg("dim", theme.strikethrough("removed"))

// Color on colored background
theme.bg("toolErrorBg", theme.fg("error", "Error: something broke"))

// All three text styles (uncommon but valid)
theme.bold(theme.italic(theme.strikethrough("everything")))
```

## Markdown Component

For full markdown rendering (headings, bold, italic, code blocks, links, lists), use the `Markdown` TUI component:

```typescript
import { Markdown, getMarkdownTheme } from "@earendil-works/pi-coding-agent";

// Inside a render callback:
const md = new Markdown(
  "# Title\n\nSome **bold** and *italic* text.\n\n" +
  "- Item one\n- Item two\n\n" +
  "`inline code` and:\n\n" +
  "```typescript\nconst x = 1;\n```",
  1,   // paddingX
  0,   // paddingY
  getMarkdownTheme()
);
```

The `Markdown` component implements the standard `Component` interface (`render`, `invalidate`), so it can be returned directly from `setHeader()`, `setWidget()`, or `setFooter()`:

```typescript
ctx.ui.setHeader((_tui, theme) => {
  return new Markdown(
    "**Welcome** to the `dev` branch.",
    1,
    0,
    getMarkdownTheme()
  );
});
```

### Supported Markdown

| Syntax | Renders as |
|--------|-----------|
| `# Heading` | Colored heading |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `` `code` `` | Inline code with accent color |
| ` ``` ` blocks | Code block with syntax highlighting |
| `[text](url)` | Link text + dimmed URL |
| `- item` | Bulleted list |
| `> quote` | Blockquote with border |
| `---` | Horizontal rule |

## Quick Reference: Header Example

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    if (!ctx.hasUI) return;

    ctx.ui.setHeader((_tui, theme) => {
      return {
        render(_width: number): string[] {
          return [
            "",
            theme.fg("accent", theme.bold("  Welcome back!")),
            theme.fg("muted", "  Project: ") + theme.fg("text", "my-app"),
            theme.fg("success", "  ✓") + theme.fg("dim", " 3 agents ready"),
            "",
          ];
        },
        invalidate() {},
      };
    });
  });
}
```
