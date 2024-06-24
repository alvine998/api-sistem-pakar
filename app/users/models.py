from app import mysql, bcrypt
import MySQLdb.cursors


class User:
    def __init__(self, id, name, email, password, role, status):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    @staticmethod
    def get_users(page, limit, search=None):
        offset = (page - 1) * limit
        cursor = mysql.connection.cursor()

        if search:
            # Search by name or email
            cursor.execute("SELECT * FROM users WHERE deleted=0 AND name LIKE %s OR email LIKE %s LIMIT %s, %s",
                           ('%' + search + '%', '%' + search + '%', offset, limit))
        else:
            cursor.execute("SELECT * FROM users WHERE deleted=0 LIMIT %s, %s", (offset, limit))        
        
        users_data = cursor.fetchall()
        cursor.close()

        users = []
        for user_data in users_data:
            users.append(User(id=user_data[0], name=user_data[1], email=user_data[2], password=user_data[3], role=user_data[4], status=user_data[5]))

        return users

    @staticmethod
    def create(name, email, password, role):
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role, status) VALUES (%s, %s, %s, %s, 1)",
            (name, email, hash_password, role),
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s AND deleted=0", (id,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return User(
                id=user_data[0],
                name=user_data[1],
                email=user_data[2],
                password=user_data[3],
            )
        return None

    def update(self, name=None, email=None, password=None):
        cursor = mysql.connection.cursor()
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf-8")

        cursor.execute(
            "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s",
            (self.name, self.email, self.password, self.id),
        )
        mysql.connection.commit()
        cursor.close()

    def delete(self):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET deleted=%s WHERE id=%s", (1, self.id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s AND deleted = 0", (email,))
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
