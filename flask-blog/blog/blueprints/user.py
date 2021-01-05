import sqlite3
from flask import Blueprint, render_template, request, redirect
from blog.db import get_db
from wtforms import StringField, SubmitField, validators,PasswordField
from flask_wtf import FlaskForm

# define our blueprint
user_bp = Blueprint('user', __name__)

class UserForm(FlaskForm):
    first_name = StringField('What is your first name :', [validators.InputRequired()])
    last_name = StringField('What is your last name :', [validators.InputRequired()])
    password = PasswordField('Enter your password ')

    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    first_name = StringField('Enter new first name :', [validators.InputRequired()])
    last_name = StringField('Enter new last name :', [validators.InputRequired()])
    submit = SubmitField('Edit')






@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    form=UserForm()
    if request.method == 'GET':
        # render add user blueprint
        return render_template('user/index.html',form=form)
    else:
        
        first_name =form.first_name.data 
        last_name =form.last_name.data 
        password =form.password.data



        # get the DB connection
        db = get_db()

        # insert user into DB
        try:
            # execute our insert SQL statement
            db.execute("INSERT INTO user (first_name,last_name,password) VALUES (?,?,?);",(first_name,last_name,password))

            # write changes to DB
            db.commit()
            
            return redirect("/users")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

@user_bp.route('/users')
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)

@user_bp.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form=UserForm()
    eform=EditForm()
    if request.method == 'GET':
        # render add user blueprint
        return render_template('user/edit.html',formn=eform,formo=form)
    else:

        n_f_n=eform.first_name.data
        n_l_n=eform.last_name.data
        o_f_n=form.first_name.data
        o_l_n=form.last_name.data
        db = get_db()
         # get all users from the db
        try:
            # execute our insert SQL statement
            # db.execute("UPDATE user SET first_name=? ,last_name=?  WHERE first_name=? ",(n_f_n,n_l_n,o_f_n))
            # sql = "UPDATE user SET first_name = %s WHERE last_name = %s"
            # val = ("hiiii","blus")
            db.execute("UPDATE user SET first_name = 'hiii' WHERE last_name = 'blus'")


            # write changes to DB
            db.commit()
            
            return redirect("/users")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")


    

