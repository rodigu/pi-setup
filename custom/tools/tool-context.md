# Tool Context: How the LLM Knows How to Use Tools

## Overview

When pi starts, it builds a **system prompt** sent to the LLM on every request. This prompt includes tool definitions, summaries, and behavioral guidelines that tell the model *what* tools are available and *how* to use them.

## How the LLM Discovers Tools

1. **Tool definitions** — Each tool's `name`, `description`, and `parameters` (JSON schema) are registered with the model provider's tool-calling API.
2. **"Available tools" section** — A one-line snippet per tool for quick scanning.
3. **"Guidelines" section** — Behavioral rules on when and how to use tools.

## Providing Context for Custom Tools

When calling `pi.registerTool()`, three fields control what the LLM sees:

```typescript
pi.registerTool({
  name: "my_tool",
  description: "What this tool does (shown to LLM)",
  promptSnippet: "One-liner for the Available tools section",
  promptGuidelines: [
    "Use my_tool when the user asks to summarize previously generated text.",
    "Always pass the full file path to my_tool, not relative paths."
  ],
  parameters: Type.Object({ ... }),
  async execute(...) { ... },
});
```

### Field Reference

| Field | Where it appears | Purpose |
|---|---|---|
| `description` | Tool definition sent to the model | Core purpose of the tool |
| `promptSnippet` | "Available tools" section | One-line summary for quick scanning |
| `promptGuidelines` | "Guidelines" section | Behavioral instructions — when to call it, how to use it correctly |

### Key Rules

- Each guideline bullet **must name the tool explicitly** (e.g., "Use my_tool when...").
- Avoid "Use this tool when..." — guidelines are appended flat with no tool name prefix, so the LLM can't tell which tool "this" means.
- `promptSnippet` is optional; if omitted, the tool is left out of the "Available tools" section.
- `promptGuidelines` are only included when the tool is active (e.g., after `pi.setActiveTools([...])`).

## Built-in Example

Built-in tools like `read` have guidelines such as:

> *"Use read to examine files instead of cat or sed."*

This is how the LLM knows to prefer `read` over `bash` with `cat`.

## See Also

- [Extensions docs](../../docs/extensions.md) — Full `registerTool` API and all fields
- [examples/extensions/dynamic-tools.ts](../../examples/extensions/dynamic-tools.ts) — Dynamic tool registration example
