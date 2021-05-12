from logging import info
from typing import Optional

from discord import Guild, Member, Role
from discord.utils import get


async def add_role_to_user(
    role: Role,
    member: Member,
    reason: Optional[str] = None,
):
    """
    Add the role to a specific user.

    Args:
        - role: the role to add.
        - member: the member to add the role.
        - reason: the reason to add the role to the user.
    """
    info(
        f"Atribuindo o cargo {role.name} para o usuário {member.display_name}"
    )
    await member.add_roles(role, reason=reason)


async def remove_role_from_user(
    role: Role,
    member: Member,
    reason: Optional[str] = None,
):
    """
    Remove the role from a specific user.

    Args:
        - role: the role to remove.
        - member: the member to remove the role.
        - reason: the reason to remove the role from user.
    """
    info(f"Removendo o cargo {role.name} do usuário {member.display_name}")
    await member.remove_roles(role, reason=reason)


async def remove_all_roles(
    guild: Guild,
    member: Member,
    reason: Optional[str] = None,
):
    """
    Remove all from a specific member.

    Args:
        - guild: the guild object.
        - member: the member object.
        - reason: the reason to remove the member role.
    """
    all_roles = tuple(
        get(guild.roles, id=role.id)
        for role in member.roles
        if role.name != "@everyone"  # Cannot remove @everyone
    )

    info(f"Removendo todos os cargos do membro {member.display_name}")

    await member.remove_roles(
        *all_roles,
        reason=reason,
    )
