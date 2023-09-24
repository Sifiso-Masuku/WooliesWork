import datetime
from flask import Flask, render_template,flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from forms import  InfoForm, Student_TypeForm, LoginForm
from sqlalchemy import create_engine
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
import pymysql
from pycountry import countries
import random
import requests
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import psycopg2

from manage import UserForm
#...Fields...
#BooleanField
#DateField
#DateTimeField
#DecimalField
#FileField
#MultipleFileField
#FloatField
#IntegerField
#RadioField
#SelectField
#SelectMultipleField
#SubmitField
#StringField
#HiddenField
#PasswordField
#TextAreaField

#...Validators...
#DataRequired
#Email
#EqualTo
#InputRequired
#IPAddress
#Length
#MacAddress
#NumberRange
#Optional
#Regexp
#URL
#UUID
#AnyOf
#NoneOf



#Initilize database
db = SQLAlchemy()

#create flask App
app = Flask (__name__)

#Set database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masuku@localhost:3306/Information_Capture'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sifiso:masuku@localhost:5432/informationcapture'
# # Establish the connection
# conn = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     user="sifiso",
#     password="masuku",
#     database="informationcapture"
# )

#  Initialize a Flask App to use for the DATABASE
db.init_app(app)

 
     
#Secret Key
app.config['SECRET_KEY'] = "Sifiso"


#Create Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_type = db.Column(db.String(50), nullable=False)
    user_number  = db.Column(db.String(100), nullable=False)
    stdLName = db.Column(db.String(100), nullable=False)
    stdFNames = db.Column(db.String(100), nullable=False)
    stdEmailP = db.Column(db.String(100), nullable=False)
    stdID = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    user_system_email = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    stdAge = db.Column(db.Integer, nullable=False)
    stdGender = db.Column(db.String(10), nullable=False)
    stdNationality = db.Column(db.String(100), nullable=False)
    stdCountry = db.Column(db.String(100), nullable=False)
    date_added =db.Column(db.DateTime, default=datetime.datetime.now) 

    def __repr__(self):
      return '<name %r>' % self.name
    
    def __init__(self, student_type, user_number , stdLName, stdFNames, stdEmailP, stdID, address, user_system_email, area, stdAge, stdGender, stdNationality, stdCountry,date_added):
        self.student_type = student_type
        self.user_number = user_number 
        self.stdLName = stdLName
        self.stdFNames = stdFNames
        self.stdEmailP = stdEmailP
        self.stdID = stdID
        self.address = address
        self.user_system_email = user_system_email
        self.area = area
        self.stdAge = stdAge
        self.stdGender = stdGender
        self.stdNationality = stdNationality
        self.stdCountry = stdCountry
        self.date_added = date_added

# this is needed in order for database session calls (e.g. db.session.commit)
with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))

db = SQLAlchemy()


   

#Generate User Number
def generate_user_number():
    # Get the current system date and time
    current_time = datetime.datetime.now()
    
    # Format the date and time as YYMMDDhhmmss
    formatted_date = current_time = datetime.datetime.now().strftime("%y%m%d")
    formatted_time = current_time = datetime.datetime.now().strftime("%H%M%S")
    
    # Generate a random number with 4 digits
    random_number = str(random.randint(1000, 9999))
    
    # Combine the components to create the user number
    user_number = formatted_date + formatted_time + random_number
    
    return user_number 

# Generate a new user number
user_number = generate_user_number()
#Generate Student System Email
def generate_user_system_email(last_name, first_names):
    # Combine the student's last name and initials of first and middle names
    initials = "".join(name[0] for name in first_names.split())
    user_system_email = last_name + initials + "@SmartSystem.com"
    
    # Check if the generated email already exists
    email_exists = check_email_exists(user_system_email)
    
    # If the email already exists, append a number to ensure uniqueness
    if email_exists:
       user_system_email = generate_unique_email(user_system_email)
    
    return user_system_email


def check_email_exists(user_system_email):
    # Simulated function to check if the email already exists in the system
    # Replace this with your own logic to check if the email exists in the database
    existing_emails = [
        "DanielsTA@SmartSystem.com",
        "SmithJP@SmartSystem.com",
        "JohnsonLM@SmartSystem.com"
    ]
    
    return user_system_email in existing_emails


def generate_unique_email(user_system_email):
    # Append a number to the email to ensure uniqueness
    counter = 1
    unique_email = user_system_email
    while check_email_exists(unique_email):
        unique_email = user_system_email[:-4] + "{:02d}".format(counter) + user_system_email[-4:]
        counter += 1
    
    return unique_email

