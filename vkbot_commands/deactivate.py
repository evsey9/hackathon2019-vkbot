import vk_api
from vk_api import keyboard
def deactivate(arguments, user_session, db):
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
    if session_vars["arguments"] == []:
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=False)
        newkeyboard.add_button("активировать бота", color="positive", payload=["активировать бота"])
        returndict["keyboard"] = newkeyboard.get_keyboard()
        returndict["message"] = db["situationanswers"].find_one(situation="BotDeactivated")["output"]
    elif session_vars["arguments"] == ["активировать бота"]:
        newkeyboard = user_session.commands_keyboard(False)
        returndict["message"] = db["situationanswers"].find_one(situation="BotActivated")["output"]
        returndict["keyboard"] = newkeyboard.get_keyboard()
        returndict["new_curcommand"] = "RESET"
    return returndict