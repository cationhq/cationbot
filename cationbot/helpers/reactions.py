from logging import info

from discord import Member, Message


async def remove_reactions_from_message(message: Message, member: Member):
    """
    Remove all reactions from a member on a specific message.

    Args:
        - message: the message object.
        - member: the member object.
    """
    info(
        f"Removendo todas as reações do membro {member.nick}"
        f" da mensagem {message.id} - {message.content}."
    )

    for reaction in message.reactions:
        users = await reaction.users().flatten()
        if member in users:
            await message.remove_reaction(
                emoji=reaction.emoji,
                member=member,
            )
