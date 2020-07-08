from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import BookClubForm, MeetingForm

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # data is returned as dictionaries instead of tuples
app.config['SECRET_KEY'] = 'df98f563f178fb5297613961bb4beace'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', active={'index':True})

@app.route('/members')
def members():
    return render_template('members.html', active={'members':True})

@app.route('/bookclubs')
def bookclubs():
    form = BookClubForm()
    return render_template('bookclubs.html', form=form, active={'bookclubs':True})

@app.route('/meetings')
def meetings():
    form = MeetingForm()
    return render_template('meetings.html', form=form, active={'meetings':True})
    
@app.route('/books')
def books():
    return render_template('books.html', active={'books':True})


if __name__ == '__main__':
    app.run(debug=True)