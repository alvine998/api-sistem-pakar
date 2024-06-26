from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime


def calculate_age(birth_date):
    today = datetime.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


class UserApp:
    def __init__(self, id, name, email, phone, birth_date, age, password, status):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.age = age
        self.password = password
        self.status = status

    @staticmethod
    def get_users(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute(
                "SELECT * FROM user_apps WHERE deleted=0 AND name LIKE %s OR email LIKE %s OR phone LIKE %s LIMIT %s, %s",
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
                "SELECT * FROM user_apps WHERE deleted=0 LIMIT %s, %s", (offset, limit)
            )

        users_data = cursor.fetchall()
        cursor.close()

        users = []
        for user_data in users_data:
            users.append(
                User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password=user_data[3],
                    phone=user_data[4],
                    birth_date=user_data[5],
                    age=user_data[6],
                    status=user_data[7],
                )
            )

        return users

    @staticmethod
    def create(name, email, password, phone, birth_date):
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO user_apps (name, email, password, phone, birth_date, age, status) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)",
            (name, email, hash_password, phone, birth_date, calculate_age(birth_date)),
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
            return User(
                id=user_data[0],
                name=user_data[1],
                email=user_data[2],
                password=user_data[3],
                phone=user_data[4],
                birth_date=user_data[5],
                age=user_data[6],
                status=user_data[7],
            )
        return None

    def update(self, name=None, email=None, password=None, phone=None, birth_date=None, age=None, status=None):
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
        if age:
            self.age = age
        if status:
            self.status = status

        cursor.execute(
            "UPDATE user_apps SET name=%s, email=%s, password=%s, phone=%s, birth_date=%s, age=%s, status=%s WHERE id=%s",
            (self.name, self.email, self.password, self.phone, self.birth_date, calculate_age(self.birth_date),self.status, self.id),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE user_apps SET deleted=%s WHERE id=%s", (1, self.id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_apps WHERE email = %s AND deleted = 0", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
            )
        return None

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
