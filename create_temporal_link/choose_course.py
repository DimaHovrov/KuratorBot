from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import Update, InlineKeyboardMarkup

import general.patterns_states as p_s

import re

import model.GroupsModels.StudyGroup as study_group

max_count_buttons_in_line = 4
prefix_course_pattern = "study_group "

def choose_course_buttons_ccalback(update: Update, context: CallbackContext):
    # Срабатывает когда юзер выбирает курс
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    course_id = int(result[0])
    uchp_id = int(context.user_data['choose_uchp_id'])
    context.user_data['choose_course_id'] = course_id

    groups = study_group.get_study_groups_by_ids(uchp_id, course_id)
    reply_markup = InlineKeyboardMarkup(
        generate_groups_inline_buttons(groups))
    
    query.message.edit_text(text="Выберите группу", reply_markup=reply_markup)

    return p_s.CHOOSE_GROUP_LINK_STATE


def generate_groups_inline_buttons(groups):
    groups_keyboard = []
    groups_keyboard.append([])

    row_index = 0
    iteration_index = 0
    
    for group in groups:
        iteration_index += 1

        study_group_id = group.StudyGroupId
        course_year = group.CourseNumber
        group_name = group.GroupName
        type_name = group.TypeName

        name = f"""{type_name}-{group_name}-{course_year}"""
        if iteration_index % (max_count_buttons_in_line+1) == 0:
            row_index += 1
            groups_keyboard.append([])
        pattern = prefix_course_pattern + str(study_group_id)
        groups_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=pattern))

    return groups_keyboard
