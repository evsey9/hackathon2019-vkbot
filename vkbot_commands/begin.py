import vk_api
from vk_api import keyboard
def begin(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
    returndict = {
        "message": "",
        "keyboard": "",
        "new_curcommand": "",
        "new_arguments": ""
    }
    # TEMPLATE BLOCK END
    returndict["message"] = db["situationanswers"].find_one(situation="EnterQuery")["output"]
    returndict["keyboard"] = user_session.commands_keyboard(False).get_keyboard()
    returndict["new_curcommand"] = "RESET"
    return returndict