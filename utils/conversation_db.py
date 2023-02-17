import db.query_db as db
import json

def conversations_start(telegram_id, data: str):
    #пользователь запускает новый конверсейшн
    delete_previous_conversation(telegram_id)#удаление всех предыдущих данных с конверсейшна
    max_id = get_max_id()
    id = max_id +1 if max_id != None else 1

    db.query = f"""insert into UserData (id, Data, TelegramId)
                   values ({id}, '{data}', {telegram_id});"""
    result = db.pool.retry_operation_sync(db.execute_query)

    
    

def conversation_state_changed(telegram_id, data: str):
    db.query = f"""update UserData
                   set Data = '{data}'
                   where TelegramId = {telegram_id}"""
    result = db.pool.retry_operation_sync(db.execute_query)


def conversation_end(telegram_id):
    #пользователь завершает конверсейшн
    return 


def get_current_conversation_data(telegram_id):
    db.query = f"""select Data from UserData where TelegramId={telegram_id}"""
    result = db.pool.retry_operation_sync(db.execute_query)
    data = result[0].rows[0].Data
    temp = json.loads(data)
    return temp


def get_max_id():
    db.query = f"""select max(id) as id from UserData"""
    result = db.pool.retry_operation_sync(db.execute_query)
    id = result[0].rows[0].id
    return id

def delete_previous_conversation(telegram_id):
    db.query = f"""delete from UserData where TelegramId = {telegram_id}"""
    result = db.pool.retry_operation_sync(db.execute_query)