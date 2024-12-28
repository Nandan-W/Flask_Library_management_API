from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import books, auth , members


db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(books.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)

    with app.app_context():
        db.create_all()

    return app