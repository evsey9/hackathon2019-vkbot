import vk_api
from vk_api import keyboard
def school(arguments, user_session, db):
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
    def school_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        schools = db.query("SELECT * FROM locations")
        for i in schools:
            button_list.append(i["name"])
        newkeyboard.add_button("Назад", color="negative")
        newkeyboard.add_button("Все", color="positive")
        newkeyboard.add_line()
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i], color="primary", payload=[button_list[i]])
        return newkeyboard

    returndict["keyboard"] = school_keyboard(False).get_keyboard()
    if not session_vars["arguments"]:  # Если аргументов нет
        returndict["message"] = db["commands"].find_one(name=session_vars["curcommand"])["no_argument_response"]
    else:
        found = []
        if session_vars["arguments"][0] != "Все":
            found = db["locations"].find(name=session_vars["arguments"][0])
        else:
            found = db.query("SELECT * FROM locations")
        schools = []
        didfind = False
        for i in found:
            if i:
                schools.append(i)
                didfind = True
        if didfind:  # Если написали заданную фразу
            msg = []
            for i in schools:
                msg.append(i["name"] + " - " + i["street"] + " " + i["building"] + "\n")
                returndict["message"] = "".join(msg)
        else:
            returndict["message"] = db["commands"].find_one(name=session_vars["curcommand"])["not_found_response"]
    return returndict