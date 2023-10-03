# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = '1234'
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'ved'
}
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'ved'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return redirect(url_for('home'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		branch = request.form['branch']
		year = request.form['year']
		subject = request.form['subject']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM register WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO register VALUES (NULL, % s, % s, % s, % s, % s, % s)', (username, email, branch,year, subject,password))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return render_template('login.html', msg=msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
	
@app.route('/home')
def home():
	return render_template('home.html')

# Route to display user profile
@app.route('/user/<user_id>')
def user_profile(user_id):
    try:
        # Connect to MySQL using Flask-MySQLDB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Execute the query to fetch user data
        cursor.execute("SELECT * FROM users WHERE prn = %s", (user_id,))
        user_data = cursor.fetchone()
		
        cursor.close()
		
        if user_data:
            # Pass user data to the template
            return render_template('user_profile.html', user=user_data)
        else:
            return "Data not found"

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)


