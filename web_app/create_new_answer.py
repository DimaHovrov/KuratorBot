import model.VoteModels.VoteAnswer as VoteAnswer
import model.VoteModels.AnswerQuestion as AnswerQuestion
import model.VoteModels.AnswerOption as AnswerOption
import model.User as User
import json


def create_new_answer(user:User, data):
    json_data = json.loads(data.data)
    user_id = user.id
    vote_id = json_data["vote_id"]
    answer_id = VoteAnswer.add_answer(vote_id, user_id)

    if (answer_id == False):
        return False

    for quest in json_data["answers"]:
        question_id = quest["question_id"]
        answer_question_id = AnswerQuestion.add_answer_question(answer_id, question_id)
        if answer_question_id == False:
            return False
        for answer_id in quest["answer"]:
            answer_option_id=AnswerOption.add_answer_option(answer_question_id, answer_id)
            if answer_option_id == False:
                return False
    
    return True



