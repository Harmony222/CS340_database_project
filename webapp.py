from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from forms import *
from db_connector import connect_to_database, execute_query
import MySQLdb

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
        add_members(firstName, lastName, email)
    
    all_members = get_all_members()
    #print("test: ")
    #print(all_members[0][0])
    #print("********")

    return render_template('members.html', form=members_form, active={'members':True}, members=all_members)

@app.route('/bookclubs', methods=['POST', 'GET'])
def bookclubs():
    clubs = get_all_clubs()
    genres_list = get_genres()
    club_names_list = get_club_names()
    form = BookClubForm()
    form.clubGenre.choices = genres_list
    formSignUp = ClubSignUp()
    formSignUp.clubName.choices = club_names_list #https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
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
    formNewMeeting = NewMeetingForm()
    formNewMeeting.clubName.choices = club_names_list
    formNewMeeting.meetingBook.choices = [('0', 'Please select a book club first.')]

    if request.method == 'POST':
        print(formNewMeeting.validate())
        print(formNewMeeting.validate_on_submit())
        club = request.form['clubName']
        date = request.form['meetingDate']
        time = request.form['meetingTime']
        book = request.form['meetingBook']
        leader_email = request.form['meetingLeaderEmail']
        print(club, date, time, book, leader_email)
    return render_template('meetingsnew.html',
                            formNewMeeting=formNewMeeting,
                            active={'meetings':True, 'new':True})

@app.route('/get_books', methods=['GET', 'POST'])
def get_books():
    clubID = request.args['clubID']
    print('clubID', clubID)
    db_connection = connect_to_database()
    query = '''
            SELECT b.bookID, b.title, b.author
            FROM Books b
            WHERE b.bookGenreID = (SELECT bc.clubGenreID 
                                   FROM BookClubs bc 
                                   WHERE bc.bookClubID = %s)       
            '''
    books = execute_query(db_connection, query, (clubID,)).fetchall()
    print(books)
    return jsonify(books)



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

    if request.method == 'POST' and formSignUp.validate_on_submit():
        # signUp_meetingID = formSignUp.meetingID.data
        signUp_meetingID = request.form['meetingID']
        signUp_email = request.form['email']
        print(signUp_meetingID, signUp_email)
        db_connection = connect_to_database()
        query = 'SELECT memberID FROM Members WHERE email = %s'
        data = signUp_email,
        memberID = execute_query(db_connection, query, data).fetchone()
        print('memberID', memberID)
        if not memberID:
            flash('Invalid email! Please sign up as a member first.', 'danger')
            print('memberID not found')
            return redirect('/meetingssignup')
        try:
            query = '''
                    INSERT INTO meetings_members (meetingID, memberID) 
                    VALUES (%s, %s)
                    ''' 
            data = (signUp_meetingID, memberID)
            execute_query(db_connection, query, data)
        except MySQLdb.Error as err:
            flash('Error: {}'.format(err), 'danger')
            print(err)
            return redirect('/meetingsignup')
        flash('Sucessfully signed up for meeting!', 'success')
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

@app.route('/get_attendees', methods = ['GET', 'POST'])
def get_attendees():
    '''
    Route called from Meetings/Who's attending page to 
    retrieve a list of meeting attendees based on meetingID. 
    meetingID is received in the GET request header.
    Returns list of attendees for that meeting as a tuple.
    '''
    meetingID = request.args['meetingID']
    # print('meetingID', meetingID)
    db_connection = connect_to_database()
    query = '''
            SELECT mm.meetingID, m.memberID, m.firstName, m.lastName, m.email 
            FROM Members m
            JOIN meetings_members mm ON m.memberID = mm.memberID 
            WHERE mm.meetingID = %s
            '''
    attendees = execute_query(db_connection, query, meetingID).fetchall()
    # print(attendees)
    return jsonify(attendees)

@app.route('/books', methods=['POST', 'GET'])
def books():
    books_form = BooksForm()
    # Week 7: Learn using Python and Flask Framework - Inserting Data Using Flask Video
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']

    genres_list = get_genres()
    books_form.genre.choices = genres_list
    all_books = get_all_books()
    print(all_books)
        
    return render_template('books.html', form=books_form, active={'books':True}, books = all_books)

@app.route('/genres', methods=['POST', 'GET'] )
def genres():
    form = GenresForm()
    genre_exists = {} # dict which will be sent back to client
    if request.method == 'POST':
        genre = request.form['genre']
        genre = genre.lower() # make input lowercase

        # check if genre exists already, if it does, the front-end will handle this 
        genre_exists = check_genre(genre, genre_exists)
        
        # if not add the genre to Genres table
        if 'exists' not in genre_exists.keys():
            add_genre(genre)

    all_genres = get_genres()
    return render_template('genres.html', form=form, active={'index':True}, genres=all_genres, exists = genre_exists)


def get_genres():
    '''
    Retrieves all genres from mysql database.
    Returns a list of all genres.
    '''
    db_connection = connect_to_database()
    query = 'SELECT * FROM Genres'
    genres = execute_query(db_connection, query).fetchall()
    return genres

