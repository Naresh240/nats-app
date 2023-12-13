FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install nats-py
CMD [ "python", "./app.py" ]
