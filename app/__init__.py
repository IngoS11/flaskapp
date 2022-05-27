from os import environ
from flask import Flask, jsonify, redirect
from app.auth import auth
from app.bookmarks import bookmarks
from app.database import db
from flask_jwt_extended import JWTManager
from app.database import Bookmark
from http import HTTPStatus
from flasgger import Swagger, swag_from
from app.config.swagger import template, swagger_config

def create_app(test_config=None):
    app = Flask(__name__,
        instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'title':"Bookmarks API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)

    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()

        return redirect(bookmark.url)

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def handle_404(e):
        return (jsonify({'error': "Not found"}), HTTPStatus.NOT_FOUND)

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (jsonify({'error': "Something went wrong, please try again"}), HTTPStatus.INTERNAL_SERVER_ERROR)

    return app
