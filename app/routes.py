from app import app
from flask import request


@app.route('/')
def base():
	return "nothing here, yet"


@app.route('/home')
def home():
	return("Sentinel...")

@app.route('/help')
def help():
	return("there's no help for you")

