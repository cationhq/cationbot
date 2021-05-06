from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def use_bot(mocker):
    bot = mocker.MagicMock()
    return bot


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
def use_guild(faker, use_role):
    """Create a mock from guild."""

    guild = AsyncMock()
    guild.roles = [use_role]
    return guild


@pytest.fixture
def use_reaction_event(faker, use_member):
    """Create a mock from reaction event."""

    event = AsyncMock()
    event.emoji.name = faker.word()
    event.message_id = faker.pyint()
    event.guild_id = faker.pyint()
    event.user_id = use_member.id
    event.event_type = faker.word(
        ext_word_list=[
            "REACTION_ADD",
            "REACTION_REMOVE",
        ]
    )
    return event
