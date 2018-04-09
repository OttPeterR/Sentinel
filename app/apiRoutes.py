from app import app
from flask import request


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
	if status == 'True':
		# FIXME
		return "set to True"
	elif status == 'False':
		# FIXME
		return "set to False"
	else:
		# FIXME
		return "error"

