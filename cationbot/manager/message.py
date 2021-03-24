from typing import Optional

from discord import Message
from discord.ext.commands.bot import Bot


async def get_message_from_channel(
    bot: Bot,
    channel_id: int,
    message_id: int,
) -> Optional[Message]:
    """
    Get info about a specific message on a channel.

    Args:
        bot: the bot instance.
        channel_id: the channel identifier.
        message_id: the message identifier.

    Returns:
        The message data, if it exists. Otherwise, None.
    """
    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)
    return message
