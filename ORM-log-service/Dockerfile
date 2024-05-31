FROM python:3.12

ADD . /app

# ADD ./orm-post-service/app.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn
RUN pip3 install python-dotenv

EXPOSE 8008
CMD ["uvicorn", "app.server.app:app", "--port", "8010", "--host", "0.0.0.0", "--reload"]
