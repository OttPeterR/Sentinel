import ConfigParser
import DefaultConfigCreator
import os


class ConfigHelper():
    global loader
    global ConfigParser
    global defaultConfigPath

    loaded = False
    ConfigParser = ConfigParser.ConfigParser()

    #loads up the config file, or a default if its missing
    def startUp(self):
        global loaded
        if loaded:
            return
        else:
            self.reloadConfig()


    def reloadConfig(self):
        global configParser

        # check if config is missing
        if not os.path.exists(self.getConfigPath()):
            # create it if needed
            DefaultConfigLoader.createDefaultConfig()

        # now that we know it's there, load it up
        self.loadConfig()


    def getConfigPath(self):
        return DefaultConfigLoader.getConfigPath()

    #given the path to the config, load it
    def loadConfig(self):
        global configParser
        global loaded

        configParser.read(self.getConfigPath())
        loaded = True
        return

    def resetConfig(self):
        DefaultConfigLoader.createDefaultConfig()
        loaded = True





######################################
########### access methods ###########
######################################




# Telegram_Bot
telegram = 'Telegram_Bot'

def getBotID():
    return configParser.get(telegram, "Bot_ID")


# Designated_User
user = 'Designated_User'

def getUser():
    return configParser.get(user,'designated_user')
def getUserChatID():
    return configParser.get(user,'user_chat_Id')
def getUserMAC():
    return configParser.get(user,'user_MAC')
def checkForUserOnWiFi():
    return configParser.getboolean(user,'check_for_user_on_wifi')
def getWiFiCheckFrequency():
    return configParser.get(user,'wifi_check_freq')
def getUserPresentCooldown():
    return configParser.get(user,'user_is_present_cooldown_minutes')


# Image_Motion_Detection
image = 'Image_Motion_Detection'

def getImageRefreshFreq():
    return configParser.get(image, 'image_refresh_freq')
def getResX():
    return configParser.get(image, 'res_x')
def getResY():
    return configParser.get(image, 'res_y')
def detectIfUserIsPresent():
    return configParser.getboolean(image, 'detect_if_user_present')
def getPixelDiffThreshold():
    return configParser.get(image, 'pixel_diff_threshold')
def getImageChangeThreshold():
    return configParser.get(image, 'image_change_threshold')







