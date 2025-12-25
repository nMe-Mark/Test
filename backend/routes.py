# from datetime import datetime
# from flask import Blueprint, jsonify, request
# from services import generate_token
# from models import User, Team
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
# from models import Task
# from functools import wraps
# from decorators import role_required
# from extensions import get_db 
# from bson import ObjectId

# auth_bp = Blueprint('auth', __name__)  # Премахнат url_prefix тук

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#     role = data.get('personal')

#     if not username or not email or not password:
#         return jsonify({"msg": "Missing required fields"}), 400

#     if User.find_by_username(username) or User.find_by_email(email):
#         return jsonify({"msg": "User already exists"}), 409

#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
#     user = User.create_user(username, email, hashed_password)

#     return jsonify({"msg": "User registered successfully", "user": User.to_string(user)}), 201


# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     print("Получени данни:", data)
    
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"msg": "Missing required fields"}), 400

#     user = User.find_by_email(email)
#     if user and check_password_hash(user['password'], password):
#         token = generate_token(identity=user['_id'], role=user['role'])
#         return jsonify({
#             "token": token,
#             "user_id": user['_id'],
#             "username": user['username'],
#             "role": user['role']
#         }), 200

#     return jsonify({"msg": "Invalid credentials"}), 401


# @auth_bp.route('/all_users', methods=['GET'])
# def get_all_users():
#     users = list(get_db()['users'].find({}, {'password': 0}))
#     for user in users:
#         user['_id'] = str(user['_id'])
#     return jsonify(users), 200


# @auth_bp.route('/tasks', methods=['POST'])
# @jwt_required()
# def create_task():
#     data = request.get_json()
#     user_id = get_jwt_identity()
#     title = data.get('title')
#     description = data.get('description')
#     due_date = data.get('due_date')

#     if not title or not due_date:
#         return jsonify({"msg": "Missing title or due date"}), 400

#     task = Task.create_task(title, description, due_date, user_id)
#     task['_id'] = str(task['_id'])
#     return jsonify(task), 201


# @auth_bp.route('/tasks', methods=['GET'])
# @jwt_required()
# def get_tasks():
#     user_id = get_jwt_identity()
#     tasks = Task.get_tasks_by_user(user_id)
#     return jsonify(tasks), 200


# @auth_bp.route('/tasks/<task_id>', methods=['PUT'])
# @jwt_required()
# def update_task(task_id):
#     data = request.get_json()
#     user_id = get_jwt_identity()
#     success = Task.update_task(task_id, data, user_id)
#     if success:
#         return jsonify({"msg": "Task updated"}), 200
#     return jsonify({"msg": "Task not found"}), 404


# @auth_bp.route('/tasks/<task_id>', methods=['DELETE'])
# @jwt_required()
# def delete_task(task_id):
#     user_id = get_jwt_identity()
#     success = Task.delete_task(task_id, user_id)
#     if success:
#         return jsonify({"msg": "Task deleted"}), 200
#     return jsonify({"msg": "Task not found"}), 404


# @auth_bp.route("/test", methods=["GET"])
# def test():
#     return jsonify({"message": "Auth blueprint is working"}), 200

# @auth_bp.route('/team/create', methods=['POST'])
# @jwt_required()
# def create_team():
#     data = request.get_json()
#     team_name = data.get('name')
#     if not team_name:
#         return jsonify({"msg": "Missing team name"}), 400
#     user_id = get_jwt_identity()
#     team = Team.create_team(team_name, user_id)
#     return jsonify({"msg": "Team created", "team": team}), 201

# @auth_bp.route('/team/add_member', methods=['POST'])
# @jwt_required()
# def add_member():
#     data = request.get_json()
#     team_id = data.get('team_id')
#     user_id = data.get('user_id')
#     role = data.get('role', 'member')
#     if not Team.is_admin(get_jwt_identity(), team_id):
#         return jsonify({"msg": "Admin only"}), 403
#     # if not team_id or not user_id:
#     #     return jsonify({"msg": "Missing team_id or user_id"}), 400
#     Team.add_member(team_id, user_id, role)
#     return jsonify({"msg": "Member added"}), 200


# @auth_bp.route('/team/members/<team_id>', methods=['GET'])
# @jwt_required()
# def get_team_members(team_id):
#     members = Team.get_members(team_id)
#     return jsonify(members), 200


# # @auth_bp.route('/team-only', methods=['GET'])
# # @jwt_required()
# # def team_only():
# #     if get_jwt().get("role") not in ["admin", "member"]:
# #         return jsonify({"msg": "Team users only"}), 403

#     # return jsonify({"msg": "Welcome!"}), 200

# @auth_bp.route('/team/all', methods=['GET'])
# @jwt_required()
# def get_all_teams():
#     teams = list(get_db()['teams'].find({}, {"members": 0}))
#     for t in teams:
#         t['_id'] = str(t['_id'])
#     return jsonify(teams), 200

# @auth_bp.route('/team/promote', methods=['POST'])
# @jwt_required()
# def promote_member():
#     claims = get_jwt()
#     data = request.get_json()
#     team_id = data.get('team_id')
#     user_id = data.get('user_id')
#     new_role = data.get('role')
#     if not Team.is_admin(get_jwt_identity(), team_id):
#         return jsonify({"msg": "Admin only"}), 403
#     if not Team.is_owner(get_jwt_identity(), team_id):
#         return jsonify({"msg": "Only owner"}), 403


