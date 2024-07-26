from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import Disease
from app import mysql, bcrypt

diseases = Blueprint("diseases", __name__)


@diseases.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"message": "Name are required"}), 400
    
    nameupper = name.upper()

    result = Disease.create(name=nameupper)

    if result:
        return jsonify({"message": "disease exist"}, 400)

    return jsonify({"message": "disease created successfully"}), 201


@diseases.route("/update/<int:disease_id>", methods=["PATCH"])
def update(disease_id):
    data = request.get_json()
    name = data.get("name")

    disease = Disease.get_by_id(disease_id)
    if not disease:
        return jsonify({"message": "disease not found"}), 404
    
    nameupper = name.upper()

    result = disease.update(name=nameupper)

    if result:
        return jsonify({"message": "disease exist"}, 400)

    return jsonify({"message": "disease updated successfully"}), 200


@diseases.route("/delete/<int:disease_id>", methods=["DELETE"])
def delete(disease_id):
    disease = Disease.get_by_id(disease_id)
    if not Disease:
        return jsonify({"message": "disease not found"}), 404
    disease.delete()
    return jsonify({"message": "disease deleted successfully"}), 200


@diseases.route("/list", methods=["GET"])
def get():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search")

    result = Disease.get_data(page=page, limit=limit, search=search)

    diseases_list = []
    for disease in result["items"]:
        diseases_list.append({"id": disease.id, "name": disease.name})

    return jsonify({"items": diseases_list,  "total_items": result["total_count"], "page": page, "limit": limit})
