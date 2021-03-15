from typing import Optional, Union

from discord import Member, RawReactionActionEvent, User
from discord.ext.commands.bot import Bot


def is_reaction_on_message(
    bot: Bot,
    event: RawReactionActionEvent,
    message_id: int,
) -> bool:
    """
    Check if the reaction is on rules message.

    Args:
        bot: the bot client.
        event: the reaction event.

    Returns:
        True if the user react to the rules message with a green check mark
        emoji. Otherwise, False is returned.

    """
    if event.user_id == bot.user.id:
        return False

    return event.message_id == message_id


async def get_member_from_reaction(
    bot: Bot,
    event: RawReactionActionEvent,
) -> Optional[Union[Member, User]]:
    """
    Get the member from reaction action.

    Args:
        bot: the bot client.
        event: the reaction event.

    Returns:
        The member from reaction event.
    """
    guild = await bot.fetch_guild(event.guild_id)
    member = await guild.fetch_member(event.user_id)
    return member
