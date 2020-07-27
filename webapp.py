from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Markup
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


# ----------------------- MEMBERS ROUTE ----------------------------
@app.route('/members', methods=['POST', 'GET'])
def members():
    members_form = MembersForm()
    # Week 7: Learn using Python and Flask Framework - Inserting Data Using Flask Video
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        try:
            add_members(firstName, lastName, email)
            flash('Welcome to Novel Hovel, {}!'.format(firstName), 'success')
            #return redirect('/members')
        except:
            flash('Email unavailable. Please enter a different email.', 'danger')
    
    all_members = get_all_members()
    return render_template('members.html', form=members_form, active={'members':True}, members=all_members)


# ----------------------- BOOKCLUBS ROUTE ---------------------------
@app.route('/bookclubs', methods=['POST', 'GET'])
def bookclubs():
    clubs = get_all_clubs()
    genres_list = get_genres()
    club_names_list = get_club_names()
    form = BookClubForm()
    form.clubGenre.choices = genres_list
    formSignUp = ClubSignUp()
    formSignUp.clubName.choices = club_names_list #https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
    if request.method == 'POST' and form.validate_on_submit():
        club_name = request.form['clubName']
        meeting_frequency = request.form['meetingFrequency']
        genreID = request.form['clubGenre']
        leader_email = request.form['clubLeaderEmail']
        # check if leader is a Novel Hovel Member, if not flash error message
        leaderID = validate_member(leader_email)
        if leaderID:
            try:
                db_connection = connect_to_database()
                query = '''
                        INSERT INTO BookClubs (clubName, meetingFrequency,
                                               clubGenreID, clubLeaderID)
                        VALUES (%s, %s, %s, %s)
                        '''
                data = (club_name, meeting_frequency, genreID, leaderID)
                execute_query(db_connection, query, data)

                # Club Leader must be added to bookclubs_members intersection table
                query = '''
                        SELECT bookClubID FROM BookClubs WHERE clubName = %s
                        '''
                data = (club_name,)
                clubID = execute_query(db_connection, query, data).fetchone()
                addMember_bookClub(clubID, leader_email)

                flash('Sucessfully created {} Book Club!'.format(club_name), 'success')    
            except MySQLdb.Error as err:
                flash('Error: {}'.format(err), 'danger')
                print(err)
            return redirect('/bookclubs')
        else:
            pass
    return render_template('bookclubs.html', 
                            form=form, 
                            formSignUp=formSignUp,
                            active={'bookclubs':True},
                            clubs=clubs)

# ----------------- BOOKCLUB SIGNUP ROUTE ------------------------
@app.route('/bookclubsignup', methods=['GET','POST'])
def bookclubsignup():
    club_names_list = get_club_names()
    formSignUp = ClubSignUp()
    formSignUp.clubName.choices = club_names_list #https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
    if request.method == 'POST':
        clubName = request.form['clubName']
        email = request.form['email']
        try:
            addMember_bookClub(clubName, email)
            flash('Welcome to the club!', 'success')
        except:
            flash('You already signed up this club!', 'danger')
    return render_template('bookclubsignup.html', formSignUp=formSignUp, active={'bookclubsignup':True})

# ------------- VIEW BOOKCLUB MEMBERS ROUTE ----------------------
@app.route('/view_clubMembers/<int:id>')
def view_clubMembers(id):
    '''
        
    '''
    db_connection = connect_to_database()
    query = ''' 
        SELECT tmp.firstName as `First Name`, tmp.lastName as `Last Name` 
        FROM (SELECT bc.bookClubId, m.firstName, m.lastName 
        FROM BookClubs as bc 
        JOIN bookclubs_members as bm 
        ON bc.bookClubID = bm.bookClubId 
        JOIN Members as m 
        ON m.memberID = bm.memberID) as tmp 
        WHERE bookClubId = %s
        '''
    data = (id,)
    club_members = execute_query(db_connection, query, data).fetchall()
    query = '''
            SELECT clubName FROM BookClubs WHERE bookClubID = %s
            '''
    clubName = execute_query(db_connection, query, data).fetchone()
    clubName = clubName[0]
    #print(result)
    return render_template('bookclubmembers.html', active={'view_clubMembers':True}, club_members=club_members, clubName = clubName)

