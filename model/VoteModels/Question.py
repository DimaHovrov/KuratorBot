import db.query_db as db

class Question:
    id:int
    vote_id:int
    one_choice:bool
    text: str

    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.vote_id = kwargs['vote_id']
        self.one_choice = kwargs['one_choice']
        self.text = kwargs['text']


def add_question(question: Question):
    try:    
        max_id = get_max_id() + 1
        question.id = max_id
        db.query = f"""insert into Question (id, OneChoice, Text, VoteId)
                       values ({question.id}, {question.one_choice}, '{question.text}', {question.vote_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return True
    except Exception as exp:
        print(exp)
        return False


def get_question_by_vote_id(vote_id):
    try:
        db.query = f"""select * from Question
                       where VoteId = {vote_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        questions = []
        for row in result[0].rows:
            quest = Question(id = row.id, vote_id = row.VoteId, one_choice=row.OneChoice, text=row.Text)
            questions.append(quest)
        return questions
    except Exception as exp:
        print(exp)
        return False


def get_max_id():
    db.query = f"""select max(id) as id from Question"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id