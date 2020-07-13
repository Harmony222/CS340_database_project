from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import BookClubForm, MeetingForm, MembersForm, BooksForm, ClubSignUp, MeetingSignUp, GenresForm

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
    clubs = get_all_clubs()
    genres_list = get_genres()
    club_names_list = get_club_names()
    form = BookClubForm()
    form.clubGenre.choices = genres_list
    formSignUp = ClubSignUp()
    formSignUp.clubName.choices = club_names_list
    return render_template('bookclubs.html', 
                            form=form, 
                            formSignUp=formSignUp,
                            active={'bookclubs':True},
                            clubs=clubs)

@app.route('/meetings')
def meetings():
    all_meetings = get_all_meetings()
    club_names_list = get_club_names()
    form = MeetingForm()
    form.clubName.choices = club_names_list
    formSignUp = MeetingSignUp()
    formSignUp.clubName.choices = club_names_list
    return render_template('meetings.html', 
                            form=form, 
                            formSignUp=formSignUp,
                            active={'meetings':True},
                            all_meetings=all_meetings)
    
@app.route('/books')
def books():
    form = BooksForm()
    return render_template('books.html', form=form, active={'books':True})

@app.route('/genres')
def genres():
    form = GenresForm()
    return render_template('genres.html', form=form, active={'index':True})


def get_genres():
    cur = mysql.connection.cursor()
    result_val = cur.execute('SELECT * FROM Genres')
    if result_val > 0:
        genres_dict = cur.fetchall()
    genres_list = []
    for g in genres_dict:
        genres_list.append((g['genreID'], g['genre'].capitalize())) 
    return genres_list

def get_club_names():
    cur = mysql.connection.cursor()
    result_val = cur.execute('SELECT bookClubID, clubName FROM BookClubs')
    if result_val > 0:
        club_names_dict = cur.fetchall()
    club_names_list = []
    for c in club_names_dict:
        club_names_list.append((c['bookClubID'], c['clubName']))
    return club_names_list

def get_all_clubs():
    cur = mysql.connection.cursor()
    result_val = cur.execute('''
        SELECT b.bookClubID, b.clubName, b.meetingFrequency, g.genre, m.firstName, m.lastName
        FROM BookClubs as b
        JOIN Genres as g ON b.clubGenreID = g.genreID
        JOIN Members as m ON b.clubLeaderID = m.memberID''')
    if result_val > 0:
        clubs = cur.fetchall()
    else:
        clubs = dict()

    print(clubs)
    return clubs

def get_all_meetings():
    cur = mysql.connection.cursor()
    result_val = cur.execute('''
        SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
        FROM ClubMeetings as cm
        JOIN Books as b ON cm.meetingBookID = b.bookID
        JOIN Members as m on cm.meetingLeaderID = m.memberID
        JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID''')
    if result_val > 0:
        meetings = cur.fetchall()
    else:
        meetings = dict()
    return meetings

if __name__ == '__main__':
    app.run(debug=True)