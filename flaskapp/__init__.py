from flask import Flask
from flaskapp.config import Config
from flaskapp.api.tables import db
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_mail import Mail


# created the instances
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    # Init the instances
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    mail.init_app(app)


    # init blueprints
    from flaskapp.main.route import main
    from flaskapp.api.routes import back

    app.register_blueprint(main)
    app.register_blueprint(back)

    return app