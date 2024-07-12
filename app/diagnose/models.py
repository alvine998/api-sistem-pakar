from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


class Diagnose:
    def __init__(
        self,
        id=None,
        symptoms=None,
        period=None,
        level=None,
        user_app_id=None,
        user_app_name=None,
        disease_accuracy_score=None,
        disease_precision_score=None,
        disease_recall_score=None,
        disease_f1_score=None,
        disease_diagnose=None,
        medicine_accuracy_score=None,
        medicine_recommendation=None,
        created_on=None,
    ):
        self.id = id
        self.symptoms = symptoms
        self.period = period
        self.level = level
        self.user_app_id = user_app_id
        self.user_app_name = user_app_name
        self.disease_accuracy_score = disease_accuracy_score
        self.disease_precision_score = disease_precision_score
        self.disease_recall_score = disease_recall_score
        self.disease_f1_score = disease_f1_score
        self.disease_diagnose = disease_diagnose
        self.medicine_accuracy_score = medicine_accuracy_score
        self.medicine_recommendation = medicine_recommendation
        self.created_on = created_on

    def to_dick(self):
        return {
            "id": self.id,
            "symptoms": self.symptoms,
            "period": self.period,
            "level": self.level,
            "user_app_id": self.user_app_id,
            "user_app_name": self.user_app_name,
            "disease_accuracy_score": self.disease_accuracy_score,
            "disease_precision_score": self.disease_precision_score,
            "disease_recall_score": self.disease_recall_score,
            "disease_f1_score": self.disease_f1_score,
            "disease_diagnose": self.disease_diagnose,
            "medicine_accuracy_score": self.medicine_accuracy_score,
            "medicine_recommendation": self.medicine_recommendation,
            "created_on": self.created_on,
        }

    @staticmethod
    def get_data(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM diagnose_histories WHERE deleted=0 AND user_app_name LIKE %s OR symptoms LIKE %s, OR disease_diagnose LIKE %s, OR medicine_recommendation LIKE %s ORDER BY id DESC LIMIT %s , %s",
                (
                    "%" + search + "%",
                    "%" + search + "%",
                    "%" + search + "%",
                    "%" + search + "%",
                    offset,
                    limit,
                ),
            )
        else:
            cursor.execute(
                "SELECT * FROM diagnose_histories WHERE deleted=0 ORDER BY id DESC LIMIT %s, %s",
                (offset, limit),
            )

        items = cursor.fetchall()

        # Count all items
        cursor.execute("SELECT COUNT(*) FROM diagnose_histories WHERE deleted=0")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result else 0

        cursor.close()

        arrays = []
        for item in items:
            arrays.append(
                Diagnose(
                    id=item[0],
                    user_app_id=item[1],
                    user_app_name=item[2],
                    symptoms=item[3],
                    period=item[4],
                    level=item[5],
                    disease_accuracy_score=item[6],
                    disease_precision_score=item[7],
                    disease_recall_score=item[8],
                    disease_f1_score=item[9],
                    disease_diagnose=item[10],
                    medicine_accuracy_score=item[11],
                    medicine_recommendation=item[12],
                    created_on=item[13],
                )
            )

        response = {"items": arrays, "total_count": total_count}

        return response
