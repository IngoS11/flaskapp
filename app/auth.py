import validators
from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app.database import db, User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from('./docs/auth/register.yml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
   
    if len(password) < 6:
        return (jsonify({'error': "Password is too short"}),
        HTTPStatus.BAD_REQUEST)

    if not username.isalnum() or " " in username:
        return (jsonify({'error': "User has to be alphanumeric and without spaces"}),
        HTTPStatus.BAD_REQUEST)

    if User.query.filter_by(username=username).first() is not None:
        return (jsonify({'error': "User already exists"}),
        HTTPStatus.CONFLICT)

    if not validators.email(email):
        return (jsonify({'error': "Email is not valid"}),
        HTTPStatus.BAD_REQUEST)

    if User.query.filter_by(email=email).first() is not None:
        return (jsonify({'error': "Email is already taken"}),
        HTTPStatus.CONFLICT)

    # add user to the database
    user=User(username, email, password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User Created",
        'user': {
            'username': username,
            'email': email
        }
    }), HTTPStatus.CREATED


@auth.post("/login")
@swag_from('./docs/auth/login.yml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    username = request.json.get('username', '')

    if email:
        user=User.query.filter_by(email=email).first()
    else:
        user=User.query.filter_by(username=username).first()

    if user:
        is_pass_correct = user.check_password(password)
        
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return (jsonify({
                'user' : {
                    'access_token':access,
                    'refresh_token':refresh,
                    'username': user.username,
                    'email': user.email
                }
            }), HTTPStatus.OK)
        else:
            return (jsonify({
                'error':"Authentication failed"
            }), HTTPStatus.UNAUTHORIZED)

    return (jsonify({
        'error':"Authentication failed"
    }), HTTPStatus.UNAUTHORIZED)

@auth.get("/whoami")
@jwt_required()
def whoami():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return (jsonify({
        'username': user.username,
        'email': user.email
    }), HTTPStatus.OK)

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return (jsonify({
        'access' : access
    }), HTTPStatus.OK)
