#Imports important stuff
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash, json
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer, String, Boolean
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
import math

#Creates flask app using config from config.py
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

#Imports models from models.py
from main import db
import models

#Login Functions
def current_user():
    if session.get('useron'):
        return models.User.query.get(session['useron'])
    else:
        return False

@app.context_processor
def add_current_user():
    if session.get('useron'):
        return dict(current_user = models.User.query.get(session['useron']))
    return dict(current_user = None)

@app.route('/createuser', methods = ['GET', 'POST'])
def createuser():
    if request.method == "POST":
        new_username = request.form["username"] #Collects username from form
        new_userpassword = generate_password_hash(request.form.get('password'), salt_length = 10) #Collects password from form and encrypts it
        new_user = models.User(username = new_username, password = new_userpassword) #Puts info into a tuple
        db.session.add(new_user) #Adds info to table

        db.session.commit() #Commits addition
        return redirect("/") #Redirects user to homepage
    return render_template('usercreate.html') #This page is loaded when "/createuser" is called

@app.route('/login', methods = ['GET', 'POST'])
def login():
    #If user is currently logged in, instantly redirects them to home
    #The login button is not displayed when logged in anyway, but the user can type "/login" into the address bar
    if session.get('useron'):
        return redirect('/')
    if request.method == "POST":
        useron = models.User.query.filter(models.User.username == request.form.get('login_username')).first()

        #Checks if username and password are correct
        if useron and check_password_hash(useron.password, request.form.get('login_password')):
            session['useron'] = useron.UserID
            return redirect("/")
        else:
            #Returns user to the start of the form with an error message if username or password dont match
            return render_template('userlogin.html', error = 'Username or Password Incorrect')
    return render_template('userlogin.html')

@app.route('/logout')
def logout():
    try:
        #Removes the user from the session, logging them out
        session.pop('useron')
    except:
        #If the user is not logged in, sends them to the login page
        return redirect('/login')
    return redirect('/')

#Simple function that redirects users from the default '/' route to the '/spells' route
@app.route('/')
def reroute():
    return redirect('/spells')

@app.route('/spells')
def contents():
    return render_template('contents.html')

@app.route('/spells/<int:SourceID>')
def spells(SourceID):
    spells = models.Spell.query.filter_by(SourceID=SourceID).all()
    SID = SourceID
    return render_template('spells.html', spells=spells, source=SID)

@app.route('/spells/<int:SourceID>/<int:SchoolID>')
def spellssortschool(SourceID, SchoolID):
    spells = models.Spell.query.filter_by(SourceID=SourceID, SchoolID=SchoolID).all()
    SID = SourceID
    return render_template('spells.html', spells=spells, source=SID)

@app.route('/addspell', methods = ["GET", "POST"])
def addspell():
    schools = models.School.query.all()
    sources = models.Source.query.all()
    if request.method == "POST":
        #Collects spell info from form
        new_spell_name = request.form["spell_name"]
        new_spell_level = request.form["spell_level"]
        new_spell_duration_amount = request.form["spell_duration"]
        new_spell_duration_unit = request.form["spell_duration_unit"]
        new_spell_concentration = request.form["spell_concentration"]

        new_v = request.form["v_component"]
        new_s = request.form["s_component"]
        new_m = request.form["m_component"]

        if new_spell_duration_unit == "Instantaneous":
            new_spell_duration = new_spell_duration_unit
        else:
            new_spell_duration = new_spell_duration_amount + " " + new_spell_duration_unit

        new_spell_school = request.form["spell_school"]
        new_spell_school_id = models.School.query.filter_by(SchoolName = new_spell_school).first()

        new_spell_source = request.form["spell_source"]
        new_spell_source_id = models.Source.query.filter_by(SourceName = new_spell_source).first()
        
        new_spell_description = request.form["spell_desc"]

        new_spell = models.Spell(
            SpellName = new_spell_name,
            SpellLevel = new_spell_level,
            Duration = new_spell_duration,
            Concentration = new_spell_concentration,
            owner = current_user(),
            school = new_spell_school_id,
            source = new_spell_source_id,
            Description = new_spell_description,
            V = new_v,
            S = new_s,
            M = new_m,
        )

        db.session.add(new_spell)
        db.session.commit()

        return redirect("/spells")
    return render_template('addspell.html', schools=schools, sources=sources)

@app.route('/viewspell/<int:SpellID>', methods = ["GET", "POST"])
def viewspell(SpellID):
    if request.method == "GET":
        spells = models.Spell.query.filter_by(SpellID = SpellID).all()
    return render_template('viewspell.html', spells=spells)

@app.route('/deletespell/<int:SpellID>', methods = ["GET", "POST"])
def deletespell(SpellID):
    if request.method == "GET":
        models.Spell.query.filter_by(SpellID = SpellID).delete()
        db.session.commit()
    return redirect("/spells")

if __name__ == "__main__":
    app.run(debug=True)



# Copy and paste into powershell terminal because school computers dont remember github login
'''
git config --global user.email "17441@burnside.school.nz"
'''