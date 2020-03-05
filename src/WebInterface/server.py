import time
import os
import psycopg2
from flask import Flask, flash, request, render_template, redirect, url_for
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'hashstaged'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def insertToDB(filename, hash_type):
    USERNAME = "postgres"
    PASSWORD = "password1"
    HOST = "127.0.0.1" 
    DB_NAME = "cracking"
    PORT = "5432"

    try:
        connection = psycopg2.connect(database = DB_NAME,
                                      user = USERNAME,                              
                                      password = PASSWORD,
                                      host = HOST,
                                      port = PORT)

        cursor = connection.cursor()
        
        filename = "hashstaged/"+filename
        hashFile = open(filename, "r")

        while True:
            line = hashFile.readline()
            if not line:
                break
            else:
                #TODO insert to DB
                SQL = "INSERT INTO hashes (hash, type, solving, result) VALUES (%s, %s, %s, %s);"
                data = (line, hash_type, "False", "NULL")
                cursor.execute(SQL, data)

        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
      
        # TODO read from form 
        hash_type = request.args.get('hashtype')
        
        if file.filename == '':# or  hash_type != "":
            flash('Bad Form!!')
            return redirect(request.url)
        
        # Save the file if everything is fine
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            insertToDB(filename, hash_type);


        return redirect('/')

    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    
    app.run(debug=True)
