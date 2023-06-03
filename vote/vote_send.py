from telegram import (Update, InlineKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardMarkup)
from telegram.ext import CallbackContext
import sud_messages.sud_messages as sud_messages
#import model.Groups as Groups

import model.GroupsModels.StudyGroup as StudyGroup

import model.User as User
import model.VoteModels.VoteGroups as VoteGroups
import model.VoteModels.VoteAnswer as VoteAnswer
import model.VoteModels.Vote as Vote
import vote.vote_answer_result as vote_answer_result

import general.keyboards as keyboards
import re

prefix_choose_vote_command = '/vote_'
prefix_group_pattern = 'vote_groups '#паттерн выбора групп для рассылки опроса
user_data_groups = 'selected_vote_groups'#название свойства где лежат id выбранных групп


def vote_choose(update: Update, context: CallbackContext):
    #когда юзер выбирает опрос по команде /vote_
    result = re.findall("[0-9]+", update.message.text)
    vote_id = int(result[0])
    telegram_id = update.message.from_user.id

    user = User.get_user_by_telegram_id(telegram_id)

    if (user == None):
        update.message.reply_text('У вас нет доступа к данной команде')
        return

    user_access = User.get_user_access(user)
    reply_markup = ''

    vote = Vote.get_vote_by_id(vote_id)

    if (user_access == User.ADMIN or user_access == User.TUTOR):
        out_vote_for_tutor(update, context, vote)
        
        return
    
    #проверка на доступ к опросу
    check_access_to_vote = VoteGroups.check_group_to_vote(user.groups_id, vote.id)
    if check_access_to_vote == False:
        update.message.reply_text('У вас нет доступа к данному опросу')
        return
    
    #проверка дан ли ответ к опросу данным юзером
    check_answered = VoteAnswer.check_answer_to_vote(user.id, vote.id)
    if check_answered:
        update.message.reply_text('Вы уже ответили на данный опрос')
        return
    
    web_app_button = [[KeyboardButton(text="Ответить на опрос", web_app=WebAppInfo(f"""https://kurator-bot.website.yandexcloud.net/#/answer?voteId={vote.id}"""))]]
    reply_markup = ReplyKeyboardMarkup(web_app_button)
    update.message.reply_text('Чтобы отвеить на данный опрос пожалуйста нажмите на кнопку "Ответить на опрос"', reply_markup=reply_markup)


def send_vote_icallback(update: Update, context: CallbackContext):
    """Когда юзер нажимает кнопку отправить после выбора опроса"""
    query = update.callback_query
    query.answer()
    context.user_data[user_data_groups] = []
    
    reply_markup = InlineKeyboardMarkup(
        update_inline_keyboard_groups(context.user_data[user_data_groups], groups_keyboard))
    query.message.reply_text(
        'Выберите группы на которые хотите отправить опрос', reply_markup=reply_markup)
    

def select_groups_icalback(update: Update, context: CallbackContext):
    """Обработка кнопок выбора группы для рассылки"""
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    id, row, col = int(result[0]), int(result[1]), int(result[2])

    group_selected(id, row, col, context.user_data)
    reply_markup = InlineKeyboardMarkup(
        update_inline_keyboard_groups(context.user_data[user_data_groups], groups_keyboard))
    query.edit_message_reply_markup(reply_markup=reply_markup)


def out_vote_for_tutor(update, context, vote):
    message = vote_answer_result.out_vote_answer_result(vote)
    context.user_data['choosed_vote_id'] = vote.id
    context.user_data['choosed_vote_description'] = vote.description
    #message = f"""Описание: {vote.description}"""
    reply_markup = InlineKeyboardMarkup(keyboards.keyboard_send_vote)
    update.message.reply_text(text=message, reply_markup=reply_markup)


def update_inline_keyboard_groups(selected_group, groups_keyboard):
    for i in range(len(groups_keyboard)):
        for j in range(len(groups_keyboard[i])):
            result = re.findall(
                "[0-9]+", groups_keyboard[i][j].callback_data)
            if len(result) == 0:
                continue
            id_button = int(result[0])
            fl = 0
            for id in selected_group:
                if id == id_button:
                    groups_keyboard[i][j].text = default_groups_keyboard[i][j].text + '+'
                    fl = 1
                    break
            if fl == 0:
                groups_keyboard[i][j].text = default_groups_keyboard[i][j].text

    return groups_keyboard


def send_info_messages_after_icallback(update: Update, context: CallbackContext):
    """Срабатывает когда юзер нажимает кнопку отправить после выбора групп"""
    query = update.callback_query
    query.answer()
    selected_groups = context.user_data[user_data_groups]

    vote_id = context.user_data['choosed_vote_id']
    vote_description = context.user_data['choosed_vote_description']
    vote_text = f"""Описание {vote_description}\n {prefix_choose_vote_command}{vote_id}"""
    
    add_vote_groups(vote_id, selected_groups)
    for group_id in selected_groups:
        if not group_id:
            continue
        telegram_ids = User.get_students_telegram_id_by_group_id(group_id)

        for telegram_id in telegram_ids:
            if not telegram_id:
                continue
            query.bot.send_message(
                chat_id=telegram_id, text=vote_text)
    
    query.message.reply_text(text="Опрос успешно отправилось")


def group_selected(id, row, col, user_data):
    if check_selected_group(id, user_data) == False:
        add_group(id, row, col, user_data)
    else:
        remove_group(id, row, col, user_data)


def check_selected_group(id, user_data):
    # Проверяет был ли выбран данная группа юзером
    if user_data_groups not in user_data:
        return False

    is_selected_group = id in user_data[user_data_groups]
    return is_selected_group


def add_group(id, row, col, user_data):
    if user_data_groups not in user_data:
        user_data[user_data_groups] = []

    user_data[user_data_groups].append(id)


def remove_group(id, row, col, user_data):
    user_data[user_data_groups].remove(id)


def add_vote_groups(vote_id, groups_id):
    """Добавляет в таблицу VoteAnswer доступные учебные группы опроса"""

    for id in groups_id:
        VoteGroups.add_group(vote_id=vote_id, group_id=id)



groups = StudyGroup.get_all_study_group_with_name()
default_groups_keyboard = sud_messages.generate_inline_buttons_group(groups, prefix_group_pattern, prefix_group_pattern)
groups_keyboard = sud_messages.generate_inline_buttons_group(groups, prefix_group_pattern, prefix_group_pattern)