from random import choice

from discord import DMChannel, Intents, Message
from discord.ext.commands import Bot
from discord.ext.tasks import loop

from . import activities, env

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


@loop(minutes=env.CHANGE_PRESENCE_IN_MINUTES)
async def change_presence():
    """Loop for change the bot presence."""

    activity = choice(activities)
    await bot.change_presence(activity=activity)


@bot.event
async def on_ready():  # noqa: D102
    """When bot is ready to receive commands."""
    await bot.wait_until_ready()
    change_presence.start()


@bot.event
async def on_message(message: Message):  # pragma: no cover
    """On any new message."""
    if isinstance(message.channel, DMChannel) and message.author != bot.user:
        """Reply to direct messages."""
        await message.channel.send(env.DEFAULT_DM_RESPONSE)
