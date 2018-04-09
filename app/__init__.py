from flask import Flask

app = Flask("Sentinel")

from app import routes
from app import apiRoutes
