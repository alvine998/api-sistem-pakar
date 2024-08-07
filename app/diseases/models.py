from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


class Disease:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def to_dick(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def get_data(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM diseases WHERE deleted=0 AND name LIKE %s ORDER BY id DESC LIMIT %s , %s",
                ("%" + search + "%", offset, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM diseases WHERE deleted=0 ORDER BY id DESC LIMIT %s, %s",
                (offset, limit),
            )

        items = cursor.fetchall()

        # Count all items
        cursor.execute("SELECT COUNT(*) FROM diseases WHERE deleted=0")
        count_result = cursor.fetchone()
        total_count = count_result[0] if count_result else 0

        cursor.close()

        arrays = []
        for item in items:
            arrays.append(Disease(id=item[0], name=item[1]))

        response = {
            "items": arrays,
            "total_count": total_count
        }

        return response

    @staticmethod
    def create(name):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM diseases WHERE name = %s AND deleted=0", (name,))
        item = cursor.fetchone()
        if item:
            return item
        cursor.execute(
            "INSERT INTO diseases (name) VALUES (%s)",
            (name,),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM diseases WHERE id = %s AND deleted=0", (id,))
        items = cursor.fetchone()
        cursor.close()

        if items:
            return Disease(id=items[0], name=items[1])
        return None

    def update(self, name=None):
        cursor = mysql.connection.cursor()
        if name:
            self.name = name

        cursor.execute("SELECT * FROM diseases WHERE name = %s AND deleted=0", (name,))
        item = cursor.fetchone()
        if item:
            return item

        cursor.execute(
            "UPDATE diseases SET name=%s, updated_on=%s WHERE id=%s",
            (
                self.name,
                datetime.now(),
                self.id,
            ),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE diseases SET deleted=%s, updated_on=%s WHERE id=%s",
            (1, datetime.now(), self.id),
        )
        mysql.connection.commit()
        cursor.close()
