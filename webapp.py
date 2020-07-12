from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import BookClubForm, MeetingForm, MembersForm, BooksForm, ClubSignUp, MeetingSignUp

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
    form = MembersForm()
    return render_template('members.html', form=form, active={'members':True})

@app.route('/bookclubs')
def bookclubs():
    genres_list = get_genres()
    clubs_list = get_clubs()
    form = BookClubForm()
    form.clubGenre.choices = genres_list
    formSignUp = ClubSignUp()
    formSignUp.clubName.choices = clubs_list
    return render_template('bookclubs.html', 
                            form=form, 
                            formSignUp=formSignUp,
                            active={'bookclubs':True})

@app.route('/meetings')
def meetings():
    form = MeetingForm()
    formSignUp = MeetingSignUp()
    return render_template('meetings.html', 
                            form=form, 
                            formSignUp=formSignUp,
                            active={'meetings':True})
    
@app.route('/books')
def books():
    form = BooksForm()
    return render_template('books.html', form=form, active={'books':True})

@app.route('/genres')
def genres():
    return render_template('genres.html', active={'index':True})



def get_genres():
    cur = mysql.connection.cursor()
    result_val = cur.execute('SELECT * FROM Genres')
    if result_val > 0:
        genres_dict = cur.fetchall()
    genres_list = []
    for g in genres_dict:
        genres_list.append((g['genreID'], g['genre'].capitalize())) 
    return genres_list

def get_clubs():
    cur = mysql.connection.cursor()
    result_val = cur.execute('SELECT bookClubID, clubName FROM BookClubs')
    if result_val > 0:
        clubs_dict = cur.fetchall()
    clubs_list = []
    for c in clubs_dict:
        clubs_list.append((c['bookClubID'], c['clubName']))
    return clubs_list


if __name__ == '__main__':
    app.run(debug=True)