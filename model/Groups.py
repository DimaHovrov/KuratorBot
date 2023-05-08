import db.query_db as db


class Groups:
    id: int
    name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


def get_all_groups():
    db.query = "select * from Groups"
    result = db.pool.retry_operation_sync(db.execute_query)
    groups = []
    for group in result[0].rows:
        group = Groups(id=group.Id, name=group.Name)
        groups.append(group)
    
    return groups
