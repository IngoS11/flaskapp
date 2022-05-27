from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
import string

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="users")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f'User>>> {self.username} Email>>> {self.email}'

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    short_url = Column(String(3), nullable=True)
    visits = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        characters  = string.digits + string.ascii_letters
        picked_chars=''.join(random.choices(characters, k=3))
       
        link=self.query.filter_by(short_url=picked_chars).first()
        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, url, body, user_id):
        self.url = url
        self.body = body
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'Bookmark>>> {self.url}'