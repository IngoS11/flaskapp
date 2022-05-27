# Restful Flask Application for Demo

## Initialize Database before first use
To create an empty database use the flask shell in a terminal
```
>flask shell
>>>from app.database import db
>>>db.create_all()
>>>quit()
```