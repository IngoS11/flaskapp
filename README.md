# Restful Flask Application for Demo

## Initialize Database
Once the development container is build and started, open a terminal inside
Visual Sutdio code and initialize the database by either running `flask db init`
or by using the flask shell with
```
>flask shell
>>>from app.database import db
>>>db.create_all()
>>>quit()
```

## Start Flask applicationç
The application can then be started with
```
> flask run
```