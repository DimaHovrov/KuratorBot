from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (CommandHandler, MessageHandler,
                          CallbackContext, Filters, ConversationHandler)
from telegram import Update, InlineKeyboardMarkup

import general.patterns_states as p_s

import re

import requests

def choose_group_buttons_ccalback(update:Update, context:CallbackContext):
    # Срабатывает когда юзер выбирает группу
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    group_id = int(result[0])
    context.user_data['choose_study_group_id'] = group_id

    try:
        query.message.reply_text(f"Ссылка создается, подождите ...")
        response = requests.get(f'https://localhost:7046/Registration/CreateLink?groupId={group_id}',verify=False)
        query.message.edit_text(f"Ссылка создана {response.text}")
    except Exception as exp:
        query.message.reply_text(f"При создании ссылки возникла ошибка")

    
    return ConversationHandler.END