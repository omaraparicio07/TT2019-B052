from flask import Flask, jsonify, request
import os
import jwt
import datetime

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)

@app.route("/", methods=['GET'])
def greet():
  response = {
    'response':"Hello!"
    }
  return jsonify(response)

@app.route("/login", methods=['POST'])
def login():
  auth = request.get_json()
  if app.config.get('LOGIN_USERNAME') == auth['user']and app.config.get('LOGIN_PASSWORD') == auth['password']:
    # Tiempo de expiracion del token de 30 minutos
    expirationToken = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payloadToken  = {
      'user' : auth['user'],
      'exp' : expirationToken
    }
    print(payloadToken)
    token = jwt.encode(payloadToken, app.config['SECRET_KEY'])
    print(token.decode('UTF-8'))
    response = {
      "auth":True,
      "token":token.decode('UTF-8')
    }
  else :
    response={
      "response":"Usuario no autorizado"
    }

  return jsonify(response)


if __name__=='__main__':
  app.run(debug=True)
