FROM python:3.12
ADD . /app

# ADD ./orm-community-service/app.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn
RUN pip3 install python-dotenv

EXPOSE 8003
CMD ["uvicorn", "app.server.app:app", "--port", "8005", "--host", "0.0.0.0", "--reload"]
