from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # data is returned as dictionaries instead of tuples

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/bookclubs')
def bookclubs():
    return render_template('bookclubs.html')
    
@app.route('/meetings')
def meetings():
    return render_template('meetings.html')

@app.route('/books')
def books():
    return render_template('books.html')