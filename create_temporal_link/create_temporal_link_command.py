from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CallbackContext)

import model.User as user_module
import model.GroupsModels.Uchp as uchp

import general.patterns_states as p_s

max_count_buttons_in_line = 4
prefix_uchp_pattern = "uchp "


def create_temporal_link(update: Update, context: CallbackContext) -> None:
    # Создание временной ссылки для конкретной группы
    telegram_id = update.message.from_user.id

    user = user_module.get_user_by_telegram_id(telegram_id)

    if (user == None):
        update.message.reply_text('У вас нет доступа к данной команде')
        return

    user_access = user_module.get_user_access(user)
    if not (user_access == user_module.ADMIN or user_access == user_module.TUTOR):
        update.message.reply_text('У вас нет доступа к данной команде')
        return

    uchps = uchp.get_all_uchp()
    reply_markup = InlineKeyboardMarkup(
        generate_uchp_inline_buttons(uchps))
    update.message.reply_text(
        "Выберите УчП группы на которой хотите зарегестрировать студентов", reply_markup=reply_markup)

    return p_s.CHOOSE_UCHP_LINK_STATE


def generate_uchp_inline_buttons(uchps):
    uchps_keyboard = []
    uchps_keyboard.append([])

    row_index = 0
    iteration_index = 0
    for uchp in uchps:
        iteration_index += 1
        name = uchp.name
        if iteration_index % (max_count_buttons_in_line+1) == 0:
            row_index += 1
            uchps_keyboard.append([])
        pattern = prefix_uchp_pattern + str(uchp.id)
        uchps_keyboard[row_index].append(InlineKeyboardButton(
            name, callback_data=pattern))

    return uchps_keyboard
