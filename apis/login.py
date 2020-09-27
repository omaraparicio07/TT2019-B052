from flask_restplus import Namespace, Resource, fields
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db
import jwt

api = Namespace('login', description='User authentication operations')

login = api.model('Login', {
  'email': fields.String(required=True, description= 'Un correo eléctronico valido', example= 'email@domain.com'),
  'password': fields.String(required=True, description= 'Una contraseña de al menos 8 caracteres', example= 'Pas5w0rd*')
})


@api.route('/')
class User(Resource):    
  @api.expect(login, validate=True)
  @api.response(200, 'Autenticación correcta')
  @api.response(403, 'email o contraseña incorrectos')
  @api.response(500, 'Error en el servidor')
  def post(self):
    '''get token user after login'''
    user_exists = db.db.users.find_one({'email': api.payload['email']})
    if user_exists and check_password_hash(user_exists['password'], api.payload['password']):
      payloadToken  = {
        'user' : api.payload['email']
      }

      token = jwt.encode(payloadToken, current_app.config['SECRET_KEY'])

      response = {
        "email":api.payload['email'],
        "name": user_exists['name'],
        "token":token.decode('UTF-8')
      }
      return response, 200
    else:
      api.abort(403, status="email o contraseña incorrectos")