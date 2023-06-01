import db.query_db as db

class AnswerOption:
    id:int
    answer_question_id:int
    option_id:int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.answer_question_id = kwargs['answer_question_id']
        self.option_id = kwargs['option_id']


def add_answer_option(answer_question_id, option_id):
    try:
        max_id = get_max_id() + 1
        db.query=f"""insert into AnswerOption (id, AnswerQuestionId, OptionId)
                       values ({max_id}, {answer_question_id}, {option_id})"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return max_id
    except Exception as exc:
        print(exc)
        return False


def get_max_id():
    db.query = f"""select max(id) as id from AnswerOption"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id
