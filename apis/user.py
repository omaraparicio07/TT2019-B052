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
  'username': fields.String(required=False, readonly=True, description="a username", example="username"),
  'name': fields.String(required=True ),
  'email': fields.String(required=True, example="email@domain.com"),
  'password': fields.String(required=True, example="P4ssw0rd*"),
  'diagram': fields.String(example="{}", readonly=True),
})


@api.route('/')
class Users(Resource):
  @api.marshal_list_with(user)
  def get(self):
    '''Listar todos los usuarios'''
    users = db.db.users.find()
    response = list(users)
    return response
  
  @api.response(200, 'Usuario creado correctamente')
  @api.response(400, 'Faltan algunos argumentos')
  @api.response(409, 'El email ya se encuentra registrado')
  @api.response(500, 'Error en el servidor')
  @api.expect( user )
  def post(self):
    '''Crear un nuevo usuario'''
    email = api.payload['email']
    password = api.payload['password']
    name = api.payload['name']
    existing_user = db.db.users.find_one({'email' : email})

    if existing_user:
      api.abort(409, status = "El email del usuario ya se encuentra registrado")
    
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
      api.abort(500, status = "Ocurrio un error en el proceso")

@api.route('/<email>')
class user(Resource):
  @api.doc(params={'email':'user email'})
  @api.response(200, "Usuario encontrado")
  @api.response(404, "Usuario no encontrado")
  @api.response(500, "Error en el servidor")
  @api.marshal_with(user)
  def get(self, email):
    '''Obtener infomación de un usuario a través de su email'''
    user = db.db.users.find_one({'email': email})
    if user:
      return user
    else:
      api.abort(404, "No se encontro información asociada a esta cuenta de email")