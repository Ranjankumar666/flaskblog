from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    submit = SubmitField('Create')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[
                          DataRequired()], widget=TextArea())
    submit = SubmitField('Update')
