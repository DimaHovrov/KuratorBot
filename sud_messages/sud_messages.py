from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

import general.patterns_states as p_s
keyboard_choosed_messaged_info = [[
    InlineKeyboardButton("Отправить", callback_data=str(p_s.SEND_MESSAGE_PATTERN)),
    InlineKeyboardButton("Изменить", callback_data=str(p_s.UPDATE_MESSAGE_PATTERN)),
    InlineKeyboardButton("Удалить", callback_data=str(p_s.DELETE_MESSAGE_PATTERN))
]]


def send_info_messages_icallback(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.reply_text(text="its worked");