from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import Symptom
from app import mysql, bcrypt

symptoms = Blueprint("symptoms", __name__)


@symptoms.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name are required"}), 400

    Symptom.create(name=name)

    return jsonify({"message": "Symptom created successfully"}), 201


@symptoms.route("/update/<int:symptom_id>", methods=["PATCH"])
def update(symptom_id):
    data = request.get_json()
    name = data.get("name")

    symptom = Symptom.get_by_id(symptom_id)
    if not symptom:
        return jsonify({"message": "Symptom not found"}), 404

    symptom.update(name=name)

    return jsonify({"message": "Symptom updated successfully"}), 200


@symptoms.route("/delete/<int:symptom_id>", methods=["DELETE"])
def delete(symptom_id):
    symptom = Symptom.get_by_id(symptom_id)
    if not symptom:
        return jsonify({"message": "symptom not found"}), 404
    symptom.delete()
    return jsonify({"message": "symptom deleted successfully"}), 200


@symptoms.route("/list", methods=["GET"])
def get():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search")

    symptoms = Symptom.get_data(page=page, limit=limit, search=search)

    symptoms_list = []
    for user in symptoms:
        symptoms_list.append({"id": user.id, "name": user.name})

    return jsonify({"items": symptoms_list, "page": page, "limit": limit})
