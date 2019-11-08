import vk_api
from vk_api import keyboard
def help(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
    teachers = db["teachers"]
    groups = db["groups"]
    location = db["locations"]
    returndict = {
        "message": "",
        "keyboard": "",
        "new_curcommand": "",
        "new_arguments": ""
    }
    # TEMPLATE BLOCK END
    def command_help_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        commands = db.query("SELECT * FROM commands")
        for i in commands:
            button_list.append(i["name"])
        newkeyboard.add_button("Назад", color="negative")
        newkeyboard.add_button("Все", color="positive")
        newkeyboard.add_line()
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i], color="primary", payload=[button_list[i]])
        return newkeyboard

    returndict["keyboard"] = command_help_keyboard(False).get_keyboard()
    if not session_vars["arguments"]:  # Если аргументов нет
        returndict["message"] = "Введите название команды"
    else:
        found = []
        if session_vars["arguments"][0] != "Все":
            found = db["commands"].find(name=session_vars["arguments"][0])
        else:
            found = db.query("SELECT * FROM commands")
        commands = []
        didfind = False
        for i in found:
            if i:
                commands.append(i)
                didfind = True
        if didfind:  # Если написали заданную фразу
            msg = []
            for i in commands:
                msg.append(i["name"] + " - " + i["description"] + "\n\n")
                returndict["message"] = "".join(msg)
        else:
            returndict["message"] = 'Команда не найдена. Нажмите кнопку "все" чтобы вывести список всех команд.'
    return returndict