# Sub-comms

member local communication system.

Team members have their own directory.
In it, they have an inbox directory with:

- received
- read

## Teck stack

- pi's rcp functionality
- SQLite messages storage and retrieval
- Message handler python script
  - a single one may exist at a time
  - at start checks for `./.subcom/.running`
    - returns error saying another crew is running
  - Read message request JSONs periodically from `./.subcom/queue/send/`
  - Send steer messages to agent's stdio
  - Read query request JSONs periodically from `./subcom/queue/query/`
  - at end deletest `./.subcom/.running`

## Proposal

Method for inter-agent communication.

Use pi's RPC functionality to handle communication between agents.

Agents are created the `--session-id <id>` flag so that they have a unique id.
The id is created with a combination of `skill`, current date and time, and a random 4-digit string.
The orchestrator's id is its own session's id.

> [!Note]: there should be an easy way for the orchestrator to generate the ids, and to figure out its own.
> A function to give it the 4-digit string it can use would be good.
> A tool or function that returns the calling agent's id too.
> That way they don't have to go looking through sessions and pollute their context.

Agent crew spawned by a single tool call: `spawn-crew`.
The agent who spawned the crew is the *orchestrator*.
Agents called by the tool (the *team members*) cannot have access to the `spawn-crew` tool call.
team members should not even know that the tool exists (check if possible).

The orchestrator itself doesn't need to know the full inner workings of the messaging system, only enough to use it.

team members have access to a `send-message` tool to send messages to each-other.

team members should have a very precise, finite reason for being. They must always have a final output they are working towards.

There should be a way to spawn in new agents to the crew.

## Sub-agent types

team members must always have a clearly defined goal to achieve.
They should be run with the `-nc` flag, so they do not receive any context outside what is given to them.

team members only must only have in their context:

1. the system prompt
2. the context for the messaging system
   1. their own id
   2. how the system works for it
   3. how it can use the system (precise, succinct information), and the message char limit
   4. it does not need the full architecture, implementation details, or understanding for functionality it has no access to
   5. the orchestrator's id
3. access to a file (`./.subcom/crew/<crew-id>/<member-id>.json`) that has its team-mates':
   1. id
   2. a very brief description of what the teammate does
   3. what messages may be sent to it
   4. what messages it should expect to receive from it
4. access to a file (`./.subcom/crew/<crew-id>/<member-id>.notes.md`) for note-taking:
   1. members should periodically write notes with important information they need to recall at a later time
5. the skill they will use
6. the task being performed

And nothing else.

Note that each member will have its own `.teammates.md` file.

Included in the teammates file is a reference to the parent agent who spawned the crew.

### Reviewer

### Planner

Input: final product specifications
Output: implementation plan

## Architecture

An orchestrator:

- spawns a message handler. the handler
  -

  - checks if a database file already exists
    - creates the database if it doesn't
  - creates all directories required
- spawns members

The members communicate with each other and the orchestrator through the messages database and the message handler.

### Database tables

#### Messages table

Columns:

| Name             | Type             | Nullable | Description                                                              | Example               |
| :--------------- | :--------------- | :------: | :----------------------------------------------------------------------- | --------------------- |
| pk               | id               |    No    | Primary key (sequential, automatically added)                            | 102                   |
| dt_sent          | datetime         |    No    | Datetime message was sent (at `*-send-message` tool call)                | <datetime-iso-format> |
| dt_steered       | datetime         |   Yes    | Datetime handler sent the steer message                                  | <datetime-iso-format> |
| dt_read          | datetime         |   Yes    | Datetime message was read (at `*-read-message` tool call)                | <datetime-iso-format> |
| sender           | string           |    No    | Sub-agent id `skill`-`rnd_4_digit`, generated at creation                | review-8472           |
| recipient        | string           |    No    | Recipient id                                                             | code-review-2501      |
| crew_id          | string           |    No    | Sub-agent's crew id `datetime`-`rnd_4_digit`, generated at crew creation | 202511010942-7623     |
| message_type     | string           |    No    | Type of message being sent                                               | request               |
| message_priority | int              |    No    | Message priority (low, middle, high)                                     | middle                |
| content          | string(max 1000) |    No    | Message content                                                          | Arbitrary length      |

> [!Question]: what might be the optimal length for content.
> Needs to be enough to communicate, but not too long so as to polute the other agents' context.

