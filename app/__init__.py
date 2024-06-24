from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

mysql = MySQL()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config.from_object('config.Config')

    mysql.init_app(app)
    bcrypt.init_app(app)
    
    # Make MySQL accessible through app context
    app.mysql = mysql

    # Register blueprints
    from .users.routes import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # from .offices import offices as offices_blueprint
    # app.register_blueprint(offices_blueprint, url_prefix='/offices')

    return app
