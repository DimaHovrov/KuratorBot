from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackContext)
from telegram import Update
import general.patterns_states as p_s

import re

import model.GroupsModels.Course as course

import datetime

max_count_buttons_in_line = 2
prefix_course_pattern = "course "

def choose_uchp_buttons_ccalback(update:Update, context:CallbackContext):
    # Срабатывает когда юзер выбирает учп
    query = update.callback_query
    query.answer()
    result = re.findall("[0-9]+", query.data)
    uchp_id = int(result[0])

    context.user_data['choose_uchp_id'] = uchp_id

    courses = course.get_all_courses()
    reply_markup = InlineKeyboardMarkup(
        generate_course_inline_buttons(courses))
    query.message.edit_text(text="Выберите курс обучения",reply_markup=reply_markup)
    return p_s.CHOOSE_COURSE_LINK_STATE


def generate_course_inline_buttons(courses):
    courses_keyboard = []
    courses_keyboard.append([])

    row_index = 0
    iteration_index = 0

    current_year = datetime.date.today().year
    for course in courses:
        iteration_index += 1
        course_id = course.id
        course_number = (current_year%100) - course.number
        type_name = course.type_name

        name = f"""{course_number} курс ({type_name})"""
        if iteration_index % (max_count_buttons_in_line+1) == 0:
            row_index += 1
            courses_keyboard.append([])
        pattern = prefix_course_pattern + str(course_id)
        courses_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=pattern))

    return courses_keyboard