from cationbot.manager.reaction import is_reaction_event_on_message


def test_should_return_false_if_user_id_is_the_same_of_bot_id(faker, mocker):
    user_id = faker.pyint()

    bot = mocker.MagicMock()
    bot.user.id = user_id

    event = mocker.MagicMock()
    event.user_id = user_id

    assert not is_reaction_event_on_message(bot, event, faker.pyint())


def test_should_return_false_if_event_message_id_is_not_equal_the_param_provided(
    faker,
    mocker,
):
    bot_user_id = faker.pyint(min_value=1, max_value=9)
    event_user_id = faker.pyint(min_value=10, max_value=19)
    event_message_id = faker.pyint(min_value=1, max_value=10)
    message_id = faker.pyint(min_value=11, max_value=20)

    bot = mocker.MagicMock()
    bot.user.id = bot_user_id

    event = mocker.MagicMock()
    event.user_id = event_user_id
    event.message_id = event_message_id

    assert not is_reaction_event_on_message(bot, event, message_id)


def test_should_return_true_if_event_message_id_is_equal_the_param_provided(
    faker,
    mocker,
):
    bot_user_id = faker.pyint(min_value=1, max_value=9)
    event_user_id = faker.pyint(min_value=10, max_value=19)
    message_id = faker.pyint()

    bot = mocker.MagicMock()
    bot.user.id = bot_user_id

    event = mocker.MagicMock()
    event.user_id = event_user_id
    event.message_id = message_id

    assert is_reaction_event_on_message(bot, event, message_id)
