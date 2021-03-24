from unittest.mock import AsyncMock

import pytest

from cationbot.controllers.auto_member_role import toggle_member_role

MODULE = "cationbot.controllers.auto_member_role"


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_member_role_if_user_is_not_found(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    bot = AsyncMock()
    event = AsyncMock()

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=False,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_member_role_if_the_reaction_is_not_a_green_check_mark(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_member_role_if_the_member_is_not_found(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=None,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_member_role_if_the_guild_is_not_found(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    guild_id = faker.pyint()

    bot = AsyncMock()
    bot.fetch_guild.return_value = None
    member = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_member_role_if_the_guild_is_not_found(
    faker,
    mocker,
):
    member_role_id = faker.pyint()
    rules_message_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = faker.word()

    guild = AsyncMock()
    guild.roles = guild_roles

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    member = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id
    env.MEMBERS_ROLE_ID = member_role_id

    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    utils_get = mocker.patch(f"{MODULE}.utils.get", return_value=None)
    info = mocker.patch(f"{MODULE}.logging.info")

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=member_role_id)
    info.assert_called_once_with(
        "Failed to edit the member role on reaction to rules message.",
        bot,
        event,
    )

    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_add_the_member_role_if_the_event_type_is_REACTION_ADD(
    faker,
    mocker,
):
    member_role_id = faker.pyint()
    rules_message_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = faker.word()
    role = faker.word()

    guild = AsyncMock()
    guild.roles = guild_roles

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    member = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.event_type = "REACTION_ADD"
    event.guild_id = guild_id

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id
    env.MEMBERS_ROLE_ID = member_role_id

    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    utils_get = mocker.patch(f"{MODULE}.utils.get", return_value=role)
    info = mocker.patch(f"{MODULE}.logging.info")

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=member_role_id)
    info.assert_not_called()
    add_role_to_member.assert_called_once_with(member, role)
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_remove_the_member_role_if_the_event_type_is_different_than_REACTION_ADD(
    faker,
    mocker,
):
    member_role_id = faker.pyint()
    rules_message_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = faker.word()
    role = faker.word()

    guild = AsyncMock()
    guild.roles = guild_roles

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    member = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.event_type = faker.word()
    event.guild_id = guild_id

    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = rules_message_id
    env.MEMBERS_ROLE_ID = member_role_id

    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    utils_get = mocker.patch(f"{MODULE}.utils.get", return_value=role)
    info = mocker.patch(f"{MODULE}.logging.info")

    await toggle_member_role(bot, event)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=member_role_id)
    info.assert_not_called()
    add_role_to_member.assert_not_called()
    remove_role_from_member.assert_called_once_with(member, role)
