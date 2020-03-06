FROM python:3.7

RUN pip install fastapi==0.52.0 uvicorn==0.11.3 psycopg2==2.8.4 \
                simplejson==3.17.0 python-multipart==0.0.5

EXPOSE 80

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

