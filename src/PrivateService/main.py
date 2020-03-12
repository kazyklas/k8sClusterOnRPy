#####################################
# Creator: Tomas Klas
# Contact: tomas.klas@seznam.cz
# Date: 2020-03-05
#####################################

from fastapi import FastAPI
import psycopg2
import simplejson

app = FastAPI()


"""
Worker will ask for work and will get the hash and the type that he should solve.
Worker than will ask if he realy can take the wokr and will start solving.
"""
@app.get("/get-work/")
async def find_work_for_worker():
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host="127.0.0.1", port="5432")
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
        return simplejson.dumps(result)

    except (Exception, psycopg2.Error) as error:
        return {
            "Not such a result": "Failed"
        }


"""
Worker will confirm if he can start on the fiven work in the previous get request.
If the work is assigned to another worker in that time it will return False and 
worker won't start working.
"""
@app.put("/start-work/{hashid}")
async def start_work_on_hash(hashid):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        cursor.execute("""SELECT solving FROM hashes WHERE hash = %s""", [hashid, ])
        line = cursor.fetchone()
        print(line[0])
        # Work was probably given to another worker before
        # Worker will ask again after the False response on work.
        if line[0] != "False":
            return {
                "False wrong fetch"
            }
        else:
            cursor.execute(
                """
                UPDATE hashes
                SET solving = 'True'
                WHERE hash = %s;    
                """,
                [hashid, ]
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
@app.put("/work-done/{hashid}/{result}")
async def update_result_for_hash(hashid, result):
    try:
        connection = psycopg2.connect(database="cracking", user="postgres", password="password1", host="127.0.0.1", port="5432")
        # TODO add check to hash it by myself before insert
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE hashes
            SET solving = 'Done',
                result = %s
            WHERE hash = %s;    
            """,
            [result, hashid, ]
        )
        connection.commit()
        return {
            "Great job worker"
        }

    except (Exception, psycopg2.Error) as error:
        return {
            "Not such a result": "Failed"
        }


# TODO
"""
Working with Consul:
    Consul will send posts about the dead workers and API will update the DB.
    The DB should be update with one more collum with worker ID.
    Will have to check how to make the ID or how to identify them.
"""

"""
On the root return just the info about this service.
"""
@app.get("/")
async def main():
    return {
        "This is private service, it serves data from DB to the workers"
    }
