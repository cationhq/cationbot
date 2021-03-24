from unittest.mock import AsyncMock

import pytest

from cationbot.manager.message import get_message_from_channel


@pytest.mark.asyncio
async def test_should_fetch_the_channel_message_correctly(faker):
    channel_id = faker.pyint()
    message_id = faker.pyint()
    message = faker.word()

    channel = AsyncMock()
    channel.fetch_message.return_value = message

    bot = AsyncMock()
    bot.fetch_channel.return_value = channel

    actual = await get_message_from_channel(bot, channel_id, message_id)

    assert actual == message
    bot.fetch_channel.assert_called_once_with(channel_id)
    channel.fetch_message.assert_called_once_with(message_id)
