import validators
from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app.database import db, Bookmark
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=['GET', 'POST'])
@jwt_required()
def handle_bookmark():
    """
    Create a bookmark
    ---
    tags:
      - Bookmarks
    description: Create a new bookmark
    parameters:
      - name: body
        description: The body contains the user login data in json format
        in: body
        required: true
        schema:
            type: object
            required:
              - "body"
              - "url"
            properties:
              body:
                type: "String"
                example: "Bookmark to the Google Website"
              url:
                type: "string"
                example: "https://google.com"
    responses:
      201:
        description: Bookmark successfully created
      401:
        description: Incorrect credentials supplied
    security:
      - Bearer: [] 
    """    
    current_user = get_jwt_identity()
    
    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return (jsonify({
                'error': "no valid URL specified"
            }), HTTPStatus.BAD_REQUEST)

        if Bookmark.query.filter_by(url=url).first():
            return (jsonify({
                'error': "URL already exists"
            }), HTTPStatus.CONFLICT)

        bookmark = Bookmark(url,body,user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return (jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTPStatus.CREATED)
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmark.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)
        data = []

        for bookmark in bookmarks.items:
            data.append({
                'id' : bookmark.id,
                'url': bookmark.url,
                'short_url' : bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            })

        meta = {
            'page': bookmarks.page,
            'pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,
        }
        return (jsonify({'data':data, 'meta':meta}), HTTPStatus.OK)

@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    """
    Bookmark details
    ---
    tags:
      - Bookmarks
    description: Show details for a bookmark
    parameters:
        - name: id
          in: path
          type: string
          required: true
    responses:
      201:
        description: Bookmark successfully created
      401:
        description: Incorrect credentials supplied
    security:
      - Bearer: [] 
    """    
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(
                              user_id=current_user, id=id).first()

    if not bookmark:
        return (jsonify({'message': "Bookmark not found"}), HTTPStatus.NOT_FOUND)

    return (jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,     
    }), HTTPStatus.OK)

@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
@jwt_required()
def update_bookmark(id):
    """
    Update a bookmark
    ---
    tags:
      - Bookmarks
    description: Update a bookmark
    parameters:
      - name: id
        in: path
        type: string
        required: true
      - name: body
        description: The body contains the bookmark details in json format
        in: body
        required: true
        schema:
          type: object
          required:
            - "body"
            - "url"
          properties:
            body:
              type: "String"
              example: "Bookmark to the Google Website"
            url:
              type: "string"
              example: "https://google.com"
    security:
      - Bearer: [] 
    """
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(
                              user_id=current_user, id=id).first()

    if not bookmark:
        return (jsonify({'message': "Bookmark not found"}), HTTPStatus.NOT_FOUND)

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return (jsonify({
            'error': "no valid URL specified"
        }), HTTPStatus.BAD_REQUEST)

    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return (jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTPStatus.OK)

@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    """
    Delete a bookmark
    ---
    tags:
      - Bookmarks
    description: Delete a bookmark
    parameters:
        - name: id
          in: path
          type: string
          required: true
    security:
      - Bearer: []    
    """
    
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(
                              user_id=current_user, id=id).first()

    if not bookmark:
        return (jsonify({'message': "Bookmark not found"}), HTTPStatus.NOT_FOUND)

    db.session.delete(bookmark)
    db.session.commit()

    return(jsonify({}), HTTPStatus.NO_CONTENT)

@bookmarks.get("/stats")
@jwt_required()
def get_stats():
    """
    Bookmark Statistics
    ---
    tags:
      - Bookmarks
    description: Statistics for all bookmarks of the current user
    responses:
      200:
        description: User successfully logged in
      400:
        description: User login failed
      401:
        description: Incorrect credentials supplied
    security:
      - Bearer: [] 
    """
    current_user = get_jwt_identity()

    data = []

    items = Bookmark.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link={
            'visits': item.visits,
            'url': item.url,
            'id': item.id,
            'short_url': item.short_url,
        }
        data.append(new_link)

    return (jsonify({'data': data}), HTTPStatus.OK)
