from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import  InfoForm
from sqlalchemy import create_engine
import pymysql



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
# with app.app_context():
#     db.create_all()
#Set database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Information_Capture.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:M@$ukust2@localhost:3306/Information_Capture'

#  Initialize a Flask App to use for the DATABASE
db.init_app(app)

 # this is needed in order for database session calls (e.g. db.session.commit)
with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
     
#Secret Key
app.config['SECRET_KEY'] = "Sifiso"

#Create Model
class students(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   stdLName =db.Column(db.String(200), nullable=False)
   stdFNames =db.Column(db.String(200), nullable=False)
   stdEmailP =db.Column(db.String(200), nullable=False, unique=True)
   stdID =db.Column(db.String(200), nullable=False)
   stdAddrs =db.Column(db.String(200), nullable=False)
   date_added =db.Column(db.DateTime, default=datetime.now)

   #Create a string
   def __repr__(self):
      return '<name %r>' % self.name





#Create a router decorator
@app.route("/")


def index():
    return render_template("index.html")

# USER ROUTES
@app.route('/user/<name>/', methods=['GET', 'POST'])
def user_profile(name):
    return render_template('user_profile.html', name=name)

#Create Information Capture Page
@app.route('/InfoCapture', methods=['GET','POST'])
def InfoCapture():
   
    stdLName  = None
    stdFNames = None
    stdEmailP = None
    stdID = None
    stdAddrs = None
    form = InfoForm()

   #Validate Form

    if form.validate_on_submit(): 
        user = students.query.filter_by(stdEmailP=form.stdEmailP.data).first()

        user = students(stdLName=form.stdLName.data, stdFNames=form.stdFNames.data, stdEmailP=form.stdEmailP.data, stdID=form.stdID.data,
                         stdAddrs=form.stdAddrs.data)
            
        stdLName = form.stdLName.data
        form.stdLName.data = ''
        form.stdFNames.data = ''
        form.stdEmailP.data = ''
        form.stdID.data = ''
        form.stdAddrs.data = ''
        flash('User Added Successfully!')
    our_users = students.query.order_by(students.date_added)
    return render_template('InfoCapture.html', form=form, stdLName = stdLName, our_users=our_users)

   # if form.validate_on_submit():
   #     user = students.query.filter_by(stdEmailP=form.stdEmailP.data).first()
   #    stdLName = form.stdLName.data
   #    form.name.data = ''
   #    flash("Data Saved Successfully")
   # return render_template("InfoCapture.html",
   #   stdLName = stdLName,
   #   stdFNames = stdFNames,

   #    form = InfoForm())



if __name__ == '__main__': 
    app.run(debug=True)