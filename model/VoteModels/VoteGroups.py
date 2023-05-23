import db.query_db as db


class VoteGroups:
    id:int
    vote_id:int
    group_id:int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.vote_id = kwargs['vote_id']
        self.group_id = kwargs['group_id']


def add_group(vote_id, group_id):
    try:    
        max_id = get_max_id() + 1
        db.query = f"""insert into VoteGroups (id, GroupId, VoteId)
                       values ({max_id}, {group_id}, {vote_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        print(exp)
        return False


def check_group_to_vote(user_group_id, vote_id):
    """Проверяет есть ли доступ юзеру с группой user_group_id к опросу с id vote_id"""
    try:
        db.query = f"""select * from VoteGroups
                       where GroupId = {user_group_id} and VoteId = {vote_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)

        if len(result[0].rows) == 0:
            return False
        else:
            return True
    except Exception as exp:
        print(exp)
        return False
        

def get_max_id():
    db.query = f"""select max(id) as id from VoteGroups"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id