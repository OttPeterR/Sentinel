import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import authentication

def init_bot(config, camera):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    return Bot(config, camera)

def print_status(message):
    print("[Sentinel]: %s" % str(message))


class Bot:
    def __init__(self, config, camera):
        # take values from config
        self.config = config
        self._loginAttemptLimit = config["LoginAttemptLimit"]
        self._is_running = True
        self._logged_in_users = authentication.get_logged_in_users()

        # set camera
        self.camera = camera

        # hook up message responses
        self.updater = Updater(token=config["Token"])
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

        # start checking for messages
        self.updater.start_polling()


    def setup_handlers(self):
        # /start
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # /password
        password_handler = CommandHandler('password', self.password)
        self.dispatcher.add_handler(password_handler)

        # /toggle
        toggle_handler = CommandHandler('toggle', self.toggle)
        self.dispatcher.add_handler(toggle_handler)

        # catch all for text
        text_handler = MessageHandler(Filters.text, self.filter_text)
        self.dispatcher.add_handler(text_handler)

    def is_running(self):
        return self._is_running


    #### message handlers ####


    def start(self, bot, update):
        auth_message = "Please authenticale with: /password PASSWORD"
        bot.send_message(chat_id=update.message.chat_id, text=auth_message)

    # user auth's with the password
    def password(self, bot, update):
        auth_status = authentication.get_login_status(update)
        # check if they are already logged in
        if auth_status:
            bot.send_message(chat_id=update.message.chat_id, text="You are already logged in.")
            return 
        # check password
        else:
            auth_status = authentication.validate_password(bot, update, self.config)
            # update the logged in users list
            self._logged_in_users = authentication.get_logged_in_users()

    
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
