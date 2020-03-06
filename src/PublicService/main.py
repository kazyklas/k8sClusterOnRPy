import psycopg2
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import simplejson

"""
Creator: Tomas Klas
Contact: tomas.klas@seznam.cz
Date: 2020-03-05
"""


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


# Create_file is a function to get the file with hashes from user and update DB
# with data that are in the file.
# Also it will get the name of the hash for future cracking.
@app.post("/files/")
async def create_file(files: UploadFile = File(...), hashtype: str = Form(...)):
    try:
        # connect to DB. TODO change ip address to the hostname of the DB.
        connection = psycopg2.connect(database="cracking",
                                      user="postgres",
                                      password="password1",
                                      host="127.0.0.1",
                                      port="5432")

        cursor = connection.cursor()
        
        # TODO check file extension and hashtype that are supported.

        # Read file line by line and generate SQL query.
        while True:
            line = files.file.readline().decode("UTF-8")
            if line == '':
                break
            else:
                SQL_query = "INSERT INTO hashes (hash, type, solving, result) VALUES (%s, %s, %s, %s);"
                data = (line, hashtype, "False", "NULL")
                cursor.execute(SQL_query, data)

        # Commit the changes to hte database and return success.
        connection.commit()
        return {
            "Database Fill": "Success"
        }

    except (Exception, psycopg2.Error) as error :
        return {
            "Database Fill": "Failed"
        }


# This function will return the set of the hashes that are in the DB.
# It will show ale the data that are in the DB.
# Not solving which user added or another stuff like that.
# TODO Try to monetize this in the diploma thesis
@app.get("/solved")
async def print_database():
    try:
        # Connect to DB. TODO change ip address to the hostname of the DB.
        connection = psycopg2.connect(database="cracking",
                                      user="postgres",
                                      password="password1",
                                      host="127.0.0.1",
                                      port="5432")

        # Get the data from DB
        SQL_query = "select * from hashes"
        cursor = connection.cursor()
        cursor.execute(SQL_query)
        records = cursor.fetchall()
        
        # Generate dict for future jsoning and responding
        hashes = []
        for row in records:
             hash = {
                 'hash': row[0],
                 'type': row[1],
                 'sovling': row[2],
                 'result': row[3]
             }
             hashes.append(hash)

        return simplejson.dumps(hashes)

    except (Exception, psycopg2.Error) as error :
        return {
            "Connect to DB": "Failed"
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

