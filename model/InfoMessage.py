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
    return result[0].rows


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
