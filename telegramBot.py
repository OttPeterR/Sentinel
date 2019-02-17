def init_bot(config):
    return Bot(config)

class Bot:
    def __init__(self, config):
        self._token = config["Token"]
        self._password = config["Password"]
        self._is_running = True

    def is_running(self):
        return self._is_running