def init_camera(config):
    return Camera(config)

class Camera:
    def __init__(self, config):
        self.camera = None
        self.is_watching = False
        self.fps = config["Framerate"]
        self.xres = config["ResX"]
        self.yres = config["ResY"]
        self.rgb_thresh = config["RGBChangeThreshold"]
        self.image_change_percentage = config["ImageChangePercentage"]

    def start_watching(self):
        self.start_watching = True

    def toggle(self):
        self.is_watching = not self.is_watching
        return self.is_watching