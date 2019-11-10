import vk_api, pytz
from vk_api import keyboard
import datetime
def events(arguments, user_session, db):
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
    now = datetime.datetime.now()
    found = db.query("SELECT e.description, e.date_from, e.date_to, et.name, g.name 'group_name' FROM events AS e INNER JOIN event_types et \n"
                     "LEFT JOIN groups g ON e.group_id = g.id \n"
                     "WHERE e.date_from >= now() OR e.date_to >= now()")
    eventss = []
    didfind = False
    for i in found:
        if i:
            eventss.append(i)
            didfind = True
    msg = []
    if didfind:  # Если написали заданную фразу
        for i in eventss:
            date_from = (pytz.utc.localize(i["date_from"])).astimezone(pytz.timezone('Etc/GMT-5'))
            date_to = (pytz.utc.localize(i["date_to"])).astimezone(pytz.timezone('Etc/GMT-5'))
            if "group_name" in i.keys() and i["group_name"] is not None:
                msg.append(i["group_name"] + " - ")
            msg.append(i["name"] + " c " + str(date_from).split("+")[0] + " на " + str(date_to).split("+")[0] + ". " + i["description"] + "\n")
    returndict["message"] = "".join(msg)
    returndict["new_curcommand"] = "RESET"
    return returndict