from unittest.mock import AsyncMock

import pytest

from cationbot.manager.role import remove_role_from_member


@pytest.mark.asyncio
async def test_should_logging_and_remove_the_role_from_member(faker, mocker):
    role_name = faker.word()
    role_id = faker.pyint()
    info = mocker.patch("cationbot.manager.role.logging.info")

    member = AsyncMock()
    role = AsyncMock()
    role.name = role_name
    role.id = role_id

    await remove_role_from_member(member, role)
    info.assert_called_once_with(
        f"Removed the role {role.name} (#{role.id}) from {member}."
    )
