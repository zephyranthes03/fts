FROM python:3.12

ADD . /app

# ADD ./orm-comment-service/app.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn
RUN pip3 install python-dotenv

EXPOSE 8009
CMD ["uvicorn", "app.server.app:app", "--port", "8009", "--host", "0.0.0.0", "--reload"]
