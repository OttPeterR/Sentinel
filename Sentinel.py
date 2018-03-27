# SentinelBot for Telegram
#
# This will only run on a Raspberry Pi with a camera module
#
# monitors RaspberryPi camera for movement
# will send a picture upon seeing movement or upon request

# install:
#    do the usual updates for apt-get and pip
#    
#    sudo apt-get install python-picamera
#    sudo apt-get install python3-picamera
#    sudo pip install telepot
#    sudo apt-get install libjpeg-dev
#    sudo apt-get install gcc python-dev
#    sudo pip install Pillow
#    sudo pip install ConfigParser


# commands:
#  pic - captures and sends a picture
#  heartbeat - replies with 'heartbeat' if powered on
#  whoshere - True if a recognized device is present, False otherwise
#  motion_watch [enable, disable] - Controls the motion detection

import io
import os
import time
from datetime import datetime

# Raspberry PI specific imports
# these imports may error when not on a pi, don't worry about it
import picamera
from PIL import Image

# for telegram
import telepot

from Config import ConfigHelper

# general
name = 'Sentinel'
ConfigHelper.ConfigHelper().startUp()

# network
local_IP = ConfigHelper.getWiFiAddress()

# user parameters
approved_user = ConfigHelper.getUser()
approved_user_chat_id = ConfigHelper.getUserChatID()
approved_local_MAC_addresses = [ConfigHelper.getUserMAC()]
last_user_check_time = 0
check_for_user_on_wifi = ConfigHelper.checkForUserOnWiFi()
user_check_frequency = 1000 * ConfigHelper.getWiFiCheckFrequency()  # check every x seconds
user_is_present = False
user_is_present_cooldown = 60000 * ConfigHelper.getUserPresentCooldown()  # wait x minutes before user is marked as gone
user_last_seen_time = 0

# chat parameters
chat_refresh_frequency = 50  # milliseconds between each chat check
image_refresh_frequency = 1000 * ConfigHelper.getImageRefreshFreq()  # x seconds per image check

# camera related parameters
motion_watch = ConfigHelper.getMotionWatch()
motion_image_width = ConfigHelper.getResX()
motion_image_height = ConfigHelper.getResY()
time_of_last_image = 0
previous_image_buffer = 0
current_image_buffer = 0
disable_cam_if_user_is_present = True

# image difference parameters
pixel_diff_threshold = ConfigHelper.getPixelDiffThreshold()  # how different a pixel is from another
picture_change_threshold = ConfigHelper.getImageChangeThreshold()  # percent difference for a picture to be considered changed


def handle(msg):
    if validateUser(msg['from']['username']):
        handleMessage(msg)
    else:
        print("message from unknown sender: \n\tname: %s\n\tchat: %s" % (msg['from']['username'], msg['chat']['id']))

def handleMessage(msg):
    global motion_watch
    global current_image_buffer

    chat_id = msg['chat']['id']
    command = msg['text']
    user_name = msg['from']['username']
    args = command.split()[1:]
    if command[0] == '/':
        command = command[1:]
        print('From: %s (%s)\n\t%s' % (user_name, chat_id, command))

        if command == 'heartbeat':
            bot.sendMessage(chat_id, 'heartbeat')
        elif command == 'pic':
            if motion_watch is False:
                current_image_buffer = takePic()
            sendMostRecentPic(chat_id)
        elif command == 'whoshere':
            bot.sendMessage(chat_id, user_is_present)
        elif command.startswith('motion_watch'):
            if len(args) > 0:
                if args[0] == 'enable':
                    motion_watch = True
                    ConfigHelper.setMotionWatch(True)
                    bot.sendMessage(chat_id, "MotionWatch: enabled")
                elif args[0] == 'disable':
                    motion_watch = False
                    ConfigHelper.setMotionWatch(False)
                    bot.sendMessage(chat_id, "MotionWatch: disabled")
                else:
                    bot.sendMessage(chat_id, "Please use **enable** or **disable** to control MotionWatch.")
            else:
                bot.sendMessage(chat_id, "Please use **enable** or **disable** to control MotionWatch.")


def validateUser(user_name):
    global approved_user
    return user_name in approved_user


# saves the buffer to a file then
# returns the path to the file
def imageBufferToFile(img_buffer):
    if (img_buffer == 0):
        img_buffer = takePic()
    # image = Image.open(img_buffer)
    now = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    img_buffer.save(filename)
    return filename


