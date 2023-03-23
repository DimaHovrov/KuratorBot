from telegram import InlineKeyboardButton
import menus.info_messages_menu as info_menu


keyboard_menu_messages_info_student = [
    [
        InlineKeyboardButton("Вывести весь список объявлений", callback_data=str(
            info_menu.ADD_INFO_MESSAGE)),
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(info_menu.TITLE_SEARCH)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(info_menu.CATEGORY_SEARCH))
    ],
]


keyboard_menu_messages_info_no_std = [
    [
        InlineKeyboardButton("Вывести весь список объявлений", callback_data=str(
            info_menu.ADD_INFO_MESSAGE))
    ],
    [
        InlineKeyboardButton("Выбор объявления",
                             callback_data=str(info_menu.TITLE_SEARCH))
    ],
    [
        InlineKeyboardButton("Поиск по заголовкам",
                             callback_data=str(info_menu.TITLE_SEARCH)),
        InlineKeyboardButton("Поиск по категориям",
                             callback_data=str(info_menu.CATEGORY_SEARCH))
    ],
    [
        InlineKeyboardButton("Создать объявление", callback_data=str(
            info_menu.ADD_INFO_MESSAGE)),
        InlineKeyboardButton("Создать категорию",
                             callback_data=str(info_menu.ADD_INFO_MESSAGE))
    ]
]
