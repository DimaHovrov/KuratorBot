import model.VoteModels.VoteAnswer as VoteAnswer
import model.VoteModels.AnswerQuestion as AnswerQuestion
import model.VoteModels.AnswerOption as AnswerOption

import model.VoteModels.Vote as Vote
import model.VoteModels.Question as Question
import model.VoteModels.Option as Option

import model.User as User
import model.GroupsModels.StudyGroup as StudyGroup

def out_vote_answer_result(vote:Vote):
    vote_id = vote.id
    vote_answers = VoteAnswer.get_vote_answer_by_vote_id(vote_id)
    total = len(vote_answers)
    count_options = { }# <option_id>: <count> 
    count_question = { }# <question_id>: <count> 
    users_id_options={}# id юзеров выбравших <option_id>: <user_id>
    answers = {"vote_answers":vote_answers, "answer_questions":{}, "answer_option":{"users_id":[]}}
    
    if len(vote_answers) == 0:
        return 'Количество ответов: 0\n'+'Описание: ' + vote.description
    
    for vote_answer in vote_answers:
        vote_answer_id = vote_answer.id
        answer_questions = AnswerQuestion.get_answer_question_by_vote_answer_id(vote_answer_id)
        answers["answer_questions"][vote_answer_id] = answer_questions
        for answer_question in answer_questions:
            answer_question_id = answer_question.id
            answer_options = AnswerOption.get_answer_options_by_answer_question_id(answer_question_id)
            answers["answer_option"][answer_question_id] = answer_options
            count_question[answer_question.question_id] = 0
            for answer_option in answer_options:
                option_id = answer_option.option_id
                if option_id not in count_options:
                    count_options[option_id] = 1
                else:
                    count_options[option_id] += 1
                count_question[answer_question.question_id] += 1 # подсчет кол-во ответов в вопросе
                #сохранения user_id ответивших option_id
                if option_id not in users_id_options:
                    users_id_options[option_id] = [vote_answer.user_id]
                else:
                    users_id_options[option_id].append(vote_answer.user_id)

    return create_result_message(total,count_question,count_options,users_id_options,vote)


def create_result_message(total,count_question,count_options,users_id_options, vote):
    questions = Question.get_question_by_vote_id(vote.id)
    message = f"Количество ответов: {total}\n"
    for quest in questions:
        message += f"{quest.text} – {count_question[quest.id]}\n\n"
        options = Option.get_options_by_question_id(quest.id)
        for option in options:
            text=option.text
            count = count_options[option.id] if option.id in count_options else 0
            precent = int(count*100/count_question[quest.id])
            message += f"""{text} – {count} \n{precent}%\n"""

            if count == 0:
                continue
            users_id = users_id_options[option.id]
            for user_id in users_id:
                user = User.get_user_by_user_id(user_id)
                message += f"{user.surname} {user.name} {user.patronymic} "
                study_group = StudyGroup.get_study_group_with_name_by_group_id(user.groups_id)
                group_name = f"{study_group.type_name}-{study_group.group_name}-{study_group.course_number}"
                message += f"{group_name}\n"
            message += '\n'
        message += '\n'
    return message

