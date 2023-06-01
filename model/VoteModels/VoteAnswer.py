import db.query_db as db


class VoteAnswer:
    id:int
    vote_id:int
    user_id:int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.vote_id = kwargs['vote_id']
        self.user_id = kwargs['user_id']


def add_answer(vote_id, user_id):
    try:    
        max_id = get_max_id() + 1
        db.query = f"""insert into VoteAnswer (id, UserId, VoteId)
                       values ({max_id}, {user_id}, {vote_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return max_id
    except Exception as exp:
        print(exp)
        return False


def check_answer_to_vote(user_id, vote_id):
    """Проверяет дал ли ответ юзер к опросу"""
    try:
        db.query = f"""select * from VoteAnswer
                       where VoteId = {vote_id} and UserId = {user_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)

        if len(result[0].rows) == 0:
            return False
        else:
            return True
    except Exception as exp:
        print(exp)
        return False


def get_max_id():
    db.query = f"""select max(id) as id from VoteAnswer"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id