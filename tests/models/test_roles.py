from unittest.mock import AsyncMock

import pytest

from cationbot.models.roles import find_role_by_name, toggle_role


def test_find_role_by_name_should_return_none_if_role_is_not_found(
    faker,
    mocker,
):

    mocker.patch.dict("cationbot.models.roles.tech_roles", {})
    mocker.patch.dict("cationbot.models.roles.hierarchy_roles", {})

    guild = mocker.MagicMock()

    assert (
        find_role_by_name(
            role=faker.word(),
            guild=guild,
        )
        is None
    )


def test_find_role_by_name_should_call_utils_from_discord_lib(
    faker,
    mocker,
):
    role = faker.word()
    role_id = faker.pyint()

    guild = mocker.MagicMock()
    guild.roles = role

    utils = mocker.patch("cationbot.models.roles.utils")
    utils.get.return_value = role

    mocker.patch.dict("cationbot.models.roles.tech_roles", {role: role_id})
    mocker.patch.dict("cationbot.models.roles.hierarchy_roles", {})

    assert role == find_role_by_name(
        role=role,
        guild=guild,
    )

    utils.get.assert_called_once_with(role, id=role_id)


@pytest.mark.asyncio
async def test_toggle_role_should_add_role_when_add_is_true(
    faker,
    mocker,
):
    username = faker.user_name()
    role = faker.word()
    logging = mocker.patch("cationbot.models.roles.logging")

    member = AsyncMock()
    member.__str__.return_value = username
    roles = AsyncMock()
    roles.__str__.return_value = role

    await toggle_role(member=member, roles=roles, add=True)
    logging.info.assert_called_once_with(
        f"Added roles '{role}' to/from '{username}'"
    )


@pytest.mark.asyncio
async def test_toggle_role_should_remove_role_when_add_is_false(
    faker,
    mocker,
):
    username = faker.user_name()
    role = faker.word()
    logging = mocker.patch("cationbot.models.roles.logging")

    member = AsyncMock()
    member.__str__.return_value = username
    roles = AsyncMock()
    roles.__str__.return_value = role

    await toggle_role(member=member, roles=roles, add=False)
    logging.info.assert_called_once_with(
        f"Removed roles '{role}' to/from '{username}'"
    )
