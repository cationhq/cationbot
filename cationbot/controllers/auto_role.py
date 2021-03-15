from discord import RawReactionActionEvent
from discord.ext.commands.bot import Bot

from cationbot.core.roles import tech_roles
from cationbot.core.settings import settings
from cationbot.models.reactions import (
    get_member_from_reaction,
    is_reaction_on_message,
)
from cationbot.models.roles import find_role_by_name, toggle_role


async def toggle_member_role(bot: Bot, event: RawReactionActionEvent):
    """Toggle the member role to a member."""

    if (
        is_reaction_on_message(bot, event, settings.RULES_MESSAGE_ID)
        and event.emoji.name == "✅"
    ):
        member = await get_member_from_reaction(bot=bot, event=event)
        guild = await bot.fetch_guild(event.guild_id)

        if member and guild:
            role = find_role_by_name(
                role=settings.MEMBER_ROLE_NAME,
                guild=guild,
            )
            await toggle_role(
                member=member,
                roles=role,
                add=event.event_type == "REACTION_ADD",
            )


async def toggle_tech_role(bot: Bot, event: RawReactionActionEvent):
    """Toggle the respective tech role to a member."""

    if (
        is_reaction_on_message(bot, event, settings.CHOOSE_TECH_MESSAGE_ID)
        and event.emoji.name in tech_roles.keys()
    ):
        member = await get_member_from_reaction(bot=bot, event=event)
        guild = await bot.fetch_guild(event.guild_id)

        if member and guild:
            role = find_role_by_name(role=event.emoji.name, guild=guild)
            await toggle_role(
                member=member,
                roles=role,
                add=event.event_type == "REACTION_ADD",
            )
