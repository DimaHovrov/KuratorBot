from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

import model.User as user_module
import model as m
import re

import menus.info_messages_menu as info_messages_menu
import sud_messages.sud_messages as sud_messages
import general.patterns_states as p_s

def start(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('Share contact', request_contact=True)]], resize_keyboard=True)
    update.message.reply_text('Привет!', reply_markup=reply_markup)


def menu_messages_info(update: Update, context: CallbackContext) -> None:
    title_menu_messages_info = 'Меню объявлений'
    telegram_id = update.message.from_user.id

    user = user_module.get_user_by_telegram_id(telegram_id)

    if (user == None):
        update.message.reply_text('У вас нет доступа к данной команде')
        return

    user_access = user_module.get_user_access(user)
    reply_markup = ''

    if (user_access == user_module.ADMIN or user_access == user_module.TUTOR):
        reply_markup = InlineKeyboardMarkup(
            info_messages_menu.keyboard_menu_messages_info_no_std)
    else:
        reply_markup = InlineKeyboardMarkup(
            info_messages_menu.keyboard_menu_messages_info_student)

    update.message.reply_text(title_menu_messages_info,
                              reply_markup=reply_markup)


def contact_user(update: Update, context: CallbackContext) -> None:
    print(update.message.contact.phone_number)
    user_module.user_reg_in_bot(update)


def send_info_message(update: Update, context: CallbackContext) -> None:
    result = m.get_all_info_messages()

    send_info_message = ''
    for info_message in result:
        id = info_message.id
        message = info_message.Message
        title = info_message.Title
        command = f'/message_{id}'

        if (len(message) > 30):
            short_message = ''
            for i in range(30):
                short_message += message[i]
            message = short_message + '...'

        send_info_message += f"{str(id)}. {title} \n {message}\n {command}\n\n"
    update.message.reply_text(send_info_message)


def select_info_message(update: Update, context: CallbackContext) -> None:
    command = update.message.text
    result = re.match(r'\/message_[0-9]+', command)

    if result is None:
        update.message.reply_text('Такой команды нет!')

    start = result.start() + 9
    end = result.end()

    id = ''

    for i in range(start, end):
        id += command[i]

    info_message = m.get_info_message_by_id(int(id))

    if len(info_message) == 0:
        update.message.reply_text('Такого сообщения нет')
        return

    message = info_message[0].Message
    title = info_message[0].Title

    if (len(message) > 30):
        short_message = ''
        for i in range(30):
            short_message += message[i]
        message = short_message + '...'

    send_info_message = f"{str(id)}. {title} \n {message}\n"

    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(send_info_message, reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Option 1 selected", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_reply_markup(reply_markup=reply_markup)


def reg_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler(
        "send_info_message", send_info_message))
    dispatcher.add_handler(CommandHandler(
        "menu_messages_info", menu_messages_info))

    conv_handler_title_search = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            info_messages_menu
            .title_search_icallback, pattern="^" + str(p_s.TITLE_SEARCH_PATTERN) + "$")],
        states={
            p_s.TITLE_SEARCH_STATE: [MessageHandler(Filters.text, info_messages_menu.title_search_ccallback)],
            p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_menu.choose_message_ccallback)],
        },
        fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
        name='TITLE_SEARCH_CONVERSATION',
        persistent=True
    )

    conv_handler_category_search = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            info_messages_menu
            .category_search_icallback, pattern="^" + str(p_s.CATEGORY_SEARCH_PATTERN) + "$")],
        states={
            p_s.CATEGORY_SEARCH_STATE: [MessageHandler(Filters.text, info_messages_menu.category_search_ccallback)],
            p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_menu.choose_message_ccallback)],
        },
        fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
        name='CATEGORY_SEARCH_CONVERSATION',
        persistent=True
    )
    dispatcher.add_handler(CallbackQueryHandler(sud_messages.send_info_messages_icallback, pattern="^" + str(p_s.SEND_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(sud_messages.select_groups_icalback, pattern="^group [0-9]+$"))
    dispatcher.add_handler(conv_handler_title_search)
    dispatcher.add_handler(conv_handler_category_search)
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_user))
