from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


class UserApp:
    def __init__(
        self,
        id=None,
        name=None,
        email=None,
        phone=None,
        birth_date=None,
        password=None,
        status=1,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.password = password
        self.status = status

    def to_dick(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date,
            "status": self.status,
        }

    @staticmethod
    def get_users(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM user_apps WHERE deleted=0 AND name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY id DESC LIMIT %s, %s",
                (
                    "%" + search + "%",
                    "%" + search + "%",
                    "%" + search + "%",
                    offset,
                    limit,
                ),
            )
        else:
            cursor.execute(
                "SELECT * FROM user_apps WHERE deleted=0 ORDER BY id DESC LIMIT %s, %s", (offset, limit)
            )

        users_data = cursor.fetchall()
        cursor.close()

        users = []
        for user_data in users_data:
            users.append(
                UserApp(
                    id=user_data[0],
                    name=user_data[1],
                    birth_date=user_data[2],
                    phone=user_data[3],
                    email=user_data[4],
                    password=user_data[5],
                    status=user_data[6],
                )
            )

        return users

    @staticmethod
    def create(name, email, password, phone, birth_date, status):
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO user_apps (name, email, password, phone, birth_date, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                name,
                email,
                hash_password,
                phone,
                birth_date,
                status,
            ),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_apps WHERE id = %s AND deleted=0", (id,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return UserApp(
                id=user_data[0],
                name=user_data[1],
                birth_date=user_data[2],
                phone=user_data[3],
                email=user_data[4],
                password=user_data[5],
                status=user_data[6],
            )
        return None

    def update(
        self,
        name=None,
        email=None,
        password=None,
        phone=None,
        birth_date=None,
        status=None,
    ):
        cursor = mysql.connection.cursor()
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        if phone:
            self.phone = phone
        if birth_date:
            self.birth_date = birth_date
        if status:
            self.status = status

        cursor.execute(
            "UPDATE user_apps SET name=%s, email=%s, password=%s, phone=%s, birth_date=%s, status=%s, updated_on=%s WHERE id=%s",
            (
                self.name,
                self.email,
                self.password,
                self.phone,
                self.birth_date,
                self.status,
                datetime.now(),
                self.id,
            ),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE user_apps SET deleted=%s, updated_on=%s WHERE id=%s",
            (1, datetime.now(), self.id),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM user_apps WHERE email = %s AND deleted = 0", (email,)
        )
        user_data = cursor.fetchone()
        cursor.close()
        print(user_data)
        if user_data:
            return UserApp(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
                phone=user_data["phone"],
                birth_date=user_data["birth_date"],
                status=user_data["status"],
            )
        return None

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
