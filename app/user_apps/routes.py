from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import UserApp
from datetime import datetime


userapps = Blueprint("userapps", __name__)


@userapps.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    birth_date = data.get("birth_date")

    if not name or not email or not password or not phone or not birth_date:
        return (
            jsonify(
                {"message": "Name, email, phone, birht_date, password are required"}
            ),
            400,
        )

    existing_user = UserApp.get_by_email(email)
    if existing_user:
        return jsonify({"message": "Email already exists"}), 409

    new_user = UserApp(
        name=name,
        email=email,
        password=password,
        phone=phone,
        birth_date=birth_date,
        status=1,
    )
    UserApp.create(
        name=name,
        email=email,
        password=new_user.password,
        phone=new_user.phone,
        birth_date=new_user.birth_date,
        status=new_user.status,
    )

    return jsonify({"message": "User created successfully"}), 201


@userapps.route("/update/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    birth_date = data.get("birth_date")
    status = data.get("status")

    user = UserApp.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.update(
        name=name,
        email=email,
        password=password,
        phone=phone,
        birth_date=birth_date,
        status=status,
    )

    return jsonify({"message": "User updated successfully"}), 200


@userapps.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserApp.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200


@userapps.route("/login", methods=["POST"])
def login_users():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = UserApp.get_by_email(email)
    if user and user.check_password(password):
        return jsonify({"message": "Valid credentials", "user":user.to_dick()}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@userapps.route("/list", methods=["GET"])
def get_users():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search")

    users = UserApp.get_users(page=page, limit=limit, search=search)

    users_list = []
    for user in users:
        users_list.append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "birth_date": user.birth_date,
                "status": user.status,
            }
        )

    return jsonify({"items": users_list, "page": page, "limit": limit})
