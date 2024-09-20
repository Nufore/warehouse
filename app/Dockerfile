FROM python:3.11.8-slim

ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ADD main.py /app/main.py
ADD config.py /app/config.py
COPY .env /app/.env

COPY /database /app/database
COPY /fastapi_app /app/fastapi_app


CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app", "--reload"]