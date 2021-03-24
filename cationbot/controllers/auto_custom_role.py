import logging

from discord import RawReactionActionEvent, utils
from discord.ext.commands.bot import Bot

from cationbot import core, manager


async def toggle_custom_role(bot: Bot, event: RawReactionActionEvent):
    """Toggle the respective tech role to a member."""

    roles = {
        **core.language_roles,
        **core.misc_roles,
    }

    member = await manager.reaction.get_member_from_reaction_event(bot, event)

    if member and (
        manager.role.member_has_role(
            member,
            core.env.MEMBERS_ROLE_ID,
        )
        and event.emoji.name in roles.keys()
        and manager.reaction.is_reaction_event_on_message(
            bot,
            event,
            core.env.ROLES_MESSAGE_ID,
        )
    ):
        guild = await bot.fetch_guild(event.guild_id)
        role = utils.get(guild.roles, id=roles[event.emoji.name])

        if not role:
            logging.info(
                "Failed to edit the member custom role.",
                bot,
                event,
            )
            return

        if event.event_type == "REACTION_ADD":
            await manager.role.add_role_to_member(member, role)
        else:
            await manager.role.remove_role_from_member(member, role)
