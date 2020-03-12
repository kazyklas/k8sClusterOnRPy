FROM python:3.7

ENV FASTAPI          0.52.0 
ENV UVICORN          0.11.3
ENV PSYCOPG2         2.8.4
ENV SIMPLEJSON       3.17.0
ENV PYTHON-MULTIPART 0.0.5

RUN pip install fastapi==${FASTAPI} \
                uvicorn==${UVICORN} \
                psycopg2==${PSYCOPG2} \
                simplejson==${SIMPLEJSON} \
                python-multipart==${PYTHON-MULTIPART}

EXPOSE 8080

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

