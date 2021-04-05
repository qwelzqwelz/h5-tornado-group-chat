from tornado.web import RequestHandler
from services.user_sessions import SESSION


class UserRequest(RequestHandler):
    def set_current_user(self, user_name: str):
        result = SESSION.create_or_fetch_user(user_name)
        self.set_cookie("token", result["token"])

    def get_current_user(self):
        result = self.get_cookie("token")
        if result:
            result = SESSION.get_user_by_token(result)
        return result
