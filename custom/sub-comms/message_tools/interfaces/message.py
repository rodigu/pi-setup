from typing import TypedDict
from crew_handler.interfaces.member import MemberID, CrewID
from crew_handler.interfaces.crew_meta import get_member_path

class Message(TypedDict):
    sender_id: MemberID
    recipient_id: MemberID
    crew_id: CrewID
    message_type: str
    message_priority: str
    content: str

message_types={
    "stuck":"Sender is stuck, and can't do anything until you reply",
    "info":"For your information, does not need a reply. Neither sender nor receipients need to stop what they are doing.",
    "request":"Sender is asking for information or action from you.",
    "announcement":"Only the orchestrator may send announcements. Members may send a `request` message to the orchestrator to send announcements",
    "reply":"Reply to request you sent.",
    "deny":"Request denied.",
    "report":"May be proactively sent by members to other members or orchestrator as a progress report.",
}

def _create_message_path(message: Message) -> str:
    """Creates the filepath for the message.

    Args:
        message (Message): message content dictionary

    Returns:
        str: file path where message should be placed
    """
    from random import randint
    member_path = get_member_path(message['member_id'])
    return f"{member_path}/inbox/{message['sender_id']}-{message['priority']}-{randint(1000,9999)}"

def _parse_message_markdown(message: Message) -> str:
    """Reads `./message.md` and replaces its contents with `.format`

    Args:
        message (Message): message

    Returns:
        str: parsed message file content
    """

def write_message_to_inbox(message:Message):
    """Writes given message to recipient's inbox

    Args:
        message (Message): message
    """