import vk_api
from vk_api import keyboard
def deactivate(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
    returndict = {
        "message": "",
        "keyboard": "",
        "new_curcommand": "",
        "new_arguments": ""
    }
    # TEMPLATE BLOCK END
    if session_vars["arguments"] == []:
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=False)
        newkeyboard.add_button("активировать бота", color="positive", payload=["активировать бота"])
        returndict["keyboard"] = newkeyboard.get_keyboard()
        returndict["message"] = db["situationanswers"].find_one(situation="BotDeactivated")["output"]
    elif session_vars["arguments"][0].lower() == "активировать бота":
        newkeyboard = user_session.commands_keyboard(False)
        returndict["message"] = db["situationanswers"].find_one(situation="BotActivated")["output"]
        returndict["keyboard"] = newkeyboard.get_keyboard()
        returndict["new_curcommand"] = "RESET"
    return returndict