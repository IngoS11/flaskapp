from app.database import db, User, Bookmark

# add some users to the database
users = []
users.append(User('peterpan', 'peter@neverland.org', 'neverland'))
users.append(User('tinker', 'tinker@neverland.org', 'neverland'))
users.append(User('wendy', 'wendy@neverland.org', 'neverland'))

for user in users:
    if User.query.filter_by(username=user.username).first() is None:
        u=User(user.username, user.email, user.password)
        db.session.add(u)
        db.session.commit()

        # add the same bookmarks to all users in the database
        bookmarks = []
        bookmarks.append(Bookmark('http://google.com', 'Google', u.id))
        bookmarks.append(Bookmark('http://yahoo.com', 'Yahoo', u.id))
        bookmarks.append(Bookmark('http://bing.com', 'Bing', u.id))
        bookmarks.append(Bookmark('http://duckduckgo.com', 'DuckDuckGo', u.id))
        bookmarks.append(Bookmark('http://doesnotexist.com', 'Does Not Exist', u.id))

        for bookmark in bookmarks:
            if Bookmark.query.filter_by(url=bookmark.url, user_id=u.id).first() is None:
                db.session.add(bookmark)

db.session.commit()
