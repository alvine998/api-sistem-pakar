from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQLdb
from app import mysql, bcrypt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import json

diagnose = Blueprint("diagnose", __name__)


@diagnose.route("/predict", methods=["POST"])
def create():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT symptoms FROM dataset_diseases WHERE deleted=0")
    symptoms = cursor.fetchall()
    list_symptom = [item[0] for item in symptoms]
    cursor.execute("SELECT period FROM dataset_diseases WHERE deleted=0")
    period = cursor.fetchall()
    list_period = [item[0] for item in period]
    cursor.execute("SELECT level FROM dataset_diseases WHERE deleted=0")
    level = cursor.fetchall()
    list_level = [item[0] for item in level]
    cursor.execute("SELECT disease_name FROM dataset_diseases WHERE deleted=0")
    disease = cursor.fetchall()
    list_disease = [item[0] for item in disease]

    cursor.close()
    data = {
        "symptoms": list_symptom,
        "period": list_period,
        "level": list_level,
        "diseases": list_disease,
    }
    df = pd.DataFrame(data)

    # x = df[["symptoms", "period", "level"]]
    vectorizer = CountVectorizer()
    x_symptom = vectorizer.fit_transform(df["symptoms"])

    import scipy.sparse as sp

    x_combine = sp.hstack((x_symptom, df[["period", "level"]]))

    y = df["diseases"]

    x_train, x_test, y_train, y_test = train_test_split(
        x_combine, y, test_size=0.2, random_state=42
    )

    model = MultinomialNB()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Akurasi: ", accuracy_score(y_test, y_pred))
    print("Diagnosa: ", classification_report(y_test, y_pred))

    inputs = request.get_json()
    data1 = inputs.get("symptom")
    data2 = inputs.get("level")
    data3 = inputs.get("period")

    input_vectorized = vectorizer.transform([data1])
    input_combined = sp.hstack((input_vectorized, [[data2, data3]]))
    predicted_disease = model.predict(input_combined)

    return (
        jsonify(
            {
                "score": accuracy_score(y_test, y_pred),
                "classification": classification_report(y_test, y_pred),
                "diagnose": predicted_disease[0],
            }
        ),
        201,
    )
