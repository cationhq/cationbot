import logging

from discord import RawReactionActionEvent, utils
from discord.ext.commands.bot import Bot

from cationbot import core, manager


async def toggle_member_role(bot: Bot, event: RawReactionActionEvent):
    """Toggle the member role to a member."""

    if (
        manager.reaction.is_reaction_event_on_message(
            bot,
            event,
            core.env.RULES_MESSAGE_ID,
        )
        and event.emoji.name == "✅"
    ):
        member = await manager.reaction.get_member_from_reaction_event(
            bot,
            event,
        )
        guild = await bot.fetch_guild(event.guild_id)

        if member and guild:
            role = utils.get(guild.roles, id=core.env.MEMBERS_ROLE_ID)
            if not role:
                logging.info(
                    "Failed to edit the member role on reaction to rules message.",
                    bot,
                    event,
                )
                return

            if event.event_type == "REACTION_ADD":
                await manager.role.add_role_to_member(member, role)
            else:
                await manager.role.remove_role_from_member(member, role)
