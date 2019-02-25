import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def init_bot(config, camera):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    return Bot(config, camera)

def print_status(message):
    print("[Sentinel]: %s" % str(message))


class Bot:
    def __init__(self, config, camera):
        # take values from config
        self._token = config["Token"]
        self._password = config["Password"]
        self._loginAttemptLimit = config["LoginAttemptLimit"]
        self._is_running = True

        # set camera
        self.camera = camera

        # hook up message responses
        self.updater = Updater(token=self._token)
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


    def is_running(self):
        return self._is_running


    #### message handlers ####


    def start(self, bot, update):
        auth_message = "Please authenticale with: /password PASSWORD"
        bot.send_message(chat_id=update.message.chat_id, text=auth_message)

    # user auth's with the password
    # most of the actual work is done in check_auth
    def password(self, bot, update):
        users_json = None
        with open("users.json", 'r') as users_file:
            users_json = json.load(users_file)
            auth_status, users_json = self.check_auth(users_json, bot, update)
            if auth_status:
                bot.send_message(chat_id=update.message.chat_id, text="Authentication Successful.")
            #write file in case of any changes
        
        # save config file
        with open("users.json", 'w') as users_file:
            json.dump(users_json, users_file)

    def toggle(self, bot, update):
        status = self.camera.toggle()
        status = "camera is %s" % ("watching" if status else "not watching")
        bot.send_message(chat_id=update.message.chat_id, text=status)
    def pic(self, bot, update):
        # call camera to save image to file
        # pass image path to telegram bot and send message
        return 

    def filter_text(self, bot, update):
        # check for auth
        #0
        return


    #### Helpers ####   

    def check_auth(self, users, bot, update):
        user = update.message.chat.username

        # make a new user profile if needed
        if not users or user not in users:
            print_status("New user: %s has been added." % user)
            users[user] = {
                "LoggedIn": False,
                "LoginAttempts": 0,
                "Blocked": False,
                "Notify": False,
                "ChatID": update.message.chat_id
            }
        # check if user needs auth
        elif users[user]["Blocked"]:
            return False, users
        elif users[user]["LoggedIn"]:
            status = "You are already logged in."
            bot.send_message(chat_id=update.message.chat_id, text=status)
            return True, users

        # check for password
        input_password = update.message.text[(len('/password ')):]
        print_status("%s inputted %s as password" % (user, input_password))
        
        # correct password 
        if input_password == self._password:
            status = "Authentication Successful. Welcome, %s" % user
            bot.send_message(chat_id=update.message.chat_id, text=status)
            users[user]["LoggedIn"]=True
            users[user]["LoginAttempts"]=0
            users[user]["Blocked"]=False
            return True, users

        # incorrect password
        else:
            users[user]["LoginAttempts"] += 1
            # check if block limit is hit
            if users[user]["LoginAttempts"] == self._loginAttemptLimit:
                users[user]["Blocked"] = True
                status = "Incorrect password, you have been blocked. Goodbye."
                bot.send_message(chat_id=update.message.chat_id, text=status)
                return False, users
            else:
                remaining_attempts = self._loginAttemptLimit - users[user]['LoginAttempts']
                status = "Incorrect password, please try again. Remaining attempts: %d" % remaining_attempts
                bot.send_message(chat_id=update.message.chat_id, text=status)
                return False, users