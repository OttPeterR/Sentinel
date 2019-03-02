def toggle(self, bot, update):
    status = self.camera.toggle()
    status = "camera is %s" % ("watching" if status else "not watching")
    bot.send_message(chat_id=update.message.chat_id, text=status)
def pic(self, bot, update):
    # call camera to save image to file
    # pass image path to telegram bot and send message
    return 