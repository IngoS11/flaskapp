from os import environ
from flask import Flask, jsonify, redirect
from app.auth import auth
from app.bookmarks import bookmarks
from app.database import db
from flask_jwt_extended import JWTManager
from app.database import Bookmark

def create_app(test_config=None):
    app = Flask(__name__,
        instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()

        return redirect(bookmark.url)

    return app
