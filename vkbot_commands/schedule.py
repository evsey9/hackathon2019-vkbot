import pytz
import datetime
import vk_api
from vk_api import keyboard
def schedule(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
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
        schools = db.query("SELECT name FROM locations")
        for i in schools:
            button_list.append(i["name"])
        newkeyboard.add_button("Назад", color="negative")
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
        found = db["locations"].find(name=session_vars["arguments"][0])
        didfind = False
        for i in found:
            if i:
                didfind = True
        if didfind:  # Если написали заданную фразу
            msg = []
            for i in range(1, 7):
                result = db.query("SELECT g.name, g.description, g.room, g.time_start, g.time_end, g.id 'group_id', school.id 'loc_id', "
                                "school.name 'school_name', teach.id 'teacher_id', dof.name 'dayofweek', "
                                "teach.last_name 'last_name', subj.name 'subject_name', e.description 'event_description' \n"
                                "FROM groups AS g INNER JOIN locations school ON school.id = g.location_id \n"
                                "INNER JOIN teachers teach ON teach.id = g.teacher_id \n"
                                "INNER JOIN subjects subj ON subj.id = g.subject_id \n"
                                "INNER JOIN groups_days gd ON g.id = gd.group_id \n"
                                "INNER JOIN daysofweek dof ON gd.day_id = dof.id \n"
                                "LEFT JOIN (SELECT * FROM events WHERE events.date_from >= now() OR events.date_to >= now()) e ON g.id = e.group_id \n"
                                "WHERE school.name = '" + session_vars["arguments"][0] + "' AND gd.day_id = " + str(i) + " \n"
                                "ORDER BY g.time_start")
                # помогите :(
                didfind = False
                result1 = []
                for j in result:
                    if j:
                        print("j : ", j)
                        didfind = True
                        result1.append(j)
                if didfind:
                    msg.append(db["daysofweek"].find_one(id=i)["name"])
                    msg.append(': \n')
                    for j in result1:
                        print(j)
                        print(type(j["time_start"]))
                        time_start = (pytz.timezone('Etc/GMT-5').localize(datetime.datetime.min + j["time_start"])).astimezone(pytz.timezone('Etc/GMT-5'))
                        time_end = (pytz.timezone('Etc/GMT-5').localize(datetime.datetime.min + j["time_end"])).astimezone(pytz.timezone('Etc/GMT-5'))
                        time_start = time_start.strftime("%H:%M")
                        time_end = time_end.strftime("%H:%M")
                        startzrs = 1 if len(time_start.split(":")[1]) == 1 else 0
                        endzrs = 1 if len(time_end.split(":")[1]) == 1 else 0
                        time_start = time_start.split(":")[0] + ":" + "0" * startzrs + time_start.split(":")[1]
                        time_end = time_end.split(":")[0] + ":" + "0" * endzrs + time_end.split(":")[1]
                        msg.append(j["name"] + " - " + time_start + "-" + time_end + " " + j["subject_name"] + ", учитель: " + j["last_name"])
                        if "room" in j.keys() and j["room"] is not None:
                            msg.append(", ауд. " + str(j["room"]) + ".")
                        if "description" in j.keys() and j["description"] is not None:
                            msg.append(" " + j["description"])
                        if "event_description" in j.keys() and j["event_description"] is not None:
                            msg.append(" " + db["situationanswers"].find_one(situation="GroupHasEvent")["output"])
                        msg.append(' \n')
                    msg.append(' \n')
            print(msg)
            db["timerows"].drop()
            returndict["message"] = "".join(msg)
        else:
            returndict["message"] = db["commands"].find_one(name=session_vars["curcommand"])["not_found_response"]
    return returndict