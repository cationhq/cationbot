from unittest.mock import AsyncMock

import pytest

from cationbot.manager.role import add_role_to_member


@pytest.mark.asyncio
async def test_should_logging_and_add_the_role_to_member(faker, mocker):
    role_name = faker.word()
    role_id = faker.pyint()
    info = mocker.patch("cationbot.manager.role.logging.info")

    member = AsyncMock()
    role = AsyncMock()
    role.name = role_name
    role.id = role_id

    await add_role_to_member(member, role)
    info.assert_called_once_with(
        f"Added the role {role.name} (#{role.id}) to '{member}."
    )
