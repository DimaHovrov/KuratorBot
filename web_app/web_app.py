from telegram import (Update, InlineKeyboardMarkup)
from telegram.ext import (ContextTypes)
import web_app.create_new_vote as create_new_vote
import general.keyboards as keyboards


def web_app_data(update: Update, context: ContextTypes):
    web_app_data = update.message.web_app_data
    telegram_id = update.message.from_user.id
    vote = create_new_vote.create_new_vote(telegram_id, web_app_data)

    context.user_data['choosed_vote_id'] = vote.id
    context.user_data['choosed_vote_description'] = vote.description

    message = f"""Описание: {vote.description}"""
    reply_markup = InlineKeyboardMarkup(keyboards.keyboard_send_vote)
    update.message.reply_text(text=message, reply_markup=reply_markup)