from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dicttoxml import dicttoxml
from flask_mysqldb import MySQL

app = Flask(__name__)

# JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'b34c727409750641308b5b8f5764d0fccf59be8de6386b1c2142b58e959cbf45'
jwt = JWTManager(app)

# MYSQL CONFIG
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'malatecselec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return jsonify(message="Flask is running!")
# ---------------- AUTH ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data or 'username' not in data or 'password' not in data:
        return jsonify(error="Invalid request"), 400

    if data['username'] == 'admin' and data['password'] == 'admin123':
        token = create_access_token(identity=data['username'])
        return jsonify(access_token=token)

    return jsonify(error="Invalid credentials"), 401


# ---------------- READ ----------------
@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    cur = mysql.connection.cursor()

    query = """
    SELECT s.id, s.last_name, s.first_name, s.middle_name,
           s.age, s.block, s.year,
           i.first_name AS instructor,
           p.description AS program
    FROM student s
    JOIN instructor i ON s.instructor_id = i.id
    JOIN program p ON s.program_id = p.id
    """

    cur.execute(query)
    students = cur.fetchall()
    cur.close()

    format = request.args.get('format', 'json')
    if format == 'xml':
        return make_response(
            dicttoxml(students),
            200,
            {'Content-Type': 'application/xml'}
        )

    return jsonify(students)

# ---------------- CREATE ----------------
@app.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.json
    if not data:
        return jsonify(error="Request body is empty"), 400

    required = ['last_name', 'first_name', 'age', 'block', 'year',
                'instructor_id', 'program_id']

    if not all(field in data for field in required):
        return jsonify(error="Missing required fields"), 400

    cur = mysql.connection.cursor()

    sql = """
    INSERT INTO student
    (last_name, first_name, middle_name, age, block, year,
     instructor_id, program_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(sql, (
        data['last_name'],
        data['first_name'],
        data.get('middle_name'),
        data['age'],
        data['block'],
        data['year'],
        data['instructor_id'],
        data['program_id']
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify(message="Student created"), 201


# ---------------- UPDATE ----------------
@app.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE student
        SET age=%s, block=%s, year=%s
        WHERE id=%s
    """, (data['age'], data['block'], data['year'], id))

    if cur.rowcount == 0:
        cur.close()
        return jsonify(error="Student not found"), 404

    mysql.connection.commit()
    cur.close()
    return jsonify(message="Student updated")



# ---------------- DELETE ----------------
@app.route('/students/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (id,))

    if cur.rowcount == 0:
        cur.close()
        return jsonify(error="Student not found"), 404

    mysql.connection.commit()
    cur.close()
    return jsonify(message="Student deleted")

# ---------------- SEARCH ----------------
@app.route('/students/search', methods=['GET'])
@jwt_required()
def search_students():
    name = request.args.get('name')

    if not name:
        return jsonify(error="Missing search parameter"), 400

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM student
        WHERE last_name LIKE %s OR first_name LIKE %s
    """, (f"%{name}%", f"%{name}%"))

    results = cur.fetchall()
    cur.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
