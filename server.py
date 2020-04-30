from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import json_util, objectid
from functools import wraps
from werkzeug.security import generate_password_hash
import jwt
import os
import datetime

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)

mongo = PyMongo(app)
CORS(app)

#Funcion para validad el token en cada peticion que sea anotada
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.headers['Authorization']
    print(token)
    if not token:
      response = {
        'message': 'Token no encontrado en la petición'
      }
      return jsonify(response),403

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
    except:
      response = {
        'message': 'Token inválido'
      }
      return jsonify(response),403

    return f(*args, **kwargs)

  return decorated

@app.route("/", methods=['GET'])
def greet():
  response = {
    'response':"Hello!"
    }
  return jsonify(response)

@app.route("/login", methods=['POST'])
def login():
  auth = request.get_json()
  if app.config.get('LOGIN_EMAIL') == auth['email']and app.config.get('LOGIN_PASSWORD') == auth['password']:
    # Tiempo de expiracion del token de 30 minutos
    expirationToken = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    payloadToken  = {
      'user' : auth['email'],
      'exp' : expirationToken
    }
    token = jwt.encode(payloadToken, app.config['SECRET_KEY'])

    response = {
      "email":auth['email'],
      "username":auth['email'] + ' ' + auth['password'],
      "token":token.decode('UTF-8')
    }
    return jsonify(response)

  return make_response({'response':'Usuario no encontrado'}, 401)

@app.route("/last-diagram", methods=['GET'])
@token_required
def lastDiagram():
  # print(request.headers['Authorization'])
  response = {
    'message':'ruta que requiere token'
  }
  return jsonify(response)

# Metodos del CRUD
@app.route("/create", methods=['POST'])
def create_user():
  body = request.get_json()
  email = body['email']
  name = body['name']
  username = body['username']
  password = body['password']

  users = mongo.db.users
  existing_user = users.find_one({'email' : email})

  if existing_user:
    response = {
      'message':'El usuario ya se encuentra registrado'
    }
    return make_response(response,409)

  if username and email and name and password:
    password_hashed = generate_password_hash(password)
    idUser = mongo.db.users.insert({
        'name':name,
        'username': username,
        'email': email,
        'password': password_hashed
        })
    return make_response({'message':'Usuario creado con éxito'}, 201)
  else:
    return make_response({'message':'Ocurrio algo en el proceso'}, 409)

@app.route("/users", methods=['GET'])
def getUser():
  users = mongo.db.users.find()
  response = json_util.dumps(users)
  return make_response(response, 200)

@app.route("/user", methods=['GET'])
def getUserByEmail():
  email = request.json['email']
  print(email)
  if not email:
    return make_response({ 'message': 'Ingresar un email' }, 400)

  user = mongo.db.users.find_one( { 'email': email } )
  if user :
    response = json_util.dumps(user)
    return make_response(response, 200)
  return make_response({ 'message', 'Usuario no encontrado' },404) 

if __name__=='__main__':
  app.run(debug=True)
