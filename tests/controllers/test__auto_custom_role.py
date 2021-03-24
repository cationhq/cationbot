from unittest.mock import AsyncMock

import pytest

from cationbot.controllers.auto_custom_role import toggle_custom_role

MODULE = "cationbot.controllers.auto_custom_role"


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_custom_role_if_user_is_not_found(
    mocker,
):

    bot = AsyncMock()
    event = AsyncMock()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=None,
    )

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_custom_role_if_user_does_not_have_the_member_role(
    faker,
    mocker,
):

    bot = AsyncMock()
    event = AsyncMock()
    member = AsyncMock()
    member_role_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=False,
    )
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_custom_role_if_emoji_name_is_not_present_in_available_roles(
    faker,
    mocker,
):

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()
    member = AsyncMock()
    member_role_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=True,
    )
    mocker.patch.dict(f"{MODULE}.core.language_roles", {})
    mocker.patch.dict(f"{MODULE}.core.misc_roles", {})
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_custom_role_if_the_reaction_is_not_in_specified_message(
    faker,
    mocker,
):

    lang_name = faker.word()
    lang_id = faker.pyint()

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = lang_name
    member = AsyncMock()
    member_role_id = faker.pyint()
    roles_message_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=False,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=True,
    )
    mocker.patch.dict(f"{MODULE}.core.language_roles", {lang_name: lang_id})
    mocker.patch.dict(f"{MODULE}.core.misc_roles", {})
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id
    env.ROLES_MESSAGE_ID = roles_message_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)
    is_reaction_event_on_message.assert_called_once_with(
        bot, event, roles_message_id
    )


@pytest.mark.asyncio
async def test_should_not_add_or_remove_the_custom_role_if_the_role_is_not_found(
    faker,
    mocker,
):

    lang_name = faker.word()
    lang_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = {}

    guild = AsyncMock()
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = lang_name
    event.guild_id = guild_id
    member = AsyncMock()
    member_role_id = faker.pyint()
    roles_message_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=True,
    )
    utils_get = mocker.patch(
        f"{MODULE}.utils.get",
        return_value=None,
    )
    info = mocker.patch(f"{MODULE}.logging.info")
    mocker.patch.dict(f"{MODULE}.core.language_roles", {lang_name: lang_id})
    mocker.patch.dict(f"{MODULE}.core.misc_roles", {})
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id
    env.ROLES_MESSAGE_ID = roles_message_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        roles_message_id,
    )
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=lang_id)
    info.assert_called_once_with(
        "Failed to edit the member custom role.",
        bot,
        event,
    )


@pytest.mark.asyncio
async def test_should_add_the_custom_role_when_event_type_is_REACTION_ADD(
    faker,
    mocker,
):

    lang_name = faker.word()
    lang_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = {}

    role = AsyncMock()
    guild = AsyncMock()
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = lang_name
    event.guild_id = guild_id
    event.event_type = "REACTION_ADD"
    member = AsyncMock()
    member_role_id = faker.pyint()
    roles_message_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=True,
    )
    utils_get = mocker.patch(
        f"{MODULE}.utils.get",
        return_value=role,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )
    info = mocker.patch(f"{MODULE}.logging.info")
    mocker.patch.dict(f"{MODULE}.core.language_roles", {lang_name: lang_id})
    mocker.patch.dict(f"{MODULE}.core.misc_roles", {})
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id
    env.ROLES_MESSAGE_ID = roles_message_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        roles_message_id,
    )
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=lang_id)
    info.assert_not_called()
    add_role_to_member.assert_called_once_with(
        member,
        role,
    )
    remove_role_from_member.assert_not_called()


@pytest.mark.asyncio
async def test_should_remove_the_custom_role_when_event_type_is_different_than_REACTION_ADD(
    faker,
    mocker,
):

    lang_name = faker.word()
    lang_id = faker.pyint()
    guild_id = faker.pyint()
    guild_roles = {}

    role = AsyncMock()
    guild = AsyncMock()
    guild.roles = guild_roles
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = lang_name
    event.guild_id = guild_id
    event.event_type = faker.word()
    member = AsyncMock()
    member_role_id = faker.pyint()
    roles_message_id = faker.pyint()

    get_member_from_reaction_event = mocker.patch(
        f"{MODULE}.manager.reaction.get_member_from_reaction_event",
        return_value=member,
    )
    is_reaction_event_on_message = mocker.patch(
        f"{MODULE}.manager.reaction.is_reaction_event_on_message",
        return_value=True,
    )
    member_has_role = mocker.patch(
        f"{MODULE}.manager.role.member_has_role",
        return_value=True,
    )
    utils_get = mocker.patch(
        f"{MODULE}.utils.get",
        return_value=role,
    )
    add_role_to_member = mocker.patch(
        f"{MODULE}.manager.role.add_role_to_member"
    )
    remove_role_from_member = mocker.patch(
        f"{MODULE}.manager.role.remove_role_from_member"
    )
    info = mocker.patch(f"{MODULE}.logging.info")
    mocker.patch.dict(f"{MODULE}.core.language_roles", {lang_name: lang_id})
    mocker.patch.dict(f"{MODULE}.core.misc_roles", {})
    env = mocker.patch(f"{MODULE}.core.env")
    env.MEMBERS_ROLE_ID = member_role_id
    env.ROLES_MESSAGE_ID = roles_message_id

    await toggle_custom_role(bot, event)
    get_member_from_reaction_event.assert_called_once_with(bot, event)
    member_has_role.assert_called_once_with(member, member_role_id)
    is_reaction_event_on_message.assert_called_once_with(
        bot,
        event,
        roles_message_id,
    )
    bot.fetch_guild.assert_called_once_with(guild_id)
    utils_get.assert_called_once_with(guild_roles, id=lang_id)
    info.assert_not_called()
    remove_role_from_member.assert_called_once_with(
        member,
        role,
    )
    add_role_to_member.assert_not_called()
