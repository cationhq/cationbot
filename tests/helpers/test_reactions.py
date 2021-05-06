import pytest

from cationbot.helpers.reactions import remove_reactions_from_message

MODULE = "cationbot.helpers.reactions"


@pytest.mark.asyncio
async def test_remove_reactions_from_message_should_remove_reaction_from_message(
    mocker,
    use_member,
    use_message,
):
    logging_info = mocker.patch(f"{MODULE}.logging.info")

    await remove_reactions_from_message(
        message=use_message,
        member=use_member,
    )

    logging_info.assert_called_once_with(
        f"Removendo todas as reações do membro {use_member.nick}"
        f" da mensagem {use_message.id} - {use_message.content}."
    )
    # use_message fixture generate just one reaction.
    message_reaction = use_message.reactions[0]

    message_reaction.users.assert_called_once()
    message_reaction.users.return_value.flatten.assert_awaited_once()

    use_message.remove_reaction.assert_called_once_with(
        emoji=message_reaction.emoji,
        member=use_member,
    )
