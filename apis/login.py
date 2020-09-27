from flask_restplus import Namespace, Resource, fields
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db
from util import send_email
import jwt

api = Namespace('login', description='Operaciones de autenticación de usuario')

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
    '''Obtener un token de autenticación'''
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
  
  @api.expect(login)
  @api.response(200, 'Cambio de contraseña correctamente')
  @api.response(403, 'Datos no validos')
  @api.response(500, 'Error en el servidor')
  def put(self):
    '''Cambio de contraseña'''
    email = api.payload['email']
    new_pass = api.payload['password']

    user_exists = db.db.users.find_one({'email':email})

    if not user_exists:
      api.abort(403, 'El correo eléctronico no se encuentra registrado')
    
    hash_new_pass = generate_password_hash(new_pass)
    db_result = db.db.users.update_one({'email':email},{
      '$set':{
        'password': hash_new_pass
      }
    })

    if db_result:
      sending_email = send_email(email, new_pass, user_exists['name'], True, True)
      return ("ok, revisa la bandeja de entrada de tu correo", sending_email) if sending_email == 200 else ("Ocurrio un eror en el correo de verificación", sending_email)
    else:
      api.abort(403, "No se pudo realizar el cambio de contraseña, intente en otro momento")
  
