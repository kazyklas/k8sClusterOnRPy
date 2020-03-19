#####################################
# Creator: Tomas Klas
# Contact: tomas.klas@seznam.cz
# Date: 2020-03-05
#####################################

from fastapi import FastAPI, status
import psycopg2
import simplejson

app = FastAPI()

DB = "databaseservice"


@app.put("delete-work/{hashID}")
async def delete_work_for_hashID(hashID):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE hashes
            SET solving = 'False'
            WHERE hash = %s;    
            """,
            [hashID, ]
        )
        connection.commit()
        return {
            "Done"
        }

    except (Exception, psycopg2.Error) as error:
        return {
            "Could not connect to DB"
        }


"""
Worker will ask for work and will get the hash and the type that he should solve.
Worker than will ask if he realy can take the wokr and will start solving.
"""
@app.get("/get-work/")
async def find_work_for_worker():
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT hash,type 
            FROM hashes 
            WHERE 
            result = 'NULL'
            and 
            solving = 'False';
            """
        )
        result = cursor.fetchone()
        print(result[0], result[1])
        return {
            "hash": result[0],
            "type": result[1]
        }

        #return simplejson.dumps(result)

    except (Exception, psycopg2.Error) as error:
        return {
            "Fail" # No work have been found
        }


"""
Worker will confirm if he can start on the fiven work in the previous get request.
If the work is assigned to another worker in that time it will return False and 
worker won't start working.
"""
@app.put("/start-work/{hashID}")
async def start_work_on_hash(hashID):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        cursor = connection.cursor()
        cursor.execute(
            """SELECT solving 
            FROM hashes 
            WHERE hash = %s""",
            [hashID, ]
        )
        line = cursor.fetchone()
        print(line[0])
        # Work was probably given to another worker before
        # Worker will ask again after the False response on work.
        if line[0] != "False":
            return {
                "False"
            }
        else:
            cursor.execute(
                """
                UPDATE hashes
                SET solving = 'True'
                WHERE hash = %s;    
                """,
                [hashID, ]
            )
            connection.commit()
            return {
                "Start"
            }

    except (Exception, psycopg2.Error) as error:
        return {
            "Not such a result": "Failed"
        }


"""
After worker gets the work and he finishes it he will send put to update the DB.
He will send the hash and the result for the given hash.
"""
@app.put("/work-done/{hashID}/{result}")
async def update_result_for_hash(hashID, result):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host=DB, port="5432")
        # TODO add check to hash it by myself before insert
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE hashes
            SET solving = 'Done',
                result = %s
            WHERE hash = %s;    
            """,
            [result, hashID, ]
        )
        connection.commit()
        return {
            "Great job worker"
        }

    except (Exception, psycopg2.Error) as error:
        return {
            "Not such a result": "Failed"
        }


"""
TODO
Working with Consul:
    Consul will send posts about the dead workers and API will update the DB.
    The DB should be update with one more collum with worker ID.
    Will have to check how to make the ID or how to identify them.
"""


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


"""
On the root return just the info about this service.
"""
@app.get("/")
async def main():
    return {
        "This is private service, it serves data from DB to the workers"
    }
