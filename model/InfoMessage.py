# Класс объявления и связанные с ним запросы в бд
import db.query_db as db


class InfoMessage:
    id: int
    category_id: str
    keywords: str
    message: str
    title: str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.category_id = kwargs['category_id']
        self.keywords = kwargs['keywords']
        self.message = kwargs['message']
        self.title = kwargs['title']


info_message = InfoMessage(id=1, category_id=1,
                           keywords='сделать сходить', message='приказ приказ',
                           title='Важное мероприятие')


def get_all_info_messages():
    db.query = f"""select * from InfoMessages"""
    result = db.pool.retry_operation_sync(db.execute_query)
    info_messages = []
    for row in result[0].rows:
        id = row.id
        category_id = row.CategoryId
        keywords = row.Keywords
        message = row.Message
        title = row.Title
        info_messages.append(InfoMessage(id=id, category_id=category_id,
                                         keywords=keywords, message=message,
                                         title=title))
    return info_messages


def get_info_message_by_id(id):
    db.query = f"""select * from InfoMessages where id={id}"""
    result = db.pool.retry_operation_sync(db.execute_query)

    if (len(result[0].rows) == 0):
        return None

    id = result[0].rows[0].id
    category_id = result[0].rows[0].CategoryId
    keywords = result[0].rows[0].Keywords
    message = result[0].rows[0].Message
    title = result[0].rows[0].Title

    info_message = InfoMessage(id=id, category_id=category_id,
                               keywords=keywords, message=message,
                               title=title)

    return info_message


def get_info_messages_by_title(title_text):
    # добавить поиск по расстоянию
    db.query = f"""select * from InfoMessages where Title="{title_text}";"""
    result = db.pool.retry_operation_sync(db.execute_query)

    if (len(result[0].rows) == 0):
        return []

    id = result[0].rows[0].id
    category_id = result[0].rows[0].CategoryId
    keywords = result[0].rows[0].Keywords
    message = result[0].rows[0].Message
    title = result[0].rows[0].Title

    info_message = InfoMessage(id=id, category_id=category_id,
                               keywords=keywords, message=message,
                               title=title)

    return [info_message]


def get_info_messages_by_category(category_name):
    # добавить поиск по расстоянию
    db.query = f"""select a.id as id, a.CategoryId as CategoryId, 
                   a.Keywords as Keywords, a.Message as Message, 
                   a.Title as Title
                   from InfoMessages as a
                   inner join Catergorys as b
                   on a.CategoryId = b.id
                   where b.Name = '{category_name}'; """

    result = db.pool.retry_operation_sync(db.execute_query)

    if (len(result[0].rows) == 0):
        return []

    info_messages = []
    for row in result[0].rows:
        id = row.id
        category_id = row.CategoryId
        keywords = row.Keywords
        message = row.Message
        title = row.Title

        info_messages.append(InfoMessage(id=id, category_id=category_id,
                                   keywords=keywords, message=message,
                                   title=title))
    return info_messages

def add_info_message(info_message: InfoMessage):
    try:
        id = int(get_max_id()) + 1
        author_id = 1
        category_id = info_message.category_id
        keywords = ""
        message = info_message.message
        title = info_message.title

        print(id, author_id, category_id, message, title)
        db.query = f"""insert into InfoMessages(id, AuthorId, 
                       CategoryId, Keywords, Message, Title) 
                    values ({id},{author_id}, {category_id}, '{keywords}',
                            '{message}','{title}')"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        print(exp)
        return False


def update_info_messages(info_message: InfoMessage):
    try:
        db.query = f"""UPDATE InfoMessages
                        SET Title = '{info_message.title}',
                            CategoryId = {info_message.category_id},
                            Message = '{info_message.message}'
                        WHERE id = {info_message.id};"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as error:
        print(error)
        return False


def delete_info_message_by_id(info_message_id):
    try:
        db.query = f"""delete from InfoMessages 
                    where id = {info_message_id}"""

        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        return False


def check_author_in_info_message(user_id, info_message_id):
    db.query = f"""select AuthorId 
                   from InfoMessages
                   where id={info_message_id}"""

    result = db.pool.retry_operation_sync(db.execute_query)

    author_id = None if len(
        result[0].rows) == 0 else result[0].rows[0].AuthorId
    return author_id == user_id


def get_max_id():
    db.query = f"""select max(id) as id from InfoMessages"""
    result = db.pool.retry_operation_sync(db.execute_query)
    return result[0].rows[0].id
