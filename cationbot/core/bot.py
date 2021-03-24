from discord import DMChannel, Intents, Message, RawReactionActionEvent
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext.commands import Bot

from cationbot.controllers.auto_custom_role import toggle_custom_role
from cationbot.controllers.auto_member_role import toggle_member_role

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
async def on_raw_reaction_add(
    event: RawReactionActionEvent,
):  # pragma: no cover
    """On add any reaction on any server message."""
    await toggle_member_role(bot=bot, event=event)
    await toggle_custom_role(bot=bot, event=event)


@bot.event
async def on_raw_reaction_remove(
    event: RawReactionActionEvent,
):  # pragma: no cover
    """On remove any reaction on any server message."""
    await toggle_member_role(bot=bot, event=event)
    await toggle_custom_role(bot=bot, event=event)


@bot.event
async def on_message(message: Message):  # pragma: no cover
    """On any new message."""
    if isinstance(message.channel, DMChannel) and message.author != bot.user:
        """Reply to direct messages."""
        await message.channel.send(env.DEFAULT_DM_RESPONSE)
