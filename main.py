
from flask import Flask, render_template, redirect,request
from flask.globals import session
from flask.helpers import flash
from forms import SignUpForm, SignInForm, AddTaskForm, AddProjectForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app= Flask(__name__)
app.config['SECRET_KEY'] = 'NGUYEN  HOANG STYLE SHOP FASHION FREEDOM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signUp', methods=['GET', 'POST'])
def SignUp():
    form = SignUpForm()
    if form.validate_on_submit():
        print("validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if(db.session.query(models.User).filter_by(email =_email).count() == 0 ):
            user = models.User(first_name = _fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user = user)
        else:
            flash('Email {} is already exsits!'.format(_email))
            return render_template('signup.html', form = form)
        
    print("Not validate on submit")
    return render_template('signup.html', form = form)  

@app.route('/signIn', methods=['GET', 'POST'])
def SignIn():
    form = SignInForm()
    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email =_email).first()
        if(user is None):
            flash('Wrong email address or password!')
        else:
            if(user.check_password(_password)):
                session['user'] = user.user_id
                # return render_template('userhome.html')
                return redirect('/projectHome')
            else:
                flash('Wrong email address or password!')

    return render_template('signin.html', form = form)  

@app.route('/logOut')
def logout():
    session.pop('user', None)
    return redirect('/signIn')

@app.route('/projectHome', methods=['GET', 'POST']) 
def project_Home():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        project = db.session.query(models.Project).all()
        return render_template('home-project.html', user = user, project = project)
    else:
        return redirect('/')

@app.route('/addProject', methods=['GET', 'POST'])
def add_Project():
    form = AddProjectForm()

    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        if form.validate_on_submit():
            _name = form.inputProjectName.data
            _description = form.inputDescription.data
            _deadline = form.inputDealine.data

            
            _project_id = request.form['hiddenProjectId']

            if(_project_id == "0"):
                project = models.Project(project_name = _name, description = _description, user = user, project_deadline =_deadline, status_id = '1')
                db.session.add(project)

            else:
                project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
                project.project_name = _name
                project.description = _description
                project.project_deadline = _deadline
            db.session.commit()
            return redirect('/projectHome')
        return render_template('addproject.html',form = form, user = user)
   
    return redirect('/')

@app.route('/editProject', methods=['GET', 'POST'])
def edit_Project():
    form = AddProjectForm()
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
            form.inputProjectName.default = project.project_name
            form.inputDescription.default = project.description
            form.inputDealine.default = project.project_deadline
            form.process()
            return render_template('addproject.html',form = form, user = user, project = project)
    return redirect('/')

@app.route('/removeProject', methods=['GET', 'POST'])
def remove_Project():
    _user_id = session.get('user')
    if _user_id:
        _project_id = request.form['hiddenProjectId']
        if _project_id:
            project = db.session.query(models.Project).filter_by(project_id = _project_id).first()
            db.session.delete(project)
            db.session.commit()
        return redirect('/projectHome')

    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)