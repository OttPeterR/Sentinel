from telegram_bot.camera import camera_watcher

def toggle(bot, update):
    status = camera_watcher.toggle()
    status = "camera is %s" % ("watching" if status else "not watching")
    bot.send_message(chat_id=update.message.chat_id, text=status)

def pic(bot, update):
    # call camera to save image to file
    # pass image path to telegram bot and send message
    return 