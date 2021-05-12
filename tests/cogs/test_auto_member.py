from unittest.mock import ANY, AsyncMock, Mock

import pytest

from cationbot.cogs.auto_member import AutoMember

MODULE = "cationbot.cogs.auto_member"


@pytest.mark.asyncio
async def test_on_raw_reaction_add_should_call_toggle(mocker):
    bot = AsyncMock()
    event = AsyncMock()
    toggle = mocker.patch.object(AutoMember, "_toggle")

    auto_member = AutoMember(bot=bot)
    await auto_member.on_raw_reaction_add(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_on_raw_reaction_remove_should_call_toggle(mocker):
    bot = AsyncMock()
    event = AsyncMock()
    toggle = mocker.patch.object(AutoMember, "_toggle")

    auto_member = AutoMember(bot=bot)
    await auto_member.on_raw_reaction_remove(event)

    toggle.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_emoji_name_is_not_a_green_check_mark():
    bot = AsyncMock()
    event = AsyncMock()

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_message_id_is_not_the_rules_message_id(
    faker,
    mocker,
):
    bot = AsyncMock()
    event = AsyncMock()
    event.emoji.name = "✅"
    event.message_id = faker.pyint()

    env = mocker.patch(f"{MODULE}.core.env")
    env.RULES_MESSAGE_ID = event.message_id + 1

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_should_bypass_if_member_is_not_found(
    faker,
    mocker,
):
    guild = AsyncMock()
    guild.fetch_member.return_value = None

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.guild_id = faker.pyint()
    event.user_id = faker.pyint()
    event.emoji.name = "✅"
    event.message_id = faker.pyint()

    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = event.message_id

    add_role_to_user = mocker.patch(f"{MODULE}.add_role_to_user")
    remove_reactions_from_message = mocker.patch(
        f"{MODULE}.remove_reactions_from_message"
    )
    remove_all_roles = mocker.patch(f"{MODULE}.remove_all_roles")

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(event.guild_id)
    bot.fetch_guild.return_value.fetch_member.assert_called_once_with(
        event.user_id
    )
    add_role_to_user.assert_not_called()
    remove_reactions_from_message.assert_not_called()
    remove_all_roles.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_add_membership_role_to_user_on_REACTION_ADD(
    faker,
    mocker,
):
    member_role_id = faker.pyint()

    member = AsyncMock()
    role = AsyncMock()

    guild = AsyncMock()
    guild.roles = faker.pylist(value_types=[str])
    guild.fetch_member.return_value = member

    bot = AsyncMock()
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.guild_id = faker.pyint()
    event.user_id = faker.pyint()
    event.message_id = faker.pyint()
    event.emoji.name = "✅"
    event.event_type = "REACTION_ADD"

    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = event.message_id
    env.MEMBERS_ROLE_ID = member_role_id
    get = mocker.patch(f"{MODULE}.get", return_value=role)

    add_role_to_user = mocker.patch(f"{MODULE}.add_role_to_user")
    remove_reactions_from_message = mocker.patch(
        f"{MODULE}.remove_reactions_from_message"
    )
    remove_all_roles = mocker.patch(f"{MODULE}.remove_all_roles")

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(event.guild_id)
    bot.fetch_guild.return_value.fetch_member.assert_called_once_with(
        event.user_id
    )
    get.assert_called_once_with(guild.roles, id=member_role_id)
    add_role_to_user.assert_called_once_with(
        role,
        member,
        "Aceitação das regras",
    )
    remove_reactions_from_message.assert_not_called()
    remove_all_roles.assert_not_called()


@pytest.mark.asyncio
async def test_toggle_add_membership_role_to_user_on_REACTION_REMOVE(
    faker,
    mocker,
):
    roles_channel_id = faker.pyint()
    roles_message_id = faker.pyint()

    member = AsyncMock()
    message = AsyncMock()
    role = AsyncMock()
    guild = AsyncMock()

    channel = AsyncMock()
    channel.fetch_message.return_value = message

    bot = AsyncMock()
    bot.get_channel.return_value = channel
    bot.fetch_guild.return_value = guild
    event = AsyncMock()
    event.guild_id = faker.pyint()
    event.user_id = faker.pyint()
    event.message_id = faker.pyint()
    event.emoji.name = "✅"
    event.event_type = "REACTION_REMOVE"

    env = mocker.patch("cationbot.cogs.auto_member.core.env")
    env.RULES_MESSAGE_ID = event.message_id
    env.ROLES_CHANNEL_ID = roles_channel_id
    env.ROLES_MESSAGE_ID = roles_message_id

    add_role_to_user = mocker.patch(f"{MODULE}.add_role_to_user")
    remove_reactions_from_message = mocker.patch(
        f"{MODULE}.remove_reactions_from_message"
    )
    remove_all_roles = mocker.patch(f"{MODULE}.remove_all_roles")

    auto_member = AutoMember(bot=bot)
    await auto_member._toggle(event)

    bot.fetch_guild.assert_called_once_with(event.guild_id)
    bot.fetch_guild.return_value.fetch_member.assert_called_once_with(
        event.user_id
    )

    add_role_to_user.assert_called_once_with(
        role,
        member,
        "Aceitação das regras",
    )
    remove_reactions_from_message.assert_not_called()
    remove_all_roles.assert_not_called()


# @pytest.mark.asyncio
# async def test_toggle_remove_membership_and_all_roles_on_REACTION_REMOVE(
#     faker,
#     mocker,
#     use_bot,
#     use_guild,
#     use_member,
#     use_message,
#     use_reaction_event,
# ):
#     roles_channel_id = faker.pyint()
#     roles_message_id = faker.pyint()

#     env = mocker.patch("cationbot.cogs.auto_member.core.env")
#     env.RULES_MESSAGE_ID = use_reaction_event.message_id
#     env.ROLES_CHANNEL_ID = roles_channel_id
#     env.ROLES_MESSAGE_ID = roles_message_id
#     use_reaction_event.emoji.name = "✅"
#     use_reaction_event.event_type = "REACTION_REMOVE"

#     add_role_to_user = mocker.patch(f"{MODULE}.add_role_to_user")
#     remove_reactions_from_message = mocker.patch(
#         f"{MODULE}.remove_reactions_from_message"
#     )
#     remove_all_roles = mocker.patch(f"{MODULE}.remove_all_roles")

#     auto_member = AutoMember(bot=use_bot)
#     await auto_member._toggle(use_reaction_event)

#     use_bot.fetch_guild.assert_called_once_with(use_reaction_event.guild_id)
#     use_bot.fetch_guild.return_value.fetch_member.assert_called_once_with(
#         use_reaction_event.user_id
#     )
#     use_bot.get_channel.assert_called_once_with(roles_channel_id)
#     use_bot.get_channel.return_value.fetch_message.assert_called_once_with(
#         roles_message_id
#     )
#     add_role_to_user.assert_not_called()
#     remove_reactions_from_message.assert_called_once_with(
#         member=use_member,
#         message=ANY,
#     )
#     remove_all_roles.assert_called_once_with(
#         use_guild,
#         use_member,
#         "Remoção da aceitação das regras",
#     )
