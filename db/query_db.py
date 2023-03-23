# необходимое для запроса в ydb

import os
import ydb
from ydb.iam import ServiceAccountCredentials


def get_endpoint():
    return os.getenv("YDB_ENDPOINT")


def get_database():
    return os.getenv("YDB_DATABASE")


def get_sa_key_file():
    return os.getenv("SA_KEY_FILE")


credentials = ServiceAccountCredentials.from_file(get_sa_key_file())
driver = ydb.Driver(
    endpoint=get_endpoint(), database=get_database(), credentials=credentials
)
driver.wait(timeout=10)
pool = ydb.SessionPool(driver)

query = ""


def execute_query(session):
    # create the transaction and execute query.
    return session.transaction().execute(
        query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
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
