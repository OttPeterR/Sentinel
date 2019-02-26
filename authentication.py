import json

def get_login_status(update):
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

def validate_password(bot, update, config):
    user = update.message.chat.username
    users = get_users_json()

    # check for password
    input_password = update.message.text[(len('/password ')):]
    print_status("%s inputted %s as password" % (user, input_password))
    
    # correct password 
    if input_password == config["Password"]:
        status = "Authentication Successful. Welcome, %s" % user
        bot.send_message(chat_id=update.message.chat_id, text=status)
        users[user]["LoggedIn"]=True
        users[user]["LoginAttempts"]=0
        users[user]["Blocked"]=False
        save_users_json(users)
        return True

    # incorrect password
    else:
        users[user]["LoginAttempts"] += 1
        # check if block limit is hit
        if users[user]["LoginAttempts"] == config["LoginAttemptsLimit"]:
            users[user]["Blocked"] = True
            status = "Incorrect password, you have been blocked. Goodbye."
            bot.send_message(chat_id=update.message.chat_id, text=status)
            save_users_json(users)
            return False
        else:
            remaining_attempts = config["LoginAttemptsLimit"] - users[user]['LoginAttempts']
            status = "Incorrect password, please try again. Remaining attempts: %d" % remaining_attempts
            bot.send_message(chat_id=update.message.chat_id, text=status)
            save_users_json(users)
            return False


def get_users_json():
    with open("users.json", 'r') as users_file:
        users_json = json.load(users_file)
        return users_json

def save_users_json(users_json):
    with open("users.json", 'w') as users_file:
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