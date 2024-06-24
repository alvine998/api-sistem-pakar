from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import User

users = Blueprint("users", __name__)


@users.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"message": "Name, email, role, and password are required"}), 400

    existing_user = User.get_by_email(email)
    if existing_user:
        return jsonify({"message": "Email already exists"}), 409

    new_user = User(name=name, email=email, password=password, role=role)
    User.create(name=name, email=email, password=new_user.password, role=new_user.role)

    return jsonify({"message": "User created successfully"}), 201


@users.route("/update/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.update(name=name, email=email, password=password, role=role)

    return jsonify({"message": "User updated successfully"}), 200


@users.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200


@users.route("/login", methods=["POST"])
def login_users():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.get_by_email(email)
    if user and user.check_password(password):
        return jsonify({"message": "Valid credentials"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@users.route("/list", methods=["GET"])
def get_users():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    search = request.args.get('search')

    users = User.get_users(page=page, limit=limit, search=search)

    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'status': user.status
        })

    return jsonify({
        'items': users_list,
        'page': page,
        'limit': limit
    })
