from telegram.ext import (CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler,
                          ConversationHandler)

import menus.info_messages_search as info_messages_search
import menus.info_messages_add as info_messages_add
import menus.info_messages_menu as info_messages_menu
import menus.info_messages_add_categorys as info_messages_add_categorys
import general.patterns_states as p_s

import sud_messages.update_info_messages as update_info_messages

import create_temporal_link.choose_uchp as choose_uchp

# конверсейшн поиска сообщения по заголовку
conv_handler_title_search = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_search
        .title_search_icallback, pattern="^" + str(p_s.TITLE_SEARCH_PATTERN) + "$")],
    states={
        p_s.TITLE_SEARCH_STATE: [MessageHandler(Filters.text & ~Filters.command, info_messages_search.title_search_ccallback)],
        p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_search.choose_message_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
    name='TITLE_SEARCH_CONVERSATION',
    allow_reentry=True,
    persistent=True
)

# конверсейшн поиска сообщения по категории
conv_handler_category_search = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_search
        .category_search_icallback, pattern="^" + str(p_s.CATEGORY_SEARCH_PATTERN) + "$")],
    states={
        p_s.CATEGORY_SEARCH_STATE: [MessageHandler(Filters.text & ~Filters.command, info_messages_search.category_search_ccallback)],
        p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_search.choose_message_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
    name='CATEGORY_SEARCH_CONVERSATION',
    persistent=True
)

# конверсейшн добавления объявления
conv_handler_add_info_messages = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_add.add_info_message_icallback, pattern="^" +
        str(p_s.ADD_INFO_MESSAGE_PATTERN) + "$"
    )],
    states={
        p_s.TITLE_ENTER_STATE: [MessageHandler(Filters.text & ~Filters.command, info_messages_add.title_enter_ccallback)],
        p_s.CATEGORY_ENTER_STATE: [MessageHandler(Filters.regex("^/category_[0-9]+$"), info_messages_add.category_enter_ccallback)],
        p_s.CONTENT_ENTER_STATE: [MessageHandler(Filters.text & ~Filters.command, info_messages_add.content_enter_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
    name='ADD_INFO_MESSAGES_CONVERSATION',
    persistent=True
)


# конверсейшн добавления категории
conv_handler_add_category = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_add_categorys.add_categorys_icallback, pattern="^" +
        str(p_s.ADD_MESSAGE_CATEGORY_PATTERN) + "$"
    )],
    states={
        p_s.ADD_CATEGORY_ENTER_STATE: [MessageHandler(
            Filters.text & ~Filters.command, info_messages_add_categorys.category_name_ccallback)]
    },
    fallbacks=[CommandHandler('cancel', info_messages_menu.cancel)],
    name='ADD_CATEGORYS_CONVERSATION',
    persistent=True
)

# конверсейшн изменения сообщения
conv_handler_update_info_messages = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        update_info_messages.select_update_icallback, pattern="^" +
        str(p_s.UPDATE_MESSAGE_PATTERN) + "$"
    )],
    states={
        p_s.UPDATE_TITLE_STATE: [MessageHandler(Filters.text & ~Filters.command, update_info_messages.update_title_ccallback), CallbackQueryHandler(update_info_messages.skip_title, pattern="^" +
                                                                                                                                 str(p_s.SKIP_PATTERN) + "$")],
        p_s.UPDATE_CATEGORY_STATE: [MessageHandler(Filters.regex("^/category_[0-9]+$"), update_info_messages.update_category_callback), CallbackQueryHandler(update_info_messages.skip_category, pattern="^" +
                                                                                                                                                             str(p_s.SKIP_PATTERN) + "$")],
        p_s.UPDATE_CONTENT_STATE: [MessageHandler(Filters.text & ~Filters.command, update_info_messages.update_content_callback), CallbackQueryHandler(update_info_messages.skip_content, pattern="^" +
                                                                                                                                    str(p_s.SKIP_PATTERN) + "$")],
    },
    fallbacks=[CommandHandler('cancel', info_messages_menu.cancel)],
    name='UPDATE_INFO_MESSAGES_CONVERSATION',
    persistent=True
)

# конверсейшн создания временной ссылки
conv_handler_create_temporal_link = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        choose_uchp.choose_uchp_buttons_ccalback, pattern="^uchp [0-9]+$"
    )],
    states={
    },
    fallbacks=[CommandHandler('cancel', info_messages_menu.cancel)],
    name='CREATE_TEMPORAL_LINK_CONVERSATION',
    persistent=True
)