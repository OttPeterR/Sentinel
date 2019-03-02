from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import authentication

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
        # # /start
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        # self.add_command_handler('start', self.start)

        # # /password
        self.add_command_handler('password', self.password)

        # # /toggle
        self.add_command_handler('toggle', self.toggle)

        # # catch-all for any text
        self.add_message_handler(Filters.text, self.filter_text)

    def add_command_handler(self, command, handler_func):
        # wrapping the function with an auth check
        def wrapped_handler_func(bot, update):
            auth_status = authentication.get_login_status(update)    
            if auth_status:
                self.handler_func(bot, update)
        # attaching the function
        handler_obj = CommandHandler(command, wrapped_handler_func)
        self.dispatcher.add_handler(handler_obj)

    def add_message_handler(self, message_filter, handler_func):
        # wrapping the function with an auth check
        def wrapped_handler_func(bot, update):
            auth_status = authentication.get_login_status(update)    
            if auth_status:
                self.handler_func(bot, update)
        # attaching the function
        handler_obj = MessageHandler(message_filter, wrapped_handler_func)
        self.dispatcher.add_handler(handler_obj)

    #### message handlers ####
    def start(self, bot, update):
        # create 
        authentication.get_login_status(update)

        auth_message = "Please authenticale with: /password PASSWORD"
        bot.send_message(chat_id=update.message.chat_id, text=auth_message)

    # user auth's with the password
    def password(self, bot, update):
        auth_status = authentication.get_login_status(update)
        # check if they are already logged in
        if auth_status:
            bot.send_message(chat_id=update.message.chat_id, text="You are already logged in.")
        # check password
        else:
            auth_status = authentication.validate_password(bot, update, self.config)

    
    def toggle(self, bot, update):
        status = self.camera.toggle()
        status = "camera is %s" % ("watching" if status else "not watching")
        bot.send_message(chat_id=update.message.chat_id, text=status)
    def pic(self, bot, update):
        # call camera to save image to file
        # pass image path to telegram bot and send message
        return 

    # handles any type of message that is not a command
    def filter_text(self, bot, update):
        if authentication.get_login_status(update):
            return
        else:
            status = "You have not yet authenticated, please use \"/password PASSWORD-HERE\" to authenticate"
            bot.send_message(chat_id=update.message.chat_id, text=status)

        return


    #### Helpers ####   
    # return true or false if the user is or is not authenticated yet
