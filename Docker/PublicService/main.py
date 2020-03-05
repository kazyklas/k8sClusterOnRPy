import psycopg2
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import simplejson

app = FastAPI()


@app.post("/files/")
async def create_file(files: UploadFile = File(...), hashtype: str = Form(...)):
    try:
        connection = psycopg2.connect(database="cracking",
                                      user="postgres",
                                      password="password1",
                                      host="127.0.0.1",
                                      port="5432")

        cursor = connection.cursor()

        while True:
            line = files.file.readline().decode("UTF-8")
            if line == '':
                break
            else:
                SQL_query = "INSERT INTO hashes (hash, type, solving, result) VALUES (%s, %s, %s, %s);"
                data = (line, hashtype, "False", "NULL")
                cursor.execute(SQL_query, data)

        connection.commit()
        return {
            "Database Fill": "Success"
        }

    except (Exception, psycopg2.Error) as error :
        return {
            "Database Fill": "Failed"
        }


@app.get("/solved")
async def print_database():
    try:
        connection = psycopg2.connect(database="cracking",
                                      user="postgres",
                                      password="password1",
                                      host="127.0.0.1",
                                      port="5432")

        SQL_query = "select * from hashes"
        cursor = connection.cursor()
        cursor.execute(SQL_query)
        records = cursor.fetchall()

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
1