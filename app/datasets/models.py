from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


class Dataset:
    def __init__(
        self,
        id=None,
        symptoms=None,
        disease_id=None,
        disease_name=None,
        period=None,
        level=None,
    ):
        self.id = id
        self.symptoms = symptoms
        self.disease_id = disease_id
        self.disease_name = disease_name
        self.period = period
        self.level = level

    def to_dick(self):
        return {
            "id": self.id,
            "symptoms": self.symptoms,
            "disease_id": self.disease_id,
            "disease_name": self.disease_name,
            "period": self.period,
            "level": self.level,
        }

    @staticmethod
    def get_data(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM dataset_diseases WHERE deleted=0 AND disease_name LIKE %s OR symptoms LIKE %s ORDER BY id DESC LIMIT %s , %s",
                ("%" + search + "%", "%" + search + "%", offset, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM dataset_diseases WHERE deleted=0 ORDER BY id DESC LIMIT %s, %s",
                (offset, limit),
            )

        items = cursor.fetchall()

        # Count all items
        cursor.execute("SELECT COUNT(*) FROM dataset_diseases WHERE deleted=0")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result else 0

        cursor.close()

        arrays = []
        for item in items:
            arrays.append(
                Dataset(
                    id=item[0],
                    symptoms=item[1],
                    period=item[2],
                    level=item[3],
                    disease_id=item[4],
                    disease_name=item[5],
                )
            )

        response = {"items": arrays, "total_count": total_count}

        return response

    @staticmethod
    def create(symptoms, period, level, disease_id, disease_name):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO dataset_diseases (symptoms, period, level, disease_id, disease_name) VALUES (%s, %s, %s, %s, %s)",
            (symptoms, period, level, disease_id, disease_name),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM dataset_diseases WHERE id = %s AND deleted=0", (id,)
        )
        items = cursor.fetchone()
        cursor.close()

        if items:
            return Dataset(
                id=items[0],
                symptoms=items[1],
                period=items[2],
                level=items[3],
                disease_id=items[4],
                disease_name=items[5],
            )
        return None

    def update(
        self, symptoms=None, period=None, level=None, disease_id=None, disease_name=None
    ):
        cursor = mysql.connection.cursor()
        if symptoms:
            self.symptoms = symptoms
        if period:
            self.period = period
        if level:
            self.level = level
        if disease_id:
            self.disease_id = disease_id
        if disease_name:
            self.disease_name = disease_name

        cursor.execute(
            "UPDATE dataset_diseases SET symptoms=%s, period=%s, level=%s, disease_id=%s, disease_name=%s, updated_on=%s WHERE id=%s",
            (
                self.symptoms,
                self.period,
                self.level,
                self.disease_id,
                self.disease_name,
                datetime.now(),
                self.id,
            ),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE dataset_diseases SET deleted=%s, updated_on=%s WHERE id=%s",
            (1, datetime.now(), self.id),
        )
        mysql.connection.commit()
        cursor.close()
