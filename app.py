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

# Read All
@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    format = request.args.get('format', 'json')
    if format == 'xml':
        return make_response(dicttoxml(items), 200, {'Content-Type': 'application/xml'})
    return jsonify(items)

# Create
@app.route('/items', methods=['POST'])
@jwt_required()
def add_item():
    data = request.json
    if not data.get('item_name') or not data.get('status'):
        return jsonify(error="Missing fields"), 400

    sql = """INSERT INTO items (item_name, description, location_found, status)
             VALUES (%s, %s, %s, %s)"""
    cursor.execute(sql, (
        data['item_name'],
        data.get('description'),
        data.get('location_found'),
        data['status']
    ))
    db.commit()
    return jsonify(message="Item added"), 201

# Update
@app.route('/items/<int:id>', methods=['PUT'])
@jwt_required()
def update_item(id):
    data = request.json
    cursor.execute("UPDATE items SET status=%s WHERE id=%s",
                   (data['status'], id))
    db.commit()
    return jsonify(message="Item updated")

# Delete
@app.route('/items/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    db.commit()
    return jsonify(message="Item deleted")

if __name__ == "__main__":
        app.run(debug=True)