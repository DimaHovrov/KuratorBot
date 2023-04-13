from telegram import InlineKeyboardButton
import general.patterns_states as p_s

keyboard_menu_messages_info_student = [
    [
        InlineKeyboardButton(
            "Вывести весь список объявлений", callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN)),
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
            "Вывести весь список объявлений", callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN))
    ],
    [
        InlineKeyboardButton("Выбор объявления",
                             callback_data=str(p_s.TITLE_SEARCH_PATTERN))
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
                             callback_data=str(p_s.ADD_INFO_MESSAGE_PATTERN))
    ]
]