from telegram import (Update, InlineKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (ContextTypes)
import web_app.create_new_vote as create_new_vote
import web_app.create_new_answer as create_new_answer
import general.keyboards as keyboards

import model.User as user_module

def web_app_data(update: Update, context: ContextTypes):
    """Срабатывает когда юзер создает или отвечает на опрос"""
    web_app_data = update.message.web_app_data

    telegram_id = update.message.from_user.id
    user = user_module.get_user_by_telegram_id(telegram_id)
    user_access = user_module.get_user_access(user)

    if (user == None):
        update.message.reply_text('У вас нет доступа к данной команде')
        return
    
    if not (user_access == user_module.ADMIN or user_access == user_module.TUTOR):
        vote_answer = create_new_answer.create_new_answer(user, web_app_data)
        if vote_answer == False:
            update.message.reply_text(text = "При отправке данных произошла ошибка")
        else:
            update.message.reply_text(text = "Ваш ответ успешно отправлен", reply_markup=ReplyKeyboardRemove())
        return

    vote = create_new_vote.create_new_vote(telegram_id, web_app_data)

    context.user_data['choosed_vote_id'] = vote.id
    context.user_data['choosed_vote_description'] = vote.description

    message = f"""Описание: {vote.description}"""
    reply_markup = InlineKeyboardMarkup(keyboards.keyboard_send_vote)
    update.message.reply_text(text=message, reply_markup=reply_markup)