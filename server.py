from flask import Flask, jsonify, request
import os

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

    response = {
      "auth":True
    }
  else :
    response={
      "auth":"Usuario no autorizado"
    }

  return jsonify(response)


if __name__=='__main__':
  app.run(debug=True)
