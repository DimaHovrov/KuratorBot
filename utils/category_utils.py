import model.Category as Category
from telegram.ext import CallbackContext

choose_command_category = "/category_"


def generate_category_message_list(context: CallbackContext):
    categorys = Category.get_all_categorys()
    message = ""
    index = 1
    context.user_data['category_candidates_id'] = []
    for category in categorys:
        id = category.id
        name = category.name
        message += f"""{index}. {name} \n    {choose_command_category}{index}\n"""
        context.user_data['category_candidates_id'].append(id)
        index += 1

    return message


def get_category_id_by_command(command_name, context: CallbackContext):
    len_command = len(choose_command_category)
    category_index = int(command_name[len_command:len(
        command_name)])
    category_id = context.user_data['category_candidates_id'][category_index-1]
    return category_id
