from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import mysql.connector
from dicttoxml import dicttoxml

app = Flask(__name__) # create the Flask app instance
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

@app.route('/')
def home():
    return "Hello, Flask!"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="malatecselec"
)
cursor = db.cursor(dictionary=True) 

if __name__ == "__main__":
        app.run(debug=True)