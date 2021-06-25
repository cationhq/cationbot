import logging

from discord import RawReactionActionEvent as ReactionEvent
from discord.ext import commands
from discord.utils import get

from cationbot.core.bot import Bot
from cationbot.core.env import env


class AutoRole(commands.Cog):
    """Add/Remove the tech/misc roles."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event: ReactionEvent):
        """Handle the event to add a role to member."""
        await self._toggle(event)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event: ReactionEvent):
        """Handle the event to remove a role from member."""
        await self._toggle(event)

    async def _toggle(self, event: ReactionEvent) -> None:
        if (
            event.emoji.name in env.EMOJI_ROLES.keys()
            and event.message_id == env.ROLES_MESSAGE_ID
        ):
            guild = await self.bot.fetch_guild(event.guild_id)
            member = await guild.fetch_member(event.user_id)

            member_role = get(guild.roles, id=env.MEMBERS_ROLE_ID)
            if member_role in member.roles:
                role = get(
                    guild.roles,
                    id=env.EMOJI_ROLES[event.emoji.name],
                )

                if role:
                    logging.info(
                        f"{event.event_type}: "
                        f"Role: '{role.name}' // "
                        f"Member: '{member.display_name}'."
                    )

                    if event.event_type == "REACTION_ADD":
                        await member.add_roles(role)
                    else:
                        await member.remove_roles(role)


def setup(client):  # noqa: D103
    client.add_cog(AutoRole(client))
