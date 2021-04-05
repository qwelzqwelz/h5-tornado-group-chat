'''
Author: qwelz
Date: 2021-04-05 19:29:03
LastEditors: qwelz
LastEditTime: 2021-04-05 19:34:18
'''

from uuid import uuid4


class UserSessions:
    def __init__(self):
        self.users = dict()

    def create_or_fetch_user(self, user_name):
        result = self.users.get(user_name, None)
        if result is None:
            result = {
                "user_name": user_name,
                "token": str(uuid4()),
                "session": dict(),
            }
            self.users[user_name] = result
        return result

    def get_user_by_token(self, token: str):
        result = None
        for info in self.users.values():
            if info["token"] == token:
                result = info
                break
        return result

    def set(self, user_name, key, value):
        result = self.users.get(user_name, None)
        result["session"][key] = value
        return result

    def get(self, user_name, key):
        result = self.users.get(user_name, None)
        if result:
            result = result.get(key, None)
        return result

    def delete(self, user_name, key):
        result = self.users.get(user_name, None)
        if result and key in result:
            del result[key]
        else:
            result = None
        return result


SESSION = UserSessions()