# -------------------- MEETINGS ROUTE ----------------------------
@app.route('/meetings', methods=['GET', 'POST', 'PUT', 'DELETE'])
def meetings():
    all_meetings = get_all_meetings()
    club_names_list = get_club_names()
    # print(club_names_list)
    select_club = False
    if request.method == 'GET' and request.args:
        # Get data for meeting to be modified so that it can be used
        # in the modify form
        meetingID = request.args['meetingID']
        db_connection = connect_to_database()
        query = '''
                SELECT meetingID, bookClubID, dateTime, meetingBookID, meetingLeaderID
                FROM ClubMeetings
                WHERE meetingID = %s 
                '''
        meeting_data = execute_query(db_connection, query, (meetingID,), True).fetchone()
        leaderID = meeting_data['meetingLeaderID']
        query = '''
                SELECT email FROM Members WHERE memberID = %s
                '''
        leader_email = execute_query(db_connection, query, (leaderID,), True).fetchone()
        # get the list of books in that book club's genre plus the book that
        # is currently selected by that book club (or None if no book)
        books = get_books(meeting_data['bookClubID'], selected=meeting_data['meetingBookID'])
        # print(books)
        modify_data = {
            'meeting_data' : meeting_data,
            'leader_email' : leader_email,
            'books' : books
        }
        return jsonify(modify_data)
    if request.method == 'POST':
        # Modify club meeting form - get data from request and execute
        # MySQL query to update the club meeting
        # print(request.form)
        form_data = request.form
        meetingID = form_data['meetingID']
        clubID = form_data['clubName']
        dateTime = form_data['meetingDate'] + ' ' + form_data['meetingTime']
        bookID = form_data['meetingBook']
        if bookID == '-1':
            bookID = None
        leaderID = validate_member(form_data['meetingLeaderEmail'])
        # print(meetingID, clubID, dateTime, bookID, leaderID)
        if leaderID:
            # if leader email is valid, run query to update meeting
            try:
                db_connection = connect_to_database()
                query = '''
                        UPDATE ClubMeetings
                        SET bookClubID = %s, `dateTime` = %s, meetingBookId = %s, 
                            meetingLeaderID = %s
                        WHERE meetingID = %s
                        '''
                data = (clubID, dateTime, bookID, leaderID, meetingID)
                execute_query(db_connection, query, data).fetchall()
                # Sign leader up as a meeting attendee
                flash('Successfully modified meeting!', 'success') 
                return redirect('/meetings')
            except MySQLdb.Error as err:
                flash('Error: {}'.format(err), 'danger')
                print(err)
                return redirect('/meetings')        
    if request.method == 'DELETE':
        print('delete test')
    return render_template('meetings.html', 
                            club_names=club_names_list,
                            active={'meetings':True, 'view':True},
                            all_meetings=all_meetings,
                            select_club=select_club)

@app.route('/get_books_in_genre', methods=['GET', 'POST'])
def get_books_in_genre():
    clubID = request.args['clubID']
    books = get_books(clubID)['book_options']
    return jsonify(books)

# -------------------- DELETE MEETING ROUTE ----------------------
@app.route('/meetings_delete', methods=['GET', 'POST'])
def meetings_delete():
    if request.method == 'POST':
        print(request.form)
        meetingID = request.form['meetingID']
        try:
            db_connection = connect_to_database()
            query = '''
                    DELETE FROM ClubMeetings WHERE meetingID = %s
                    '''
            execute_query(db_connection, query, (meetingID,))
            flash('Successfully deleted meeting!', 'success')
        except MySQLdb.Error as err:
            flash('Error: {}'.format(err), 'danger')
            print(err)
        return redirect('meetings')

# -------------------- NEW MEETINGS ROUTE ------------------------
@app.route('/meetingsnew', methods=['GET', 'POST'])
def meetingsnew():
    club_names_list = get_club_names()
    formSelectClub = SelectClub()
    formSelectClub.clubName.choices = club_names_list
    formNewMeeting = NewMeetingForm()
    formNewMeeting.clubName.choices = club_names_list
    # formNewMeeting.meetingBook.choices = [('0', 'Please select a book club first')]
    select_club = False
    form_disabled = 'disabled'

    if request.method == 'POST' and formSelectClub.validate_on_submit():
        clubID = formSelectClub.clubName.data
        books = get_books(clubID)['book_options']
        formNewMeeting.meetingBook.choices = books
        select_club = True
        form_disabled = None
    print(formNewMeeting.validate_on_submit())
    if request.method == 'POST' and formNewMeeting.validate_on_submit():
        clubID = request.form['clubName']
        dateTime = request.form['meetingDate'] + ' ' + request.form['meetingTime']
        bookID = request.form['meetingBook']
        if bookID == '-1':
            bookID = None
        leader_email = request.form['meetingLeaderEmail']
        # print(clubID, dateTime, bookID, leader_email)
        leaderID = validate_member(leader_email)
        if leaderID:
            try:
                db_connection = connect_to_database()
                query = '''
                        INSERT INTO ClubMeetings (`dateTime`, bookClubID, 
                                                   meetingBookID, meetingLeaderID)
                        VALUES (%s, %s, %s, %s)
                        '''
                data = (dateTime, clubID, bookID, leaderID)
                execute_query(db_connection, query, data)
                # https://stackoverflow.com/questions/17112852/get-the-new-record-primary-key-id-from-mysql-insert-query
                meetingID = execute_query(db_connection, 'SELECT LAST_INSERT_ID()').fetchone()
                # Sign leader up as a meeting attendee
                if meeting_signup_member(meetingID[0], leaderID, leader_email):
                    flash('Successfully scheduled a meeting!', 'success') 
                    flash('Added {} as an attendee for this meeting.'.format(leader_email), 'success')
                    return redirect('/meetingsnew')
            except MySQLdb.Error as err:
                flash('Error: {}'.format(err), 'danger')
                print(err)
                return redirect('/meetingsnew')
        else:
            return redirect(request.referrer) 
    return render_template('meetingsnew.html',
                            formSelectClub=formSelectClub,
                            formNewMeeting=formNewMeeting,
                            active={'meetings':True, 'new':True},
                            select_club=select_club,
                            form_disabled=form_disabled)


