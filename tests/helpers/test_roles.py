import pytest

from cationbot.helpers.roles import (
    add_role_to_user,
    remove_all_roles,
    remove_role_from_user,
)

MODULE = "cationbot.helpers.roles"


@pytest.mark.asyncio
async def test_add_role_to_user_should_add_the_role_to_a_user_and_log_the_action(
    faker,
    mocker,
    use_role,
    use_member,
):
    logging_info = mocker.patch(f"{MODULE}.info")

    reason = faker.word()
    await add_role_to_user(
        role=use_role,
        member=use_member,
        reason=reason,
    )

    logging_info.assert_called_once_with(
        f"Atribuindo o cargo {use_role.name} para o usuário {use_member.display_name}"
    )
    use_member.add_roles.assert_called_once_with(use_role, reason=reason)


@pytest.mark.asyncio
async def test_remove_role_from_user_should_remove_the_role_from_a_user_and_log_the_action(
    faker,
    mocker,
    use_role,
    use_member,
):
    logging_info = mocker.patch(f"{MODULE}.info")

    reason = faker.word()
    await remove_role_from_user(
        role=use_role,
        member=use_member,
        reason=reason,
    )

    logging_info.assert_called_once_with(
        f"Removendo o cargo {use_role.name} do usuário {use_member.display_name}"
    )
    use_member.remove_roles.assert_called_once_with(use_role, reason=reason)


@pytest.mark.asyncio
async def test_remove_all_roles_should_remove_all_roles_from_member_and_log_the_action(
    faker,
    mocker,
    use_guild,
    use_member,
):
    logging_info = mocker.patch(f"{MODULE}.info")
    utils_get = mocker.patch(f"{MODULE}.get", return_value=use_guild.roles)

    reason = faker.word()

    await remove_all_roles(
        guild=use_guild,
        member=use_member,
        reason=reason,
    )

    logging_info.assert_called_once_with(
        f"Removendo todos os cargos do membro {use_member.display_name}"
    )
    utils_get.assert_called_once_with(
        use_guild.roles,
        id=use_member.roles[0].id,
    )
