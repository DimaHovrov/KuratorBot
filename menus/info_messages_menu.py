from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Мне очень жаль')
    return ConversationHandler.END