#     data = request.get_json()
#     team_id = data.get('team_id')
#     user_id = data.get('user_id')
#     new_role = data.get('role')

#     # check if current user is admin
#     current_user_id = get_jwt_identity()

#     team = get_db()['teams'].find_one({"_id": team_id})

#     is_admin = False
#     for m in team['members']:
#         if m['user_id'] == current_user_id and m['role'] == 'admin':
#             is_admin = True


#     # update role
#     get_db()['teams'].update_one(
#         {"_id": team_id, "members.user_id": user_id},
#         {"$set": {"members.$.role": new_role}}
#     )

#     get_db()['users'].update_one(
#         {"_id": user_id},
#         {"$set": {"team_role": new_role}}
#     )

#     return jsonify({"msg": "Role changed"}), 200


# @auth_bp.route('/team/request_join', methods=['POST'])
# @jwt_required()
# def request_join():
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     team_id = data.get("team_id")

#     if not team_id:
#         return jsonify({"msg": "team_id missing"}), 400

#     db = get_db()
#     team = db.teams.find_one({"_id": team_id})
#     if not team:
#         return jsonify({"msg": "Team not found"}), 404

#     # check already member
#     for m in team['members']:
#         if m['user_id'] == user_id:
#             return jsonify({"msg": "Already a member"}), 400

#     # check already requested
#     existing = db.team_join_requests.find_one({
#         "team_id": team_id,
#         "user_id": user_id,
#         "status": "pending"
#     })

#     if existing:
#         return jsonify({"msg": "Already sent request"}), 400

#     db.team_join_requests.insert_one({
#         "team_id": team_id,
#         "user_id": user_id,
#         "status": "pending",
#         "created_at": datetime.now()


#     })

#     return jsonify({"msg": "Request submitted"}), 200

# @auth_bp.route('/team/requests/<team_id>', methods=['GET'])
# @jwt_required()
# def list_requests(team_id):
#     user_id = get_jwt_identity()

#     # check permission
#     @staticmethod
#     def is_admin(user_id, team_id):
#         team = get_db()['teams'].find_one({"_id": team_id})
#         if not team:
#             return False
#         for m in team['members']:
#             if m['user_id'] == user_id and m['role'] == 'admin':
#                 return True
#         return False
#     db = get_db()
#     reqs = list(db.team_join_requests.find({
#         "team_id": team_id,
#         "status": "pending"
#     }))

#     # convert IDs
#     for r in reqs:
#         r["_id"] = str(r["_id"])
#         r["team_id"] = str(r["team_id"])
#         r["user_id"] = str(r["user_id"])

#     return jsonify(reqs), 200

# @auth_bp.route('/team/approve_request', methods=['POST'])
# @jwt_required()
# def approve_request():
#     data = request.get_json()
#     req = db.team_join_requests.find_one({"_id": ObjectId(request_id)})

#     db = get_db()

#     req = db.team_join_requests.find_one({"_id": request_id})
#     if not req:
#         return jsonify({"msg": "Request not found"}), 404

#     if not Team.is_member(user_id, req["team_id"]):
#         return jsonify({"msg": "Not in team"}), 403
    
#     user_id = get_jwt_identity()

#     # permission check
#     if not Team.is_admin(get_jwt_identity(), req["team_id"]):
#         return jsonify({"msg": "Admin only"}), 403

#     # update request
#     db.team_join_requests.update_one(
#         {"_id": request_id},
#         {"$set": {"status": "approved"}}
#     )

#     # add user to team with default role
#     Team.add_member(
#         team_id=req["team_id"],
#         user_id=req["user_id"],
#         role="member"
#     )

#     return jsonify({"msg": "Approved"}), 200

# @auth_bp.route('/team/reject_request', methods=['POST'])
# @jwt_required()
# def reject_request():
#     data = request.get_json()
#     req = db.team_join_requests.find_one({"_id": ObjectId(request_id)})

#     db = get_db()

#     req = db.team_join_requests.find_one({"_id": request_id})
#     if not req:
#         return jsonify({"msg": "Request not found"}), 404

#     user_id = get_jwt_identity()

#     if not Team.is_admin(get_jwt_identity(), req["team_id"]):
#         return jsonify({"msg": "Admin only"}), 403

#     db.team_join_requests.update_one(
#         {"_id":request_id},
#         {"$set": {"status": "rejected"}}
#     )

#     return jsonify({"msg": "Rejected"}), 200



from datetime import datetime
from flask import Blueprint, jsonify, request
from services import generate_token
from models import User, Team, Task
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from bson import ObjectId
from extensions import get_db

auth_bp = Blueprint('auth', __name__)  

# ------------------ USER ------------------ #

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if User.find_by_username(username) or User.find_by_email(email):
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    user = User.create_user(username, email, hashed_password)

    return jsonify({
        "msg": "User registered successfully",
        "user": User.to_string(user)
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.find_by_email(email)

    if user and check_password_hash(user['password'], password):
        token = generate_token(identity=str(user['_id']), role=user['role'])
        return jsonify({
            "token": token,
            "user_id": str(user['_id']),
            "username": user['username'],
            "role": user['role']
        }), 200

    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route('/all_users', methods=['GET'])
def get_all_users():
    from extensions import get_db
    users = list(get_db()['users'].find({}, {'password': 0}))
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users), 200


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
    if Task.delete_task(task_id, get_jwt_identity()):
        return jsonify({"msg": "Task deleted"}), 200
    return jsonify({"msg": "Task not found"}), 404


@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Auth blueprint is working"}), 200
