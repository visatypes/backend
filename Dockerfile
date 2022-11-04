FROM python:3.10.6-slim
WORKDIR /app

# install requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY service /app/service
CMD [ "python", "-m", "service" ]
