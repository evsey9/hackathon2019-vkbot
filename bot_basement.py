# -*- coding: utf-8 -*-

import requests
import dataset
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
db = dataset.connect('sqlite:///:memory:')
teachers = db['teachers']
groups = db['groups']
address = db['address']

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
    vk_session = vk_api.VkApi(token='f341b3f7b54cf3cba2fe80c47700d3c740eb40bf04a6e62c948677a2e7eda61ca5adc72e8808eba221e22')

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            k = 0
            if event.text == 'расписание':  # Если написали заданную фразу
                    vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите учителя'
                    )
                if event.text == address.find() :  # Если написали заданную фразу
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=''
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