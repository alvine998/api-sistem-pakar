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

    from .user_apps.routes import userapps as userapps_blueprint
    app.register_blueprint(userapps_blueprint, url_prefix='/userapps')

    from .symptoms.routes import symptoms as symptoms_blueprint
    app.register_blueprint(symptoms_blueprint, url_prefix='/symptoms')

    from .diseases.routes import diseases as diseases_blueprint
    app.register_blueprint(diseases_blueprint, url_prefix='/diseases')

    return app
