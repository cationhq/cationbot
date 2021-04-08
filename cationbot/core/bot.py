from discord import Activity, ActivityType, DMChannel, Intents, Message
from discord.ext.commands import Bot

from .env import env

bot = Bot(
    # https://discordpy.readthedocs.io/en/latest/api.html#intents
    intents=Intents(
        guilds=True,
        messages=True,
        reactions=True,
    ),
    command_prefix=env.PREFIX,
    help_command=None,
)


@bot.event
async def on_ready():
    """When bot is ready to receive commands."""
    activity = Activity(type=ActivityType.watching, name="Tom & Jerry")
    await bot.change_presence(activity=activity)


@bot.event
async def on_message(message: Message):  # pragma: no cover
    """On any new message."""
    if isinstance(message.channel, DMChannel) and message.author != bot.user:
        """Reply to direct messages."""
        await message.channel.send(env.DEFAULT_DM_RESPONSE)
