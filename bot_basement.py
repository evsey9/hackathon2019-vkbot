# -*- coding: utf-8 -*-

#site package imports
import time
import requests
import dataset
import difflib
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


#custom imports
from vkbot_class.usersession import UserSession


mysqlstr = ""
with open("auth/mysqlauth.txt", "r") as f:
    mysqlstr = f.read()
db = dataset.connect("mysql://" + mysqlstr)

teachers = db["teachers"]
groups = db["groups"]
location = db["locations"]

def main():
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
    tokenstr = ""
    with open("auth/vktoken.txt", "r") as f:
        tokenstr = f.read()
    vk_session = vk_api.VkApi(token=tokenstr)

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    commands = ["расписание"]
    curcommand = ""
    arguments = []
    user_sessions = {}
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            if user_id not in user_sessions.keys():
                user_sessions[user_id] = UserSession(user_id, time.time())
                user_sessions[user_id].session_variables["arguments"] = []
                user_sessions[user_id].session_variables["curcommand"] = ""
            cur_user = user_sessions[user_id]
            session_vars = cur_user.session_variables
            cur_user.last_message_time = time.time()
            session_vars["arguments"] = []
            msgarr = event.text.split(" ")
            k = 0
            if session_vars["curcommand"] == "":
                if msgarr[0].lower() in commands:
                    session_vars["curcommand"] = msgarr[0].lower()
                    if len(msgarr) > 1:
                        session_vars["arguments"] = event.text[event.text.find(" ") + 1:].split("; ")
                else:
                    msg = "Я вас не понял, пожалуйста, повторите запрос."
                    matches = difflib.get_close_matches(msgarr[0].lower(), commands, 1)
                    if matches:
                        msg = "Я вас не понял. Возможно, вы имели в виду " + matches[0] + "?"
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=msg
                    )
            else:
                session_vars["arguments"] = event.text.split("; ")
            if msgarr[0].lower() == "назад":
                session_vars["curcommand"] = ""
            if session_vars["curcommand"] == "расписание":
                if session_vars["arguments"] == []:  # Если аргументов нет
                    vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Введите школу"
                    )
                else:
                    print(session_vars["arguments"][0])
                    found = location.find(name=session_vars["arguments"][0])
                    didfind = False
                    for i in found:
                        if i:
                            didfind = True
                    if didfind:  # Если написали заданную фразу
                        msg = []
                        loctable = db.query("SELECT g.days, g.time_start, g.time_end, g.id 'group_id', school.id 'loc_id', "
                                            "school.name 'school_name', teach.id 'teacher_id', "
                                            "teach.lastname 'last_name' \n"
                                            "FROM groups AS g INNER JOIN locations school ON school.id = g.location_id \n"
                                            "INNER JOIN teachers teach ON teach.id = g.teacher ")

                        timerows = db.create_table("timerows")
                        for i in loctable:
                            if i["school_name"] == session_vars["arguments"][0]:
                                timerows.insert(i)
                                print(i)
                        print(timerows.columns)

                        weekdays = {
                            "1": "Понедельник: ",
                            "2": "Вторник: ",
                            "3": "Среда: ",
                            "4": "Четверг: ",
                            "5": "Пятница: ",
                            "6": "Суббота: ",
                            "7": "Воскресенье: ",
                            "8": "АА СТРАШНА ВЫРУБАЙ"
                        }
                        for i in range(1, 7):
                            result = db.query("SELECT * FROM timerows WHERE days LIKE '%" + str(i) + "%'")
                            didfind = False
                            result1 = []
                            for j in result:
                                if j:
                                    print("j : ", j)
                                    didfind = True
                                    result1.append(j)
                            if didfind:
                                msg.append(weekdays[str(i)])
                                for j in result1:
                                    print(j)
                                    time_start = j["time_start"].split(" ")[1]
                                    time_end = j["time_end"].split(" ")[1]
                                    startzrs = 1 if len(time_start.split(":")[1]) == 1 else 0
                                    endzrs = 1 if len(time_end.split(":")[1]) == 1 else 0
                                    time_start = time_start.split(":")[0] + ":" + "0" * startzrs + time_start.split(":")[1]
                                    time_end = time_end.split(":")[0] + ":" + "0" * endzrs + time_end.split(":")[1]
                                    msg.append(time_start + "-" + time_end + " " + j["last_name"] + ", ")
                        print(msg)
                        db["timerows"].drop()
                        vk.messages.send(  # Отправляем сообщение
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="".join(msg)
                        )
                    else:
                        vk.messages.send(  # Отправляем сообщение
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Школа не найдена. Попробуйте обратиться к списку адресов."
                        )
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
