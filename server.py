from flask import Flask, jsonify, request, make_response, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import json_util, objectid
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
import datetime
from util import send_email, validate_email
from apis import api
from config.database import initialize_db

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)
# app.response_class.default_mimetype="application/json"

mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})
initialize_db(app)
api.init_app(app)

if __name__=='__main__':
  app.run(debug=True)
