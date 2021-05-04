import logging
from typing import NoReturn

from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get

from cationbot import core
from cationbot.helpers.reactions import remove_reactions_from_message
from cationbot.helpers.roles import remove_all_roles


class AutoMember(commands.Cog):
    """Add/Remove the 'Membro'role."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        event: RawReactionActionEvent,
    ):  # noqa: D102
        await self._toggle(event)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self,
        event: RawReactionActionEvent,
    ):  # noqa: D102
        await self._toggle(event)

    async def _toggle(self, event: RawReactionActionEvent) -> NoReturn:
        if (
            event.emoji.name == "✅"
            and event.message_id == core.env.RULES_MESSAGE_ID
        ):
            guild = await self.bot.fetch_guild(event.guild_id)
            member = await guild.fetch_member(event.user_id)

            if member:
                if event.event_type == "REACTION_ADD":
                    role = get(guild.roles, id=core.env.MEMBERS_ROLE_ID)
                    if member and role:
                        logging.info(
                            f"Atribuindo o cargo {role.name} "
                            f"para o usuário {member.nick}"
                        )
                        await member.add_roles(role)
                elif event.event_type == "REACTION_REMOVE":
                    roles_channel = self.bot.get_channel(
                        core.env.ROLES_CHANNEL_ID
                    )
                    message = await roles_channel.fetch_message(
                        core.env.ROLES_MESSAGE_ID
                    )
                    await remove_reactions_from_message(
                        member=member,
                        message=message,
                    )
                    await remove_all_roles(guild=guild, member=member)


def setup(client):  # noqa: D103 pragma: no cover
    client.add_cog(AutoMember(client))
