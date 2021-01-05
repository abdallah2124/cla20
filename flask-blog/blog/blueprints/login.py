from flask import Blueprint, render_template,request ,redirect,session
from blog.db import get_db
import sqlite3
from wtforms import  StringField, SubmitField, validators,PasswordField
from flask_wtf import FlaskForm


# define our blueprint
login_bp = Blueprint('login', __name__)

class LoginForm(FlaskForm):
    first_name = StringField('What is your first name :', [validators.InputRequired()])
    last_name = StringField('What is your last name :', [validators.InputRequired()])

    password = PasswordField('Enter your password ')

    submit = SubmitField('Submit')

@login_bp.route('/login', methods =['POST','GET'])
def login():
    form=LoginForm()
    if request.method == 'GET':
        # render add user blueprint
        return render_template('login/login.html',form=form)
    else:
        
        first_name =form.first_name.data 
        last_name =form.last_name.data
        password =form.password.data
    # if request.method == "GET":
    #     # render the login template
    #     return render_template('login/login.html')
    # else:
    #     # read values from the login form
    #     username= request.form['username']
    #     password = request.form['password']

        # get the DB connection
        db = get_db()
        
        # insert user into db
        try:
            # get user by username
            user= db.execute('SELECT * FROM user WHERE first_name LIKE ?',(first_name,)).fetchone()
            # check if username exists
            if user  != None:
                # check if credentials are valid
                if user['first_name'] == first_name and user['password'] == password and user['last_name'] == last_name:
                    # store the user ID in the session  
                    session['uid']= user['id']  
                    session['first_name'] = user['first_name']
                    session['last_name'] = user['last_name']
                    return redirect("/posts")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

@login_bp.route('/session')
def show_session():
    return dict(session)

@login_bp.route('/logout')
def logout():
    # pop 'uid' from session
    session.clear()

    # redirect to index
    return redirect("/")