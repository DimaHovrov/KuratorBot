from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)

import general.patterns_states as p_s


def add_info_message_icallback(update: Update, context: CallbackContext):
    return p_s.TITLE_ENTER_STATE


def title_enter_ccallback(update: Update, context: CallbackContext):
    return p_s.CATEGORY_ENTER_STATE


def category_enter_ccallback(update: Update, context: CallbackContext):
    return p_s.CONTENT_ENTER_STATE


def content_enter_ccallback(update: Update, context: CallbackContext):
    return ConversationHandler.END