#Verify Student Identity Number(ID)
def validate_id_number( stdID):
    # Check if the ID number is in the valid format for South African ID
    if len( stdID) != 13 or not stdID.isdigit():
        return False
    
    # Extract relevant information from the ID number
    year = int( stdID[0:2])
    month = int( stdID[2:4])
    day = int( stdID[4:6])
    gender_digit = int( stdID[6:7])
    nationality_digit = int( stdID[10:11])
    
    # Determine the gender based on the gender digit
    gender = "Male" if gender_digit < 5 else "Female"
    
    # Determine the nationality based on the nationality digit
    nationality = "South African" if nationality_digit == 0 else "Other"
    
    # Determine the age based on the birthdate
    current_year = int(datetime.datetime.now().strftime("%Y"))
    birth_year = 1900 + year if year < current_year - 2000 else 2000 + year
    age = current_year - birth_year
    
    return age, gender, nationality


def user_id_validation(stdID):
    validation_result = validate_id_number( stdID)
    
    if validation_result:
        return validation_result
    
# #Validate Residential/Physical Address
# def validate_residential_address(address):
#     # Make a request to the Google Maps Geocoding API
#     response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=YOUR_API_KEY')

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
        
#         # Check if the address is valid and has results
#         if data['status'] == 'OK' and len(data['results']) > 0:
#             # Extract relevant information from the API response
#             validated_address = data['results'][0]['formatted_address']
#             latitude = data['results'][0]['geometry']['location']['lat']
#             longitude = data['results'][0]['geometry']['location']['lng']
            
#             return validated_address, latitude, longitude
    
#     # Return None if the address is not valid or there was an error
#     return None, None, None

   #Create a string






#Create a router decorator
@app.route("/")
def index():
   return render_template('index.html')
#Create Radio options form
@app.route('/Student_Type', methods=['GET','POST'])
def Student_Type():
    form = Student_TypeForm() 
    if form.validate_on_submit():
        if form.student_type.data == 'new':
               return redirect(url_for('InfoCapture'))
            #return render_template('InfoCapture.html',form=form)
         
        elif form.student_type.data == 'returning':
              return redirect(url_for('login'))
            #return render_template('login.html',form=form)
    return render_template('Student_Type.html', form=form)
   #Create Information Capture Page
@app.route('/InfoCapture', methods=['GET','POST'])
def InfoCapture():
    form = InfoForm()
    

   #Validate Form

    if form.validate_on_submit(): 
      
       
        # Handle the form submission
        students = Student.query.filter_by(email=form.stdEmailP.data).first()
        if students is None:
             students =Student(student_type=form.student_type.data,user_number = form. user_number.data,stdLName = form.stdLName.data,stdFNames = form.stdFNames.data, stdID = form.stdID.data,address = form.address.data, stdEmailP = form.stdEmailP.data,user_system_email = form.user_system_email.data,stdAge = form.stdAge.data, stdGender = form.stdGender.data,stdNationality = form.stdNationality.data,stdCountry = form.stdCountry.data,date_added = form.date_added.data)
        db.session.add(students)
        db.session.commit()
             
        student_type =form.student_type.data
        user_number = form. user_number.data
        stdLName = form.stdLName.data
        stdFNames = form.stdFNames.data
        stdID = form.stdID.data
        address = form.address.data
        stdEmailP = form.stdEmailP.data
        user_system_email = form.user_system_email.data
        stdAge = form.stdAge.data
        stdGender = form.stdGender.data
        stdNationality = form.stdNationality.data
        stdCountry = form.stdCountry.data
        date_added = form.date_added.data
       
        flash('You have Successfully registered!')
    Information_Capture = Student.query.order_by(Student.date_added)
    # address = form. address.data
    # area = form.area.data
    # address = f"{address}, {area}"
        
    # validated_address, latitude, longitude = validate_residential_address(address)

    # if validated_address:
    #         flash(f"Validated Address: {validated_address}")
    #         flash(f"Latitude: {latitude}")
    #         flash(f"Longitude: {longitude}")
    # else:
    #         flash("Invalid address or unable to validate.")
    return render_template('InfoCapture.html', form=form,Information_Capture=Information_Capture)

   

    # Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Student.query.filter_by(user_number=form.user_number .data).first()
        #user = Student.query.filter_by(user_system_email =form.email.data).first()
		
		flash("Login Succesfull!!")
		return redirect(url_for('dashboard'))
	else:
		flash("Wrong Student email/Usernumber")
            

	return render_template('login.html', form=form)

  
# USER ROUTES
@app.route('/user/<name>/', methods=['GET', 'POST'])
def user_profile(name):
    return render_template('user_profile.html', name=name)






if __name__ == '__main__': 
    app.run(debug=True)