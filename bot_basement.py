# -*- coding: utf-8 -*-

# site package imports
import time
import requests
import dataset
import difflib
import vk_api
from vk_api import VkUpload, keyboard
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


# custom imports
from vkbot_class.usersession import UserSession

# command imports
from vkbot_commands.schedule import schedule
from vkbot_commands.begin import begin
from vkbot_commands.teacher import teacher
from vkbot_commands.subject import subject
from vkbot_commands.school import school
from vkbot_commands.help import help
from vkbot_commands.deactivate import deactivate
from vkbot_commands.events import events
from vkbot_commands.signup import signup


with open("auth/mysqlauth.txt", "r") as f:
    mysqlstr = f.read()

db = dataset.connect("mysql://" + mysqlstr)

teachers = db["teachers"]
groups = db["groups"]
location = db["locations"]

SESSION_TIMEOUT = 300  # 5 минут

def main():
    session = requests.Session()

    # Авторизация группы:
    # при передаче token вызывать vk_session.auth не нужно
    with open("auth/vktoken.txt", "r") as f:
        tokenstr = f.read()
    vk_session = vk_api.VkApi(token=tokenstr)

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    commands = {
        "деактивация": deactivate,
        "справка": help,
        "начать": begin,
        "расписание": schedule,
        "учитель": teacher,
        "предмет": subject,
        "школа": school,
        "события": events,
        "запись": signup
    }
    user_sessions = {}
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # Новое сообщение
            user_id = event.user_id
            to_del = []
            for user in user_sessions:  # Проверка на время последнего сообщения
                if time.time() - user_sessions[user].last_message_time > SESSION_TIMEOUT:
                    to_del.append(user)
            for i in to_del:
                del user_sessions[i]
            del to_del
            if user_id not in user_sessions.keys():  # Создание новой сессии пользователя
                user_sessions[user_id] = UserSession(user_id, time.time())
                user_sessions[user_id].session_variables["arguments"] = []
                user_sessions[user_id].session_variables["curcommand"] = "деактивация"
                user_sessions[user_id].commands = commands
            cur_user = user_sessions[user_id]
            session_vars = cur_user.session_variables
            cur_user.last_message_time = time.time()
            #session_vars["arguments"] = []
            msgarr = event.text.split(" ")
            k = 0
            # Обработка обычных фраз
            genans = db["genericanswers"].find_one(input=event.text.lower())
            didfind = False
            if genans:
                didfind = True
            if didfind:
                msg = genans["output"]
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=msg,
                )
                del didfind
            # Обработка комманд
            elif session_vars["curcommand"] == "":
                if msgarr[0].lower() in commands.keys():
                    session_vars["curcommand"] = msgarr[0].lower()
                    if len(msgarr) > 1:
                        session_vars["arguments"] = event.text[event.text.find(" ") + 1:].split("; ")
                else:
                    msg = db["situationanswers"].find_one(situation="NotUnderstood")["output"]
                    matches = difflib.get_close_matches(msgarr[0].lower(), commands.keys(), 1)
                    if matches:
                        msg = db["situationanswers"].find_one(situation="NotUnderstood")["output"] + matches[0] + "?"
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=msg,
                        keyboard=cur_user.commands_keyboard(False).get_keyboard()
                    )
            else:
                try:
                    payload = event.extra_values["payload"]
                    session_vars["arguments"] += payload[2:-2].split('", "')
                except:
                    session_vars["arguments"] += event.text.split("; ")
                print(session_vars["arguments"])
            if msgarr[0].lower() == "назад" and session_vars["curcommand"] != "":
                session_vars["curcommand"] = "начать"

            if session_vars["curcommand"]:  # Обработка комманд
                returndict = commands[session_vars["curcommand"]](session_vars["arguments"], cur_user, db)
                if returndict["message"]:
                    if returndict["keyboard"]:
                        vk.messages.send(  # Отправляем сообщение
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=returndict["message"],
                            keyboard=returndict["keyboard"]
                        )
                    else:
                        vk.messages.send(  # Отправляем сообщение
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=returndict["message"]
                        )
                if returndict["new_curcommand"]:
                    session_vars["curcommand"] = returndict["new_curcommand"]
                    if session_vars["curcommand"] == "RESET":
                        session_vars["curcommand"] = ""
                if returndict["new_arguments"]:
                    session_vars["arguments"] = returndict["new_arguments"]
                    print(returndict["new_arguments"])
                else:
                    session_vars["arguments"] = []

if __name__ == "__main__":
    main()
