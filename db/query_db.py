# необходимое для запроса в ydb

import os
import ydb
from ydb.iam import ServiceAccountCredentials

def get_endpoint():
    return 'grpcs://ydb.serverless.yandexcloud.net:2135'


def get_database():
    return '/ru-central1/b1gujjgo5f2o8ovcu1b9/etn21441nb8nqeka0c4j'


def get_sa_key_file():
    return os.getenv("SA_KEY_FILE")

credentials = ServiceAccountCredentials.from_file(get_sa_key_file())
driver = ydb.Driver(endpoint=get_endpoint(), database=get_database(), credentials=credentials)
driver.wait(timeout=10)
pool = ydb.SessionPool(driver)

query = ''


def execute_query(session):
        # create the transaction and execute query.
        return session.transaction().execute(
            query,
            commit_tx = True,
            settings = ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
        )

def get_max_id_Conversations():
        global query
        query = f"""select max(Id) as max from Conversations"""
        result = pool.retry_operation_sync(execute_query)
        
        if result[0].rows[0].max is None:
            return 0
        return int(result[0].rows[0].max)


# def get_max_id_UserData():
#     global query
#     query = f"""select max(Id) as max from UserData"""
#     result = pool.retry_operation_sync(execute_query)
    
#     if result[0].rows[0].max is None:
#         return 0

#     return int(result[0].rows[0].max)