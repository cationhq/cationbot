from cationbot.manager.role import member_has_role


def test_should_logging_and_check_role_by_id(faker, mocker):
    role_id = faker.pyint()
    info = mocker.patch("cationbot.manager.role.logging.info")
    member = mocker.MagicMock()

    member_has_role(member, role_id)

    info.assert_called_once_with(
        f"Checking if '{member.nick}' has role by ID: {role_id}."
    )


def test_should_logging_and_check_role_by_name(faker, mocker):
    role_name = faker.word()
    info = mocker.patch("cationbot.manager.role.logging.info")
    member = mocker.MagicMock()

    member_has_role(member, role_name)

    info.assert_called_once_with(
        f"Checking if '{member.nick}' has role by name: {role_name}."
    )
