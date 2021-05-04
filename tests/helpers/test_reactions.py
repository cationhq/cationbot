import asyncio
from unittest.mock import AsyncMock

import pytest

from cationbot.helpers.reactions import remove_reactions_from_message


@pytest.mark.asyncio
async def test_remove_reactions_from_message_should_remove_all_reactions_from_the_message_specified(
    faker,
    mocker,
):
    ab = AsyncMock()
    ab.flatten = []

    x = AsyncMock()
    x.users.return_value = ab
    # x.users.return_value.flatten.return_value = []

    # reaction = AsyncMock()
    # reaction.users.return_value = []
    # reaction.users().flatten.return_value = []
    message = AsyncMock()
    message.id = faker.pyint()
    message.content = faker.word()
    message.reactions = [x]
    member = AsyncMock()
    member.nick = faker.user_name()

    info = mocker.patch("cationbot.helpers.roles.logging.info")

    await remove_reactions_from_message(
        message=message,
        member=member,
    )

    # get.assert_called_once_with(member.roles, id=role.id)
    info.assert_called_once_with(
        f"Removendo todas as reações do membro {member.nick}"
        f" da mensagem {message.id} - {message.content}."
    )
    # member.remove_roles.assert_called_with(
    #     member.roles,
    #     reason=reason,
    # )