def get_club_names():
    '''
    Retrieves all club names from mysql database.
    Returns a list of all club names.
    '''
    db_connection = connect_to_database()
    query = 'SELECT bookClubID, clubName FROM BookClubs'
    club_names = execute_query(db_connection, query).fetchall()
    return club_names

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
    '''
    Retrieves all book clubs from mysql database.
    Returns a list of all book clubs with each club's data in dictionary format.
    '''
    db_connection = connect_to_database()
    query = '''
            SELECT b.bookClubID, b.clubName, b.meetingFrequency, 
                   g.genre, m.firstName, m.lastName, tmp.nextMeeting
            FROM BookClubs as b
            JOIN Genres as g ON b.clubGenreID = g.genreID
            JOIN Members as m ON b.clubLeaderID = m.memberID
            LEFT JOIN (
                    SELECT tmp.bookClubID, MIN(tmp.dateTime) as nextMeeting
                    FROM (SELECT cm2.bookClubID, cm2.dateTime
                          FROM ClubMeetings as cm2
                          WHERE cm2.dateTime > CURDATE()) as tmp
                          GROUP BY tmp.bookClubID) as tmp 
                    ON b.bookClubID = tmp.bookClubID 
            '''
    clubs = execute_query(db_connection, query, (), True).fetchall()
    return clubs

def get_all_meetings():
    '''
    Retrieves all meetings from mysql database.
    Returns a list of all meetings with each meeting's data in dictionary format.
    '''
    db_connection = connect_to_database()
    query = '''
            SELECT cm.meetingID, cm.dateTime, b.title, b.author, 
                   bc.clubName, m.firstName, m.lastName
            FROM ClubMeetings as cm
            JOIN Books as b ON cm.meetingBookID = b.bookID
            JOIN Members as m on cm.meetingLeaderID = m.memberID
            JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
            WHERE cm.dateTime >= CURDATE()
            ORDER BY cm.bookClubID, cm.dateTime
            '''
    meetings = execute_query(db_connection, query, (), True).fetchall()
    return meetings

def get_club_meetings(club):
    '''
    Retrieves meetings for the given club from mysql database.
    Returns a list of all meetings with each meeting's data in dictionary format.
    '''
    db_connection = connect_to_database()
    query = '''
            SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
            FROM ClubMeetings as cm
            JOIN Books as b ON cm.meetingBookID = b.bookID
            JOIN Members as m on cm.meetingLeaderID = m.memberID
            JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
            WHERE cm.dateTime >= CURDATE() AND cm.bookClubID = '{}'
            ORDER BY cm.bookClubID, cm.dateTime
            '''.format(club)
    club_meetings = execute_query(db_connection, query, (), True).fetchall()
    return club_meetings


def get_all_members():
    '''
        SELECT query on Members table.
        Returns tuple, all_members, containing
        each row of Members table as a tuple.
    '''
    db_connection = connect_to_database()
    query = "SELECT * FROM Members"
    all_members = execute_query(db_connection, query).fetchall()
    return all_members

def add_members(firstName, lastName, email):
    '''
        Executes INSERT query on Members table.
        Takes firstName, lastName, and email
        input values from the Add Members form
    '''
    db_connection = connect_to_database()
    query = '''
            INSERT INTO Members (firstName, lastName, email)
            VALUES (%s, %s, %s)
            '''
    data = (firstName, lastName, email)
    execute_query(db_connection, query, data)

def get_all_books():
    '''
        SELECT query on Books / Genres joined table. 
        Genre name is displayed instead of genreID.
        Returns tuple, all_books, containing each row of the
        table as a tuple. 
    '''
    db_connection = connect_to_database()
    query = '''SELECT b.bookID, b.title, b.author, g.genre
                FROM Books AS b
                JOIN Genres AS g 
                ON b.bookGenreID = g.genreID'''
    all_books = execute_query(db_connection, query).fetchall()
    return all_books

def add_genre(genre):
    '''
        Executes INSERT query on Genres table.
        Takes genre input values from the 
        Add Genre form
    '''
    db_connection = connect_to_database()
    query = '''
            INSERT INTO Genres (genre)
            VALUES (%s)
            '''
    data = (genre,) # single element tuple needs trailing comma
    execute_query(db_connection, query, data)

def check_genre(genre, genre_exists):
    '''
        Checks if the genre already exists in Genres database.
        Takes parameters: genre - the input value from Add Genres form
                          genre_exists - empty dictionary initialized in
                                        the /genres route
        returns genre_exists
    '''
    all_genres = get_genres() 
    genre_names = []

    # grab only the the genre names from Genres SELECT query 
    for row in all_genres:
        genre_names.append(row[1])

    # if the genre exists, create a key, 'exists' with value True
    if genre in genre_names:
        genre_exists['exists'] = True
        return genre_exists
    else:
        return genre_exists

if __name__ == '__main__':
    app.run(debug=True)
