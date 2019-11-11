import vk_api
from vk_api import keyboard
def template(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
    returndict = {
        "message": "",
        "keyboard": "",
        "new_curcommand": "",
        "new_arguments": ""
    }
    # TEMPLATE BLOCK END
    return returndict