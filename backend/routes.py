from flask import Blueprint, jsonify, request
from services import generate_token
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Проверка дали потребител вече съществува
    if User.find_by_username(username) or User.find_by_email(email):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User.create_user(username, email, hashed_password)

    return jsonify({"msg": "User registered successfully", "user": User.to_string(user)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.find_by_username(username)
    if user and check_password_hash(user['password'], password):
        token = generate_token(identity=user['_id'])
        return jsonify({
            "token": token,
            "user_id": user['_id'],
            "username": user['username']
        }), 200

    return jsonify({"msg": "Invalid credentials"}), 401

@auth_bp.route('/all_users', methods=['GET'])
def get_all_users():
    from extensions import get_db
    users = list(get_db()['users'].find({}, {'password': 0}))  # скриваме паролите
    for user in users:
        user['_id'] = str(user['_id'])  # конвертираме ObjectId към стринг, ако е нужно
    return jsonify(users), 200


from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task

@auth_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    if not title or not due_date:
        return jsonify({"msg": "Missing title or due date"}), 400

    task = Task.create_task(title, description, due_date, user_id)
    task['_id'] = str(task['_id'])
    return jsonify(task), 201

@auth_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.get_tasks_by_user(user_id)
    return jsonify(tasks), 200

@auth_bp.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    success = Task.update_task(task_id, data, user_id)
    if success:
        return jsonify({"msg": "Task updated"}), 200
    return jsonify({"msg": "Task not found"}), 404

@auth_bp.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    success = Task.delete_task(task_id, user_id)
    if success:
        return jsonify({"msg": "Task deleted"}), 200
    return jsonify({"msg": "Task not found"}), 404
