# How Pi RPC Mode Works

Pi RPC mode enables **headless operation** of the coding agent via a JSON protocol over stdin/stdout. It's designed for embedding the agent in other applications, IDEs, or custom UIs.

## Key Concepts

1. **Communication Protocol**: Uses JSONL (JSON Lines) over stdin/stdout
   - **Commands**: JSON objects sent to stdin (one per line)
   - **Responses**: JSON objects with `type: "response"` sent to stdout
   - **Events**: Agent events streamed to stdout as JSON lines

2. **Starting RPC Mode**:
   ```bash
   pi --mode rpc [options]
   ```
   Common options: `--provider`, `--model`, `--name`, `--no-session`, `--session-dir`

## Core Features

### 1. Prompting & Interaction
- **`prompt`**: Send user prompts (text + optional images)
- **`steer`**: Queue steering messages during agent execution
- **`follow_up`**: Queue follow-up messages for after agent completion
- **`abort`**: Cancel current operations

### 2. Session Management
- **`get_state`**: Get current session state (model, thinking level, etc.)
- **`get_messages`**: Retrieve all conversation messages
- **`new_session`**: Start fresh sessions
- **`switch_session`**: Load different session files
- **`fork`/`clone`**: Create session branches

### 3. Model Control
- **`set_model`**: Switch LLM providers/models
- **`cycle_model`**: Cycle through available models
- **`set_thinking_level`**: Control reasoning depth (off → xhigh)

### 4. Execution Features
- **`bash`**: Execute shell commands with streaming output
- **`compact`**: Manually compact conversation context
- **`set_auto_compaction`**: Enable/disable automatic compaction

## Event Streaming

The agent streams events in real-time:
- **`message_update`**: Streaming text/thinking/toolcall deltas
- **`tool_execution_*`**: Tool execution progress
- **`compaction_*`**: Context compaction events
- **`auto_retry_*`**: Automatic retry on transient errors

## Extension UI Protocol

Extensions can request user interaction via:
- **Dialog methods**: `select`, `confirm`, `input`, `editor` (request/response)
- **Fire-and-forget**: `notify`, `setStatus`, `setWidget`, `setTitle`

## Example Usage (Python)

```python
import subprocess, json

proc = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)

def send(cmd):
    proc.stdin.write(json.dumps(cmd) + "\n")
    proc.stdin.flush()

# Send prompt
send({"type": "prompt", "message": "Hello!"})

# Process streaming events
for line in proc.stdout:
    event = json.loads(line)
    if event.get("type") == "message_update":
        delta = event.get("assistantMessageEvent", {})
        if delta.get("type") == "text_delta":
            print(delta["delta"], end="", flush=True)
    if event.get("type") == "agent_end":
        break
```

## Key Benefits

1. **Headless Operation**: Run without terminal UI
2. **IDE Integration**: Embed in editors/IDEs
3. **Custom UIs**: Build specialized interfaces
4. **Programmatic Control**: Full agent control via JSON API
5. **Streaming**: Real-time response streaming
6. **Session Persistence**: Save/load conversation state

## What Does RPC Stand For?

**RPC stands for "Remote Procedure Call"** - a protocol that allows a program to execute code on another system or process as if it were a local function call.

In pi's context, RPC mode allows external applications to "call" the coding agent's functionality (prompting, tool execution, session management, etc.) through a standardized JSON protocol over stdin/stdout, making it behave like a remote service that can be controlled programmatically.