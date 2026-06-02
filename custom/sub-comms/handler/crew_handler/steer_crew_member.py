from crew_handler.interfaces.crew_meta import get_pid,MemberID,get_member_path

def steer(member_id: MemberID, sender: MemberID, message_priority: str):
    """
    Sends a prompt to the pi instance with `member_id`.
    Member PID found at CrewMeta.

    No need to check if it exists, you can just overwrite it."

    Args:
        member_id (MemberID): _description_
    """
    prompt_base = f"There is a new message from {sender} with priority {message_priority}."+\
        f"Before reading your messages, make sure write a summary of where you are at and what you are doing to `{get_member_path}/temporary_memory.md`."

def new_member_nofification(new_member_id: str):...

def highest_priority_message():...

def scan_member_inbox():...

def send_messages_to_inbox():...