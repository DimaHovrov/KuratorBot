from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler, ConversationHandler, ContextTypes)
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

import model.User as user_module
import model.InfoMessage as InfoMessage
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
    user_module.register_user_on_bot(update)


def reg_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
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
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.send_info_messages_icallback, pattern="^" + str(p_s.SEND_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.delete_info_messages_icallback, pattern="^" + str(p_s.DELETE_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.select_groups_icalback, pattern="^group [0-9]+ [0-9]+ [0-9]+$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.send_info_messages_after_icallback, pattern="^group send$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.delete_info_messages_icallback, pattern="^" + str(p_s.DELETE_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.question_delete_icallback, pattern="^q_delete [0-9]+$"))
    dispatcher.add_handler(conv_handler_title_search)
    dispatcher.add_handler(conv_handler_category_search)
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_user))
