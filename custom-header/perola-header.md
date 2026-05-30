# Customizing Pi's Startup Header

Pi's interactive mode shows a **startup header** at the top of the screen when it launches. By default this is a small ASCII-art logo plus a list of keyboard shortcuts. You can replace it with anything you want using a pi **extension**.

## How It Works

Pi is extended through TypeScript files called **extensions**. An extension is just a single file that exports a default function. Pi calls that function when it starts up, passing in an API object that lets you hook into pi's behavior.

The relevant pieces for a custom header are:

1. **Events** — Pi fires lifecycle events like `session_start` when it initializes. You subscribe to these with `pi.on("session_start", ...)`.
2. **`ctx.ui.setHeader()`** — Inside the `session_start` handler, calling `ctx.ui.setHeader(...)` replaces the default header with your own.
3. **`theme`** — The render callback receives a `theme` object you can use to color text (e.g. `theme.fg("accent", "hello")` colors "hello" with the accent color from whatever theme pi is using).

## The Extension File

The code lives in a single TypeScript file. Here's what each part does:

```
pi.on("session_start", async (_event, ctx) => { ... })
```

This runs once when pi starts a session. It's the right place to set up UI customizations because the terminal is ready at this point.

```
ctx.ui.setHeader((_tui, theme) => { ... })
```

This tells pi: "don't draw your default header; call my function instead." The callback you pass receives:

| Argument | What it is |
|----------|-----------|
| `_tui`  | The terminal UI instance (rarely needed directly) |
| `theme` | The current color theme — use `theme.fg("accent", text)`, `theme.fg("muted", text)`, etc. |

Your callback must return an object with two methods:

```typescript
{
  render(width: number): string[],
  invalidate(): void
}
```

- **`render(width)`** — Called every time pi redraws the screen. Return an array of strings where each string is one line. `width` is the current terminal column count (useful for centering or truncating).
- **`invalidate()`** — Called when the theme changes so you can clear any cached styled text. For simple extensions, an empty body is fine.

```
ctx.ui.setHeader(undefined)
```

Passing `undefined` restores pi's default header. This is what the `/builtin-header` command does.

## Color Tokens

The `theme` object provides named colors that match the user's selected theme. Common ones:

| Token | Typical use |
|-------|-------------|
| `"accent"` | Highlights, links, primary color |
| `"muted"` | Secondary, less important text |
| `"dim"` | Very subtle, tertiary text |
| `"success"` | Green — success states |
| `"error"` | Red — errors |
| `"text"` | Default foreground |

Usage: `theme.fg("accent", "some text")` returns the string with ANSI color codes applied.

You can also style text: `theme.bold(text)`, `theme.italic(text)`, `theme.strikethrough(text)`.

## Installation

1. Place `perola-header.ts` in one of these directories:

   | Path | Scope |
   |------|-------|
   | `~/.pi/agent/extensions/` | Global — applies to every project |
   | `.pi/extensions/` | Project-local — only for this repo |

2. Start (or restart) pi. You can also run `/reload` inside an active pi session to hot-load the extension.

3. To go back to the default header, either:
   - Run `/builtin-header` inside pi (command registered by the extension), or
   - Delete the file and restart pi.

## Example: ASCII Art Header

You can return any text in `render()`. For a bigger splash, draw ASCII art:

```typescript
return {
  render(_width: number): string[] {
    return [
      "",
      theme.fg("accent", "  ██████╗ ██╗"),
      theme.fg("accent", "  ██╔══██╗██║"),
      theme.fg("accent", "  ██████╔╝██║"),
      theme.fg("accent", "  ██╔═══╝ ██║"),
      theme.fg("accent", "  ██║     ██║"),
      theme.fg("accent", "  ╚═╝     ╚═╝"),
      "",
      theme.fg("muted", "  Welcome back, Perola!"),
      "",
    ];
  },
  invalidate() {},
};
```

Each string in the array is one terminal line, so make sure no line exceeds the terminal width (or use the `width` parameter to truncate).
