import db.query_db as db


class Vote:
    id:int
    description:str
    author_id:int
    data:str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.description = kwargs['description']
        self.author_id = kwargs['author_id']
        self.data = kwargs['data']



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

def get_vote_by_id(id):
    try:
        db.query = f"""select * from Vote
                       where id = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        vote = Vote(id = id, description=row.Description, author_id = row.AuthorId, data = row.Data)
        return vote
    except Exception as exp:
        print(exp)
        return False
    
def get_votes_by_author_id(id):
    try:
        db.query = f"""select * from Vote
                       where AuthorId = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        votes = []
        for row in result[0].rows:
            vote = Vote(id = row.id, description=row.Description, author_id = row.AuthorId, data = row.Data)
            votes.append(vote)
        return votes
    except Exception as exp:
        print(exp)
        return False
    

def update_vote_data_by_id(vote_id, data):
    try:
        db.query = f"""update Vote
                       set Data='{data}'
                       where id = {vote_id}"""
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

