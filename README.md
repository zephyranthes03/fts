# Assignment

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Language & Database : Python(FastAPI) & Mysql

## External domain : http://imgroo.kr

## Check environment setting : .env or .env.sample

# User-service 


user-service port : 8001

Documents link : http://imgroo.kr:8001/docs


## Mysql Database : user, Table : user 

```
use user;
sqlalchemy.Table(
    user,
    metadata,
    # sqlalchemy.Column("id", sqlalchemy.String(64), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(64), primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("create_date", sqlalchemy.DateTime),
    sqlalchemy.Column("community", sqlalchemy.Text),
    sqlalchemy.Column("phone", sqlalchemy.String(15)),
    sqlalchemy.Column("email_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("message_acceptance", sqlalchemy.String(255)),
    sqlalchemy.Column("user_type", sqlalchemy.String(255)),
    sqlalchemy.Column("expire_time", sqlalchemy.Integer),
    sqlalchemy.Column("last_check_time", sqlalchemy.Text),
    sqlalchemy.Column("interested_tag", sqlalchemy.Text),
    sqlalchemy.Column("message", sqlalchemy.Boolean),
    sqlalchemy.Column("friend", sqlalchemy.Text),
    sqlalchemy.Column("permission", sqlalchemy.Text),
    # sqlalchemy.Column("date_convert", sqlalchemy.Date),
)
```
## user service RestAPI endpoint



# Symptom-service 

symptom-service port : 8003

Documents link : http://imgroo.kr:8003/docs


# Community-service 

community-service port : 8005

Documents link : http://imgroo.kr:8005/docs

## MongoDB user id and password can find from .env 



## Deployment

```
docker-compose up -d mysql mongodb
```

Execute one of belows a minute later. - because It should be execute after mysql server running.

```
docker-compose up 
```
or 
```
docker-compose up -d
```

If you want to execute user-services only then You can run this way.

```
docker-compose up user-service orm-user-service
```
or 
```
docker-compose up -d user-service orm-user-service
```


file location : `user-service/process.py'



- Community-service


  