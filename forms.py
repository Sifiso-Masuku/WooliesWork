from flask_wtf import FlaskForm
from wtforms import StringField, EmailField,SelectField, SubmitField,IntegerField,DateTimeField, PasswordField,RadioField, BooleanField, ValidationError
from wtforms.validators import DataRequired,  Email,InputRequired
from wtforms.widgets import TextArea
from pycountry import countries

#Create a Form Class for students/users
class InfoForm(FlaskForm):
   student_type = student_type =StringField('User Number', validators=[DataRequired()])
   user_number  = user_number= StringField('User Number', validators=[DataRequired()])
   stdLName = stdLName = StringField('Last Name',validators=[DataRequired()])
   stdFNames=  stdFNames = StringField('First Names',validators=[DataRequired()])
   stdEmailP=  stdEmailP = EmailField( 'Personal Email', validators=[DataRequired()])
   stdID= stdID = StringField('Identity Number', validators=[DataRequired()])
   address= address = StringField('Residential Address', validators=[DataRequired()])
   stdEmailP = StringField('Personal Email', validators=[DataRequired(), Email()])
   user_system_email  = StringField('System Email', validators=[DataRequired(), Email()])
   area = StringField('Area', validators=[DataRequired()])
   stdAge = IntegerField('Age', validators=[DataRequired()])
   stdGender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
   stdNationality = SelectField('Nationality', choices=[(country.alpha_3, country.name) for country in countries], validators=[DataRequired()])
   stdCountry = SelectField('Country of Origin', choices=[(country.alpha_2, country.name) for country in countries], validators=[DataRequired()])
   date_added = DateTimeField('Registration Date')
   submit =SubmitField('Submit Info')

#Create a Form for returnig students

class Student_TypeForm(FlaskForm):
    student_type = RadioField('Student Type', choices=[('new', 'New Student'), ('returning', 'Returning Student')], validators=[InputRequired()]) 
    Submit = SubmitField('Continue') 

class LoginForm(FlaskForm):
 user_number  = StringField("Student Number", validators=[DataRequired()])
 user_system_email = StringField('Email',validators=[DataRequired(), Email()])
 Submit = SubmitField("Login")


 