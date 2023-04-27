from telegram import Update
from telegram.ext import (
    CallbackContext)



def get_all_messages_ccallback(update: Update, context : CallbackContext):
    query = update.callback_query
    query.answer()
    
