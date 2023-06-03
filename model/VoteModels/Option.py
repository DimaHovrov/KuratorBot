import db.query_db as db

class Option:
    id:int
    vote_id:int
    question_id:int
    text:str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.vote_id = kwargs['vote_id']
        self.question_id = kwargs['question_id']
        self.text = kwargs['text']


def add_option(option: Option):
    try:    
        max_id = get_max_id() + 1
        option.id = max_id
        db.query = f"""insert into Option (id, QuestionId, Text, VoteId)
                       values ({max_id}, {option.question_id}, '{option.text}', {option.vote_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        print(exp,"asdfdsafdsaf")
        return False


def get_options_by_question_id(question_id):
    try:
        db.query = f"""select * from Option
                       where QuestionId = {question_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        options = []
        for row in result[0].rows:
            option = Option(id = row.id, vote_id = row.VoteId, question_id=row.QuestionId, text=row.Text)
            options.append(option)
        return options
    except Exception as exp:
        print(exp)
        return False
    

def get_max_id():
    db.query = f"""select max(id) as id from Option"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id