from unittest.mock import AsyncMock

import pytest

from cationbot.controllers.auto_role import (
    toggle_member_role,
    toggle_tech_role,
)

MODULE = "cationbot.controllers.auto_role"


@pytest.mark.asyncio
async def test_toggle_member_role_should_not_set_role_if_the_reaction_is_not_in_correct_message(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=False,
    )

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction"
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_not_called()
    bot.fetch_guild.assert_not_called()
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_member_role_should_not_set_role_if_emoji_name_is_not_green_check_mark(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction"
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_not_called()
    bot.fetch_guild.assert_not_called()
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_member_role_should_not_set_role_if_member_is_not_found(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )
    guild_id = faker.pyint()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=None,
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_member_role_should_not_set_role_if_guild_is_not_found(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    guild_id = faker.pyint()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=AsyncMock(),
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    bot.fetch_guild.return_value = None
    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_member_role_should_add_role_if_emoji_is_green_check_mark_and_event_type_is_reaction_add(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    member_role_name = faker.word()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id
    settings.MEMBER_ROLE_NAME = member_role_name

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    guild_id = faker.pyint()
    member = AsyncMock()
    guild = AsyncMock()
    role_by_name = AsyncMock()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=member,
    )
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild

    find_role_by_name = mocker.patch(
        f"{MODULE}.find_role_by_name",
        return_value=role_by_name,
    )
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id
    event.event_type = "REACTION_ADD"

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_called_once_with(
        role=member_role_name, guild=guild
    )
    toggle_role.assert_called_once_with(
        member=member,
        roles=role_by_name,
        add=True,
    )


@pytest.mark.asyncio
async def test_toggle_member_role_should_remove_role_if_emoji_is_green_check_mark_and_event_type_is_different_than_reaction_add(
    faker,
    mocker,
):
    rules_message_id = faker.pyint()
    member_role_name = faker.word()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.RULES_MESSAGE_ID = rules_message_id
    settings.MEMBER_ROLE_NAME = member_role_name

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    guild_id = faker.pyint()
    member = AsyncMock()
    guild = AsyncMock()
    role_by_name = AsyncMock()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=member,
    )
    bot = AsyncMock()
    bot.fetch_guild.return_value = guild

    find_role_by_name = mocker.patch(
        f"{MODULE}.find_role_by_name",
        return_value=role_by_name,
    )
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    event = AsyncMock()
    event.emoji.name = "✅"
    event.guild_id = guild_id
    event.event_type = faker.word()

    await toggle_member_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        rules_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_called_once_with(
        role=member_role_name, guild=guild
    )
    toggle_role.assert_called_once_with(
        member=member,
        roles=role_by_name,
        add=False,
    )


@pytest.mark.asyncio
async def test_toggle_tech_role_should_not_set_role_if_the_reaction_is_not_in_correct_message(
    faker,
    mocker,
):
    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=False,
    )

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction"
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_not_called()
    bot.fetch_guild.assert_not_called()
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_tech_role_should_not_set_role_if_emoji_name_is_not_in_tech_roles(
    faker,
    mocker,
):

    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )
    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction"
    )
    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = faker.word()

    mocker.patch.dict(f"{MODULE}.tech_roles", {})

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_not_called()
    bot.fetch_guild.assert_not_called()
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_tech_role_should_not_set_role_if_member_is_not_found(
    faker,
    mocker,
):
    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    tech_role = faker.word()
    tech_role_id = faker.pyint()
    guild_id = faker.pyint()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=None,
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    mocker.patch.dict(f"{MODULE}.tech_roles", {tech_role: tech_role_id})

    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = tech_role
    event.guild_id = guild_id

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_tech_role_should_not_set_role_if_guild_is_not_found(
    faker,
    mocker,
):
    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    tech_role = faker.word()
    tech_role_id = faker.pyint()
    guild_id = faker.pyint()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=AsyncMock(),
    )

    find_role_by_name = mocker.patch(f"{MODULE}.find_role_by_name")
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    mocker.patch.dict(f"{MODULE}.tech_roles", {tech_role: tech_role_id})

    bot = AsyncMock()
    bot.fetch_guild.return_value = None
    event = AsyncMock()
    event.emoji.name = tech_role
    event.guild_id = guild_id

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_not_called()
    toggle_role.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_member_role_should_add_tech_role_if_emoji_is_in_tech_roles_dict_and_event_type_is_reaction_add(
    faker,
    mocker,
):
    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    tech_role = faker.word()
    tech_role_id = faker.pyint()
    guild_id = faker.pyint()

    member = AsyncMock()
    guild = AsyncMock()
    role = AsyncMock()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=member,
    )

    find_role_by_name = mocker.patch(
        f"{MODULE}.find_role_by_name",
        return_value=role,
    )
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    mocker.patch.dict(f"{MODULE}.tech_roles", {tech_role: tech_role_id})

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = tech_role
    event.guild_id = guild_id
    event.event_type = "REACTION_ADD"

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_called_once_with(role=tech_role, guild=guild)
    toggle_role.assert_called_once_with(member=member, roles=role, add=True)


@pytest.mark.asyncio
async def test_toggle_member_role_should_remove_tech_role_if_emoji_is_in_tech_roles_dict_and_event_type_is_different_than_reaction_add(
    faker,
    mocker,
):
    choose_tech_message_id = faker.pyint()

    settings = mocker.patch(f"{MODULE}.settings")
    settings.CHOOSE_TECH_MESSAGE_ID = choose_tech_message_id

    is_reaction_on_message = mocker.patch(
        f"{MODULE}.is_reaction_on_message",
        return_value=True,
    )

    tech_role = faker.word()
    tech_role_id = faker.pyint()
    guild_id = faker.pyint()

    member = AsyncMock()
    guild = AsyncMock()
    role = AsyncMock()

    get_member_from_reaction = mocker.patch(
        f"{MODULE}.get_member_from_reaction",
        return_value=member,
    )

    find_role_by_name = mocker.patch(
        f"{MODULE}.find_role_by_name",
        return_value=role,
    )
    toggle_role = mocker.patch(f"{MODULE}.toggle_role")

    mocker.patch.dict(f"{MODULE}.tech_roles", {tech_role: tech_role_id})

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.emoji.name = tech_role
    event.guild_id = guild_id
    event.event_type = faker.word()

    await toggle_tech_role(bot=bot, event=event)
    is_reaction_on_message.assert_called_once_with(
        bot,
        event,
        choose_tech_message_id,
    )
    get_member_from_reaction.assert_called_once_with(bot=bot, event=event)
    bot.fetch_guild.assert_called_once_with(guild_id)
    find_role_by_name.assert_called_once_with(role=tech_role, guild=guild)
    toggle_role.assert_called_once_with(member=member, roles=role, add=False)
