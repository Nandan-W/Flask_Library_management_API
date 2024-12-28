from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .routes import books, auth , users
        
        app.register_blueprint(books.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(users.bp)

        db.create_all()

    return app