from telegram import (Update)
from telegram.ext import (ContextTypes)

def web_app_data(update: Update, context: ContextTypes):
    web_app_data = update.message.web_app_data
    update.message.reply_text(web_app_data)