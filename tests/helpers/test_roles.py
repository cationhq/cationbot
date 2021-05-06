from unittest.mock import AsyncMock

import pytest

from cationbot.helpers.roles import remove_all_roles

MODULE = "cationbot.helpers.roles"


@pytest.mark.asyncio
async def test_remove_all_roles_should_remove_all_roles_from_member(
    faker,
    mocker,
    use_guild,
    use_member,
):
    logging_info = mocker.patch(f"{MODULE}.logging.info")
    utils_get = mocker.patch(f"{MODULE}.get", return_value=use_guild.roles)

    reason = faker.word()

    await remove_all_roles(
        guild=use_guild,
        member=use_member,
        reason=reason,
    )

    logging_info.assert_called_once_with(
        f"Removendo todos os cargos do membro {use_member.nick}"
    )
    utils_get.assert_called_once_with(
        use_guild.roles,
        id=use_member.roles[0].id,
    )
