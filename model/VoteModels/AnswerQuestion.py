import db.query_db as db


class AnswerQuestion:
    id:int
    answer_id:int
    question_id:int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.answer_id = kwargs['answer_id']
        self.question_id = kwargs['question_id']



def add_answer_question(answer_id, question_id):
    try:
        max_id = get_max_id() + 1
        print(answer_id, question_id)
        db.query=f"""insert into AnswerQuestion (id, AnswerId, QuestionId)
                       values ({max_id}, {answer_id}, {question_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return max_id
    except Exception as exc:
        print(exc)
        return False


def get_max_id():
    db.query = f"""select max(id) as id from AnswerQuestion"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id