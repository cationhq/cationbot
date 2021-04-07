import logging
from typing import NoReturn

from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get

from cationbot import core


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
            role = get(guild.roles, id=core.env.MEMBERS_ROLE_ID)

            if member and role:

                logging.info(
                    f"{event.event_type}: "
                    f"Role: '{role.name}' // "
                    f"Member: '{member.display_name}'."
                )

                if event.event_type == "REACTION_ADD":
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)


def setup(client):  # noqa: D103 pragma: no cover
    client.add_cog(AutoMember(client))
