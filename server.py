from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import jwt
import os
import base64
import datetime

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)
CORS(app)

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


if __name__=='__main__':
  app.run(debug=True)
