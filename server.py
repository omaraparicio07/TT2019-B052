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

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)
app.response_class.default_mimetype="application/json"

mongo = PyMongo(app)
CORS(app)

#Funcion para validad el token en cada peticion que sea anotada
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.headers['Authorization']

    if not token:
      response = {
        'message': 'Token no encontrado en la petición'
      }
      return jsonify(response),403

    if "Bearer " in token:
      token = token[token.index(' ')+1:]

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
  emailUser = request.json['email']
  passwordUser = request.json['password']
  password_hashed = generate_password_hash(passwordUser)

  existing_user = mongo.db.users.find_one({'email' : emailUser})
  if existing_user and check_password_hash(existing_user['password'], passwordUser):
    # Tiempo de expiracion del token
    # expirationToken = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    payloadToken  = {
      'user' : emailUser
      # 'exp' : expirationToken
    }
    token = jwt.encode(payloadToken, app.config['SECRET_KEY'])

    response = {
      "email":emailUser,
      "name": existing_user['name'],
      "token":token.decode('UTF-8')
    }
    return jsonify(response)

  return make_response({'error':'email o contraseña incorrectos'}, 401)

@app.route("/last-diagram", methods=['GET'])
@token_required
def lastDiagram():
  token = request.headers['Authorization']

  if "Bearer " in token:
      token = token[token.index(' ')+1:]

  token_decode = jwt.decode(token, app.config['SECRET_KEY'])
  email = token_decode['user']
  try:
    existing_user = mongo.db.users.find_one( { 'email': email }, {'_id':0,'email':1,'diagram':1} )
    # print(existing_user)
    return Response(json_util.dumps(existing_user),200)
  except:
    return Response({'error':'Usuario no encontrado'}, 404)

@app.route("/diagram", methods=['POST'])
@token_required
def saveDiagram():
  token = request.headers['Authorization']

  if "Bearer " in token:
      token = token[token.index(' ')+1:]

  token_decode = jwt.decode(token, app.config['SECRET_KEY'])
  email = token_decode['user']
  diagram = request.json['diagram']
  try:
    existing_user = mongo.db.users.update_one( { 'email': email },
                    {
                      '$set': { 'diagram': diagram }
                    })
    return make_response({'response':'Diagrama guardado'}, 201)
  except:
    return make_response({'error':'Ocurrio algo en el proceso'}, 500)

# Metodos del CRUD
@app.route("/register", methods=['POST'])
def create_user():
  body = request.get_json()
  email = body['email']
  name = body['name']
  password = body['password']

  users = mongo.db.users
  existing_user = users.find_one({'email' : email})

  if existing_user:
    response = {
      'error':'El email del usuario ya se encuentra registrado'
    }
    return make_response(response,409)

  if  validate_email(email) and name and password:
    password_hashed = generate_password_hash(password)
    idUser = mongo.db.users.insert_one({
        'name':name,
        'email': email,
        'password': password_hashed,
        'diagram':{}
        })

    if idUser:
      expirationToken = datetime.datetime.utcnow() + datetime.timedelta(days=1)
      payloadToken  = {
        'user' : email,
        'exp' : expirationToken
        }

      token = jwt.encode(payloadToken, app.config['SECRET_KEY'])
      response = {
        "email":email,
        "name": name,
        "token":token.decode('UTF-8')
      }
      email_result = send_email(email, password, name)
      return make_response(response, 201)
    else:
      return make_response({'error':'Ocurrio un error en el proceso'}, 500)

  else:
    return make_response({'error':'Asegurese de enviar todos los datos y que sean correctos'}, 409)

@app.route("/users", methods=['GET'])
def getUser():
  users = mongo.db.users.find()
  response = json_util.dumps(users)
  return Response(response)

@app.route("/user", methods=['GET'])
def getUserByEmail():
  email = request.json['email']
  if not email:
    return make_response({ 'error': 'Ingresar un email' }, 400)

  user = mongo.db.users.find_one( { 'email': email } )
  if user :
    response = json_util.dumps(user)
    return Response(response)
  return Response({ 'error':'Usuario no encontrado' },404)

@app.route("/users", methods=['DELETE'])
def deleteUser():
  email = request.json['email']
  if not email:
    return make_response({ 'error': 'Ingresar un email' }, 400)

  user = mongo.db.users.find_one( { 'email': email } )

  if user:
    id = mongo.db.users.delete_one( { 'email': email } )
    response = {
      "message":"Usuarios borrado exitosamente"
    }
    return make_response(response, 200)
  else :
    return make_response({ 'error': 'Usuario no encontrado' }, 404)

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  body = request.get_json()
  email = body['email']
  name = body['name']
  username = body['username']
  password = body['password']

  existing_user = mongo.db.users.find_one( { '_id' : objectid.ObjectId(id) })

  if not existing_user:
    response = {
      'error':'El usuario no se encuentra registrado'
    }
    return make_response(response,404)

  if username and email and password and name:
      password_hashed = generate_password_hash(password)
      db_result = mongo.db.users.update_one({'_id': objectid.ObjectId(id)},
      {'$set':{
        'username': username,
        'name': name,
        'email': email,
        'password':password_hashed
        }
      })
      if db_result:
        response = { 'message': 'Usuario actualizado correctamente'}
        return make_response(response,  201)
      else :
        return make_response({'error':'Ocurrio algo en el proceso'}, 500)
  else:
    return make_response({'error':'Asegurese de enviar todos los campos'}, 400)

@app.route('/recovery-password', methods=['PUT'])
def recovery_pass():
  body = request.get_json()
  email = body['email']
  password = body['password']

  existing_user = mongo.db.users.find_one( { 'email' : email })

  if not existing_user:
    response = {
      'error':'El usuario no se encuentra registrado'
    }
    return make_response(response,404)

  if email and password:
      password_hashed = generate_password_hash(password)
      db_result = mongo.db.users.update_one({'email': email},
      {'$set':{
        'password':password_hashed
        }
      })
      if db_result:
        email_result = send_email(email, password, existing_user['name'], True, True)
        response = { 'message': 'Usuario actualizado correctamente'}
        return make_response(response,  201)
      else :
        return make_response({'message':'Ocurrio algo en el proceso'}, 500)
  else:
    return make_response({'message':'Asegurese de enviar todos los campos'}, 400)


if __name__=='__main__':
  app.run(debug=True)
