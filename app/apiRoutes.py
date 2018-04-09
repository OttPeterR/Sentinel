from app import app

base='/api'

@app.route(base+'/heartbeat')
def heartbeat():
	return "heartbeat"

@app.route(base+'/requestPic')
def requestPic():
	return "implemented/path/to/pic"

@app.route(base+'/motionWatch')
def motionWatch():
	status = request.args.get('status')
	if status == True:
		# FIXME
		pass
	elif status == False:
		# FIXME
		pass
	else:
		# FIXME
		pass
