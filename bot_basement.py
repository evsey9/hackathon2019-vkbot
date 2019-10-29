# -*- coding: utf-8 -*-

import requests
import dataset
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
mysqlstr = ""
with open("auth/mysqlauth.txt", 'r') as f:
    mysqlstr = f.read()
db = dataset.connect('mysql://' + mysqlstr)

teachers = db['teachers']
groups = db['groups']
location = db['locations']

def main():
    session = requests.Session()

    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
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
    with open('auth/vktoken.txt', 'r') as f:
        tokenstr = f.read()
    vk_session = vk_api.VkApi(token=tokenstr)

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    curcommand = ""
    arguments = []
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            k = 0
            msgarr = event.text.split(' ')
            if curcommand == "":
                curcommand = msgarr[0]
            if len(msgarr) > 1:
                arguments = event.text[event.text.find(' ') + 1:].split('; ')
            if curcommand == 'Расписание' and arguments == []:  # Если написали заданную фразу
                vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите школу'
                )
            elif event.text.split(' ')[0] == 'Расписание' and (len(event.text.split())) > 1:
                msgcommand = event.text[event.text.find(' ') + 1:]
                print(msgcommand)
                found = location.find(name=msgcommand)
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

                    timerows = db.create_table('timerows')
                    for i in loctable:
                        if i['school_name'] == msgcommand:
                            timerows.insert(i)
                            print(i)
                    #loctable = db.
                    print(timerows.columns)

                    #print(loctable)
                    weekdays = {
                        '1': "Понедельник: ",
                        '2': "Вторник: ",
                        '3': "Среда: ",
                        '4': "Четверг: ",
                        '5': "Пятница: ",
                        '6': "Суббота: ",
                        '7': "Воскресенье: ",
                        '8': "АА СТРАШНА ВЫРУБАЙ"
                    }
                    for i in range(1, 7):
                        result = db.query("SELECT * FROM timerows WHERE days LIKE '%" + str(i) + "%'")
                        didfind = False 
                        result1 = []
                        for j in result:
                            if j:
                                print('j : ', j)
                                didfind = True
                                result1.append(j)
                        if didfind:
                            msg.append(weekdays[str(i)])
                            for j in result1:
                                print(j)
                                time_start = j['time_start'].split(' ')[1]
                                time_end = j['time_end'].split(' ')[1]
                                startzrs = 1 if len(time_start.split(':')[1]) == 1 else 0
                                endzrs = 1 if len(time_end.split(':')[1]) == 1 else 0
                                time_start = time_start.split(':')[0] + ':' + '0' * startzrs + time_start.split(':')[1]
                                time_end = time_end.split(':')[0] + ':' + '0' * startzrs + time_end.split(':')[1]
                                msg.append(time_start + '-' + time_end + ' ' + j['last_name'] + ', ')
                    print(msg)
                    db['timerows'].drop()
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=''.join(msg)
                    )
                else:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Школа не найдена. Попробуйте обратиться к списку адресов."
                    )
            elif event.text == 'расписание':  # Если написали заданную фразу
                k = 0
                vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                random_id=get_random_id(),
                message='5'
                )
            elif event.text == 'школа':  # Если написали заданную фразу
                k = 0
                vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                random_id=get_random_id(),
                message='5'
                )
            elif event.text == 'назад':  # Если написали заданную фразу
                k = 1


if __name__ == '__main__':
    main()
