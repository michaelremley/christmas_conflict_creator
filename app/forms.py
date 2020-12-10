from flask_wtf import FlaskForm
from wtforms import  SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired

class SubmitForm(FlaskForm):
    file = FileField('CSV File', validators=[DataRequired()])
    chaotic = BooleanField('Chaotic?', default=True)
    submit = SubmitField('Submit File')
