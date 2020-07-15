from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, DateTimeField, SelectField
from wtforms.validators import InputRequired, Length, Email, equal_to

class BookClubForm(FlaskForm):
    clubName = StringField('Book Club Name', validators=[InputRequired(), Length(min=2, max=100)])
    meetingFrequency = SelectField(u'Meeting Frequency', 
                                    choices=[('monthly', 'Monthly'),
                                             ('twice monthly', 'Twice Monthly'),
                                             ('weekly', 'Weekly')])
    clubGenre = SelectField('Genre', coerce=int, validators=[InputRequired()])
    clubLeaderEmail = StringField('Club Leader Email', validators=[InputRequired(), Email()])
    clubSubmit = SubmitField('Create New Book Club')

class NewMeetingForm(FlaskForm):
    clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    meetingDate = DateField('Meeting Date', format='%Y-%m-%d', validators=[InputRequired()])
    meetingTime = DateTimeField('Meeting Time', format='%H:%M')
    meetingBook = StringField('Meeting Book')
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
    genre = StringField('Genre', validators=[InputRequired()])
    submit = SubmitField('Add New Book')

class ClubSignUp(FlaskForm):
    clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    email = StringField('Member Email', validators=[InputRequired(), Email()])
    signUpSubmit = SubmitField('Sign Up For Book Club')

class SelectClub(FlaskForm):
    clubName = SelectField('Book Club', coerce=int, validators=[InputRequired()])
    selectClubSubmit = SubmitField('View Upcoming Meetings')

class MeetingSignUp(FlaskForm):
    meetingID = IntegerField('Meeting ID', validators=[InputRequired()])
    email = StringField('Member Email', validators=[InputRequired(), Email()])
    signUpSubmit = SubmitField('Sign Up For Club Meeting')

class GenresForm(FlaskForm):
    genre = StringField('Genre', validators=[InputRequired()])
    genreSubmit = SubmitField('Add New Genre')
