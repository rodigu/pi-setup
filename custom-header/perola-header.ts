/**
 * Perola Header Extension
 *
 * Replaces pi's default startup header (the logo and keybinding hints)
 * with a custom greeting.
 *
 * INSTALLATION:
 *   1. Copy this file to one of these locations:
 *        - ~/.pi/agent/extensions/perola-header.ts   (global, all projects)
 *        - .pi/extensions/perola-header.ts           (project-local)
 *
 *   2. Restart pi (or run /reload inside pi to hot-load extensions)
 *
 *   3. To restore the default header, run /builtin-header inside pi,
 *      or simply delete/rename this file and restart.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    // ctx.hasUI is false when running in non-interactive modes (e.g. pi -p)
    if (!ctx.hasUI) return;

    ctx.ui.setHeader((_tui, theme) => {
      // The render function returns an array of strings.
      // Each string becomes one line in the terminal.
      // `width` is the terminal column count if you need to truncate or center.
      return {
        render(_width: number): string[] {
          return [
            "",
            theme.fg("accent", "  Welcome back, Perola!"),
            theme.fg("muted", "  Ready to build something great."),
            "",
          ];
        },
        invalidate() {
          // Called when the theme changes. If you cache any themed strings,
          // clear them here so they get rebuilt with the new colors.
          // For this simple extension there's nothing to cache.
        },
      };
    });
  });

  // Register a slash command so you can restore the default header
  // without deleting this file. Type /builtin-header in pi to use it.
  pi.registerCommand("builtin-header", {
    description: "Restore pi's default startup header",
    handler: async (_args, ctx) => {
      ctx.ui.setHeader(undefined); // undefined = restore default
      ctx.ui.notify("Default header restored.", "info");
    },
  });
}
