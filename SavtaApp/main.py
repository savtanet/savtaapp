from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "full_name" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'full_name' in request.form and 'password' in request.form:
        # Create variables for easy access
        full_name = request.form['full_name']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM savtas WHERE full_name = %s AND password = %s', (full_name, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['full_name'] = account['full_name']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or full_name/password incorrect
            msg = 'Incorrect full_name/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)
    
    
    # http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
   
   # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'full_name' in request.form and 'password' in request.form and 'age' in request.form and 'address' in request.form and 'floor' in request.form and 'elevator' in request.form and 'phone_number' in request.form and 'limitations' in request.form and 'people_living_with' in request.form:
        # Create variables for easy access
        full_name = request.form['full_name']
        password = request.form['password']
        age = request.form['age']
        address = request.form['address']
        floor = request.form['floor']
        elevator = request.form['elevator']
        phone_number = request.form['phone_number']
        limitations = request.form['limitations']
        people_living_with = request.form['people_living_with']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM savtas WHERE full_name = %s and password=%s', (full_name,password,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', full_name):
            msg = 'Full name must contain only characters!'
        elif not ('full_name' in request.form and 'password' in request.form and 'age' in request.form and 'address' in request.form and 'floor' in request.form and 'elevator' in request.form and 'phone_number' in request.form and 'limitations' in request.form and 'people_living_with' in request.form):
            msg = 'Please fill out the form!'
        else:		
            cursor.execute('INSERT INTO savtas VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (full_name, password, age, address, floor, elevator, phone_number, limitations, people_living_with,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form, 	no post data!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', full_name=session['full_name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


