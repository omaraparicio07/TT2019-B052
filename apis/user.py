from flask_restplus import Namespace, Resource, fields
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db
from bson import json_util, objectid
from util import send_email, validate_email
import datetime
import jwt

api = Namespace('user', description='Operaciones sobre un usuario')

user = api.model('User', {
  '_id': fields.String(required=False, readonly=True),
  'name': fields.String(required=True, readonly=True),
  'username': fields.String,
  'email': fields.String(required=True),
  'password': fields.String(required=True),
  'diagram': fields.String,
})


@api.route('/')
class User(Resource):
  @api.marshal_list_with(user)
  def get(self):
    '''Listar todos los usuarios'''
    users = db.db.users.find()
    response = list(users)
    return response
  
  @api.doc(responses={ 200: 'OK', 400: 'Faltan algunos argumentos', 500: 'Error en el servidor' } )
  @api.expect( user )
  def post(self):
    '''Crear un nuevo usuario'''
    users = db.db.users
    existing_user = users.find_one({'email' : email})

    if existing_user:
      api.abort(500, status = "El email del usuario ya se encuentra registrado", statusCode = "409")
    
    if validate_email(email) and name and password:
      password_hashed = generate_password_hash(password)
      idUser = db.db.users.insert_one({
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

      token = jwt.encode(payloadToken, current_app.config['SECRET_KEY'])
      response = {
        "email":email,
        "name": name,
        "token":token.decode('UTF-8')
      }
      email_result = send_email(email, password, name)
      return response
    else:
      api.abort(500, status = "Ocurrio un error en el proceso", statusCode = "500")