from unittest.mock import AsyncMock

import pytest

from cationbot.models.reactions import (
    get_member_from_reaction,
    is_reaction_on_message,
)


def test_is_reaction_on_message_should_return_false_when_user_id_is_the_same_of_bot_id(
    faker,
    mocker,
):
    user_id = faker.pyint()

    event = mocker.MagicMock()
    event.user_id = user_id

    bot = mocker.MagicMock()
    bot.user.id = user_id

    assert not is_reaction_on_message(
        bot=bot,
        event=event,
        message_id=faker.pyint(),
    )


def test_is_reaction_on_message_should_return_false_if_the_event_message_id_is_not_the_id_provide_on_param(
    faker,
    mocker,
):
    event = mocker.MagicMock()
    event.user_id = faker.pyint(min_value=1, max_value=99)
    event.message_id = faker.pyint(min_value=1, max_value=99)

    bot = mocker.MagicMock()
    bot.user.id = faker.pyint(min_value=100, max_value=199)

    assert not is_reaction_on_message(
        bot=bot,
        event=event,
        message_id=faker.pyint(min_value=100, max_value=199),
    )


def test_is_reaction_on_rules_message_should_return_true_if_the_event_message_id_is_equal_to_the_id_provided_on_parameters(
    faker,
    mocker,
):
    message_id = faker.pyint()

    event = mocker.MagicMock()
    event.user_id = faker.pyint(min_value=1, max_value=99)
    event.message_id = message_id

    bot = mocker.MagicMock()
    bot.user.id = faker.pyint(min_value=100, max_value=199)

    assert is_reaction_on_message(
        bot=bot,
        event=event,
        message_id=message_id,
    )


@pytest.mark.asyncio
async def test_get_member_from_reaction_should_fetch_guild_and_member_with_correct_params(
    faker,
):
    guild_id = faker.pyint()
    user_id = faker.pyint()

    guild = AsyncMock()
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.guild_id = guild_id
    event.user_id = user_id

    await get_member_from_reaction(bot=bot, event=event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
