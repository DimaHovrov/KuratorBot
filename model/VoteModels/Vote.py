import db.query_db as db


class Vote:
    id:int
    description:str
    author_id:int
    data:str
    groups_id:str
    users_id:str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.description = kwargs['description']
        self.author_id = kwargs['author_id']
        self.data = kwargs['data']
        self.groups_id = kwargs['groups_id']
        self.users_id = kwargs['users_id']



def add_vote(vote: Vote):
    try:
        max_id = get_max_id() + 1
        vote.id = max_id
        db.query = f"""insert into Vote (id, AuthorId, Data, Description)
                       values ({max_id}, {vote.author_id}, '{vote.data}', 
                       '{vote.description}')"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        print(exp)
        return False



def get_max_id():
    db.query = f"""select max(id) as id from Vote"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id