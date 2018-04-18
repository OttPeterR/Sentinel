# Sentinel
The Raspberry Pi Telegram Bot that keeps watch on your home.


## Install
1. Clone this git repo onto your Raspberry Pi.
1. Register a new Telegram bot through the @BotFather Telegram bot.
 1. Put the new bots api key into the Sentinel config file.
1. Run Sentinel: `python Sentinel.py` and message the bot. You will need to retrieve your chat ID from the console.
 1. You guessed it: put that into the config file as well as your Telegram user name.
 1. You can add multiple users this way.
1. Stop Sentinel with a `ctrl+c` and restart it, this will reload the config file.
1. Test it out! Send a `/heartbeat` message to it and see if it responds with `heartbeat`, if so, you're good to go.
to get it running, you'll need to install the pi-camera package (will add what this actually is later) and a few python packages



## Config File
**Important:** 
* You need to register a bot in Telegram through the BotFather and then put in its info into the config file.
* You need to run Sentinel and message it to get what your chat ID is and then put that into the config file.

There is a accompanying config file **iForgetWhatItsCalled.file** that will let you control various aspects of Sentinel.
