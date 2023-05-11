# Assignment

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Language & Database : Python(FastAPI) & Mysql

### Mysql Database : user, Table : user 

```
use user;
sqlalchemy.Table(
    user,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(45), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(45), primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("create_date", sqlalchemy.Date),
    sqlalchemy.Column("community", sqlalchemy.Text),
    sqlalchemy.Column("phone", sqlalchemy.String(15)),
    sqlalchemy.Column("email_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("message_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("user_type", sqlalchemy.String(255)),
)
```

## REST API

### orm-user-service : http://localhost:8002/docs

### user-service : http://localhost:8001/docs

## Deployment

```
docker-compose up -d mysql
```

Execute one of belows a minute later. - because It should be execute after mysql server running.

```
docker-compose up 
```
or 
```
docker-compose up -d
```


file location : `user-service/process.py'



