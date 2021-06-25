from unittest.mock import AsyncMock

import pytest

from cationbot.cogs.auto_role import AutoRole


@pytest.mark.asyncio
async def test_on_raw_reaction_add_should_call_toggle(mocker):
    toggle = mocker.patch.object(AutoRole, "_toggle")

    bot = AsyncMock()
    event = AsyncMock()

    auto_role = AutoRole(bot=bot)
    await auto_role.on_raw_reaction_add(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_on_raw_reaction_remove_should_call_toggle(mocker):
    toggle = mocker.patch.object(AutoRole, "_toggle")

    bot = AsyncMock()
    event = AsyncMock()

    auto_role = AutoRole(bot=bot)
    await auto_role.on_raw_reaction_remove(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_emoji_name_is_not_present_on_available_roles(
    faker,
    mocker,
):
    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.EMOJI_ROLES = {}

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_reaction_is_not_on_rules_message(
    faker,
    mocker,
):
    role_name = faker.word()
    role_id = faker.pyint()
    event_message_id = faker.pyint(min_value=0, max_value=9)
    roles_message_id = faker.pyint(min_value=10, max_value=19)

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = role_name
    event.message_id = event_message_id

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.ROLES_MESSAGE_ID = roles_message_id
    env.EMOJI_ROLES = {role_name: role_id}

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_user_does_not_have_the_member_role(
    faker,
    mocker,
):
    role_name = faker.word()
    role_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    message_id = faker.pyint()
    member_role_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])

    member = AsyncMock()
    guild = AsyncMock()
    guild.fetch_member.return_value = member
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = role_name
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.ROLES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = member_role_id
    env.EMOJI_ROLES = {role_name: role_id}
    get = mocker.patch("cationbot.cogs.auto_role.get", return_value=None)

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)

    get.assert_called_once_with(guild_roles, id=member_role_id)


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_role_not_found(
    faker,
    mocker,
):
    role_name = faker.word()
    role_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    message_id = faker.pyint()
    member_role_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])

    role = AsyncMock()
    member = AsyncMock()
    member.roles = [role]
    guild = AsyncMock()
    guild.fetch_member.return_value = member
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = role_name
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.ROLES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = member_role_id
    env.EMOJI_ROLES = {role_name: role_id}
    get = mocker.patch(
        "cationbot.cogs.auto_role.get", side_effect=[role, None]
    )
    logging = mocker.patch("cationbot.cogs.auto_role.logging")

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)

    assert get.call_count == 2
    get.assert_any_call(guild_roles, id=member_role_id)
    get.assert_any_call(guild_roles, id=role_id)
    logging.info.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_add_role_if_event_type_is_REACTION_ADD(
    faker,
    mocker,
):
    role_name = faker.word()
    role_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    message_id = faker.pyint()
    member_role_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])
    display_name = faker.name()

    role = AsyncMock()
    role_to_add = AsyncMock()
    role_to_add.name = role_name
    member = AsyncMock()
    member.roles = [role]
    member.display_name = display_name
    guild = AsyncMock()
    guild.fetch_member.return_value = member
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = role_name
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id
    event.event_type = "REACTION_ADD"

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.ROLES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = member_role_id
    env.EMOJI_ROLES = {role_name: role_id}
    get = mocker.patch(
        "cationbot.cogs.auto_role.get", side_effect=[role, role_to_add]
    )
    logging = mocker.patch("cationbot.cogs.auto_role.logging")

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)

    assert get.call_count == 2
    get.assert_any_call(guild_roles, id=member_role_id)
    get.assert_any_call(guild_roles, id=role_id)
    logging.info.assert_called_once_with(
        "REACTION_ADD: "
        f"Role: '{role_name}' // "
        f"Member: '{display_name}'."
    )
    member.add_roles.assert_called_once_with(role_to_add)
    member.remove_roles.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_remove_role_if_event_type_is_different_than_REACTION_ADD(
    faker,
    mocker,
):
    role_name = faker.word()
    role_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    message_id = faker.pyint()
    member_role_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])
    display_name = faker.name()
    event_type = faker.word()

    role = AsyncMock()
    role_to_remove = AsyncMock()
    role_to_remove.name = role_name
    member = AsyncMock()
    member.roles = [role]
    member.display_name = display_name
    guild = AsyncMock()
    guild.fetch_member.return_value = member
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = role_name
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id
    event.event_type = event_type

    env = mocker.patch("cationbot.cogs.auto_role.env")
    env.ROLES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = member_role_id
    env.EMOJI_ROLES = {role_name: role_id}
    get = mocker.patch(
        "cationbot.cogs.auto_role.get", side_effect=[role, role_to_remove]
    )
    logging = mocker.patch("cationbot.cogs.auto_role.logging")

    auto_role = AutoRole(bot=bot)
    await auto_role._toggle(event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)

    assert get.call_count == 2
    get.assert_any_call(guild_roles, id=member_role_id)
    get.assert_any_call(guild_roles, id=role_id)
    logging.info.assert_called_once_with(
        f"{event_type}: "
        f"Role: '{role_name}' // "
        f"Member: '{display_name}'."
    )
    member.add_roles.assert_not_called()
    member.remove_roles.assert_called_once_with(role_to_remove)