#### Agents dimension table

At creation, handler module

#### Tasks table

Should there be a tasks system?
With its own database, that members use to track their own work, and the orchestrator uses to check progress.

Might be too many systems for their context to handle.

### Messages

All messages have a single sender.

The `send-message` tools are direct queries to the database.
The agent provides:

- message
- priority
- type
- recipient
- content

All other properties are defined automatically by the `send-message` tool.

#### Handler

The message handler continually selects (in pseudo-sql):

```sql
select pk pk_to_steer, recipient unread_recipent
where dt_read is None
    or (
        dt_read is None -- has not read
        and minutes(now() - dt_steered) > 3 -- 3 minutes have passed since last steer attempt
    )
from messages_table
```

Steers the unread_recipient members through rcp.

Then:

```sql
update messages_table
set dt_steered=now()
where pk in pk_to_steer
```

When an agent uses a sent-, the message handler script sends a steer prompt to the recipients, saying there is a new message for them, and letting them know of the message type, the sender, and the priority.

# TODO: Refactor to single send-message

#### Messaging tools

The `send-message` tools check if the recipient exists.
If it doesn't, it returns a list with possible recipients, and advises member to read the <member-id>.teammates.md file again.

> [!Question]: I have a strong preference for using SQLite.
> However, I don't think SQLite can do parallel processing.
> Maybe have a `./.subcom/queue/` that members write files to, and the handler watches periodically to clean the queue and insert to the messages table.
> Each file in queue could be a `<member-id>-<epoch>.json` file created by the `send-message` tool.

`send-message` then does a simple query to the database, returning on success.

`read-message` does a simple query to the databse using the agent's id.

- `orchestrator-send-message`: only the agent that spawned the crew can use this tool to send a message
  - the only tool that allows for `announcements` type messages
  - the only tool that allows for `high` priority messages
  - registers datetime for `dt_sent`
- `orchestrator-read-messages`: only the agent that spawned the crew can use this tool to read any messages from the whole crew
  - used to check if tasks are being done, if any member is in a loop or can't progress
- `member-send-message`: members use it to send messages
  - registers datetime for `dt_sent`
- `member-read-message`: members use it to receive messages

> [!Question]: is there is a way for the `send-messages` tool to get the sender id?
> If there is a way for the tool to get the id without having to rely on self-reporting,
> there can be a single `read-message` and a single `send-message`

#### Message Priorities

Messages have priorities low, medium, and high.
High priority means the agent needs to stop whatever they are doing, reply, and then wait for a response.
Only the orchestrator may send a high priority message.

#### Message Types

- `stuck`: When an agent gets stuck, tney send a message to the agent or agents that needs to do something to unblock the sender.
  - The agent stops what they are doing until a steer message is received from the message handler
- `info`: Information, does not need a reply. Neither sender nor receipients need to stop what they are doing.
- `request`:
  - the orchestrator may send high priority requests
- `announcement`: only the orchestrator may send announcements
  - members may send a `request` message to the orchestrator to send announcements
- `reply`
- `acknowledge`
- `deny`
- `report` may be proactively sent by the members to other members or the orchestrator to repost progress

### `send-message` tool

Should have access to the tool-caller id (the id of the member calling the tool).

### `spawn-crew` tool

Tool interfaces:

```ts
interface memberParameters {
    id: string;
    model: string;
    thinking: "off" | "minimal" | "low" | "medium" | "high";
    skill: string; // skill given to the agent for use
    task_file: string; // path to file containing details for the member's task
}
interface SpawnCrewParameters {
    sub_agents:memberParameters[];
}
interface SpawnCrewReturn {
    crew_id: string;
}

SpawnCrew: (SpawnCrewParameters) => SpawnCrewReturn
```

## Workflow example

### 1. User requests crew to implement spec

By invoking a `/skill:create-crew`.

### 2. `create-crew` skill

The skill has only the exact information the agent needs create a crew.

It has the templates in `create-crew/templates/`:

- `tasks.md` template for member task files
- `crew-proposal.md` crew proposal teplate markdown
  - includes a markdown table with the proposed `memberParameters`

### 3. Crew proposal

The skill includes instructions on a step-by-step process to create a crew proposal with:

- task file generation
  - a process that stops to clarify any ambiguities with the user
  - it also waits for human validation
- member parameters (skill, task files, model, thinking, context)
