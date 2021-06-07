from unittest.mock import AsyncMock

import pytest

from cationbot.cogs.suggestions import Suggestions


@pytest.mark.asyncio
async def test_should_add_reactions_if_message_is_sent_on_suggestions_channel(
    faker,
    mocker,
):
    channel_id = faker.pyint()
    usefull_reaction = "👍"
    useless_reaction = "👎"

    bot = AsyncMock()
    env = mocker.patch("cationbot.cogs.suggestions.env")
    env.SUGGESTIONS_CHANNEL_ID = channel_id
    env.SUGGESTIONS_USEFULL_EMOJI = usefull_reaction
    env.SUGGESTIONS_USELESS_EMOJI = useless_reaction

    message = AsyncMock()
    message.channel.id = channel_id

    suggestions = Suggestions(bot)
    await suggestions.on_message(message)

    message.add_reaction.assert_any_call(usefull_reaction)
    message.add_reaction.assert_any_call(useless_reaction)
    assert message.add_reaction.call_count == 2


@pytest.mark.asyncio
async def test_should_not_add_reactions_if_message_is_not_sent_on_suggestions_channel(
    faker,
    mocker,
):
    channel_id = faker.pyint(max_value=99)
    message_channel_id = faker.pyint(min_value=100)

    bot = AsyncMock()
    env = mocker.patch("cationbot.cogs.suggestions.env")
    env.SUGGESTIONS_CHANNEL_ID = channel_id

    message = AsyncMock()
    message.channel.id = message_channel_id

    suggestions = Suggestions(bot)
    await suggestions.on_message(message)

    message.add_rection.assert_not_called()
