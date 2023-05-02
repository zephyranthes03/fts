# Assignment

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Language & Database : Python(FastAPI) & Mysql

## Problem 1 - Data Modeling

### Mysql Database : weather, Table : weather 

```
CREATE DATABASE `weather`;
use weather;
CREATE TABLE weather (
    id varchar(20) PRIMARY KEY,
    date varchar(8),
    station varchar(11),
    min_temperature DECIMAL(5,1),
    max_temperature DECIMAL(5,1),
    precipitation DECIMAL(5,1)
);
```

## Problem 2 - Ingestion

file location : `assignment/process.py'
function : add_weather - using restAPI per line by line
function : add_weathers - using restAPI for all records once.

Elapsed time printed on the logs.

** The id(station and date combination) has PRIMARY KEY attribute. So the weather table couldn't have duplicate station and date combication.


## Problem 3 - Data Analysis

file location : `assignment/process.py'
function : statistic_weather()


## Problem 4 - REST API

### orm-user-service : http://localhost:8001/docs

### user-service : http://localhost:8000/docs
To use assignment call It should copy `code-challenge-template` folder around assignment folder.
(default code-challenge-template location : `~/user-service/code-challenge-template`)


## Extra Credit - Deployment

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
function : pandas_statistic_user()

* Simple pandas library test version 


