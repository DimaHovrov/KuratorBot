from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

import general.patterns_states as p_s
import model.Group as Group
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
    query.edit_message_text(text=f"Selected option: {query.data}")


def send_info_messages_icallback(update: Update, context: CallbackContext):
    global groups_keyboard
    query = update.callback_query
    query.answer()

    reply_markup = InlineKeyboardMarkup(groups_keyboard)
    query.message.reply_text(
        'Выберите группы на которые хотите отправить сообщение', reply_markup=reply_markup)


def get_id_group_by_pattern(pattern):
    len_prefix = len(prefix_group_pattern)
    len_pattern = len(pattern)
    pattern_index = pattern[len_prefix:len_pattern]
    return int(pattern_index)  # число после group


def get_button_group_index(pattern_index):
    row = pattern_index/max_count_buttons_in_line
    col = pattern_index % max_count_buttons_in_line
    return (row, col)


def get_inline_buttons_group(groups):
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
        groups_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=prefix_group_pattern+str(group.id)))
    return groups_keyboard

groups = Group.get_all_groups()
groups_keyboard = get_inline_buttons_group(groups)
