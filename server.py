from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import os.path

from handlers.login_handler import LoginHandler
from handlers.index_handler import IndexHandler
from handlers.groups.get_messages_handler import GetMessagesHandler
from handlers.groups.send_message_handler import SendMessageHandler
from handlers.websocket_handler import WebsocketMessagesHandler

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

parse_command_line()
app = tornado.web.Application(
    [
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        #
        (r"/groups/send-message", SendMessageHandler),
        (r"/groups/get-messages", GetMessagesHandler),
        #
        (r"/websocket", WebsocketMessagesHandler),
    ],
    cookie_secret="just-a-secret",
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    debug=options.debug,
)
app.listen(options.port)
tornado.ioloop.IOLoop.current().start()
