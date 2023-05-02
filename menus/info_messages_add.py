from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext, ConversationHandler)

import general.patterns_states as p_s
import model.Category as Category
import model.InfoMessage as info_message

import utils.info_message_utils as info_message_utils
import utils.category_utils as category_utils

choose_command_category = "/category_"


def add_info_message_icallback(update: Update, context: CallbackContext):
    """Начинается конверсейшн по добавлению объявления"""
    query = update.callback_query
    query.answer()
    query.message.reply_text('Введите заголовок')
    return p_s.TITLE_ENTER_STATE


def title_enter_ccallback(update: Update, context: CallbackContext):
    """Пользователь вводит заголовок"""
    title_text = update.message.text
    context.user_data['add_info_messages_title'] = title_text

    category_list_message = category_utils.generate_category_message_list(
        context)
    update.message.reply_text(
        text="Выберите категорию\n" + category_list_message)
    return p_s.CATEGORY_ENTER_STATE


def category_enter_ccallback(update: Update, context: CallbackContext):
    choosed_category_command = update.message.text
    category_id = category_utils.get_category_id_by_command(
        choosed_category_command, context)

    context.user_data['add_info_messages_category_id'] = int(category_id)

    update.message.reply_text(text="Введите содержание объявление")
    return p_s.CONTENT_ENTER_STATE


def content_enter_ccallback(update: Update, context: CallbackContext):
    """юзер вводит содержание объявления"""
    id = None
    category_id = context.user_data['add_info_messages_category_id']
    keywords = None
    message = update.message.text
    title = context.user_data['add_info_messages_title']
    info_message_model = info_message.InfoMessage(
        id=id, category_id=category_id, keywords=keywords, message=message, title=title)

    info_message_text = info_message_utils.convert_model_to_message(
        info_message_model)
    if info_message.add_info_message(info_message_model):
        update.message.reply_text("Ваше сообщение успешно создано")
        update.message.reply_text(text=info_message_text)
    else:
        update.message.reply_text(
            "При создании сообщения произошла какая-то ошибка")

    return ConversationHandler.END
