import db.query_db as db


class Group:
    id: int
    name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


def get_group_by_id(id):
    try:
        db.query = f"""select * from Group where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        group = Group(id=id, name=row.Name)
        return group
    except Exception as exp:
        return False
