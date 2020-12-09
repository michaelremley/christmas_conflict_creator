from flask_wtf import FlaskForm
from wtforms import  SubmitField, FileField
from wtforms.validators import DataRequired

class SubmitForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Submit File')
