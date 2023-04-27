from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext, ConversationHandler)

import general.patterns_states as p_s
import model.Category as Category
import model.InfoMessage as info_message
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

    category_list_message = generate_category_message_list()
    update.message.reply_text(
        text="Выберите категорию\n" + category_list_message)
    return p_s.CATEGORY_ENTER_STATE


def category_enter_ccallback(update: Update, context: CallbackContext):
    update.message.reply_text(text=str(update.message.text))
    choosed_category_command = update.message.text
    len_command = len(choose_command_category)

    category_index = choosed_category_command[len_command:len(
        choosed_category_command)]

    context.user_data['add_info_messages_category_id'] = int(category_index)

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

    if info_message.add_info_message(info_message_model):
        update.message.reply_text("Ваше сообщение успешно создано")
    else:
        update.message.reply_text(
            "При создании сообщения произошла какая-то ошибка")

    return ConversationHandler.END


def generate_category_message_list():
    categorys = Category.get_all_categorys()
    message = ""
    for category in categorys:
        id = category.id
        name = category.name
        message += f"""{id}. {name} \n    {choose_command_category}{id}\n"""

    return message