def areImagesDifferent(image_buffer1, image_buffer2):
    global pixel_diff_threshold
    # are either image the default blank string?
    current_pixels_changed = 0
    diff = 0
    # loop through x and y of both images
    for x in range(motion_image_width):
        for y in range(motion_image_height):
            # check the green channel, (with [1]) because it's the most clear
            diff = abs(image_buffer1.getpixel((x, y))[1] - image_buffer2.getpixel((x, y))[1])
            if diff >= pixel_diff_threshold:
                current_pixels_changed += 1
    resolution = motion_image_width * motion_image_height
    percentage_changed = (100.0 * current_pixels_changed) / resolution

    # True if there were enough changed pixels
    print('  changed pixels: ' + str(current_pixels_changed) + ', changed percent: ' + str(percentage_changed))
    return percentage_changed >= picture_change_threshold


def checkForMotion():
    global time_of_last_image
    global current_image_buffer
    global previous_image_buffer
    global motion_watch

    # should we even refresh?
    if motion_watch and not user_is_present:
        current_time = int(round(time.time() * 1000))  # milliseconds
        # test if enough time has passed to check for motion
        motion_diff_time = current_time - time_of_last_image
        if motion_diff_time >= image_refresh_frequency:
            # time to refresh
            current_image_buffer = takePic()
            if previous_image_buffer != 0:
                if areImagesDifferent(previous_image_buffer, current_image_buffer):
                   for chat_id in approved_user_chat_id:   
                       sendMostRecentPic(chat_id)
            time_of_last_image = current_time
            previous_image_buffer = current_image_buffer


def takePic():
    print("taking picture")
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        print(" capturing")
        camera.capture(stream, format='jpeg')
    stream.seek(0)
    img = Image.open(stream)
    print(" done")
    return img


def checkIfUserIsPresent():
    global last_user_check_time
    global user_last_seen_time
    global user_is_present

    if check_for_user_on_wifi:

        current_time = int(round(time.time() * 1000))
        if current_time - last_user_check_time >= user_check_frequency:
            if userOnWiFiNetwork():
                if user_is_present == False:
                    bot.sendMessage(approved_user_chat_id, 'Welcome back')
                user_is_present = True
                user_last_seen_time = current_time
            elif current_time - user_last_seen_time >= user_is_present_cooldown:
                if user_is_present == True:
                    bot.sendMessage(approved_user_chat_id, 'Goodbye')
                user_is_present = False
            last_user_check_time = current_time
        return user_is_present
    return False


def sendMostRecentPic(chat_id):
    global current_image_buffer
    sendPicFile(chat_id, imageBufferToFile(current_image_buffer))


def sendPicFile(chat_id, photo_path):
    # save the photo to a file and pass in the file path
    bot.sendMessage(chat_id, 'image is being uploaded...')
    bot.sendPhoto(chat_id, open(photo_path))


def userOnWiFiNetwork():
    global local_IP
    for mac in approved_local_MAC_addresses:
        output = os.popen('sudo nmap -sP -n %s/24 | grep %s' % (local_IP, mac)).read()
        if output != "":
            return True
    return False


###############################
##### Handling the Camera #####
###############################
# cam = picamera.PiCamera()


def startup():
    global motion_watch
    global bot
    global approved_user_chat_id
    global approved_user

    bot = telepot.Bot(ConfigHelper.getBotID())
    bot.message_loop(handle)
    print('%s is online...' % name)

    for (user, chat_id) in zip(approved_user, approved_user_chat_id):
        print('  sending active message to %s at %s' % (user, chat_id))
        bot.sendMessage(chat_id, 'Sentinel: online')
        #bot.sendMessage(chat_id, "MotionWatch: %s" % motion_watch)
        print("message sent")

    previous_image_buffer = takePic()
    # print 'powered on'


############################
##### Handling the Bot #####
############################
startup()

# lifecycle loop
# with keyboard interrput exception handler
try:
    while True:
        time.sleep(chat_refresh_frequency / 1000)
        # wifi scan takes a really long time
        # make this a seperate thread or something
        # checkIfUserIsPresent()
        checkForMotion()
except KeyboardInterrupt:
    print("\nSentinel - Keyboard Interrupt - Shutting down...\n")
    for chat_id in approved_user_chat_id:
        bot.sendMessage(chat_id, 'Sentinel: offline')
    os._exit(0)
