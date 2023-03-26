import db.query_db as db


class Group:
    id: int
    name: str
    telegram_login: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.telegram_login = kwargs['telegram_login']


def get_all_groups():
    db.query = "select * from Groups"
    result = db.pool.retry_operation_sync(db.execute_query)
    groups = []
    for group in result[0].rows:
        group = Group(id=group.Id, name=group.Name,
                      telegram_login=group.TelegramLogin)
        groups.append(group)
    
    return groups
