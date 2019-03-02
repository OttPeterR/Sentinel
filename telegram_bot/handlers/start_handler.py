from telegram_bot import authentication

def handle(bot, update):
    auth_status = authentication.get_login_status(update)
    if not auth_status:
        auth_message = "Please authenticale with: /password PASSWORD"
        bot.send_message(chat_id=update.message.chat_id, text=auth_message)
    else:
        auth_message = "You have already authenticated"
        bot.send_message(chat_id=update.message.chat_id, text=auth_message)
