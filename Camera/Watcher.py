import MotionWatchCamera


def imageRequestResponseFunc(pathToImage):
	print("I was given this image: "+str(pathToImage))


def notifyUserFunc(pathToImage):
	print("I got an image: "+str(pathToImage))

MotionWatchCamera.beginWatching(notifyUserFunc=notifyUserFunc, imageRequestResponseFunc=imageRequestResponseFunc)

