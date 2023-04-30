from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext, ConversationHandler)

import general.patterns_states as p_s
import model.Category as Category
import model.InfoMessage as info_message
import model.Category as Category


def add_categorys_icallback(update: Update, context: CallbackContext):
    """Пользователь нажимает Создать категорию"""
    query = update.callback_query
    query.answer()
    query.message.reply_text(text='Введите название категории')
    return p_s.ADD_CATEGORY_ENTER_STATE


def category_name_ccallback(update: Update, context: CallbackContext):
    "Пользователь вводит название категории"
    category_name = update.message.text
    result = Category.add_new_category(category_name)

    if result:
        update.message.reply_text("Категория успешно создана")
    else:
        update.message.reply_text(
            "При создании категории произошла какая-то ошибка")
    return ConversationHandler.END
