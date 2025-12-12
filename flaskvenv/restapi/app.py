from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
import requests
from dicttoxml import dicttoxml
import jwt
from functools import wraps

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'animals'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

SECRET_KEY = "mysecretkey123"

@app.route('/')
def home():
    return {
        "message": "Welcome to the Birds API!",
        "endpoints": {
            "GET all birds": "GET /birds",
            "GET one bird": "GET /birds/<id>",
            "CREATE bird": "POST /birds (token required)",
            "UPDATE bird": "PUT /birds/<id> (token required)",
            "DELETE bird": "DELETE /birds/<id> (token required)",
            "SEARCH birds": "GET /birds/search?name=...&habitat=...&status=...",
            "Login for token": "POST /login { 'username': 'admin', 'password': 'password' }"
        },
        "note": "Add ?format=xml for XML output"
    }


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == "admin" and password == "password":
        token = jwt.encode(
            {"user": username},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 403

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated


def format_output(data, format_type="json"):
    if format_type == "xml":
        xml = dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml, 200)
        response.headers['Content-Type'] = 'application/xml'
        return response

    return jsonify(data)


@app.route('/birds', methods=['GET'])
def get_birds():
    format_type = request.args.get("format", "json")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM birds")
    birds = cursor.fetchall()
    return format_output(birds, format_type)


@app.route('/birds/<int:id>', methods=['GET'])
def get_bird(id):
    format_type = request.args.get("format", "json")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM birds WHERE idbirds=%s", (id,))
    bird = cursor.fetchone()
    if not bird:
        return jsonify({"error": "Bird not found"}), 404
    return format_output(bird, format_type)


@app.route('/birds', methods=['POST'])
@token_required
def create_bird():
    data = request.get_json()
    required = ["specificname", "scientificname", "habitat", "status"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO birds (specificname, scientificname, habitat, status)
        VALUES (%s, %s, %s, %s)
    """, (data["specificname"], data["scientificname"], data["habitat"], data["status"]))
    mysql.connection.commit()
    return jsonify({"message": "Bird added successfully"}), 201


@app.route('/birds/<int:id>', methods=['PUT'])
@token_required
def update_bird(id):
    data = request.get_json()
    required = ["specificname", "scientificname", "habitat", "status"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM birds WHERE idbirds=%s", (id,))
    bird = cursor.fetchone()
    if not bird:
        return jsonify({"error": "Bird not found"}), 404

    cursor.execute("""
        UPDATE birds
        SET specificname=%s, scientificname=%s, habitat=%s, status=%s
        WHERE idbirds=%s
    """, (data["specificname"], data["scientificname"], data["habitat"], data["status"], id))
    mysql.connection.commit()
    return jsonify({"message": "Bird updated successfully"}), 200


@app.route('/birds/<int:id>', methods=['DELETE'])
@token_required
def delete_bird(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM birds WHERE idbirds=%s", (id,))
    bird = cursor.fetchone()
    if not bird:
        return jsonify({"error": "Bird not found"}), 404

    cursor.execute("DELETE FROM birds WHERE idbirds=%s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Bird deleted successfully"}), 200


@app.route('/birds/search', methods=['GET'])
def search_birds():
    format_type = request.args.get("format", "json")
    name = request.args.get("name", "")
    habitat = request.args.get("habitat", "")
    status = request.args.get("status", "")

    query = "SELECT * FROM birds WHERE 1=1"
    params = []

    if name:
        query += " AND specificname LIKE %s"
        params.append(f"%{name}%")

    if habitat:
        query += " AND habitat LIKE %s"
        params.append(f"%{habitat}%")

    if status:
        query += " AND status=%s"
        params.append(status)

    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    birds = cursor.fetchall()
    return format_output(birds, format_type)


if __name__ == "__main__":
    app.run(debug=True)
