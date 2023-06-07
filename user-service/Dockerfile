FROM python:3.11
ADD . /app

# ADD ./orm-setting-service/app.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn[standard]
RUN pip3 install python-dotenv

EXPOSE 8001
CMD ["uvicorn", "app.server.app:app", "--port", "8001", "--host", "0.0.0.0", "--reload"]
