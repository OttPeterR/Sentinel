from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram_bot import authentication
from telegram_bot.handlers import camera_handler
from telegram_bot.handlers import password_handler
from telegram_bot.handlers import start_handler
from telegram_bot.handlers import text_handler

def init_bot(config, camera):
    
    return Bot(config, camera)

def print_status(message):
    print("[Sentinel]: %s" % str(message))


class Bot:
    def __init__(self, config, camera):
        # take values from config
        self.config = config
        self._loginAttemptLimit = config["LoginAttemptLimit"]

        # set camera
        self.camera = camera

        # hook up message responses
        self.updater = Updater(token=config["Token"])
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

        # start checking for messages
        self.updater.start_polling()


    def setup_handlers(self):
        print_status("Binding Commands...")

        # # /start and login
        self.add_command_handler(command_string='start', 
                                 handler_func=start_handler.handle, 
                                 require_auth=False)
        self.add_command_handler(command_string='password', 
                                 handler_func=password_handler.password_handler, 
                                 require_auth=False)

        # camera controls
        self.add_command_handler(command_string='toggle', 
                                 handler_func=camera_handler.toggle)
        self.add_command_handler(command_string='pic', 
                                 handler_func=camera_handler.pic)

        # # catch-all for any text
        self.add_message_handler(message_filter=Filters.text, 
                                 handler_func=text_handler.filter_text)

        print_status("Command Binding Complete")


    def add_command_handler(self, command_string, handler_func, require_auth=True):
        # wrapping the function with an auth check
        print_status("Command initialized: /%s" % command_string)
        def wrapped_handler_func(bot, update):
            user = update.message.chat.username
            message = update.message.text
            auth_status = authentication.get_login_status(update)    
            if require_auth and auth_status:
                print_status("Function call from: %s: %s" % (user, message))
                handler_func(bot, update)
            elif not require_auth:
                print_status("Function call from: %s: %s" % (user, message))
                handler_func(bot, update)
            else:
                print_status("Unsuccessful function call from %s: %s" % (user, message))
            return

        # attaching the function
        handler_obj = CommandHandler(command_string, wrapped_handler_func)
        self.dispatcher.add_handler(handler_obj)

    def add_message_handler(self, message_filter, handler_func):
        # wrapping the function with an auth check
        print_status("Command initialized: Text Handling")
        def wrapped_handler_func(bot, update):
            user = update.message.chat.username
            message = update.message.text
            auth_status = authentication.get_login_status(update)    
            if auth_status:
                print_status("Message recieved from user: %s: %s" % (user, message))
                handler_func(bot, update)
            else:
                print_status("Message recieved from unauthenticated user: %s: %s" % (user, message))

            return
        # attaching the function
        handler_obj = MessageHandler(message_filter, wrapped_handler_func)
        self.dispatcher.add_handler(handler_obj)
    
