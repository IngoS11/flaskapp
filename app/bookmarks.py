import validators
from flask import Blueprint, jsonify, request
from http import HTTPStatus
from app.database import db, Bookmark
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=['GET', 'POST'])
@jwt_required()
def handle_bookmark():
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