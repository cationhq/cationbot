from unittest.mock import AsyncMock

import pytest

from cationbot.cogs.auto_member import AutoMember


@pytest.mark.asyncio
async def test_on_raw_reaction_add_should_call_toggle(mocker):
    toggle = mocker.patch.object(AutoMember, "_toggle")

    bot = AsyncMock()
    event = AsyncMock()

    auto_member = AutoMember(bot=bot)
    await auto_member.on_raw_reaction_add(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_on_raw_reaction_remove_should_call_toggle(mocker):
    toggle = mocker.patch.object(AutoMember, "_toggle")

    bot = AsyncMock()
    event = AsyncMock()

    auto_member = AutoMember(bot=bot)
    await auto_member.on_raw_reaction_remove(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_emoji_name_is_not_a_green_check_mark(
    faker,
):
    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_message_id_is_not_the_rules_message_id(
    faker,
    mocker,
):
    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = faker.pyint(min_value=0, max_value=4)

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.message_id = faker.pyint(min_value=5, max_value=10)

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_member_is_not_found(
    faker,
    mocker,
):
    members_role = faker.pyint()
    message_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])

    logging = mocker.patch("cationbot.cogs.auto_member.logging")
    get = mocker.patch("cationbot.cogs.auto_member.get")
    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = members_role

    guild = AsyncMock()
    guild.roles = guild_roles
    guild.fetch_member.return_value = None
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = "✅"
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
    get.assert_called_once_with(guild_roles, id=members_role)
    logging.info.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_role_is_not_found(
    faker,
    mocker,
):
    members_role = faker.pyint()
    message_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])

    logging = mocker.patch("cationbot.cogs.auto_member.logging")
    get = mocker.patch("cationbot.cogs.auto_member.get", return_value=None)
    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = members_role

    member = AsyncMock()
    guild = AsyncMock()
    guild.roles = guild_roles
    guild.fetch_member.return_value = member
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = "✅"
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
    get.assert_called_once_with(guild_roles, id=members_role)
    logging.info.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_add_role_when_event_type_is_REACTION_ADD(
    faker,
    mocker,
):
    members_role = faker.pyint()
    message_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])
    role_name = faker.word()
    display_name = faker.name()

    role = AsyncMock()
    role.name = role_name

    logging = mocker.patch("cationbot.cogs.auto_member.logging")
    get = mocker.patch("cationbot.cogs.auto_member.get", return_value=role)
    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = members_role

    member = AsyncMock()
    member.display_name = display_name
    guild = AsyncMock()
    guild.roles = guild_roles
    guild.fetch_member.return_value = member
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = "✅"
    event.event_type = "REACTION_ADD"
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
    get.assert_called_once_with(guild_roles, id=members_role)

    member.add_roles.assert_called_once_with(role)
    member.remove_roles.assert_not_called()
    logging.info.assert_called_once_with(
        f"REACTION_ADD: "
        f"Role: '{role_name}' // "
        f"Member: '{display_name}'."
    )


@pytest.mark.asyncio
async def test_toggle_should_add_role_when_event_type_is_different_than_REACTION_ADD(
    faker,
    mocker,
):
    members_role = faker.pyint()
    message_id = faker.pyint()
    guild_id = faker.pyint()
    user_id = faker.pyint()
    guild_roles = faker.pylist(value_types=[str])
    role_name = faker.word()
    display_name = faker.name()
    event_type = faker.word()

    role = AsyncMock()
    role.name = role_name

    logging = mocker.patch("cationbot.cogs.auto_member.logging")
    get = mocker.patch("cationbot.cogs.auto_member.get", return_value=role)
    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = message_id
    env.MEMBERS_ROLE_ID = members_role

    member = AsyncMock()
    member.display_name = display_name
    guild = AsyncMock()
    guild.roles = guild_roles
    guild.fetch_member.return_value = member
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = "✅"
    event.event_type = event_type
    event.message_id = message_id
    event.guild_id = guild_id
    event.user_id = user_id

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(guild_id)
    guild.fetch_member.assert_called_once_with(user_id)
    get.assert_called_once_with(guild_roles, id=members_role)

    member.remove_roles.assert_called_once_with(role)
    member.add_roles.assert_not_called()
    logging.info.assert_called_once_with(
        f"{event_type}: "
        f"Role: '{role_name}' // "
        f"Member: '{display_name}'."
    )
