from telegram import Update
from telegram.ext import (
    CallbackContext)

import utils.category_utils as category_utils
import utils.info_message_utils as info_message_utils

import model.InfoMessage as InfoMessages
import model.Category as Category


def get_all_categorys_icallback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    category_list_message = category_utils.generate_category_message_list(
        context)
    query.message.reply_text(
        text="Список категорий\n" + category_list_message)


def get_messages_by_category(update: Update, context: CallbackContext):
    choosed_category_command = update.message.text
    category_id = category_utils.get_category_id_by_command(
        choosed_category_command, context)

    category = Category.get_category_by_id(category_id)
    info_messages = InfoMessages.get_info_messages_by_category(category.name)

    print(category.name)
    print(len(info_messages))

    message = info_message_utils.convert_models_to_message_short(
        info_messages, context)
    if len(message) == 0:
        update.message.reply_text('Сообщения с такими категориями не найдены')
    update.message.reply_text(message)
