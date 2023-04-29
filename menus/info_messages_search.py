from telegram import update
from telegram.ext import (
    CallbackContext,  ConversationHandler)
from telegram import Bot, Update, InlineKeyboardMarkup
import model.InfoMessage as info_message_module
import model.User as user_module

import general.patterns_states as p_s
import sud_messages.sud_messages as sud_messages
import utils.info_message_utils as info_message_utils

MAX_DESC_LEN = 40


# inline callbacks


def title_search_icallback(update: Update, context: CallbackContext) -> None:
    """Начинается конв поиска по заголовку"""
    query = update.callback_query
    query.answer()
    query.message.reply_text('Введите заголовок')
    return p_s.TITLE_SEARCH_STATE


def category_search_icallback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text('Введите название категории')

    return p_s.CATEGORY_SEARCH_STATE


choose_command_info_message = '/message_'


# conversation callback
# автомат поиска по заголовку
def title_search_ccallback(update: Update, context: CallbackContext):
    """Пользователь ввел заголовок поиска"""
    title_text = update.message.text

    info_messages = info_message_module.get_info_messages_by_title(title_text)
    count_message = len(info_messages)

    if count_message == 0:
        update.message.reply_text("Объявление с таким заголовком не найден")
        return p_s.TITLE_SEARCH_STATE

    new_message = ''
    for i in range(count_message):
        if info_messages[i] == None:
            continue

        new_message = str(
            i+1) + '. '+info_message_utils.convert_model_to_message_short(info_messages[i]) + '\n'
        new_message += choose_command_info_message + str(i+1) + '\n'
    update.message.reply_text(new_message)

    candidates = get_ids_messages(info_messages)

    context.user_data['title'] = title_text
    context.user_data['candidates_id'] = candidates

    return p_s.CHOOSE_MESSAGE_STATE


def choose_message_ccallback(update: Update, context: CallbackContext):
    """Пользователь выбрал сообщение"""

    choosed_message_command = update.message.text
    len_command = len(choose_command_info_message)

    message_index = choosed_message_command[len_command:len(
        choosed_message_command)]

    if message_index.isdigit() == False:
        update.message.reply_text('Команда не распознана. Попробуйте еще раз.')
        return p_s.CHOOSE_MESSAGE_STATE
    else:
        message_index = int(message_index)
        # db index
        message_index = context.user_data["candidates_id"][message_index-1]

    choosed_message_object = info_message_module.get_info_message_by_id(
        message_index)

    if choosed_message_object == None:
        update.message.reply_text(
            'Сообщение не найдено. Выберите сообщение заново')
        return p_s.CHOOSE_MESSAGE_STATE

    info_text_message = info_message_utils.convert_model_to_message(
        choosed_message_object)

    telegram_id = update.message.from_user.id

    reply_markup = ''

    if (user_module.is_user_admin_or_tutor(telegram_id)):
        reply_markup = InlineKeyboardMarkup(
            sud_messages.keyboard_choosed_messaged_info)

    update.message.reply_text(info_text_message, reply_markup=reply_markup)

    context.user_data["choosed_info_message_id"] = message_index
    return ConversationHandler.END


# автомат поиска по категории
def category_search_ccallback(update: Update, context: CallbackContext):
    """Пользователь ввел категорию"""

    category_text = update.message.text
    info_messages = info_message_module.get_info_messages_by_category(
        category_text)

    count_message = len(info_messages)
    if count_message == 0:
        update.message.reply_text("Объявление с такой категорией не найден")
        return p_s.CATEGORY_SEARCH_STATE

    new_message = ''

    for i in range(count_message):
        if info_messages[i] == None:
            continue
        new_message = str(
            i+1) + '. ' + info_message_utils.convert_model_to_message_short(info_messages[i]) + '\n'
        new_message += choose_command_info_message + str(i+1) + '\n'

    update.message.reply_text(new_message)
    candidates = get_ids_messages(info_messages)

    context.user_data['category'] = category_text
    context.user_data['candidates_id'] = candidates

    return p_s.CHOOSE_MESSAGE_STATE


def get_ids_messages(info_messages):
    # возвращает array с id кандидатами
    data = []
    for i in range(len(info_messages)):
        if info_messages[i] == None:
            continue

        id = info_messages[i].id
        data.append(id)
    return data
