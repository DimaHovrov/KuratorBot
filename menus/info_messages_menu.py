from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
import model.InfoMessage as info_message_module
import utils.conversation_db as c_db
import model.User as user_module

import general.patterns_states as p_s
import sud_messages.sud_messages as sud_messages

MAX_DESC_LEN = 40

keyboard_menu_messages_info_student = [
    [
        InlineKeyboardButton(
            "Вывести весь список объявлений", callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN)),
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(p_s.CATEGORY_SEARCH_PATTERN))
    ],
]


keyboard_menu_messages_info_no_std = [
    [
        InlineKeyboardButton(
            "Вывести весь список объявлений", callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN))
    ],
    [
        InlineKeyboardButton("Выбор объявления",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN))
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(p_s.CATEGORY_SEARCH_PATTERN))
    ],
    [
        InlineKeyboardButton("Создать объявление",
                             callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN)),
        InlineKeyboardButton("Создать категорию",
                             callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN))
    ]
]




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

    info_messages = [
        info_message_module.get_info_messages_by_title(title_text)]

    new_message = ''
    for i in range(len(info_messages)):
        if info_messages[i] == None:
            continue

        title = info_messages[i].title
        new_message = str(i+1) + '.' + title + '\n'
        short_desc = info_messages[i].message[:MAX_DESC_LEN] + \
            (info_messages[i].message[:MAX_DESC_LEN] and '...')
        new_message += short_desc + '\n'
        new_message += choose_command_info_message + str(i+1)
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
    info_messages = context.user_data['candidates_id']

    if message_index.isdigit() == False or int(message_index) not in info_messages:
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

    info_text_message = 'Заголовок: ' + choosed_message_object.title + '\n'
    info_text_message += 'Содержание' + choosed_message_object.message[:MAX_DESC_LEN] + (
        choosed_message_object.message[:MAX_DESC_LEN] and '...')

    telegram_id = update.message.from_user.id

    reply_markup = ''

    if (user_module.is_user_admin_or_tutor(telegram_id)):
        reply_markup = InlineKeyboardMarkup(sud_messages.keyboard_choosed_messaged_info)

    update.message.reply_text(info_text_message, reply_markup=reply_markup)

    context.user_data["choosed_info_message_id"] = message_index
    return ConversationHandler.END


# автомат поиска по категории
def category_search_ccallback(update: Update, context: CallbackContext):
    """Пользователь ввел категорию"""

    category_text = update.message.text
    info_messages = [
        info_message_module.get_info_messages_by_category(category_text)]

    new_message = ''
    for i in range(len(info_messages)):
        if info_messages[i] == None:
            continue
        title = info_messages[i].title
        new_message = str(i+1) + '.' + title + '\n'
        short_desc = info_messages[i].message[:MAX_DESC_LEN] + \
            (info_messages[i].message[:MAX_DESC_LEN] and '...')
        new_message += short_desc + '\n'
        new_message += choose_command_info_message + str(i+1)

    update.message.reply_text(new_message)
    candidates = get_ids_messages(info_messages)

    context.user_data['category'] = category_text
    context.user_data['candidates_id'] = candidates

    return p_s.CHOOSE_MESSAGE_STATE


def choose_category_ccallback(update: Update, context: CallbackContext):
    update.message.reply_text('Текст')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Мне очень жаль')
    return ConversationHandler.END


def get_ids_messages(info_messages):
    # возвращает array с id кандидатами
    data = []
    for i in range(len(info_messages)):
        if info_messages[i] == None:
            continue

        id = info_messages[i].id
        data.append(id)
    return data
