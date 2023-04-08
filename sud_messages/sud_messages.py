from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

import re
import general.patterns_states as p_s
import model.Group as Group
import model.User as User
import model.InfoMessage as InfoMessage
from functools import cache

keyboard_choosed_messaged_info = [[
    InlineKeyboardButton(
        "Отправить", callback_data=str(p_s.SEND_MESSAGE_PATTERN)),
    InlineKeyboardButton("Изменить", callback_data=str(
        p_s.UPDATE_MESSAGE_PATTERN)),
    InlineKeyboardButton("Удалить", callback_data=str(
        p_s.DELETE_MESSAGE_PATTERN))
]]

prefix_group_pattern = "group "
max_count_buttons_in_line = 4


def select_groups_icalback(update: Update, context: CallbackContext):
    """Обработка кнопок выбора группы для рассылки"""
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    id, row, col = int(result[0]), int(result[1]), int(result[2])

    group_selected(id, row, col, context.user_data)
    reply_markup = InlineKeyboardMarkup(
        update_inline_keyboard_groups(context.user_data['selected_group']))
    query.edit_message_reply_markup(reply_markup=reply_markup)


def send_info_messages_icallback(update: Update, context: CallbackContext):
    global groups_keyboard
    query = update.callback_query
    query.answer()

    reply_markup = InlineKeyboardMarkup(groups_keyboard)
    query.message.reply_text(
        'Выберите группы на которые хотите отправить сообщение', reply_markup=reply_markup)


def send_info_messages_after_icallback(update: Update, context: CallbackContext):
    """Срабатывает когда юзер нажимает кнопку отправить после выбора групп"""
    query = update.callback_query
    query.answer()
    selected_groups = context.user_data['selected_group']

    info_message_text = InfoMessage.get_info_message_by_id(
        context.user_data['choosed_info_message_id']).message

    for group_id in selected_groups:
        if not group_id:
            continue
        telegram_ids = User.get_users_telegram_id_by_group_id(group_id)

        for telegram_id in telegram_ids:
            if not telegram_id:
                continue
            query.bot.send_message(
                chat_id=telegram_id, text=info_message_text)

    query.message.reply_text(text="Сообщение успешно отправилось")


def get_id_group_by_pattern(pattern):
    len_prefix = len(prefix_group_pattern)
    len_pattern = len(pattern)
    pattern_index = pattern[len_prefix:len_pattern]
    return int(pattern_index)  # число после group


def generate_inline_buttons_group(groups):
    groups_keyboard = []
    groups_keyboard.append([])

    row_index = 0
    iteration_index = 0
    for group in groups:
        iteration_index += 1
        name = group.name
        if iteration_index % (max_count_buttons_in_line+1) == 0:
            row_index += 1
            groups_keyboard.append([])
        pattern = prefix_group_pattern + \
            str(group.id) + " " + str(row_index) + " " + \
            str(len(groups_keyboard[row_index]))
        groups_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=pattern))

    groups_keyboard.append([])
    row_index += 1
    pattern = prefix_group_pattern + 'send'
    name = 'Отправить'
    groups_keyboard[row_index].append(InlineKeyboardButton(
        name, callback_data=pattern))
    return groups_keyboard


def update_inline_keyboard_groups(selected_group):
    global groups_keyboard
    for i in range(len(groups_keyboard)):
        for j in range(len(groups_keyboard[i])):
            result = re.findall(
                "[0-9]+", groups_keyboard[i][j].callback_data)
            if len(result) == 0:
                continue
            id_button = int(result[0])
            fl = 0
            for id in selected_group:
                if id == id_button:
                    groups_keyboard[i][j].text = default_groups_keyboard[i][j].text + '+'
                    fl = 1
                    break
            if fl == 0:
                groups_keyboard[i][j].text = default_groups_keyboard[i][j].text

    return groups_keyboard


def group_selected(id, row, col, user_data):
    if check_selected_group(id, user_data) == False:
        add_group(id, row, col, user_data)
    else:
        remove_group(id, row, col, user_data)


def check_selected_group(id, user_data):
    # Проверяет был ли выбран данная группа юзером
    if 'selected_group' not in user_data:
        return False

    is_selected_group = id in user_data['selected_group']
    return is_selected_group


def add_group(id, row, col, user_data):
    if 'selected_group' not in user_data:
        user_data['selected_group'] = []

    user_data['selected_group'].append(id)


def remove_group(id, row, col, user_data):
    user_data['selected_group'].remove(id)


groups = Group.get_all_groups()
default_groups_keyboard = generate_inline_buttons_group(groups)
groups_keyboard = generate_inline_buttons_group(groups)
