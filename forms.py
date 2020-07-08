from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, equal_to

class BookClubForm(FlaskForm):
    clubName = StringField('Book Club Name', validators=[DataRequired(), Length(min=2, max=100)])
    meetingFrequency = IntegerField('Meeting Frequency')
    clubGenre = StringField('Genre', validators=[DataRequired()])   #Drop down list created from database query??
    clubLeaderFirst = StringField('Leader First Name')
    clubLeaderLast = StringField('Leader Last Name')
    clubSubmit = SubmitField('Create New Book Club')


class MeetingForm(FlaskForm):
    clubName = StringField('Book Club Name', validators=[DataRequired(), Length(min=2, max=100)])
    meetingDate = DateField('Meeting Date', format='%Y-%m-%d', validators=[DataRequired()])
    meetingTime = DateTimeField('Meeting Time', format='%H:%M')
    meetingBook = StringField('Meeting Book', validators=[DataRequired()])
    meetingLeaderFirst = StringField('Leader First Name')
    meetingLeaderLast = StringField('Leader Last Name')
    meetingSubmit = SubmitField('Schedule Meeting')

class MembersForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[Email()]) # pip3 install email-validator if you get exception
    submit = SubmitField('Add New Member')