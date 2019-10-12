from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='flask',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app=Flask(__name__)


@app.route('/login',methods=['GET', 'POST'])
def login():
	error = None
	flag = 0
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']

		try:
			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM user WHERE username = '" + email + "'")
				result = cursor.fetchone()
				if result is None:
					flag = 1
					return 'Email ID not registered'
				else:
					cursor.execute("SELECT * FROM user WHERE username = '" + email + "' AND password = '" + password + "'")
					result1 = cursor.fetchone()
					if result1 is None:
						flag = 2
						return 'Wrong Password'
					else:
						flag = 3
						return redirect(url_for('index'))
		finally:
			connection.close()
			if flag == 0:
				return 'Nothing happened'
			elif flag == 1:
				return 'Email Id not registered'
			elif flag == 2:
				return 'Wrong Password'
			else:
				return redirect(url_for('index'))

	return render_template('login.html', error=error)
#    else:
#    	return "error."

@app.route('/')
def index():
	return 'Hello User!'

@app.route('/profile/<username>')
def profile(username):
	return render_template('profile.html', username=username)

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#	error= None
#	if request.method == 'POST':
#		if request.form['username'] != 'sudeshna' or request.form['password'] != 'mini':
#			#return 'Invalid Credentials! Try Again!'
#			return redirect(url_for('login'))
#		else:
#			return redirect(url_for('index'))
#	return render_template('login.html', error=error)
#
if __name__ == '__main__':
    app.debug = True
    app.run()