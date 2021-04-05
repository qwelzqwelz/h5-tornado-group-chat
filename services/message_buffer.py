from uuid import uuid4
from time import time


class MessageBuffer(object):
    def __init__(self):
        self.cache = []
        self.cache_size = 200

    def get_messages(self, group, cursor=None):
        results = []
        for msg in reversed(self.cache):
            if cursor and msg["id"] == cursor:
                break
            if msg["group"] != group:
                continue
            results.append(msg)
        results.reverse()
        return results

    def add_message(self, user, group, text):
        result = {
            "group": group,
            "user_name": user,
            "timestamp": time(),
            "text": text,
            "uuid": str(uuid4()),
        }
        self.cache.append(result)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]
        return result


MESSAGES = MessageBuffer()
