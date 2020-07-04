from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, equal_to

class BookClubForm(FlaskForm):
    clubName = StringField('Book Club Name', validators=[DataRequired(), Length(min=2, max=100)])
    meetingFrequency = IntegerField('Meeting Frequency')
    clubGenre = StringField('Genre', validators=[DataRequired()])   #Drop down list created from database query??
    clubLeaderFirst = StringField('Leader First Name')
    clubLeaderLast = StringField('Leader Last Name')
    submit = SubmitField('Create New Book Club')