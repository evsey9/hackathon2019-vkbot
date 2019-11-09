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
    returndict["message"] = "Введите запрос"
    returndict["keyboard"] = user_session.commands_keyboard(False).get_keyboard()
    returndict["new_curcommand"] = "RESET"
    return returndict