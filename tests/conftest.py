from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def use_bot(use_guild, use_channel):
    """Create a mock from the bot client."""

    bot = AsyncMock()
    bot.fetch_guild.return_value = use_guild
    bot.get_channel.return_value = use_channel
    return bot


@pytest.fixture
def use_channel(use_message):
    """Create a mock from channel."""

    channel = AsyncMock()
    channel.fetch_message.return_value = use_message
    return channel


@pytest.fixture
def use_member(faker, use_role):
    """Create a mock from member."""

    member = AsyncMock()
    member.id = faker.pyint()
    member.display_name = faker.user_name()
    member.nick = faker.user_name()
    member.roles = [use_role]
    return member


@pytest.fixture
def use_role(faker):
    """Create a mock from role."""

    role = AsyncMock()
    role.name = faker.word()
    role.id = faker.pyint()
    return role


@pytest.fixture
def use_reaction(faker, mocker, use_member):
    """Create a mock from reaction."""
    users = AsyncMock()
    users.flatten.return_value = [use_member]

    reactions = mocker.MagicMock()
    reactions.users.return_value = users
    reactions.emoji = faker.word()
    return reactions


@pytest.fixture
def use_message(faker, use_reaction):
    """Create a mock from message."""

    message = AsyncMock()
    message.id = faker.pyint()
    message.content = faker.sentence()
    message.reactions = [use_reaction]
    return message


@pytest.fixture
def use_guild(use_role, use_member):
    """Create a mock from guild."""

    guild = AsyncMock()
    guild.roles = [use_role]
    guild.fetch_member.return_value = use_member
    return guild


@pytest.fixture
def use_reaction_event(faker, use_member, use_guild, use_message):
    """Create a mock from reaction event."""

    event = AsyncMock()
    event.emoji.name = faker.word()
    event.message_id = use_message.id
    event.guild_id = use_guild.id
    event.user_id = use_member.id
    event.event_type = faker.word(
        ext_word_list=[
            "REACTION_ADD",
            "REACTION_REMOVE",
        ]
    )
    return event
