from telegram import Update
from telegram.ext import (
    CallbackContext)

import utils.info_message_utils as info_messages_utils
import model.InfoMessage as InfoMessages


def get_all_messages_ccallback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    all_messages = InfoMessages.get_all_info_messages()
    all_messages = info_messages_utils.convert_models_to_message_short(
        all_messages, context)

    query.message.reply_text(text=all_messages)
