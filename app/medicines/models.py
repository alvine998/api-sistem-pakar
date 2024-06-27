from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


class Medicine:
    def __init__(
        self,
        id=None,
        name=None,
        dose=None
    ):
        self.id = id
        self.name = name
        self.dose = dose

    def to_dick(self):
        return {
            "id": self.id,
            "name": self.name,
            "dose": self.dose
        }

    @staticmethod
    def get_data(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM medicines WHERE deleted=0 AND name LIKE %s ORDER BY id DESC LIMIT %s , %s",
                ("%" + search + "%", offset, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM medicines WHERE deleted=0 ORDER BY id DESC LIMIT %s, %s", (offset, limit)
            )

        items = cursor.fetchall()
        cursor.close()

        arrays = []
        for item in items:
            arrays.append(
                Medicine(
                    id=item[0],
                    name=item[1],
                    dose=item[2]
                )
            )

        return arrays

    @staticmethod
    def create(name, dose):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO medicines (name, dose) VALUES (%s, %s)",
            (name, dose,),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM medicines WHERE id = %s AND deleted=0", (id,))
        items = cursor.fetchone()
        cursor.close()

        if items:
            return Medicine(
                id=items[0],
                name=items[1],
                dose=items[2]
            )
        return None

    def update(self, name=None, dose=None):
        cursor = mysql.connection.cursor()
        if name:
            self.name = name
        if dose:
            self.dose = dose

        cursor.execute(
            "UPDATE medicines SET name=%s, dose=%s, updated_on=%s WHERE id=%s",
            (
                self.name,
                self.dose,
                datetime.now(),
                self.id,
            ),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE medicines SET deleted=%s, updated_on=%s WHERE id=%s",
            (1, datetime.now(), self.id),
        )
        mysql.connection.commit()
        cursor.close()
