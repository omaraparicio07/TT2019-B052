from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from functools import wraps
import jwt
import os
import base64
import datetime

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)
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

if __name__=='__main__':
  app.run(debug=True)