# --------------- MEETINGS SIGN UP ROUTE --------------------------
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
        # print(signUp_meetingID, signUp_email)
        memberID = validate_member(signUp_email)
        if not memberID:
            return redirect('/meetingssignup')
        if meeting_signup_member(signUp_meetingID, memberID, signUp_email):
            flash('Sucessfully signed up for meeting!', 'success')
        return redirect('/meetingssignup')

    return render_template('meetingssignup.html',
                            formSelectClub=formSelectClub,
                            formSignUp=formSignUp,
                            active={'meetings':True, 'signup':True},
                            club_meetings=club_meetings,
                            select_club=select_club)


def meeting_signup_member(meetingID, memberID, email):
    '''
    Tries signing up a member to specified meeting. 
    If successful, inserts into meetings_members, and flashes success message,
    otherwise flashes error message.
    '''
    try:
        db_connection = connect_to_database()
        query = '''
                INSERT INTO meetings_members (meetingID, memberID) 
                VALUES (%s, %s)
                ''' 
        data = (meetingID, memberID)
        execute_query(db_connection, query, data)
    except MySQLdb.Error as err:
        print(err)
        if err.args[0] == 1062:
            flash('''
                  Member with email {} is already signed up 
                  for that meeting.
                  '''.format(email), 'danger')
        else:
            flash('Error: {}'.format(err), 'danger')
        return False
    return True


def validate_member(email):
    '''
    Checks to see if email is a Novel Hovel Member. 
    Returns MemberID if True, otherwise flashes invalid email message and returns False.
    '''
    db_connection = connect_to_database()
    query = 'SELECT memberID FROM Members WHERE email = %s'
    data = email,
    memberID = execute_query(db_connection, query, data).fetchone()
    # print('memberID', memberID)
    if not memberID:
        # https://stackoverflow.com/questions/21248718/how-to-flashing-a-message-with-link-using-flask-flash
        flash(Markup('''
                     Invalid email! Please sign up as a Novel 
                     Hovel Member first. <a href="/members">
                     Sign up.</a>
                     '''), 'danger')
        print('memberID not found')
        return False
    return memberID


# -------------------- ATTENDEES ROUTE --------------------------
@app.route('/attendees', methods=['GET', 'POST', 'DELETE'])
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
    if request.method == 'DELETE':
        meetingID = request.args['meetingID']
        memberID = request.args['memberID']
        # print('meetingID', meetingID, 'memberID', memberID)
        db_connection = connect_to_database()
        query = '''
                DELETE FROM meetings_members
                WHERE meetingID = %s AND memberID = %s
                ''' 
        data = (meetingID, memberID)
        execute_query(db_connection, query, data)
        select_query = '''
                       SELECT * FROM meetings_members
                       WHERE meetingID = %s AND memberID = %s
                       '''
        row = execute_query(db_connection, select_query, data).fetchall()
        if len(row) == 0:
            print('attendee succussfully deleted')
            return 'OK', 200

    return render_template('attendees.html',
                            formSelectClub=formSelectClub,
                            active={'meetings':True, 'attendees':True},
                            club_meetings=club_meetings,
                            select_club=select_club)


# ------------------- GET ATTENDEES ROUTE -----------------------
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
    attendees = execute_query(db_connection, query, (meetingID,)).fetchall()
    # print(attendees)
    return jsonify(attendees)

# ----------------------- BOOKS ROUTE ----------------------------
@app.route('/books', methods=['POST', 'GET'])
def books():
    books_form = BooksForm()
    # Week 7: Learn using Python and Flask Framework - Inserting Data Using Flask Video
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        bookGenreID = request.form['genre']
        try:
            add_books(title, author, bookGenreID)
            flash('Successfully added {} by {}!'.format(title, author), 'success')
            #return redirect('/books')
        except:
            flash('The book already exists. Please add a new book.', 'danger')
        
    genres_list = get_genres()
    books_form.genre.choices = genres_list
    all_books = get_all_books()    
    return render_template('books.html', form=books_form, active={'books':True}, books = all_books)

