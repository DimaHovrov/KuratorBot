from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import Update, InlineKeyboardMarkup

import re

def choose_uchp_buttons_ccalback(update:Update, context:CallbackContext):
    # Срабатывает когда юзер выбирает учп
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    id = int(result[0])

    query.message.reply_text(str(id))