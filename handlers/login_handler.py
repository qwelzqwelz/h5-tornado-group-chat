from handlers.user_request import UserRequest


class LoginHandler(UserRequest):
    """
    登录
    """

    def get(self):
        return self.render("login.html")

    def post(self):
        user_name = self.get_argument("user-name")
        if not user_name:
            return self.send_error(404)
        self.set_current_user(user_name)
        self.redirect("/")