# ---------------------- DELETE BOOK ROUTE ------------------------
@app.route('/delete_book/<int:id>')
def delete_book(id):
    '''
        REFERENCE: Week 7: UPDATE & DELETE functionality using Flask
        id is grabbed from the respective table row in the View
        Books table.
    '''
    try:
        db_connection = connect_to_database()
        query = "SELECT title from Books WHERE bookID = %s"
        data = (id,)
        title = execute_query(db_connection, query, data).fetchone()
        title = title[0]
        query = "DELETE from Books WHERE bookID = %s"
        execute_query(db_connection, query, data)
        flash('{} has been deleted!'.format(title), 'success')
    except:
        flash('An error has occurred. Please try again', 'danger')
    return redirect('/books')
    

# ----------------------- GENRES ROUTE -----------------------------
@app.route('/genres', methods=['POST', 'GET'] )
def genres():
    form = GenresForm()
    if request.method == 'POST':
        genre = request.form['genre']
        genre = genre.lower() # make input lowercase
        try:
            add_genre(genre)
            flash('Successfully added {} genre!'.format(genre), 'success')
            #return redirect('/genres')
        except:
            flash('Genre already exists. Please enter a new genre.', 'danger')

    all_genres = get_genres()
    return render_template('genres.html', form=form, active={'index':True}, genres=all_genres)

# ------------------------- MISC HELPER FUNCTIONS ---------------------------
def get_genres():
    '''
    Retrieves all genres from mysql database.
    Returns a tuple of all genre data (genreID, genre).
    '''
    db_connection = connect_to_database()
    query = 'SELECT * FROM Genres ORDER BY genre'
    genres = execute_query(db_connection, query).fetchall()
    return genres

def get_club_names():
    '''
    Retrieves all club names from mysql database.
    Returns a tuple of all club name data (clubID, clubNames).
    '''
    db_connection = connect_to_database()
    query = 'SELECT bookClubID, clubName FROM BookClubs ORDER BY clubName'
    club_names = execute_query(db_connection, query).fetchall()
    return club_names

def get_books(clubID, selected=False):
    '''
    Retrieve books that are in the genre associated with clubID.
    Only selects those books that are NOT already assigned to a meeting. 
    Returns a list of tuples (bookiD, book name + author).
    Add on selected book if a bookID is passed to function (used for modify meeting).
    '''
    # print('clubID', clubID)
    db_connection = connect_to_database()
    query = '''
            SELECT b.bookID, b.title, b.author
            FROM Books b
            WHERE b.bookID NOT IN (
                SELECT cm.meetingBookID 
                FROM ClubMeetings cm 
                WHERE cm.meetingBookID IS NOT NULL)
            AND b.bookGenreID = (
                SELECT bc.clubGenreID 
                FROM BookClubs bc 
                WHERE bc.bookClubID = %s)
            '''
    books = execute_query(db_connection, query, (clubID,), True).fetchall()
    book_options = []
    for book in books:
        book_options.append((book['bookID'], book['title'] + ' by ' + book['author']))
    book_options.append((-1, 'None'))
    selected_book = False
    if selected is None:
        selected_book = (-1, 'None')
    if selected:
        query = '''
                SELECT b.bookID, b.title, b.author
                FROM Books b
                WHERE b.bookID = %s 
                '''
        selected_book = execute_query(db_connection, query, (selected,), True).fetchone()
        # print('selected_book', selected_book)
        selected_book = (selected_book['bookID'], 
                selected_book['title'] + ' by ' + selected_book['author'])
    return {'selected_book': selected_book, 'book_options': book_options}

def get_all_clubs():
    '''
    Retrieves all book clubs from mysql database pluse the next book club
    meeting date.
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
            LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
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
            LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
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

def add_books(title, author, bookGenreID):
    '''
        Executes INSERT query on Books table.
        Takes title, author, genre input values
        from the Add Book form.

    '''
    db_connection = connect_to_database()
    query = '''
            INSERT INTO Books (title, author, bookGenreID)
            VALUES (%s, %s, %s);
            '''
    data = (title,author,bookGenreID) 
    execute_query(db_connection, query, data)


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

def addMember_bookClub(clubName, email):
    memberID = validate_member(email)
    db_connection = connect_to_database()
    query = '''
            INSERT INTO bookclubs_members (memberID, bookClubID)
            VALUES (%s, %s)
            '''
    data = (memberID, clubName)
    execute_query(db_connection, query, data)


    

if __name__ == '__main__':
    app.run(debug=True)
