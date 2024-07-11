from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from app import mysql, bcrypt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
)
import json

diagnose = Blueprint("diagnose", __name__)


def train_model():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT symptoms, period, level, diagnose, medicine FROM dataset_diseases"
    )
    data = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(data)
    X = df[["symptoms", "period", "level"]]
    y_disease = df["diagnose"]
    y_medicine = df["medicine"]

    X = pd.get_dummies(X, columns=["symptoms", "period"])

    # Split the data into training and testing sets
    X_train_disease, X_test_disease, y_train_disease, y_test_disease = train_test_split(
        X, y_disease, test_size=0.3, random_state=42
    )

    # Train Naive Bayes model for disease prediction
    nb_model = GaussianNB()
    nb_model.fit(X_train_disease, y_train_disease)
    # model = GaussianNB()
    # model.fit(X, y)

    # Predict on the test set and calculate accuracy for disease prediction
    y_pred_disease = nb_model.predict(X_test_disease)
    accuracy_disease = accuracy_score(y_test_disease, y_pred_disease)
    precision_disease = precision_score(y_test_disease, y_pred_disease, average='macro')
    recall_disease = recall_score(y_test_disease, y_pred_disease, average='macro')
    f1_disease = f1_score(y_test_disease, y_pred_disease, average='macro')

    # Split the data into training and testing sets for medicine recommendation
    X_train_medicine, X_test_medicine, y_train_medicine, y_test_medicine = (
        train_test_split(X, y_medicine, test_size=0.3, random_state=42)
    )

    # Train KNN model for medicine recommendation
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train_medicine, y_train_medicine)

    # Predict on the test set and calculate accuracy for medicine recommendation
    y_pred_medicine = knn_model.predict(X_test_medicine)
    accuracy_medicine = accuracy_score(y_test_medicine, y_pred_medicine)

    return (
        nb_model,
        knn_model,
        X.columns,
        accuracy_disease,
        accuracy_medicine,
        precision_disease,
        recall_disease,
        f1_disease,
    )


def predict_disease(model, model_columns, symptoms, period, level):
    input_data = pd.DataFrame(
        {"symptoms": [symptoms], "period": [period], "level": [level]}
    )
    input_data = pd.get_dummies(input_data, columns=["symptoms", "period"])

    # Ensure all necessary columns are present
    for col in model_columns:
        if col not in input_data:
            input_data[col] = 0

    prediction = model.predict(input_data[model_columns])[0]
    return prediction


# Function to recommend medicine using the trained KNN model
def recommend_medicine(model, model_columns, symptoms, period, level):
    input_data = pd.DataFrame(
        {"symptoms": [symptoms], "period": [period], "level": [level]}
    )
    input_data = pd.get_dummies(input_data, columns=["symptoms", "period"])

    # Ensure all necessary columns are present
    for col in model_columns:
        if col not in input_data:
            input_data[col] = 0

    recommendation = model.predict(input_data[model_columns])[0]
    return recommendation


@diagnose.route("/predict", methods=["POST"])
def create():
    inputs = request.get_json()
    data1 = inputs.get("symptoms")
    data2 = inputs.get("period")
    data3 = inputs.get("level")
    print(inputs)

    (
        nb_model,
        knn_model,
        model_columns,
        accuracy_disease,
        accuracy_medicine,
        precision_disease,
        recall_disease,
        f1_disease,
    ) = train_model()
    disease = predict_disease(nb_model, model_columns, data1, data2, data3)
    medicine = recommend_medicine(knn_model, model_columns, data1, data2, data3)
    return jsonify(
        {
            "disease_accuracy_score": accuracy_disease,
            "disease_precision_score": precision_disease,
            "disease_recall_score": recall_disease,
            "disease_f1_score": f1_disease,
            "disease_diagnose": disease,
            "medicine_accuracy_score": accuracy_medicine,
            "medicine_recommendation": medicine,
        },
        200,
    )
