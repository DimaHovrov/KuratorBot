from telegram import InlineKeyboardButton, KeyboardButton, WebAppInfo
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
    KeyboardButton(
        "Открыть страницу опросов", web_app=WebAppInfo("https://kurator-bot.website.yandexcloud.net/"))
]]

keyboard_send_vote = [[InlineKeyboardButton(text="Отправить",
                                            callback_data=str(p_s.SEND_VOTE_PATTERN))]]