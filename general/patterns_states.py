# Паттерны каллбэков кнопок меню объявлений
(ALL_INFO_MESSAGES_PATTERN, TITLE_SEARCH_PATTERN,

 CATEGORY_SEARCH_PATTERN, ADD_INFO_MESSAGE_PATTERN,

 ADD_MESSAGE_CATEGORY_PATTERN, SEND_MESSAGE_PATTERN,

 UPDATE_MESSAGE_PATTERN, DELETE_MESSAGE_PATTERN,

 YES_DELETE_PATTERN, NO_DELETE_PATTERN,
#Отмена Назад
 BACK_PATTERN, CANCEL_PATTERN
) = range(12)

# состояния converations

# поиск по заголовкам и категориям состояния
(TITLE_SEARCH_STATE, CHOOSE_MESSAGE_STATE,
 CATEGORY_SEARCH_STATE, CHOOSE_CATEGORY_STATE,
# создание объявления
 TITLE_ENTER_STATE, CATEGORY_ENTER_STATE,
 CONTENT_ENTER_STATE) = range(1,8)
