from flask_restplus import Namespace, Resource, fields
from flask import current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config.database import db
from util import send_email
import jwt

api = Namespace('diagram', description='Operaciones sobre un diagrama')

diagram = api.model('diagram', {
  'diagram': fields.String(example="{}", required= True),
})


def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    try:
      token = request.headers['Authorization']
    except:
      response = {
        'message': 'Token no encontrado en la petición'
      }
      return response,401

    if "Bearer " in token:
      token = token[token.index(' ')+1:]

    try:
      jwt.decode(token, current_app.config['SECRET_KEY'])
    except:
      response = {
        'message': 'Token inválido'
      }
      return response,401

    return f(*args, **kwargs)

  return decorated


@api.route('/')
class User(Resource):
  @api.doc(security='Bearer Auth')
  @api.response(201, 'Guardado éxitoso')
  @api.response(401, 'No autorizado')
  @api.response(403, 'email o contraseña incorrectos')
  @api.response(500, 'Error en el servidor')
  @api.expect(diagram)
  @token_required
  def post(self):
    '''Guargar un diagrama'''
    token = request.headers['Authorization']

    if "Bearer " in token:
        token = token[token.index(' ')+1:]

    token_decode = jwt.decode(token, current_app.config['SECRET_KEY'])
    email = token_decode['user']
    diagram = api.payload['diagram']
    try:
      existing_user = db.db.users.update_one( { 'email': email },
                      {
                        '$set': { 'diagram': diagram }
                      })
      return 'Diagrama guardado correctamente'
    except:
      api.abort(500, 'Ocurrio algo en el proceso')


  @api.doc(security='Bearer Auth')
  @api.response(201, 'Ok')
  @api.response(401, 'No autorizado')
  @api.response(500, 'Error en el servidor')
  @token_required
  def get(self):
    '''Obtener el diagrama de un usuario'''
    token = request.headers['Authorization']

    if "Bearer " in token:
        token = token[token.index(' ')+1:]

    token_decode = jwt.decode(token, current_app.config['SECRET_KEY'])
    email = token_decode['user']
    try:
      existing_user = db.db.users.find_one( { 'email': email }, {'_id':0,'email':1,'diagram':1} )
      return existing_user
    except:
      api.abort(404, 'No hay datos disponibles')
  