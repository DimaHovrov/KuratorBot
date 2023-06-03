# Класс юзера и связанные с ним запросы в бд

import test
import db.query_db as db
from telegram import Update, ReplyKeyboardRemove

welcome_text = 'Я вас узнал. Ваши данные присутствуют в базе, поэтому у вас есть доступ к командам данного бота'
goodbye_text = 'Я вас не узнал. Иди- ка ты нафиг!'

NO_REG, STUDENT, TUTOR, ADMIN = range(0, 4)  # возможные доступы юзера


class User:
    """Класс пользователя"""
    id: int
    surname: str
    name: str
    patronymic: str
    groups_id: str
    telegram_login: str
    telegram_id: int
    is_connected_on_bot: bool
    is_admin: bool
    is_tutor: bool
    is_student: bool

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.surname = kwargs['surname']
        self.name = kwargs['name']
        self.patronymic = kwargs['patronymic']
        self.groups_id = kwargs['groups_id']
        self.telegram_login = kwargs['telegram_login']
        self.telegram_id = kwargs['telegram_id']
        self.is_connected_on_bot = kwargs['is_connected_on_bot']
        self.is_admin = kwargs['is_admin']
        self.is_tutor = kwargs['is_tutor']
        self.is_student = kwargs['is_student']


def user_reg_in_bot_by_contact(contact):
    """ проверка на существование в базе юзера"""
    phone_number = contact.phone_number
    user = get_user_by_phone_number(phone_number)

    return user


def welcome_user(update: Update, user: User):
    Id = user.id
    telegram_id = update.message.from_user.id
    set_telegram_id_by_id(Id, telegram_id)

    update.message.reply_text(welcome_text, reply_markup=ReplyKeyboardRemove())


def register_user_on_bot(update: Update):
    """Проверяет на существования юзера в бд. Если есть регает иначе посылает подальше"""
    contact = update.message.contact
    user = user_reg_in_bot_by_contact(contact)

    if user is not None:
        welcome_user(update, user)
    else:
        update.message.reply_text(
            goodbye_text, reply_markup=ReplyKeyboardRemove())


def get_user_by_phone_number(phone_number):
    db.query = f"""select * from Users as user where user.PhoneNumber = "{phone_number}";"""

    result = db.pool.retry_operation_sync(db.execute_query)

    if len(result[0].rows) == 0:
        return None

    user = make_user_object(result)

    return user


def get_user_by_telegram_id(telegram_id):

    db.query = f"""select * from Users as user where user.TelegramId = {telegram_id};"""

    result = db.pool.retry_operation_sync(db.execute_query)

    if len(result[0].rows) == 0:
        return None

    user = make_user_object(result)

    return user


def get_user_by_user_id(user_id):

    db.query = f"""select * from Users as user where user.Id = {user_id};"""

    result = db.pool.retry_operation_sync(db.execute_query)

    if len(result[0].rows) == 0:
        return None

    user = make_user_object(result)

    return user


def set_telegram_id_by_id(id, telegram_id):
    db.query = f"""update Users set TelegramId = {telegram_id} where Id = {id} """
    result = db.pool.retry_operation_sync(db.execute_query)
    # return result[0].rows


def get_user_access(user: User):
    if user == None:
        return NO_REG
    if bool(user.is_admin) == True:
        return ADMIN
    if bool(user.is_tutor) == True:
        return TUTOR
    if (bool(user.is_student) == True):
        return STUDENT


def get_students_telegram_id_by_group_id(group_id):
    """Возвращает массив юзеров по айди группы"""
    db.query = f"""select TelegramId 
                   from Users where GroupsId = {group_id} and IsStudent=true"""
    result = db.pool.retry_operation_sync(db.execute_query)
    result = [item.get('TelegramId') for item in result[0].rows]
    return result


def make_user_object(result):
    id = result[0].rows[0].Id
    surname = result[0].rows[0].Surname
    name = result[0].rows[0].Name
    patronymic = result[0].rows[0].Patronymic
    groups_id = result[0].rows[0].GroupsId
    telegram_login = result[0].rows[0].TelegramLogin
    telegram_id = result[0].rows[0].TelegramId
    is_connected_on_bot = result[0].rows[0].IsConnectedOnBot
    is_admin = result[0].rows[0].IsAdmin
    is_tutor = result[0].rows[0].IsTutor
    is_student = result[0].rows[0].IsStudent

    user = User(id=id, surname=surname,
                name=name, patronymic=patronymic,
                groups_id=groups_id, telegram_login=telegram_login,
                telegram_id=telegram_id, is_connected_on_bot=is_connected_on_bot,
                is_admin=is_admin, is_tutor=is_tutor,
                is_student=is_student)

    return user


def is_user_admin_or_tutor(telegram_id) -> bool:
    user = get_user_by_telegram_id(telegram_id)

    user_access = get_user_access(user)
    return user_access == ADMIN or user_access == TUTOR


"""user = User(id = 1, surname='Hovrov', 
            name='Dima', patronymic='Evg', 
            groups_id='1', telegram_login='',
            telegram_id='', is_connected_on_bot='',
            is_admin=True, is_tutor=False,
            is_student=False)

test.text = 'User'
print(test.text)
"""
