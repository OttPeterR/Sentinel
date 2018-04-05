import os
import ConfigParser
from Config import DefaultConfigCreator


class ConfigHelper():
    global loader
    global configParser
    global defaultConfigPath

    loaded = False
    configParser = ConfigParser.ConfigParser()

    # loads up the config file, or a default if its missing
    def startUp(self):
        global configParser

        # check if config is missing
        if not os.path.exists(self.getConfigPath()):
            # create it if needed
            DefaultConfigCreator.createDefaultConfig()

        # now that we know it's there, load it up
        self.loadConfig()

    def getConfigPath(self):
        return DefaultConfigCreator.getConfigPath()

    # given the path to the config, load it
    def loadConfig(self):
        global configParser
        global loaded

        configParser.read(self.getConfigPath())
        loaded = True
        return

    def resetConfig(self):
        DefaultConfigCreator.createDefaultConfig()
        loaded = True


######################################
########### access methods ###########
######################################




# Telegram_Bot
telegram = 'Telegram_Bot'


def getBotID():
    return configParser.get(telegram, "bot_id")


# Designated_User
user = 'Designated_User'


def getUser():
    config_val = configParser.get(user, 'designated_user')
    return [user_name.strip() for user_name in config_val.split(',')]

def getUserChatID():
    config_val = configParser.get(user, 'user_chat_id')
    return [chat_id.strip() for chat_id in config_val.split(',')]

def getUserMAC():
    config_val = configParser.get(user, 'user_MAC')
    return [mac.strip() for mac in config_val.split(',')]

def checkForUserOnWiFi():
    return configParser.getboolean(user, 'check_for_user_on_wifi')


def getWiFiCheckFrequency():
    return float(configParser.get(user, 'wifi_check_freq'))


def getWiFiAddress():
    return configParser.get(user, 'ip_address_to_scan')


def getUserPresentCooldown():
    return float(configParser.get(user, 'user_is_present_cooldown_minutes'))


# Image_Motion_Detection
image = 'Image_Motion_Detection'


def getMotionWatch():
    if (configParser.get(image, 'motion_watch') == 'True'):
        return True
    else:
        return False


def setMotionWatch(motion_watch):
    configParser.set(image, 'motion_watch', motion_watch)

def getImageRefreshFreq():
    return float(configParser.get(image, 'image_refresh_freq'))


def getResX():
    return int(configParser.get(image, 'res_x'))


def getResY():
    return int(configParser.get(image, 'res_y'))


def detectIfUserIsPresent():
    return configParser.getboolean(image, 'detect_if_user_present')


def getPixelDiffThreshold():
    return float(configParser.get(image, 'pixel_diff_threshold'))


def getImageChangeThreshold():
    return float(configParser.get(image, 'image_change_threshold'))

def getFPS():
    return int(configParser.get(image, 'fps'))
