#!/usr/bin/env python

"""
Creates crew member's json file, and notes file.

Receives: a json path for input parameters matching NewCrewMemberParameters.

Generates <member-id> (<skill>-<4-random-digits>).

Creates

Runs the pi subprocess and registers its PID.
Registers crew member's PID to `./.subcom/crew/<crew-id>/crew_pids.json`.

Updates each crew member's json file with the new crewmmate.

Sends message to all crew members warning that a new crewmmate was added.

Returns new member's <member-id>.
"""

from pathlib import Path
from crew_handler.interfaces.member import MemberID, MemberPID, CrewMemberParameters
from crew_handler.interfaces.crew_meta import (
    CrewID,
    read_crew_id,
    get_crew_path,
    get_member_path,
)

_VERBOSE = 1


def _spawn_pi_instance(
    member_id: MemberID, member_parameters: CrewMemberParameters, prompt: str
) -> MemberPID:
    """Spawns pi instance subprocess in rpc mode.

    The instances' `sessions` filepath is `.subcom/crew/{crew_id}/sessions/`.

    `member_id` is used as a session id.
    Other pi parameters are set using keys from `member_parameters`

    Args:
        member_parameters (NewCrewMemberParameters): parameters for the new crew member
        member_id (MemberID): member id

    Returns:
        MemberPID: spawned process PID
    """


def _create_member_notes(member_id: MemberID) -> str:
    """Creates empty member notes at `{get_crew_path}/notes.md`

    Args:
        member_id (MemberID): member id

    Returns:
        str: path_to_notes
    """


def _create_members_json(member_id: MemberID) -> str:
    """Creates member's json at `{get_member_path}/members.json`

    Args:
        member_id (MemberID): member id

    Returns:
        str: path_to_json
    """
    from crew_handler.interfaces.member import TeamMembersJSON


def _update_crew_json():
    """Updates the `members.json` file for each member, adding the new member to them."""


def _parse_member_prompt(
    member_id: MemberID, member_parameters: CrewMemberParameters
) -> str:
    """Reads `'./member_prompt.md` and parses with python's built-in `.format`, providing given parameters.

    Args:
        member_id (MemberID): member id
        member_parameters (CrewMemberParameters): member parameters

    Returns:
        str: Parsed member prompt
    """


def _append_member_pid(pid: MemberPID, member_id: MemberID):
    """Appends the crew member's PID using `crew_meta.append_pid`

    Args:
        pid (MemberPID): member pid
        member_id (MemberID): member id
    """
    from crew_handler.interfaces.crew_meta import append_pid


def _generate_member_id(skill: str) -> MemberID:
    """Generates 4-digit member id.

    Args:
        skill (str): skill string

    Returns:
        MemberID: member id

    Examples:
        >>> _generate_member_id(skill="revise")
        'revise-0173'
        >>> _generate_member_id(skill="code-review")
        'code-review-9812'
    """


def _read_new_member_json(filepath: str) -> CrewMemberParameters:
    """Reads the JSON file with the new crew member's parameters

    Args:
        filepath (str): filepath for the new crew member

    Returns:
        NewCrewMemberParameters: typed dictionary with parameters for the new crew member
    """


def _add_member(member_parameters: CrewMemberParameters) -> MemberPID:
    """Runs steps to add member to crew.

    Args:
        member_parameters (NewCrewMemberParameters): parameters for the new crew member

    Returns:
        MemberPID: member PID
    """
    member_id = _generate_member_id(skill=member_parameters["skill"])
    new_member_prompt = _parse_member_prompt(member_parameters=member_parameters)
    _create_member_notes(member_id=member_id)
    _create_members_json(member_id=member_id)

    member_pid = _spawn_pi_instance(
        member_id=member_id,
        member_parameters=member_parameters,
        prompt=new_member_prompt,
    )

    _append_member_pid(pid=member_pid, member_id=member_id)

    _update_crew_json()


def _is_crew_running() -> bool:
    return Path("./.subcom/.running").exists()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Add crew member to running handler.")

    parser.add_argument(
        "filepath", help="New crew member JSON filepath.", type=str, required=True
    )
    parser.add_argument("-v", "--verbose", help="Verbose mode.", type=bool, default=1)

    if not _is_crew_running():
        raise RuntimeError(
            "No active crew handler found. Start a crew handler to add members."
        )

    args = parser.parse_args()
    _VERBOSE = args.verbose

    member_parameters = _read_new_member_json(filepath=parser.filepath)

    _add_member(member_parameters=member_parameters)
