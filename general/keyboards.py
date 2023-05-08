from telegram import InlineKeyboardButton, WebAppInfo
import general.patterns_states as p_s


keyboard_menu_messages_info_student = [
    [
        InlineKeyboardButton(
            "Вывести весь список объявлений", callback_data=str(p_s.ALL_INFO_MESSAGES_PATTERN)),
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(p_s.CATEGORY_SEARCH_PATTERN))
    ],
]


keyboard_menu_messages_info_no_std = [
    [
        InlineKeyboardButton(
            "Вывести список объявлений", callback_data=str(p_s.ALL_INFO_MESSAGES_PATTERN))
    ],
    [
        InlineKeyboardButton("Вывести список категорий",
                             callback_data=str(p_s.ALL_CATEGORYS_PATTERN))
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(p_s.CATEGORY_SEARCH_PATTERN))
    ],
    [
        InlineKeyboardButton("Создать объявление",
                             callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN)),
        InlineKeyboardButton("Создать категорию",
                             callback_data=str(p_s.ADD_MESSAGE_CATEGORY_PATTERN))
    ]
]

keyboard_vote_web_app = [[
    InlineKeyboardButton(
        "Создать опрос", web_app=WebAppInfo("https://kurator-bot.website.yandexcloud.net"))
]]

max_count_buttons_in_line = 4
prefix_uchp_pattern = "uchp "


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
