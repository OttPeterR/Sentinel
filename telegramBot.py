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
        self._logged_in_users = self.get_logged_in_users()

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
    # most of the actual work is done in check_login_status and validate_password
    def password(self, bot, update):
        users_json = None
        users_json = self.get_users_json()
        auth_status = self.check_login_status(bot, update)
        # check if they are already logged in
        if auth_status:
            bot.send_message(chat_id=update.message.chat_id, text="You are already logged in.")
            return 
        # check password
        else:
            auth_status = self.validate_password(bot, update)
    
    def toggle(self, bot, update):
        status = self.camera.toggle()
        status = "camera is %s" % ("watching" if status else "not watching")
        bot.send_message(chat_id=update.message.chat_id, text=status)
    def pic(self, bot, update):
        # call camera to save image to file
        # pass image path to telegram bot and send message
        return 

    def filter_text(self, bot, update):
        
        return


    #### Helpers ####   
    # return true or false if the user is or is not authenticated yet
    def check_login_status(self, bot, update):
        user = update.message.chat.username
        users = self.get_users_json()
        # is already logged in
        if users is not None and user in users and users[user]["LoggedIn"]:
            return True
        # make a new user profile if needed
        elif not users or user not in users:
            print_status("New user: %s has been added." % user)
            users[user] = {
                "LoggedIn": False,
                "LoginAttempts": 0,
                "Blocked": False,
                "Notify": False,
                "ChatID": update.message.chat_id
            }
            self.save_users_json(users)
        return False

    def validate_password(self, bot, update):
        user = update.message.chat.username
        users = self.get_users_json()

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
            self.save_users_json(users)
            return True

        # incorrect password
        else:
            users[user]["LoginAttempts"] += 1
            # check if block limit is hit
            if users[user]["LoginAttempts"] == self._loginAttemptLimit:
                users[user]["Blocked"] = True
                status = "Incorrect password, you have been blocked. Goodbye."
                bot.send_message(chat_id=update.message.chat_id, text=status)
                self.save_users_json(users)
                return False
            else:
                remaining_attempts = self._loginAttemptLimit - users[user]['LoginAttempts']
                status = "Incorrect password, please try again. Remaining attempts: %d" % remaining_attempts
                bot.send_message(chat_id=update.message.chat_id, text=status)
                self.save_users_json(users)
                return False


    def get_users_json(self):
        with open("users.json", 'r') as users_file:
            users_json = json.load(users_file)
            return users_json

    def save_users_json(self, users_json):
        with open("users.json", 'w') as users_file:
            json.dump(users_json, users_file)

    def get_logged_in_users(self):
        users_json = self.get_users_json()
        if users_json is None:
            return []
        else:
            logged_in_users = []
            for user in users_json:
                if users_json[user]["LoggedIn"]:
                    logged_in_users.append(user)
            return logged_in_users