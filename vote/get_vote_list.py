from telegram import Update
from telegram.ext import CallbackContext

import model.VoteModels.VoteGroups as VoteGroups
import model.VoteModels.VoteAnswer as VoteAnswer
import model.VoteModels.Vote as Vote

import model.User as User



def get_vote_list(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id

    user = User.get_user_by_telegram_id(telegram_id)

    if (user == None):
        update.message.reply_text('У вас нет доступа к данной команде')
        return
    
    user_access = User.get_user_access(user)

    if (user_access == User.ADMIN or user_access == User.TUTOR):
        get_vote_list_tutor(user, update)
    else:
        get_vote_list_student(user, update)


def get_vote_list_tutor(user:User, update: Update):
    votes = Vote.get_votes_by_author_id(user.id)
    message = ""

    if len(votes) == 0:
        update.message.reply_text(text="Ваш список опросов пуст")
        return

    for vote in votes:
        message += f"""Описание: {vote.description}\n"""
        message += f"""/vote_{vote.id}\n"""
    
    update.message.reply_text(text="Список доступных опросов")
    update.message.reply_text(text=message)

def get_vote_list_student(user: User, update: Update):
    votes_id = VoteGroups.get_list_votes_id_by_group_id(user.groups_id)
    message = ""
    for id in votes_id:
        result = VoteAnswer.check_answer_to_vote(user.id, id)

        if result:
            votes_id.remove(id)
            continue

        vote = Vote.get_vote_by_id(id)
        message += f"""Описание: {vote.description}\n"""
        message += f"""/vote_{id}\n"""
    
    if len(message) == 0:
        update.message.reply_text(text="Ваш список доступных опросов пуст")
    else:
        update.message.reply_text(text="Список доступных опросов")
        update.message.reply_text(text=message)

        

    
