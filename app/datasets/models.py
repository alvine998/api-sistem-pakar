from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


class Dataset:
    def __init__(
        self,
        id=None,
        symptoms=None,
        diagnose=None,
        medicine=None,
        period=None,
        level=None,
    ):
        self.id = id
        self.symptoms = symptoms
        self.diagnose = diagnose
        self.medicine = medicine
        self.period = period
        self.level = level

    def to_dick(self):
        return {
            "id": self.id,
            "symptoms": self.symptoms,
            "diagnose": self.diagnose,
            "medicine": self.medicine,
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
                    diagnose=item[4],
                    medicine=item[5],
                )
            )

        response = {"items": arrays, "total_count": total_count}

        return response

    @staticmethod
    def create(symptoms, period, level, diagnose, medicine):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO dataset_diseases (symptoms, period, level, diagnose, medicine) VALUES (%s, %s, %s, %s, %s)",
            (symptoms, period, level, diagnose, medicine),
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
                diagnose=items[4],
                medicine=items[5],
            )
        return None

    def update(
        self, symptoms=None, period=None, level=None, diagnose=None, medicine=None
    ):
        cursor = mysql.connection.cursor()
        if symptoms:
            self.symptoms = symptoms
        if period:
            self.period = period
        if level:
            self.level = level
        if diagnose:
            self.diagnose = diagnose
        if medicine:
            self.medicine = medicine

        cursor.execute(
            "UPDATE dataset_diseases SET symptoms=%s, period=%s, level=%s, diagnose=%s, medicine=%s, updated_on=%s WHERE id=%s",
            (
                self.symptoms,
                self.period,
                self.level,
                self.diagnose,
                self.medicine,
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
