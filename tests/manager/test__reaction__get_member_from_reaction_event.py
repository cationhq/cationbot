from unittest.mock import AsyncMock

import pytest

from cationbot.manager.reaction import get_member_from_reaction_event


@pytest.mark.asyncio
async def test_should_fetch_the_member_from_reaction_correctly(faker):
    guild_id = faker.pyint()
    user_id = faker.pyint()
    member = faker.word()

    event = AsyncMock()
    event.guild_id = guild_id
    event.user_id = user_id

    guild = AsyncMock()
    guild.fetch_member.return_value = member

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild

    actual = await get_member_from_reaction_event(bot, event)

    assert actual == member
    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
