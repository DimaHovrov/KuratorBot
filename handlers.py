from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (CommandHandler, MessageHandler,
                          CallbackContext, Filters, CallbackQueryHandler)
from telegram import Update, InlineKeyboardMarkup

import model.User as user_module
import model.GroupsModels.Uchp as uchp

import sud_messages.sud_messages as sud_messages

import menus.get_messages_menu as get_messages_menu
import menus.info_messages_search as info_messages_search
import menus.get_categorys_menu as get_categorys_menu

import general.patterns_states as p_s
import general.keyboards as keyboards
import general.conversation_handlers as conversations


def start(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('Share contact', request_contact=True)]], resize_keyboard=True)
    # update.message.reply_text('Привет! Если вы используете бот впервые отправьте номер', reply_markup=reply_markup)
    reply_markup = InlineKeyboardMarkup(keyboards.keyboard_vote_web_app)
    update.message.reply_text('Привет', reply_markup=reply_markup)


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
            keyboards.keyboard_menu_messages_info_no_std)
    else:
        reply_markup = InlineKeyboardMarkup(
            keyboards.keyboard_menu_messages_info_student)

    update.message.reply_text(title_menu_messages_info,
                              reply_markup=reply_markup)


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
        keyboards.generate_uchp_inline_buttons(uchps))
    update.message.reply_text(
        "Выберите УчП группы на которой хотите зарегестрировать студентов", reply_markup=reply_markup)


def contact_user(update: Update, context: CallbackContext) -> None:
    user_module.register_user_on_bot(update)


def reg_handlers(dispatcher):
    reg_commands(dispatcher)
    reg_callback_querys(dispatcher)
    reg_conversations(dispatcher)
    reg_message_handlers(dispatcher)


def reg_commands(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler(
        "menu_messages_info", menu_messages_info))
    dispatcher.add_handler(CommandHandler(
        "create_temporal_link", create_temporal_link))


def reg_callback_querys(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.send_info_messages_icallback, pattern="^" + str(p_s.SEND_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.delete_info_messages_icallback, pattern="^" + str(p_s.DELETE_MESSAGE_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.select_groups_icalback, pattern="^group [0-9]+ [0-9]+ [0-9]+$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.send_info_messages_after_icallback, pattern="^group send$"))
    dispatcher.add_handler(CallbackQueryHandler(
        sud_messages.question_delete_icallback, pattern="^q_delete [0-9]+$"))
    dispatcher.add_handler(CallbackQueryHandler(
        get_messages_menu.get_all_messages_ccallback, pattern="^" + str(p_s.ALL_INFO_MESSAGES_PATTERN) + "$"))
    dispatcher.add_handler(CallbackQueryHandler(
        get_categorys_menu.get_all_categorys_icallback, pattern="^" + str(p_s.ALL_CATEGORYS_PATTERN) + "$"))


def reg_conversations(dispatcher):
    dispatcher.add_handler(conversations.conv_handler_title_search)
    dispatcher.add_handler(conversations.conv_handler_category_search)
    dispatcher.add_handler(conversations.conv_handler_add_info_messages)
    dispatcher.add_handler(conversations.conv_handler_add_category)
    dispatcher.add_handler(conversations.conv_handler_update_info_messages)
    dispatcher.add_handler(conversations.conv_handler_create_temporal_link)
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_user))


def reg_message_handlers(dispatcher):
    # Когда юзер находится вне всех конверсейшнов
    dispatcher.add_handler(MessageHandler(Filters.regex(
        "^/message_[0-9]+$"), info_messages_search.choose_message_ccallback))
    dispatcher.add_handler(MessageHandler(Filters.regex(
        "^/category_[0-9]+$"), get_categorys_menu.get_messages_by_category))
