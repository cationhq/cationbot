import logging
from typing import NoReturn, Optional

from discord import Guild, Member, Role, utils

from cationbot.core.roles import hierarchy_roles, tech_roles


def find_role_by_name(role: str, guild: Guild) -> Optional[Role]:
    """
    Find the role data by the name.

    Args:
        role: the role name to query.
        guild: the guild information (used to get all roles).

    Returns:
        The role, if it exists. Otherwise, None.
    """
    role_id = {
        **tech_roles,
        **hierarchy_roles,
    }.get(role)

    if not role_id:
        return

    return utils.get(guild.roles, id=role_id)


async def toggle_role(
    member: Member,
    roles: Role,
    add: bool = True,
) -> NoReturn:
    """
    Add/Remove the role from an user.

    Args:
        member: the member to be edited.
        roles: the roles to be added.
        add: True to add the role/False to remove the role.
    """
    logging.info(
        f"{'Added' if add else 'Removed'} roles '{roles}' to/from '{member}'"
    )
    if add:
        await member.add_roles(roles)
    else:
        await member.remove_roles(roles)
