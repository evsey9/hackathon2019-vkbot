class UserSession:
    user_id = 0
    last_message_time = 0
    session_variables = {}

    def __init__(self, user_id, last_message_time):
        self.user_id = user_id
        self.last_message_time = last_message_time
