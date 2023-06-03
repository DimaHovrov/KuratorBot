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


def get_answer_question_by_vote_answer_id(vote_answer_id):
    try:
        db.query = f"""select * 
                       from AnswerQuestion
                       where AnswerId = {vote_answer_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        answer_questions = []
        for row in result[0].rows:
            answer_question = AnswerQuestion(id= row.id, answer_id=row.AnswerId, question_id=row.QuestionId)
            answer_questions.append(answer_question)
        return answer_questions
    except Exception as exp:
        print(exp)
        return False

def get_max_id():
    db.query = f"""select max(id) as id from AnswerQuestion"""
    result = db.pool.retry_operation_sync(db.execute_query)
    if result[0].rows[0].id == None:
        return 0
    return result[0].rows[0].id