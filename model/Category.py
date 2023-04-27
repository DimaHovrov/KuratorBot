import db.query_db as db

class Category:
    id:int
    name:str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.name = kwargs['name']


def get_all_categorys():
    db.query = f"""select id, Name from Catergorys"""

    result = db.pool.retry_operation_sync(db.execute_query)

    categorys = []

    for category in result[0].rows:
        categorys.append(Category(id=category.id,name=category.Name))
    
    return categorys