from handlers.user_request import UserRequest
from services.message_buffer import MESSAGES
from services.user_sessions import SESSION


class SendMessageHandler(UserRequest):

    def _broadcast(self, user_name, message):
        result = 0
        for info in SESSION.users.values():
            if info["user_name"] == user_name:
                continue
            ws = info["session"].get("websocket", None)
            if ws:
                result += 1
                ws.write_message({"messages": [message]})
        return result

    def post(self):
        result = {"status": 1}
        user_name = self.current_user["user_name"]
        #
        group = self.get_argument("group")
        text = self.get_argument("text")
        if not group or not text:
            result["status"] = 0
        else:
            # 记录消息
            result["message"] = MESSAGES.add_message(
                user=user_name,
                group=self.get_argument("group"),
                text=self.get_argument("text"),
            )
            # 广播消息
            self._broadcast(user_name, result["message"])
        self.write(result)
