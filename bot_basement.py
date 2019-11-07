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


with open("auth/mysqlauth.txt", "r") as f:
    mysqlstr = f.read()

db = dataset.connect("mysql://" + mysqlstr)

teachers = db["teachers"]
groups = db["groups"]
location = db["locations"]

SESSION_TIMEOUT = 300  # 5 минут

def main():
    def commands_keyboard(ot):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        for i in commands.keys():
            if commands[i].__name__ != "begin":
                button_list.append(i)
        for i in range(1, len(button_list) + 1):
            if i % 3 == 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i - 1], color="primary")
        return newkeyboard

    session = requests.Session()

    # Авторизация пользователя:
    """
    login, password = "python@vk.com", "mypassword"
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно
    with open("auth/vktoken.txt", "r") as f:
        tokenstr = f.read()
    vk_session = vk_api.VkApi(token=tokenstr)

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    commands = {
        "начать": begin,
        "расписание": schedule,
        "учитель": teacher
    }
    user_sessions = {}
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            to_del = []
            for user in user_sessions:
                if time.time() - user_sessions[user].last_message_time > SESSION_TIMEOUT:
                    to_del.append(user)
            for i in to_del:
                del user_sessions[i]
            del to_del
            if user_id not in user_sessions.keys():
                user_sessions[user_id] = UserSession(user_id, time.time())
                user_sessions[user_id].session_variables["arguments"] = []
                user_sessions[user_id].session_variables["curcommand"] = ""
                user_sessions[user_id].session_variables["commands"] = commands
            cur_user = user_sessions[user_id]
            session_vars = cur_user.session_variables
            cur_user.last_message_time = time.time()
            session_vars["arguments"] = []
            msgarr = event.text.split(" ")
            k = 0
            if session_vars["curcommand"] == "":
                if msgarr[0].lower() in commands.keys():
                    session_vars["curcommand"] = msgarr[0].lower()
                    if len(msgarr) > 1:
                        session_vars["arguments"] = event.text[event.text.find(" ") + 1:].split("; ")
                else:
                    msg = "Я вас не понял, пожалуйста, повторите запрос."
                    matches = difflib.get_close_matches(msgarr[0].lower(), commands.keys(), 1)
                    if matches:
                        msg = "Я вас не понял. Возможно, вы имели в виду " + matches[0] + "?"
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=msg,
                        keyboard=commands_keyboard(False).get_keyboard()
                    )
            else:
                session_vars["arguments"] = event.text.split("; ")
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
            elif session_vars["curcommand"] == "расписание":  # Если написали заданную фразу
                k = 0
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="5"
                )
                session_vars["curcommand"] = ""
            elif session_vars["curcommand"] == "школа":  # Если написали заданную фразу
                k = 0
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="5"
                )
                session_vars["curcommand"] = ""


if __name__ == "__main__":
    main()
