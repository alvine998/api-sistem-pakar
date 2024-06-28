from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from .models import Dataset
from app import mysql, bcrypt

datasets = Blueprint("datasets", __name__)


@datasets.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    symptoms = data.get("symptoms")
    period = data.get("period")
    level = data.get("level")
    disease_id = data.get("disease_id")
    disease_name = data.get("disease_name")

    if not symptoms or not period or not level or not disease_id or not disease_name:
        return (
            jsonify({"message": "Symptoms, Period, Level, Disease are required"}),
            400,
        )

    Dataset.create(
        symptoms=symptoms,
        period=period,
        level=level,
        disease_id=disease_id,
        disease_name=disease_name,
    )

    return jsonify({"message": "Data created successfully"}), 201


@datasets.route("/update/<int:dataset_id>", methods=["PATCH"])
def update(dataset_id):
    data = request.get_json()
    symptoms = data.get("symptoms")
    period = data.get("period")
    level = data.get("level")
    disease_id = data.get("disease_id")
    disease_name = data.get("disease_name")

    dataset = Dataset.get_by_id(dataset_id)
    if not dataset:
        return jsonify({"message": "dataset not found"}), 404

    dataset.update(
        symptoms=symptoms,
        period=period,
        level=level,
        disease_id=disease_id,
        disease_name=disease_name,
    )

    return jsonify({"message": "dataset updated successfully"}), 200


@datasets.route("/delete/<int:dataset_id>", methods=["DELETE"])
def delete(dataset_id):
    dataset = Dataset.get_by_id(dataset_id)
    if not dataset:
        return jsonify({"message": "dataset not found"}), 404
    dataset.delete()
    return jsonify({"message": "dataset deleted successfully"}), 200


@datasets.route("/list", methods=["GET"])
def get():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search = request.args.get("search")

    result = Dataset.get_data(page=page, limit=limit, search=search)

    datasets_list = []
    for item in result["items"]:
        datasets_list.append(
            {
                "id": item.id,
                "symptoms": item.symptoms,
                "period": item.period,
                "level": item.level,
                "disease_id": item.disease_id,
                "disease_name": item.disease_name,
            }
        )

    return jsonify(
        {
            "items": datasets_list,
            "total_items": result["total_count"],
            "page": page,
            "limit": limit,
        }
    )
