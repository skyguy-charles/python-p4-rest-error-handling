from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise NotFound()
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        raise BadRequest()
    
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/error', methods=['GET'])
def trigger_error():
    raise InternalServerError()

# Error Handlers
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({"error": "Not Found: The requested resource does not exist."}),
        404
    )
    return response

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = make_response(
        jsonify({"error": "Bad Request: Invalid data provided."}),
        400
    )
    return response

@app.errorhandler(InternalServerError)
def handle_internal_error(e):
    response = make_response(
        jsonify({"error": "Internal Server Error: Something went wrong on our end."}),
        500
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)