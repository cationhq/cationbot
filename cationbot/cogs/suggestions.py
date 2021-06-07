from discord import Message
from discord.ext import commands

from cationbot.core.env import env


class Suggestions(commands.Cog):
    """Auto add useless/usefull reactions to message on suggestion channel."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Handle the message event."""

        if message.channel.id == env.SUGGESTIONS_CHANNEL_ID:
            await message.add_reaction(env.SUGGESTIONS_USEFULL_EMOJI)
            await message.add_reaction(env.SUGGESTIONS_USELESS_EMOJI)


def setup(client):  # noqa: D103 pragma: no cover
    client.add_cog(Suggestions(client))
