from typing import TypedDict
from functools import cache
from crew_handler.interfaces.member import CrewMemberParameters, MemberID, MemberPID

type CrewID = str


class CrewPID(TypedDict):
    member_id: MemberID
    member_pid: MemberPID

class CrewMeta(TypedDict):
    """Crew meta located at `{crew_path}/meta.json`
    """
    crew_id: CrewID
    crew_name: str
    orchestrator_id: MemberID
    crew_pids: dict[MemberID,CrewPID]
    members: dict[MemberID,CrewMemberParameters]

def append_pid(crew_path: str, pid: MemberPID, member_id:MemberID):
    """Appends new crew member to crew meta's pids

    Args:
        crew_path (str): path to crew
        pid (str): new member pid
        member_id (MemberID): new member id
    """

def get_pid(crew_path: str, member_id: MemberID) -> str:
    """Fetches given member's pid from the `CrewMeta` JSON at `crew_path`.

    Args:
        crew_path (str): path for the crew's json file
        member_id (MemberID): member's id (same as its session's ID)

    Returns:
        str: member's PID
    """

@cache
def read_crew_id() -> CrewID:
    """Returns the crew's id by reading the `./.subcom/.running` file.

    Returns:
        CrewID: crew_id
    """

def get_crew_path()->str:
    """Is `./.subcom/crew/{crew_id}/`

    Returns:
        str: crew directory path
    """

def get_member_path(member_id: MemberID, crew_id:CrewID)->str:
    """Is `./.subcom/crew/{crew_id}/{member_id}`

    Args:
        member_id (MemberID): member id
        crew_id (CrewID): crew id

    Returns:
        str: directory path
    """