from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, email_validator, EqualTo, Length
from wtforms.widgets import TextArea

#Create a Form Class
class InfoForm(FlaskForm):
   stdLName = stdLName = StringField('Last Name',validators=[DataRequired()])
   stdFNames=  stdFNames = StringField('First Names',validators=[DataRequired()])
   stdEmailP=  stdEmailP = EmailField( 'Personal Email', validators=[DataRequired()])
   stdID= stdID = StringField('Identity Number', validators=[DataRequired()])
   stdAddrs= stdAddrs = StringField('Residential Address', validators=[DataRequired()])
   submit =SubmitField('Submit Info')