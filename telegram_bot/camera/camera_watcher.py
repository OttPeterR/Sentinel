# turn this into a thread-safe singleton

camera = None
is_watching = None
fps = None
xres = None
yres = None
rgb_thresh = None
image_change_percentage = None


def init_camera(config):
    camera = None
    is_watching = False
    fps = config["Framerate"]
    xres = config["ResX"]
    yres = config["ResY"]
    rgb_thresh = config["RGBChangeThreshold"]
    image_change_percentage = config["ImageChangePercentage"]
    return True

def start_watching():
    start_watching = True

def toggle():
    is_watching = not is_watching
    return is_watching