import os
import ydb
from telegram import Update
from ydb.iam import ServiceAccountCredentials


def get_endpoint():
    return 'grpcs://ydb.serverless.yandexcloud.net:2135'


def get_database():
    return '/ru-central1/b1gujjgo5f2o8ovcu1b9/etn21441nb8nqeka0c4j'


def get_sa_key_file():
    return os.getenv("SA_KEY_FILE")


welcome_text = 'Я вас узнал. Ваши данные присутствуют в базе, поэтому у вас есть доступ к командам данного бота'
goodbye_text = 'Я вас не узнал. Иди- ка ты нафиг!'

credentials = ServiceAccountCredentials.from_file(get_sa_key_file())
driver = ydb.Driver(endpoint=get_endpoint(),
                    database=get_database(), credentials=credentials)


driver.wait(timeout=5)


pool = ydb.SessionPool(driver)


def welcome_user(update: Update, result):
    Id = result[0].Id
    telegram_id = update.message.from_user.id
    set_telegram_id_by_id(Id, telegram_id)

    update.message.reply_text(welcome_text)


def user_reg_in_bot(update: Update):
    """ проверка на регистрацию юзера """
    contact = update.message.contact
    phone_number = contact.phone_number
    result = get_user_by_phone_number(phone_number)

    if len(result) > 0:
        welcome_user(update, result)
    else:
        update.message.reply_text(goodbye_text)


query = ''


def execute_query(session):
    # create the transaction and execute query.
    return session.transaction().execute(
        query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )


def get_user_by_phone_number(phone_number):
    global query
    query = f"""select * from Users as user where user.PhoneNumber = "{phone_number}";"""

    result = pool.retry_operation_sync(execute_query)
    return result[0].rows


def get_all_info_messages():
    global query
    query = f"""select * from InfoMessages"""
    result = pool.retry_operation_sync(execute_query)
    return result[0].rows


def get_info_message_by_id(id):
    global query
    query = f"""select * from InfoMessages where id={id}"""
    result = pool.retry_operation_sync(execute_query)
    return result[0].rows


def set_telegram_id_by_id(id, telegram_id):
    global query
    query = f"""update Users set TelegramId = {telegram_id} where Id = {id} """
    result = pool.retry_operation_sync(execute_query)
    return result[0].rows
