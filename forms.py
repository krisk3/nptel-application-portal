from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date

class ApplicationForm(FlaskForm):
    """
    Application Form for the user to apply for course via the webpage form
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=127)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=127)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(max=127)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    degree = StringField('Degree', validators=[DataRequired(), Length(max=127)])
    field_of_study = StringField('Field of Study', validators=[DataRequired(), Length(max=127)])
    institution = StringField('Institution', validators=[DataRequired(), Length(max=127)])
    cgpa = FloatField('CGPA', validators=[DataRequired(), NumberRange(min=0, max=10)])
    transcript = FileField('Transcript', validators=[DataRequired()])
    id_proof = FileField('ID Proof', validators=[DataRequired()])
    submit = SubmitField('Submit')
