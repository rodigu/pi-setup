# You have received a message

From: {sender_id}
Priority: {message_priority}
Type: {message_type}

## Message

{message_content}

## Message types reference

- `stuck`: Sender is stuck, and can't do anything until you reply
- `info`: For your information, does not need a reply. Neither sender nor receipients need to stop what they are doing.
- `request`: Sender is asking for information or action from you.
- `announcement`: Only the orchestrator may send announcements
  - Members may send a `request` message to the orchestrator to send announcements
- `reply`: Reply to request you sent.
- `deny`: Request denied.
- `report` May be proactively sent by members to other members or orchestrator as a progress report.

## Reminder

After reading this message, move this file to your `{member_meta_path}/read/` directory to mark the message as read.

Then read your {temp_mem_md} to remind yourself of your tasks and progress.

For high priority messages, stop what you are doing to reply to it.
Wait for a response before continuing.
