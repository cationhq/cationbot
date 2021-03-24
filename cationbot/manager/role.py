import logging
from typing import NoReturn, Union

from discord import Member, Role


async def add_role_to_member(member: Member, role: Role) -> NoReturn:
    """
    Add a role to member.

    Args:
        member: the member object.
        role: the role to be added.
    """
    logging.info(f"Added the role {role.name} (#{role.id}) to '{member}.")
    await member.add_roles(role)


async def remove_role_from_member(member: Member, role: Role) -> NoReturn:
    """
    Remove the role from member.

    Args:
        member: the member object.
        role: the role to be removed.
    """
    logging.info(f"Removed the role {role.name} (#{role.id}) from {member}.")
    await member.remove_roles(role)


def member_has_role(member: Member, role: Union[str, int]) -> bool:
    """
    Check if the member has the role.

    Args:
        member: the member object.
        role: the role. It can be the role ID or the role name.

    Returns:
        True if the member has the role. Otherwise, False.
    """
    if isinstance(role, int):
        logging.info(f"Checking if '{member.nick}' has role by ID: {role}.")
        roles = [r for r in member.roles if r.id == role]
    else:
        logging.info(f"Checking if '{member.nick}' has role by name: {role}.")
        roles = [r for r in member.roles if r.name == role]

    return any(roles)
