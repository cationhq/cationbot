import logging

from discord import Guild, Member
from discord.utils import get


async def remove_all_roles(
    guild: Guild,
    member: Member,
    reason: str = None,
):
    all_roles = tuple(
        get(guild.roles, id=role.id)
        for role in member.roles
        if role.name != "@everyone"  # Cannot remove @everyone
    )

    logging.info(f"Removendo todos os cargos do membro {member.nick}")

    await member.remove_roles(
        *all_roles,
        reason=reason,
    )
