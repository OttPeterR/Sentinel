import ConfigParser
import os

defaultConfig = '/sentinel.cfg'

def createDefaultConfig():
    fullPath = __getFullPath()

    file = open(getConfigPath(), 'w')
    config = ConfigParser.ConfigParser()

    telegram = 'Telegram_Bot'
    config.add_section(telegram)
    config.set(telegram, 'Bot_ID', '0123456789:ABCabcABCabcABCabcABCabcABCabcABCabc')

    user = 'Designated_User'
    config.add_section(user)
    config.set(user, 'designated_user', 'your-user-name-here')
    config.set(user, 'user_chat_ID', 'your-chat-ID-here')
    config.set(user, 'user_MAC', '00:00:00:00:00:00')
    config.set(user, 'check_for_user_on_wifi', True)
    config.set(user, 'wifi_check_freq', 10)
    config.set(user, 'user_is_present_cooldown_minutes', 5)

    image = 'Image_Motion_Detection'
    config.add_section(image)
    config.set(image, 'image_refresh_freq', 0.5)
    config.set(image, 'res_x', 128)
    config.set(image, 'res_y', 72)
    config.set(image, 'detect_if_user_present', False)
    config.set(image, 'pixel_diff_threshold', 15)
    config.set(image, 'image_change_threshold', 5)

    config.write(file)



def __getFullPath():
    # the -7 backs out of the /Config directory
    # to get to the top level dir
    return os.path.dirname(os.path.abspath(__file__))[:-7]

def getConfigPath():
    fullPath = str(__getFullPath())
    defaultConfigPath = fullPath + defaultConfig
    return defaultConfigPath