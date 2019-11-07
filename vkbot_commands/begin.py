import vk_api
from vk_api import keyboard
def begin(arguments, user_session, db):
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
    def commands_keyboard(ot):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        for i in session_vars["commands"].keys():
            if session_vars["commands"][i].__name__ != "begin":
                button_list.append(i)
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 1:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i], color="primary")
        return newkeyboard
    returndict["message"] = "Введите запрос"
    returndict["keyboard"] = commands_keyboard(False).get_keyboard()
    returndict["new_curcommand"] = "RESET"
    return returndict