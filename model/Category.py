import db.query_db as db


class Category:
    id: int
    name: str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.name = kwargs['name']


def get_all_categorys():
    db.query = f"""select id, Name from Catergorys"""

    result = db.pool.retry_operation_sync(db.execute_query)

    categorys = []

    for category in result[0].rows:
        categorys.append(Category(id=category.id, name=category.Name))

    return categorys


def add_new_category(category_name):
    try:
        id = get_max_id() + 1
        db.query = f"""insert into Catergorys(id, Name)
                       values({id}, '{category_name}')"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as error:
        print(error)
        return False


def get_max_id():
    db.query = f"""select max(id) as id from Catergorys"""
    result = db.pool.retry_operation_sync(db.execute_query)
    return result[0].rows[0].id
