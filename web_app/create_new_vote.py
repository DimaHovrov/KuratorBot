import model.VoteModels.Vote as Vote
import model.VoteModels.Question as Question
import model.VoteModels.Option as Option
import model.User as User
import json


def create_new_vote(telegram_id, data):
    user = User.get_user_by_telegram_id(telegram_id)
    json_data = json.loads(data.data)

    vote = Vote.Vote(id=None, description=json_data["description"], 
                author_id=user.id, data=data.data, groups_id=None, 
                users_id=None)
    
    Vote.add_vote(vote)
    create_question(vote.id,json_data)
    return vote


def create_question(vote_id, json_data):
    for quest in json_data["questions"]:
        question_text = quest["question_text"]
        one_choice = quest["one_choice"]
        question = Question.Question(id=None, vote_id=vote_id,one_choice=one_choice,text=question_text)
        Question.add_question(question)
        create_option(vote_id, question.id, quest["options"])


def create_option(vote_id, question_id, options):
    for option in options:
        option_model = Option.Option(id=None, vote_id=vote_id, question_id=question_id,text=option["option_text"])
        Option.add_option(option_model)

    

