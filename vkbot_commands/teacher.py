import vk_api
from vk_api import keyboard
def teacher(arguments, user_session, db):
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
    def teacher_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        teachers = db.query("SELECT * FROM teachers")
        for i in teachers:
            button_list.append(i["last_name"] + " " + i["first_name"] + " " + i["middle_name"])
        newkeyboard.add_button("Назад", color="negative")
        newkeyboard.add_button("Все", color="positive")
        for i in range(2, len(button_list) + 2):
            if i % 3 == 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i - 2], color="primary", payload=["name"])
        return newkeyboard

    returndict["keyboard"] = teacher_keyboard(False).get_keyboard()
    if not session_vars["arguments"]:  # Если аргументов нет
        returndict["message"] = "Введите учителя"
    else:
        print(session_vars["arguments"][0])
        found = []
        if session_vars["arguments"][0] != "Все":
            arg_last_name = session_vars["arguments"][0].split(' ')[0]
            arg_first_name = session_vars["arguments"][0].split(' ')[1]
            arg_middle_name = session_vars["arguments"][0].split(' ')[2]
            found = teachers.find(last_name=arg_last_name, first_name=arg_first_name, middle_name=arg_middle_name)
        else:
            found = db.query("SELECT * FROM teachers")
        teachers = []
        didfind = False
        for i in found:
            if i:
                teachers.append(i)
                didfind = True
        print(didfind)
        if didfind:  # Если написали заданную фразу
            msg = []
            for i in teachers:
                msg.append(i["last_name"] + " " + i["first_name"] + " " + i["middle_name"] + ", телефон: " + i["phone"] + ", почта: " + i["mail"] + "\n")
                returndict["message"] = ''.join(msg)
    return returndict