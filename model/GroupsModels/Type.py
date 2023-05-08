import db.query_db as db

class Type:
    id: int
    name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']



def get_type_by_id(id):
    try:
        db.query = f"""select * from Type where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        type = Type(id=id, name=row.Name)
        return type
    except Exception as exp:
        return False