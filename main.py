from telegram import Update
from telegram.ext import (
    Updater,
    Dispatcher,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    Filters,
)
from telegram import Bot, Update, BotCommand
import json
import os

from queue import Queue
import handlers

import model.User as User

from utils.persistance import YdbPersistance


commands = [
    BotCommand("start", "Главное меню"),
    BotCommand("menu_messages_info", "Меню объявлений"),
    BotCommand("create_temporal_link", "Создать временную ссылку регистрации")
]


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def get_token() -> str:
    """Получаем токен"""
    return os.getenv("BOT_TOKEN")


def handler(event, context):
    """Точка входа в Yandex Cloud Functions (AWS Lambda)"""
    bot = Bot(token=get_token())

    dispatcher = Dispatcher(bot, Queue())

    handlers.reg_handlers(dispatcher)

    message = json.loads(event["body"])
    update = Update.de_json(message, bot)
    dispatcher.process_update(update)
    return {"statusCode": 200}


def main() -> None:
    with open("token.txt") as f:
        token = f.read()
        updater = Updater(token, persistence=YdbPersistance())
        bot = Bot(token)
    bot.set_my_commands(commands)
    dispatcher = updater.dispatcher
    handlers.reg_handlers(dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
