from handlers.user_request import UserRequest


class IndexHandler(UserRequest):
    def get(self):
        if not self.current_user:
            return self.redirect("/login")

        data = {
            "user_name": self.current_user["user_name"],
        }
        return self.render("index.html", **data)
