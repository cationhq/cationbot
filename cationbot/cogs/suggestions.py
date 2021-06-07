from discord import Message
from discord.ext.commands import Cog

from cationbot.core.bot import Bot
from cationbot.core.env import env


class Suggestions(Cog):
    """Auto add useless/usefull reactions to message on suggestion channel."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        """Handle the message event."""

        if message.channel.id == env.SUGGESTIONS_CHANNEL_ID:
            await message.add_reaction(env.SUGGESTIONS_USEFULL_EMOJI)
            await message.add_reaction(env.SUGGESTIONS_USELESS_EMOJI)


def setup(client):  # noqa: D103 pragma: no cover
    client.add_cog(Suggestions(client))
