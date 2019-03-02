import os
from time import sleep
import json

# my stuff
from telegram_bot import telegram_bot
from telegram_bot.camera import camera_watcher


def print_status(message):
    print("[Sentinel]: %s" % str(message))

def load_config():
    config_file = open("telegram_bot/config/config.json")
    config_json = json.load(config_file)
    print_status("Config Loaded")
    return config_json

def init_telegram(telegram_bot_config):
    # obtain the raspi camera resource
    bot = telegram_bot.init_bot(telegram_bot_config)
    # return False if any issue
    if bot is None or bot is False:
        print_status("! Telegram Bot Init Failure")
        return None
    else:
        print_status("Telegram Bot Online")
        return bot

def init_camera(camera_config):
    # obtain the raspi camera resource
    camera = camera_watcher.init_camera(camera_config)
    # return False if any issue
    if camera is None or camera is False:
        print_status("! Camera Init Failure")
        return None
    else:
        print_status("Camera Active")
        return True


def startup():
    print_status("Starting Up...")
    config = load_config()

    # init bot and camera    
    camera_status = init_camera(config['Camera'])
    bot_status = init_telegram(config['TelegramBot'])

    # check that init was successful
    if(not(bot_status and camera_status)):
        print_status("Startup Failure")
        print_status("Exiting...")
        return False
    else:
        print_status("Start Up Complete")
        return True

# closes any resources cleanly
def shutdown():
    print_status("Shutting Down...")
    return


def run():
    startup_status = startup()
    print_status("Bot Is Active")
    if startup_status:
        try:
            while True:
                sleep(0.2) 
                # checks for telegram messages in background
                # 
        except KeyboardInterrupt:
            print() # this takes care of the "^C" from the user's input
            print_status("Keyboard Interrupt")
            #for chat_id in approved_user_chat_id:
            #bot.sendMessage(chat_id, 'Sentinel: offline')
    shutdown()
    os._exit(0)


if __name__ == '__main__':
    run()
