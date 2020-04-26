from flask import Flask,jsonify


app = Flask(__name__)

@app.route("/", methods=['GET'])
def greet():
  response = {
    'response':"Hello!"
    }
  return jsonify(response)


if __name__=='__main__':
  app.run(debug=True)
