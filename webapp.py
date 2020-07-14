from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import *

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

@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
    all_meetings = get_all_meetings()
    club_names_list = get_club_names()
    form = MeetingForm()
    form.clubName.choices = club_names_list
    formSelectClub = SelectClub()
    formSelectClub.clubName.choices = club_names_list
    formSignUp = MeetingSignUp()
    # if request.method == 'POST':
    #     if formSelectClub.validate_on_submit():
    if request.method == 'POST' and formSelectClub.validate():
            club = formSelectClub.clubName.data
            club_meetings = get_club_meetings(club)
            return render_template('meetings.html', 
                                       form=form, 
                            formSelectClub=formSelectClub,
                            formSignUp=formSignUp,
                            active={'meetings':True, 'signup':True},
                            all_meetings=all_meetings,
                            club_meetings=club_meetings)
    print(formSignUp.meetingID.errors)
    if request.method == 'POST' and formSignUp.validate_on_submit():
        print(formSignUp.meetingID.data)
    return render_template('meetings.html', 
                            form=form, 
                            formSelectClub=formSelectClub,
                            formSignUp=formSignUp,
                            active={'meetings':True, 'view':True},
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

def get_book_list():
    cur = mysql.connection.cursor()
    result_val = cur.execute('SELECT * FROM Books')
    if result_val > 0:
        books_dict = cur.fetchall()
    books_list = []
    for b in books_dict:
        books_list.append((b['bookID'], b['title']))
    return books_list

def get_all_clubs():
    cur = mysql.connection.cursor()
    result_val = cur.execute('''
        SELECT b.bookClubID, b.clubName, b.meetingFrequency, g.genre, m.firstName, m.lastName, tmp.nextMeeting
        FROM BookClubs as b
        JOIN Genres as g ON b.clubGenreID = g.genreID
        JOIN Members as m ON b.clubLeaderID = m.memberID
        LEFT JOIN (
                SELECT tmp.bookClubID, MIN(tmp.dateTime) as nextMeeting
                FROM (SELECT cm2.bookClubID, cm2.dateTime
                        FROM ClubMeetings as cm2
                        WHERE cm2.dateTime > CURDATE()) as tmp
                        GROUP BY tmp.bookClubID) as tmp ON b.bookClubID = tmp.bookClubID''')
    if result_val > 0:
        clubs = cur.fetchall()
    else:
        clubs = dict()
    return clubs

def get_all_meetings():
    cur = mysql.connection.cursor()
    result_val = cur.execute('''
        SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
        FROM ClubMeetings as cm
        JOIN Books as b ON cm.meetingBookID = b.bookID
        JOIN Members as m on cm.meetingLeaderID = m.memberID
        JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
        WHERE cm.dateTime >= CURDATE()
        ORDER BY cm.bookClubID, cm.dateTime''')
    if result_val > 0:
        meetings = cur.fetchall()
    else:
        meetings = dict()
    return meetings

def get_club_meetings(club):
    cur = mysql.connection.cursor()
    result_val = cur.execute(f'''
        SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
        FROM ClubMeetings as cm
        JOIN Books as b ON cm.meetingBookID = b.bookID
        JOIN Members as m on cm.meetingLeaderID = m.memberID
        JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
        WHERE cm.dateTime >= CURDATE() AND cm.bookClubID = '{club}'
        ORDER BY cm.bookClubID, cm.dateTime''')
    if result_val > 0:
        club_meetings = cur.fetchall()
    else:
        club_meetings = dict()
    return club_meetings

if __name__ == '__main__':
    app.run(debug=True)