import vk_api
from vk_api import keyboard
class UserSession:
    user_id = 0
    last_message_time = 0
    session_variables = {}
    commands = {}
    commands_positive = []
    commands_negative = []
    def __init__(self, user_id, last_message_time):
        self.user_id = user_id
        self.last_message_time = last_message_time

    def commands_keyboard(self, ot):
        newkeyboard = vk_api.keyboard.VkKeyboard(one_time=ot)
        button_list = ["о боте"]
        for i in self.commands.keys():
            if self.commands[i].__name__ != "begin":
                button_list.append(i)
        for i in range(len(button_list)):
            if i % 3 == 0 and i > 1:
                newkeyboard.add_line()
            if button_list[i] in self.commands_positive:
                newkeyboard.add_button(button_list[i], color="positive")
            elif button_list[i] in self.commands_negative:
                newkeyboard.add_button(button_list[i], color="negative")
            else:
                newkeyboard.add_button(button_list[i], color="primary")
        return newkeyboard
