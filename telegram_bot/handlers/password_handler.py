from telegram_bot import authentication

def password_handler(bot, update):
    auth_status = authentication.get_login_status(update)
    # check if they are already logged in
    if auth_status:
        bot.send_message(chat_id=update.message.chat_id, text="You are already logged in.")
    # check password
    else:
        auth_status = authentication.validate_password(bot, update)
