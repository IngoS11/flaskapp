import validators
from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app.database import db, User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from

user = Blueprint("user", __name__, url_prefix="/api/v1/user")

@user.post('/register')
def register():
    """
    Register a new user
    ---
    tags:
      - User
    parameters:
      - name: body
        description: The body should contain the username email and password
        in: body
        required: true
        schema:
          type: object
          required:
            - "username"
            - "email"
            - "password"
          properties:
            username:
              type: "string"
              example: "Maria1234"
            email:
              type: "email"
              example: "user@gmail.com"
            password:
              type: "string"
              format: password
              example: "********"
    responses:
      200:
        description: When a user successfully logs in

      400:
        description: User fails to register due to bad request data

      409:
        description: The user or the email already exists in the system
    """
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


@user.post("/login")
def login():
    """
    Authenticate a user
    ---
    tags:
      - User
    description: Authenticate user with a password
    parameters:
      - name: body
        description: The body contains the user login data in json format
        in: body
        required: true
        schema:
            type: object
            required:
              - "email"
              - "password"
            properties:
              email:
                type: "email"
                example: "peter@neverland.org"
              password:
                type: "string"
                format: password
                example: "abcd1234"
    responses:
      200:
        description: User successfully logged in
      400:
        description: User login failed
      401:
        description: Incorrect credentials supplied
    """
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

@user.get("/whoami")
@jwt_required()
def whoami():
    """
    Returns the information for the current user
    ---
    tags:
      - User
    description: Returns the information for the currently logged in user
    responses:
      200:
        description: Userinformation
        schema:
          type: object
          properties:
            username:
              type: "string"
            email:
              type: "string"
      401:
        description: Incorrect credentials supplied
    security:
      - Bearer: [] 
    """
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return (jsonify({
        'username': user.username,
        'email': user.email
    }), HTTPStatus.OK)
    

@user.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    """
    Returns the information for the current user
    ---
    tags:
      - User
    description: Returns the information for the currently logged in user
    responses:
      200:
        description: Refres the JWT Token using the refresh token supplied during login
      401:
        description: Incorrect credentials supplied
    security:
      - Bearer: [] 
    """
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return (jsonify({
        'access' : access
    }), HTTPStatus.OK)
