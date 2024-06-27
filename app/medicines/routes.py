from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import Medicine
from app import mysql, bcrypt

medicines = Blueprint("medicines", __name__)


@medicines.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    dose = data.get("dose")

    if not name or not dose:
        return jsonify({"message": "Name, Dose are required"}), 400

    Medicine.create(name=name, dose=dose)

    return jsonify({"message": "Medicine created successfully"}), 201


@medicines.route("/update/<int:medicine_id>", methods=["PATCH"])
def update(medicine_id):
    data = request.get_json()
    name = data.get("name")
    dose = data.get("dose")

    medicine = Medicine.get_by_id(medicine_id)
    if not medicine:
        return jsonify({"message": "medicine not found"}), 404

    medicine.update(name=name, dose=dose)

    return jsonify({"message": "medicine updated successfully"}), 200


@medicines.route("/delete/<int:medicine_id>", methods=["DELETE"])
def delete(medicine_id):
    medicine = Medicine.get_by_id(medicine_id)
    if not medicine:
        return jsonify({"message": "medicine not found"}), 404
    medicine.delete()
    return jsonify({"message": "medicine deleted successfully"}), 200


@medicines.route("/list", methods=["GET"])
def get():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search")

    medicines = Medicine.get_data(page=page, limit=limit, search=search)

    medicines_list = []
    for medicine in medicines:
        medicines_list.append({"id": medicine.id, "name": medicine.name, "dose": medicine.dose})

    return jsonify({"items": medicines_list, "page": page, "limit": limit})
