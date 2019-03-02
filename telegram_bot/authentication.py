import json

def print_status(message):
    print("[Sentinel]: %s" % str(message))


def get_login_status(update):
    if update is None:
        return False
    user = update.message.chat.username
    users = get_users_json()
    # is already logged in
    if users is not None and user in users and users[user]["LoggedIn"]:
        return True
    # make a new user profile if needed
    elif not users or user not in users:
        print_status("New user: %s has been added." % user)
        users[user] = {
            "LoggedIn": False,
            "LoginAttempts": 0,
            "Blocked": False,
            "Notify": False,
            "ChatID": update.message.chat_id
        }
        save_users_json(users)
    return False

def validate_password(bot, update):
    config = load_config()
    user = update.message.chat.username
    users = get_users_json()
    input_password = update.message.text[(len('/password ')):]
    # check for blocked status
    if users[user]["LoginAttempts"]+1 >= config["LoginAttemptLimit"]:
        print("blocked")
        status = "You have been blocked."
        bot.send_message(chat_id=update.message.chat_id, text=status)

        users[user]["Blocked"] = True
        save_users_json(users)
        print_status("%s is now blocked" % user)
        return False
    # correct password 

    if input_password == config["Password"] and not users[user]["Blocked"]:
        print("corret password")
        status = "Authentication Successful. Welcome, %s" % user
        bot.send_message(chat_id=update.message.chat_id, text=status)
        
        users[user]["LoggedIn"]=True
        users[user]["LoginAttempts"]=0
        users[user]["Blocked"]=False
        save_users_json(users)
        print_status("%s inputted the correct password" % user)
        return True

    # incorrect password
    else:
        print("incorrect password")
        users[user]["LoginAttempts"] += 1
        print_status("%s inputted an incorrect password" % user)
        remaining_attempts = config["LoginAttemptLimit"] - users[user]['LoginAttempts']

        status = "Incorrect password, please try again. Remaining attempts: %d" % remaining_attempts
        bot.send_message(chat_id=update.message.chat_id, text=status)

        save_users_json(users)
        print_status("%s has %d remaining password attempts" % (user, remaining_attempts))
        return False

    print("WAT")
    return False

def get_users_json():
    with open("telegram_bot/config/users.json", 'r') as users_file:
        users_json = json.load(users_file)
        return users_json

def save_users_json(users_json):
    with open("telegram_bot/config/users.json", 'w') as users_file:
        json.dump(users_json, users_file)

def get_logged_in_users():
    users_json = get_users_json()
    if users_json is None:
        return []
    else:
        logged_in_users = []
        for user in users_json:
            if users_json[user]["LoggedIn"]:
                logged_in_users.append(user)
        return logged_in_users

def load_config():
    config_file = open("telegram_bot/config/config.json")
    config_json = json.load(config_file)
    return config_json["TelegramBot"]