from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from logic import Add, Subtract, Multiply, Divide
import os


app = Flask(__name__)
api = Api(app)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")


@app.route('/')
def hello_world():
    return "Hello Thales!!!"


if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
