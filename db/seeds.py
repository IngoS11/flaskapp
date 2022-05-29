from app.database import db, User, Bookmark

# add some users to the database
users = [
    { "username": "peter", "email": "peter@neverland.org", "password": "abcd1234"},
    { "username": "wendy", "email": "wendy@neverland.org", "password": "abcd1234"},
    { "username": "tinker", "email": "tinker@neverland.org", "password": "abcd1234"},
]

bookmarks = [
    { "url" : "http://google.com", "body": "Google"},
    { "url" : "http://yahoo.com", "body": "Yahoo"},
    { "url" : "http://bing.com", "body": "Bing"},
    { "url" : "http://duckduckgo.com", "body": "Duck Duck Go"},
    { "url" : "http://someother.com", "body": "SomeOther"},
    { "url" : "http://linked.in", "body": "LinkedIn"},
]

for user in users:

    if User.query.filter_by(username=user["username"]).first() is None:
        usr = User(user["username"], user["email"], user["password"])
        db.session.add(usr)
        #db.session.commit()

        for bookmark in bookmarks:
            if Bookmark.query.filter_by(url=bookmark["url"], user_id=usr.id).first() is None:
                book = Bookmark(bookmark["url"], bookmark["body"], usr.id)
                db.session.add(book)
            
        db.session.commit()
