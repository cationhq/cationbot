from unittest.mock import AsyncMock

import pytest

from cationbot.helpers.roles import remove_all_roles


@pytest.mark.asyncio
async def test_remove_all_roles_should_remove_all_roles_from_member(
    faker,
    mocker,
):
    role = AsyncMock()
    role.name = faker.word()
    role.id = faker.pyint()

    guild = AsyncMock()
    guild.roles = [role]
    member = AsyncMock()
    member.roles = [role]
    member.nick = faker.user_name()
    member.remove_roles.return_value = []
    reason = faker.word()

    get = mocker.patch("cationbot.helpers.roles.get", return_value=guild.roles)
    info = mocker.patch("cationbot.helpers.roles.logging.info")

    await remove_all_roles(
        guild=guild,
        member=member,
        reason=reason,
    )

    get.assert_called_once_with(member.roles, id=role.id)
    info.assert_called_once_with(
        f"Removendo todos os cargos do membro {member.nick}"
    )
    member.remove_roles.assert_called_with(
        member.roles,
        reason=reason,
    )
