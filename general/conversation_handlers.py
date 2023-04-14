from telegram.ext import (CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler,
                          ConversationHandler)

import menus.info_messages_search as info_messages_search
import menus.info_messages_add as info_messages_add
import menus.info_messages_menu as info_messages_menu
import general.patterns_states as p_s

# конверсейшн поиска сообщения по заголовку
conv_handler_title_search = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_search
        .title_search_icallback, pattern="^" + str(p_s.TITLE_SEARCH_PATTERN) + "$")],
    states={
        p_s.TITLE_SEARCH_STATE: [MessageHandler(Filters.text, info_messages_search.title_search_ccallback)],
        p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_search.choose_message_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_search.cancel)],
    name='TITLE_SEARCH_CONVERSATION',
    persistent=True
)

# конверсейшн поиска сообщения по категории
conv_handler_category_search = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_search
        .category_search_icallback, pattern="^" + str(p_s.CATEGORY_SEARCH_PATTERN) + "$")],
    states={
        p_s.CATEGORY_SEARCH_STATE: [MessageHandler(Filters.text, info_messages_search.category_search_ccallback)],
        p_s.CHOOSE_MESSAGE_STATE: [MessageHandler(Filters.regex("^/message_[0-9]+$"), info_messages_search.choose_message_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_search.cancel)],
    name='CATEGORY_SEARCH_CONVERSATION',
    persistent=True
)


conv_handler_add_info_messages = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        info_messages_add.add_info_message_icallback, pattern="^" +
        str(p_s.ADD_INFO_MESSAGE_PATTERN) + "$"
    )],
    states={
        p_s.TITLE_ENTER_STATE: [MessageHandler(Filters.text, info_messages_add.title_enter_ccallback)],
        p_s.CATEGORY_ENTER_STATE: [MessageHandler(Filters.text, info_messages_add.category_enter_ccallback)],
        p_s.CONTENT_ENTER_STATE: [MessageHandler(Filters.text, info_messages_add.content_enter_ccallback)],
    },
    fallbacks=[CommandHandler("cancel", info_messages_menu.cancel)],
    name='ADD_INFO_MESSAGES_CONVERSATION',
    persistent=True
)
