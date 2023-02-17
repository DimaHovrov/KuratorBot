from telegram.ext import BasePersistence
from typing import DefaultDict
from collections import defaultdict
from telegram.ext.utils.types import ConversationDict, CDCData, UD
from db import query_db as db
import json


class YdbPersistance(BasePersistence):
    def __init__(self) -> None:
        super().__init__(
            store_user_data=True,
            store_chat_data=False,
            store_bot_data=False,
            store_callback_data=False,
        )
        

    def get_chat_data(self) -> dict[int, dict]:
        return {}


    def get_conversations(self, name) -> dict:
        db.query = f"""select Name, Key, State 
                       from Conversations
                       where Name='{name}'"""

        result = db.pool.retry_operation_sync(db.execute_query)

        conversation = {}

        for row in result[0].rows:
            key = tuple(json.loads(row.Key))
            conversation[key] = row.State
        return conversation


    def get_user_data(self) -> DefaultDict[int, dict]:
        result = defaultdict(dict)
        
        db.query = f"""select Data, TelegramId
                       from UserData"""
        
        rows = db.pool.retry_operation_sync(db.execute_query)
        for row in rows[0].rows:
            data = row.Data
            user_id = row.TelegramId
            result[user_id] = json.loads(data)

        return result


    def get_bot_data(self) -> dict:
        return {}


    def update_bot_data(self, data):
        pass


    def update_chat_data(self, chat_id, data):
        pass


    def update_conversation(self, name, key:tuple[int, ...], new_state):
        if new_state:
            max_id = db.get_max_id_Conversations() + 1
            json_key = json.dumps(key)
            db.query = f"""insert into Conversations (Id, Key, Name, State)  
                           values({max_id}, '{json_key}', '{name}', {new_state})"""
        else:
            json_key = json.dumps(key)
            db.query = f"""delete from Conversations
                           where Name='{name}' and
                           CAST(Key as Utf8) =='{json_key}'"""
        
        db.pool.retry_operation_sync(db.execute_query)


    def update_user_data(self, user_id, data:dict):
        if data:
            data = json.dumps(data)
            db.query = f"""upsert into UserData (TelegramId, Data, Updated)
                        values({user_id}, '{data}', CurrentUtcDatetime())"""
        else:
            db.query = f"""delete from UserData
                           where TelegramId = {user_id}"""
        db.pool.retry_operation_sync(db.execute_query)
        print(data)