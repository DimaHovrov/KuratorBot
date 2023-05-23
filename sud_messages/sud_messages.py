from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

import re
import general.patterns_states as p_s

#import model.Groups as Groups
import model.GroupsModels.StudyGroup as StudyGroup

import model.User as User
import model.InfoMessage as InfoMessage

prefix_group_pattern = "group "
prefix_question_delete_pattern = "q_delete "  # question_delete

keyboard_choosed_messaged_info = [[
    InlineKeyboardButton(
        "Отправить", callback_data=str(p_s.SEND_MESSAGE_PATTERN)),
    InlineKeyboardButton("Изменить", callback_data=str(
        p_s.UPDATE_MESSAGE_PATTERN)),
    InlineKeyboardButton("Удалить", callback_data=str(
        p_s.DELETE_MESSAGE_PATTERN))
]]

# кнопка уточнения удаления
keyboard_question_delete = [[InlineKeyboardButton(
    "Да", callback_data=prefix_question_delete_pattern + str(p_s.YES_DELETE_PATTERN)),
    InlineKeyboardButton("Нет", callback_data=prefix_question_delete_pattern + str(
        p_s.NO_DELETE_PATTERN))]]


max_count_buttons_in_line = 4  # максимальное количество кнопок в одной строке


def select_groups_icalback(update: Update, context: CallbackContext):
    """Обработка кнопок выбора группы для рассылки"""
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    id, row, col = int(result[0]), int(result[1]), int(result[2])
    query.message.reply_text(id)
    group_selected(id, row, col, context.user_data)
    reply_markup = InlineKeyboardMarkup(
        update_inline_keyboard_groups(context.user_data['selected_group']))
    query.edit_message_reply_markup(reply_markup=reply_markup)


def question_delete_icallback(update: Update, context: CallbackContext):
    """Срабатывает когда юзер нажимает Да или нет при вопросе о удалении"""
    query = update.callback_query
    query.answer()
    result = int(re.findall("[0-9]+", query.data)[0])
    
    current_message = query.message.text
    info_message_id = context.user_data['choosed_info_message_id']
    if result == p_s.YES_DELETE_PATTERN:
        delete_result = InfoMessage.delete_info_message_by_id(info_message_id)

        if delete_result:
            new_message = current_message.rsplit('\n', 1)[0] + '\nСообщение успешно удалено'
            query.message.edit_text(text=new_message)
        else:
            new_message = current_message.rsplit('\n', 1)[0] + '\nВозникло какая-то ошибка'
            query.message.reply_text(text=new_message)
    else:
        new_message = "\n".join(current_message.split("\n")[:-2])
        reply_markup = InlineKeyboardMarkup(keyboard_choosed_messaged_info)
        query.message.edit_text(text=new_message, reply_markup=reply_markup)


def send_info_messages_icallback(update: Update, context: CallbackContext):
    """Когда юзер нажимает кнопку Отправить после выбора сообщения"""
    global groups_keyboard
    query = update.callback_query
    query.answer()

    context.user_data['selected_group'] = []
    
    reply_markup = InlineKeyboardMarkup(
        update_inline_keyboard_groups(context.user_data['selected_group']))
    query.message.reply_text(
        'Выберите группы на которые хотите отправить сообщение', reply_markup=reply_markup)


def delete_info_messages_icallback(update: Update, context: CallbackContext):
    """Когда юзер нажимает кнопку Удалить после выбора сообщения"""
    query = update.callback_query
    query.answer()

    telegram_id = query.from_user.id
    current_user = User.get_user_by_telegram_id(telegram_id)
    choosed_message_id = context.user_data["choosed_info_message_id"]

    is_author = InfoMessage.check_author_in_info_message(
        current_user.id, choosed_message_id)
    if is_author == False:
        update.message.reply_text(text="У вас нет доступа на удаление")
        return

    edit_message = query.message.text + '\n\n' + "Вы точно хотите удалить?"
    reply_markup = InlineKeyboardMarkup(keyboard_question_delete)
    query.edit_message_text(text=edit_message, reply_markup=reply_markup)


def send_info_messages_after_icallback(update: Update, context: CallbackContext):
    """Срабатывает когда юзер нажимает кнопку отправить после выбора групп"""
    query = update.callback_query
    query.answer()
    selected_groups = context.user_data['selected_group']

    info_message_text = InfoMessage.get_info_message_by_id(
        context.user_data['choosed_info_message_id']).message

    for group_id in selected_groups:
        if not group_id:
            continue
        telegram_ids = User.get_students_telegram_id_by_group_id(group_id)

        for telegram_id in telegram_ids:
            if not telegram_id:
                continue
            query.bot.send_message(
                chat_id=telegram_id, text=info_message_text)
    
    query.message.reply_text(text="Сообщение успешно отправилось")


def get_id_group_by_pattern(pattern):
    len_prefix = len(prefix_group_pattern)
    len_pattern = len(pattern)
    pattern_index = pattern[len_prefix:len_pattern]
    return int(pattern_index)  # число после group


def generate_inline_buttons_group(groups, prefix_pattern, prefix_send_pattern):
    groups_keyboard = []
    groups_keyboard.append([])

    row_index = 0
    iteration_index = 0
    for group in groups:
        iteration_index += 1
        course_year = group.course_number
        group_name = group.group_name
        type_name = group.type_name
        name = f"""{type_name}-{group_name}-{course_year}"""
        if iteration_index % (max_count_buttons_in_line+1) == 0:
            row_index += 1
            groups_keyboard.append([])
        pattern = prefix_pattern + \
            str(group.id) + " " + str(row_index) + " " + \
            str(len(groups_keyboard[row_index]))
        groups_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=pattern))

    groups_keyboard.append([])
    row_index += 1
    pattern = prefix_send_pattern + 'send'
    name = 'Отправить'
    groups_keyboard[row_index].append(InlineKeyboardButton(
        name, callback_data=pattern))
    return groups_keyboard


def update_inline_keyboard_groups(selected_group):
    global groups_keyboard
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


def group_selected(id, row, col, user_data):
    if check_selected_group(id, user_data) == False:
        add_group(id, row, col, user_data)
    else:
        remove_group(id, row, col, user_data)


def check_selected_group(id, user_data):
    # Проверяет был ли выбран данная группа юзером
    if 'selected_group' not in user_data:
        return False

    is_selected_group = id in user_data['selected_group']
    return is_selected_group


def add_group(id, row, col, user_data):
    if 'selected_group' not in user_data:
        user_data['selected_group'] = []

    user_data['selected_group'].append(id)


def remove_group(id, row, col, user_data):
    user_data['selected_group'].remove(id)


groups = StudyGroup.get_all_study_group_with_name()
default_groups_keyboard = generate_inline_buttons_group(groups, prefix_group_pattern, prefix_group_pattern)
groups_keyboard = generate_inline_buttons_group(groups, prefix_group_pattern, prefix_group_pattern)
