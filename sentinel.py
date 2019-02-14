import os
from time import sleep


def print_status(message):
    print("[Sentinel]: %s" % str(message))

# reads config and sets up other resources like camera
def startup():
    print_status("Starting Up...")
    return

# closes any resources cleanly
def shutdown():
    print_status("Shutting Down...")
    return



# set things up
# check for messages and respond accordingly
# shut things down
def main():
    startup()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print() # this takes care of the "^C" from the user's input
        print_status("Keyboard Interrupt")
        #for chat_id in approved_user_chat_id:
        #bot.sendMessage(chat_id, 'Sentinel: offline')
    shutdown()
    os._exit(0)


if __name__ == '__main__':
    main()
