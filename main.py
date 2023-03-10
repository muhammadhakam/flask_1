from flask import Flask, jsonify
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__) # Creating our Flask Instance
app.secret_key ="gizi"

# mysql config
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = 'sql12594574'
app.config['MYSQL_PASSWORD'] = 'mXns4f3zdK'
app.config['MYSQL_DB'] = 'sql12594574'
mysql = MySQL(Flask_App)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('antro'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('antro'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/database')
def antro():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM antro''')
    antro = cursor.fetchall()
    cursor.close()

    return render_template('database.html', antro=antro)

@app.route('/database/hasil')
def hasil():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM antro''')
    antro = cursor.fetchall()
    cursor.close()

    return render_template('database_hasil.html', antro=antro)

@app.route('/database/delete/<int:id>', methods=['GET'])
def deletepasien(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE 
        FROM antro 
        WHERE id=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()
        flash('pasien deleted','success')
        return redirect(url_for('antro'))

    return render_template('database.html')

@app.route('/database/tambah', methods=['GET'])
def tambah():

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
