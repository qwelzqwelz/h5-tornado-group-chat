from handlers.user_request import UserRequest
from services.message_buffer import MESSAGES


class GetMessagesHandler(UserRequest):
    def post(self):
        group = self.get_argument("group")
        cursor = self.get_argument("cursor", None)
        self.write({
            "group": group,
            "messages": MESSAGES.get_messages(group, cursor)
        })
