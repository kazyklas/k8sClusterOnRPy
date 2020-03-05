FROM python:3.7

RUN pip install fastapi uvicorn psycopg2 simplejson python-multipart

EXPOSE 80

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

