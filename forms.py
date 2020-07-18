from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, DateTimeField, SelectField
from wtforms.validators import InputRequired, Length, Email, equal_to, DataRequired

class BookClubForm(FlaskForm):
    clubName = StringField('Book Club Name', validators=[InputRequired(), Length(min=2, max=100)])
    meetingFrequency = SelectField(u'Meeting Frequency', 
                                    choices=[('monthly', 'Monthly'),
                                             ('twice monthly', 'Twice Monthly'),
                                             ('weekly', 'Weekly'),
                                             ('None', 'None')])
    clubGenre = SelectField('Genre', coerce=int, validators=[InputRequired()])
    clubLeaderEmail = StringField('Club Leader Email', validators=[InputRequired(), Email()])
    clubSubmit = SubmitField('Create New Book Club')

class NewMeetingForm(FlaskForm):
    clubName = IntegerField('Book Club ID', validators=[InputRequired()])
    # clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    meetingDate = DateField('Meeting Date', format='%Y-%m-%d', validators=[InputRequired()])
    meetingTime = DateTimeField('Meeting Time', format='%H:%M')
    meetingBook = SelectField('Meeting Book', coerce=int)
    meetingLeaderEmail = StringField('Meeting Leader Email', validators=[InputRequired(), Email()])
    meetingSubmit = SubmitField('Schedule Meeting')

class MembersForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2, max=100)])
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[Email()]) # pip3 install email-validator if you get exception
    submit = SubmitField('Add New Member')

class BooksForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    genre = SelectField('Genre', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Add New Book')

class ClubSignUp(FlaskForm):
    # https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
    clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    email = StringField('Member Email', validators=[InputRequired(), Email()])
    signUpSubmit = SubmitField('Sign Up For Book Club')

class SelectClub(FlaskForm):
    clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    selectClubSubmit = SubmitField('View Upcoming Meetings')
    attendeeSubmit = SubmitField('View Meetings')

class MeetingSignUp(FlaskForm):
    meetingID = IntegerField('Meeting ID', validators=[InputRequired()])
    email = StringField('Member Email', validators=[InputRequired(), Email()])
    signUpSubmit = SubmitField('Sign Up For Club Meeting')

class GenresForm(FlaskForm):
    genre = StringField('Genre', validators=[InputRequired()])
    genreSubmit = SubmitField('Add New Genre')
