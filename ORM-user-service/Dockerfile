FROM python:3.11

ADD . /app

# ADD ./orm-user-service/app.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn
RUN pip3 install python-dotenv

EXPOSE 8002
CMD ["uvicorn", "app.server.app:app", "--port", "8002", "--host", "0.0.0.0", "--reload"]
