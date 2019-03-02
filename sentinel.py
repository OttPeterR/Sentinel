import os
from time import sleep
import json

# my stuff
import telegramBot
from camera import cameraWatcher


def print_status(message):
    print("[Sentinel]: %s" % str(message))

def load_config():
    config_file = open("config/config.json")
    config_json = json.load(config_file)
    print_status("Config Loaded")
    return config_json

def init_telegram(telegram_bot_config, camera):
    # obtain the raspi camera resource
    telegram_bot = telegramBot.init_bot(telegram_bot_config, camera)
    # return False if any issue
    if telegram_bot is None or telegram_bot is False:
        print_status("! Telegram Bot Init Failure")
        return None
    else:
        print_status("Telegram Bot Online")
        return telegram_bot

def init_camera(camera_config):
    # obtain the raspi camera resource
    camera = cameraWatcher.init_camera(camera_config)
    # return False if any issue
    if camera is None or camera is False:
        print_status("! Camera Init Failure")
        return None
    else:
        print_status("Camera Active")
        return camera



class Sentinel:

    def __init__(self):
        self.camera = None
        self.telegram_bot = None

    def startup(self):
        print_status("Starting Up...")
        config = load_config()

        # init bot and camera    
        self.camera = init_camera(config['Camera'])
        self.telegram_bot = init_telegram(config['TelegramBot'], self.camera)

        # check that init was successful
        if(not(self.telegram_bot and self.camera)):
            print_status("Startup Failure")
            print_status("Exiting...")
            return False
        else:
            print_status("Start Up Complete")
            return True

    # closes any resources cleanly
    def shutdown(self):
        print_status("Shutting Down...")
        return


    def run(self):
        startup_status = self.startup()
        print_status("Bot Is Active")
        if startup_status:
            try:
                while True:
                    sleep(0.2) 
                    # check for telegram messages
                    # 
            except KeyboardInterrupt:
                print() # this takes care of the "^C" from the user's input
                print_status("Keyboard Interrupt")
                #for chat_id in approved_user_chat_id:
                #bot.sendMessage(chat_id, 'Sentinel: offline')
        self.shutdown()
        os._exit(0)


if __name__ == '__main__':
    sentinel = Sentinel()
    sentinel.run()
