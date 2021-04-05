from tornado.websocket import WebSocketHandler
from handlers.user_request import UserRequest
from services.user_sessions import SESSION


class WebsocketMessagesHandler(UserRequest, WebSocketHandler):
    def open(self):
        user = self.current_user
        if not user:
            return None
        SESSION.set(user["user_name"], "websocket", self)

    def on_message(self, message):
        pass

    def on_close(self):
        pass
