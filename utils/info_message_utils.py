from telegram.ext import (CallbackContext)
import model.InfoMessage as InfoMessage

MAX_DESC_LEN = 100

choose_command_info_message = '/message_'


def convert_model_to_message(info_message: InfoMessage):
    info_text_message = 'Заголовок: ' + info_message.title + '\n'
    info_text_message += 'Содержание:\n' + info_message.message

    return info_text_message


def convert_model_to_message_short(info_message: InfoMessage):
    info_text_message = 'Заголовок: ' + info_message.title + '\n'
    info_text_message += 'Содержание:\n' + \
        convert_message_to_short(info_message.message)

    return info_text_message


def convert_models_to_message_short(info_messages):
    # Не сохраняет id выведенных сообщений в user_data
    info_text_message = ''
    i = 1
    for info_message in info_messages:
        info_text_message += str(
            i) + '. ' + convert_model_to_message_short(
            info_message) + '\n'
        info_text_message += choose_command_info_message + str(i) + '\n\n'
        i += 1
    return info_text_message


def convert_models_to_message_short(info_messages, context: CallbackContext, data_name='candidates_id'):
    # Сохраняет id выведенных сообщений в user_data
    info_text_message = ''
    i = 1
    context.user_data[data_name] = []
    for info_message in info_messages:
        info_text_message += str(
            i) + '. ' + convert_model_to_message_short(
            info_message) + '\n'
        info_text_message += choose_command_info_message + str(i) + '\n\n'
        context.user_data[data_name].append(info_message.id)
        i += 1

    return info_text_message


def convert_message_to_short(message):
    if len(message) > MAX_DESC_LEN:
        return message[:MAX_DESC_LEN] + (
            message[:MAX_DESC_LEN] and '...')
    else:
        return message
