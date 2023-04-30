from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import general.patterns_states as p_s
import model.InfoMessage as InfoMessage
import model.Category as Category
import utils.info_message_utils as info_message_utils
import utils.category_utils as category_utils

import sud_messages.sud_messages as sud_messages
choose_command_category = "/category_"


keyboard_skip = [[InlineKeyboardButton(
    "Пропустить", callback_data=str(p_s.SKIP_PATTERN))]]
skip_reply_markup = InlineKeyboardMarkup(keyboard_skip)


def select_update_icallback(update: Update, context: CallbackContext):
    """Срабатывает когда юзер нажимает кнопку изменить"""
    query = update.callback_query
    query.answer()
    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    message = f"""Старый заголовок: {info_message_model.title}\n\n"""
    message += "Введите новый заголовок: "

    reply_markup = InlineKeyboardMarkup(keyboard_skip)
    query.message.reply_text(text=message, reply_markup=skip_reply_markup)
    return p_s.UPDATE_TITLE_STATE


def update_title_ccallback(update: Update, context: CallbackContext):
    """Юзер ввел новый заголовок"""
    new_title = update.message.text
    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)
    info_message_model.title = new_title

    InfoMessage.update_info_messages(info_message_model)

    category = Category.get_category_by_id(info_message_model.category_id)
    message = f"""Старая категория: {category.name}\n\n"""
    message += "Выберите новую категорию: "
    update.message.reply_text(text=message)
    update.message.reply_text(text=category_utils.generate_category_message_list(context
                                                                                 ), reply_markup=skip_reply_markup)
    return p_s.UPDATE_CATEGORY_STATE


def update_category_callback(update: Update, context: CallbackContext):
    """Юзер выбрал категорию"""
    choosed_category_command = update.message.text
    len_command = len(choose_command_category)

    category_id = choosed_category_command[len_command:len(
        choosed_category_command)]

    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    info_message_model.category_id = category_id
    InfoMessage.update_info_messages(info_message_model)

    message = f"""Старое содержание: {info_message_utils
            .convert_message_to_short(info_message_model.message)}\n\n"""
    message += "Введите новое содержание: "
    update.message.reply_text(text=message, reply_markup=skip_reply_markup)
    return p_s.UPDATE_CONTENT_STATE


def update_content_callback(update: Update, context: CallbackContext):
    """Юзер ввел новое содержание"""
    new_content = update.message.text

    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    info_message_model.message = new_content

    InfoMessage.update_info_messages(info_message_model)

    update.message.reply_text(text="Ваше сообщение успешно изменено")

    info_message_text = info_message_utils.convert_model_to_message(
        info_message_model)

    reply_markup = InlineKeyboardMarkup(
        sud_messages.keyboard_choosed_messaged_info)

    update.message.reply_text(
        text=str(info_message_text), reply_markup=reply_markup)
    return ConversationHandler.END


def skip_title(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    category = Category.get_category_by_id(info_message_model.category_id)
    message = f"""Старая категория: {category.name}\n\n"""
    message += "Выберите новую категорию: "
    query.message.reply_text(text=message)
    query.message.reply_text(text=category_utils.generate_category_message_list(context
    ), reply_markup=skip_reply_markup)
    return p_s.UPDATE_CATEGORY_STATE


def skip_category(update: Update, context: CallbackContext):
    print('skip_category')
    query = update.callback_query
    query.answer()

    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    message = f"""Старое содержание: {info_message_utils
            .convert_message_to_short(info_message_model.message)}\n\n"""
    message += "Введите новое содержание: "
    query.message.reply_text(text=message, reply_markup=skip_reply_markup)
    return p_s.UPDATE_CONTENT_STATE


def skip_content(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    info_message_id = context.user_data['choosed_info_message_id']
    info_message_model = InfoMessage.get_info_message_by_id(info_message_id)

    query.message.reply_text(text="Ваше сообщение успешно изменено")

    info_message_text = info_message_utils.convert_model_to_message(
        info_message_model)

    reply_markup = InlineKeyboardMarkup(
        sud_messages.keyboard_choosed_messaged_info)

    query.message.reply_text(
        text=str(info_message_text), reply_markup=reply_markup)
    return ConversationHandler.END
