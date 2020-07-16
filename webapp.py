from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import *
from db_connector import connect_to_database, execute_query

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
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

@app.route('/members', methods=['POST', 'GET'])
def members():
    members_form = MembersForm()
    # Week 7: Learn using Python and Flask Framework - Inserting Data Using Flask Video
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
    
    all_members = get_all_members()
    #print("test: ")
    #print(all_members[0][0])
    #print("********")

    return render_template('members.html', form=members_form, active={'members':True}, members=all_members)

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
    return render_template('meetings.html', 
                            active={'meetings':True, 'view':True},
                            all_meetings=all_meetings)
    
@app.route('/meetingsnew', methods=['GET', 'POST'])
def meetingsnew():
    club_names_list = get_club_names()
    form = NewMeetingForm()
    form.clubName.choices = club_names_list

    return render_template('meetingsnew.html',
                            form=form,
                            active={'meetings':True, 'new':True})


@app.route('/meetingssignup', methods=['GET', 'POST'])
def meetingssignup():
    club_names_list = get_club_names()
    formSelectClub = SelectClub()
    formSelectClub.clubName.choices = club_names_list
    formSignUp = MeetingSignUp()
    club_meetings = []
    select_club = False
    if request.method == 'POST' and formSelectClub.validate():
        club = formSelectClub.clubName.data
        club_meetings = get_club_meetings(club)
        select_club = True
    # print('formSignUP valid', formSignUp.validate_on_submit())
    if request.method == 'POST' and formSignUp.validate_on_submit():
        # signUp_meetingID = formSignUp.meetingID.data
        signUp_meetingID = request.form['meetingID']
        signUp_email = request.form['email']
        # print(signUp_meetingID, signUp_email)
        cur = mysql.connection.cursor()
        result_val = cur.execute('SELECT memberID FROM Members WHERE email = %s', [signUp_email])
        if result_val > 0:
            memberID = cur.fetchall()[0]['memberID']
            print(memberID, type(memberID))
        else:
            flash(f'Invalid email! Please sign up as a member first.', 'danger')
            print('memberID not found')
            return redirect('meetingssignup')
        cur.execute('''INSERT INTO meetings_members (meetingID, memberID) 
                       VALUES (%s, %s)''', (signUp_meetingID, memberID))
        mysql.connection.commit()
        cur.close()
        return redirect('/meetingssignup')

    return render_template('meetingssignup.html',
                            formSelectClub=formSelectClub,
                            formSignUp=formSignUp,
                            active={'meetings':True, 'signup':True},
                            club_meetings=club_meetings,
                            select_club=select_club)


@app.route('/attendees', methods=['GET', 'POST'])
def attendees():
    club_names_list = get_club_names()
    formSelectClub = SelectClub()
    formSelectClub.clubName.choices = club_names_list  
    club_meetings = []
    select_club = False
    if request.method == 'POST' and formSelectClub.validate():
        club = formSelectClub.clubName.data
        club_meetings = get_club_meetings(club)
        select_club = True  
    return render_template('attendees.html',
                            formSelectClub=formSelectClub,
                            active={'meetings':True, 'attendees':True},
                            club_meetings=club_meetings,
                            select_club=select_club)


@app.route('/books', methods=['POST', 'GET'])
def books():
    books_form = BooksForm()
    # Week 7: Learn using Python and Flask Framework - Inserting Data Using Flask Video
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        print("Title is: ", title)
        print("Author is: ", author)
        print("Genre is: ", genre)
    genres_list = get_genres()
    books_form.genre.choices = genres_list
    all_books = get_all_books()
    print(all_books)
        
    return render_template('books.html', form=books_form, active={'books':True}, books = all_books)

@app.route('/genres', methods=['POST', 'GET'] )
def genres():
    form = GenresForm()
    all_genres = get_genres()
    return render_template('genres.html', form=form, active={'index':True}, genres=all_genres)


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


def get_all_members(): 
    db_connection = connect_to_database()
    query = "SELECT * FROM Members"
    all_members = execute_query(db_connection, query).fetchall()
    return all_members

def get_all_books():
    db_connection = connect_to_database()
    query = '''SELECT b.bookID, b.title, b.author, g.genre
                FROM Books AS b
                JOIN Genres AS g 
                ON b.bookGenreID = g.genreID'''
    all_books = execute_query(db_connection, query).fetchall()
    return all_books


@app.route('/get_attendees', methods = ['GET', 'POST'])
def get_attendees():
    meetingID = request.args['meetingID']
    print('meetingID from flask', meetingID)
    cur = mysql.connection.cursor()
    result_val = cur.execute('''SELECT mm.meetingID, m.memberID, m.firstName, m.lastName, m.email
                                FROM Members m
                                JOIN meetings_members mm ON m.memberID = mm.memberID 
                                WHERE mm.meetingID = %s''', [meetingID])
    attendees = []
    if result_val > 0:
        attendees = cur.fetchall()
    else:
        # handle zero attendees here?
        pass
    # print(attendees)
    # db_connection = connect_to_database()
    # query = '''SELECT m.firstName, m.lastName, m.email FROM Members m
    #            JOIN meetings_members mm ON m.memberID = mm.memberID 
    #            WHERE mm.meetingID = %s'''
    # attendees = execute_query(db_connection, query, meetingID).fetchall()
    # print(attendees)
    # to_return = {'attendees': attendees}
    return jsonify(attendees)

if __name__ == '__main__':
    app.run(debug=True)