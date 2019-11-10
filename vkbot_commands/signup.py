import vk_api
from vk_api import keyboard
def signup(arguments, user_session, db):
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

    def subject_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        subjects = db.query("SELECT * FROM subjects")
        for i in subjects:
            button_list.append(i["name"])
        newkeyboard.add_button("Назад", color="negative")
        newkeyboard.add_line()
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i], color="primary", payload=[button_list[i]])
        return newkeyboard

    def school_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = []
        schools = db.query("SELECT * FROM locations")
        for i in schools:
            button_list.append(i["name"])
        newkeyboard.add_button("Назад", color="negative")
        newkeyboard.add_line()
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 0:
                newkeyboard.add_line()
            newkeyboard.add_button(button_list[i], color="primary", payload=[button_list[i]])
        return newkeyboard

    def back_keyboard(ot=True):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        newkeyboard.add_button("Назад", color="negative")
        return newkeyboard
    if len(session_vars["arguments"]) == 0:
        returndict["message"] = db["situationanswers"].find_one(situation="SignupSelectSubject")["output"]
        returndict["keyboard"] = subject_keyboard(False).get_keyboard()
    if len(session_vars["arguments"]) == 1:
        returndict["message"] = db["situationanswers"].find_one(situation="SignupSelectLocation")["output"]
        returndict["new_arguments"] = session_vars["arguments"]
        returndict["keyboard"] = school_keyboard(False).get_keyboard()
        found = db["subjects"].find(name=session_vars["arguments"][0])
        didfind = False
        for i in found:
            if i:
                didfind = True
        if not didfind:
            returndict["message"] = db["situationanswers"].find_one(situation="SignupSubjectNotFound")["output"]
            returndict["new_arguments"] = []
            returndict["keyboard"] = subject_keyboard(False).get_keyboard()
    if len(session_vars["arguments"]) == 2:
        returndict["message"] = db["situationanswers"].find_one(situation="SignupEnterName")["output"]
        returndict["new_arguments"] = session_vars["arguments"]
        returndict["keyboard"] = back_keyboard(False).get_keyboard()
        found = db["locations"].find(name=session_vars["arguments"][1])
        didfind = False
        for i in found:
            if i:
                didfind = True
        if not didfind:
            returndict["message"] = db["situationanswers"].find_one(situation="SignupSchoolNotFound")["output"]
            returndict["new_arguments"] = session_vars["arguments"][:1]
            returndict["keyboard"] = school_keyboard(False).get_keyboard()
    if len(session_vars["arguments"]) == 3:
        returndict["message"] = db["situationanswers"].find_one(situation="SignupEnterNotes")["output"]
        returndict["new_arguments"] = session_vars["arguments"]
        returndict["keyboard"] = back_keyboard(False).get_keyboard()
        didfind = False
        if len(session_vars["arguments"][2].split(' ')) >= 3:
            didfind = True
        if not didfind:
            returndict["message"] = db["situationanswers"].find_one(situation="SignupNameWrong")["output"]
            returndict["new_arguments"] = session_vars["arguments"][:2]
            returndict["keyboard"] = back_keyboard(False).get_keyboard()
    if len(session_vars["arguments"]) == 4:
        returndict["message"] = db["situationanswers"].find_one(situation="SignupOver")["output"]
        returndict["new_curcommand"] = "RESET"
        returndict["keyboard"] = user_session.commands_keyboard(False).get_keyboard()
        subject_str = session_vars["arguments"][0]
        location_str = session_vars["arguments"][1]
        fio_split = session_vars["arguments"][2].split(' ')
        last_name, first_name, middle_name = fio_split[0], fio_split[1], fio_split[2]
        notes = session_vars["arguments"][3]
        subject_id = db["subjects"].find_one(name=subject_str)["id"]
        location_id = db["locations"].find_one(name=location_str)["id"]
        vk_id = user_session.user_id
        print(subject_id, location_id, fio_split, notes, vk_id)
        db["signups"].insert(dict(last_name=last_name, first_name=first_name, middle_name=middle_name, vk_id=vk_id, notes=notes, location_id=location_id, subject_id=subject_id))
    return returndict