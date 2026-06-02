from typing import TypedDict, Literal

type SessionID = str
type MemberID = SessionID
type MemberPID = str

class Teammate(TypedDict):
    role_description: str
    when_to_send: str # context for when to communicate with member
    messages_to_expect: str # messages to expect from teammate
    operator_context: str # for the operator teammate entry, gives context to take operator messages as priority

class TeamMembersJSON(TypedDict):
    team: dict[MemberID,Teammate]

class CrewMemberParameters(TypedDict):
    model: str
    thinking: Literal["off" | "minimal" | "low" | "medium" | "high"]
    skill: str # skill given to the agent for use
    task_file: str # path to file containing details for the subagent's task
    teammates: list[Teammate]
