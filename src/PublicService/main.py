#####################################3
# Creator: Tomas Klas
# Contact: tomas.klas@seznam.cz
# Date: 2020-03-05
#####################################3

import psycopg2
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import simplejson

# TODO Try to monetize this in the diploma thesis

app = FastAPI()

# Package          Version
# ---------------- -------
# Click            7.0
# fastapi          0.52.0
# h11              0.9.0
# httptools        0.1.1
# pip              20.0.2
# psycopg2         2.8.4
# pydantic         1.4
# python-multipart 0.0.5
# setuptools       45.2.0
# simplejson       3.17.0
# six              1.14.0
# starlette        0.13.2
# uvicorn          0.11.3
# uvloop           0.14.0
# websockets       8.1
# wheel            0.34.2


DB = "databaseservice"


"""
Create_file is a function to get the file with hashes from user and update DB
with data that are in the file.
Also it will get the name of the hash for future cracking.
"""
@app.post("/files/")
async def create_file(files: UploadFile = File(...), hashtype: str = Form(...)):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        while True:
            line = files.file.readline().decode("UTF-8").rstrip()
            if line == '':
                break
            else:
                cursor.execute(
                    """
                    INSERT INTO 
                    hashes (hash, type, solving, result) 
                    VALUES (%s, %s, %s, %s);
                    """,
                    [line, hashtype, 'False', 'NULL', ]
                )

        connection.commit()
        return {
            "Database Fill": "Success"
        }

    except (Exception, psycopg2.Error) as error:
        return {
            "Database Fill": "Failed"
        }


"""
This function will return the set of the hashes that are in the DB.
It will show ale the data that are in the DB.
Not solving which user added or another stuff like that.
"""
@app.get("/solved")
async def print_database():
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * 
            FROM hashes
            WHERE solving = 'Done' 
            """
        )
        records = cursor.fetchall()
        hashes = []
        for row in records:
            hash = {
                'hash': row[0],
                'result': row[3]
            }
            hashes.append(hash)

        return simplejson.dumps(hashes)

    except (Exception, psycopg2.Error) as error:
        return {
            "Connect to DB": "Failed"
        }


# https://stackoverflow.com/questions/57343510/how-to-use-a-string-variable-in-psycopg2-select-query
"""
This function will take an argument from the curl with result.
For this result will try to find the hash in the DB.
"""
@app.get("/solved/result/{result}")
async def print_hash_for_result(result):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT hash 
            FROM hashes h
            WHERE h.result = %s;
            """,
            [result, ]
        )

        result = cursor.fetchone()
        if result == "":
            return {
                "Not found"
            }
        return simplejson.dumps(result)

    except (Exception, psycopg2.Error) as error:
        return {
            "Connection to DB": "Failed"
        }


"""
Function will take an argument with hash and will try to find result.
Will return a JSON that contains the result, null if not solved.
"""
@app.get("/solved/hash/{hashid}")
async def print_result_from_hash(hashid):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT result 
            FROM hashes h
            WHERE h.hash = %s;
            """,
            [hashid, ]
        )

        result = cursor.fetchone()

        return simplejson.dumps(result)

    except (Exception, psycopg2.Error) as error:
        return {
            "Not such a result": "Failed"
        }


"""
Check if the service is ready aka if it is connected to db or it can be connected.
And check if it is healthy by checking its api on /health.
"""
@app.get("/ready", status_code=200)
async def check_health_for_k8s():
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        return { "Health": "OK"}
    except (Exception, psycopg2.Error) as error:
        status_code = 400
        return {
            "Ready": "False"
        }


@app.get("/health", status_code=200)
async def check_health_for_k8s():
    return {
        "Health": "OK"
    }


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="hashtype" type="text">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
