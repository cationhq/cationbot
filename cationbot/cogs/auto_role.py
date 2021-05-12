from logging import info
from typing import NoReturn

from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get

from cationbot import core
from cationbot.helpers.roles import add_role_to_user, remove_role_from_user


class AutoRole(commands.Cog):
    """Add/Remove the tech/misc roles."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.available_roles = {
            **core.language_roles,
            **core.misc_roles,
        }

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
        """
        Add/Remove the misc roles from an user.

        The automatic role feature will work only when the user already holds
        a membership, otherwise he/she will not be able to receive any
        additional roles.

        It is checked whether the reaction occurred in the specific message and
        with a known emoji. If the message corresponds to where automatic roles
        are distributed and that the user used a valid emoji, the respective
        role is given or removed from the user.
        """
        if (
            event.emoji.name in self.available_roles.keys()
            and event.message_id == core.env.ROLES_MESSAGE_ID
        ):
            guild = await self.bot.fetch_guild(event.guild_id)
            member = await guild.fetch_member(event.user_id)
            member_role = get(guild.roles, id=core.env.MEMBERS_ROLE_ID)

            # The user must have the member role before get other roles.
            if member_role in member.roles:
                role = get(
                    guild.roles,
                    id=self.available_roles[event.emoji.name],
                )

                if event.event_type == "REACTION_ADD":
                    await add_role_to_user(
                        role,
                        member,
                        "Escolha de cargo por meio de reação",
                    )
                elif event.event_type == "REACTION_REMOVE":
                    await remove_role_from_user(
                        role,
                        member,
                        "Remoção da reação na escolha de cargos",
                    )


def setup(client):  # noqa: D103 pragma: no cover
    client.add_cog(AutoRole(client))
