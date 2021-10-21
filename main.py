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
        if 4 > len(request.form.get('username')) > 16:
        #If the length of the username is less than 4 characters or more than 16 characters: 
            return render_template('usercreate.html', error='Username must be between 4 and 16 characters in length')
            #The user will fail to be created and will be returned with an error telling them why

        elif models.User.query.filter(models.User.username == request.form.get('username')).first():
        #Checks if the new username already exists, if so:
            return render_template('usercreate.html', error = 'Username already in use')
            #The user will fail to be created and will be returned with an error telling them why

        elif len(request.form.get('password')) < 7:
        #If the length of the password is less than 7 characters:
            return render_template('usercreate.html', error = 'Password must be a minimum of 7 characters') 
            #The user will fail to be created and will be returned with an error telling them why

        else:
            new_username = request.form["username"] #Collects username from form and puts it into variable
            new_userpassword = generate_password_hash(request.form.get('password'), salt_length = 10) #Collects password from form, encrypts it, and puts it into variable
            new_user = models.User(username = new_username, password = new_userpassword) #Puts info into a list 
            db.session.add(new_user) #Adds info to table
            db.session.commit() #Commits addition

            return render_template("userlogin.html", new_user=new_user) #Redirects user to login page with their username already filled in
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
            return render_template('userlogin.html', error = 'Username or Password Incorrect', new_user="")
    return render_template('userlogin.html', new_user="")

@app.route('/logout')
def logout():
    try:
        #Removes the user from the session, logging them out
        session.pop('useron')
    except:
        #If the user is not logged in, sends them to the login page
        return render_template('userlogin.html', error='Not currently logged in', new_user="")
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
    errorcheck = False
    users = models.User.query.filter_by(username = 'admin').first
    if session.get('useron'):
        if request.method == "POST":
            #Collects spell info from form
            form_name = request.form["spell_name"]
            form_level = request.form["spell_level"]

            ##Casting Time
            form_castingtime = request.form["casting_time"]
            form_castingtimeunit = request.form["casting_time_unit"]

            ctime_string = form_castingtime + " " + form_castingtimeunit

            ##Range
            form_rangetype = request.form["range_type"]
            if form_rangetype == "Ranged":
                form_rangenumber = request.form["range_number_value"]
                
            else:
                form_rangenumber = -1
                range_string = form_rangetype

            ##Duration
            form_durationtype = request.form["duration_type"]
            int_durationtypes = ['Concentration', 'Special', 'Time']
            if form_durationtype in int_durationtypes:
                form_durationnumber = request.form["spell_duration"]
                form_durationunit = request.form["duration_time_unit"]
            else:
                form_durationnumber = -1
                form_durationunit = "NULL"

            fd_string = str(form_durationnumber)

            if form_durationnumber == -1:
                duration_string = form_durationtype
            else:
                duration_string = fd_string + " " + form_durationunit

            if form_durationtype == "Concentration":
                spl_concentration = 1
            else:
                spl_concentration = 0

            ##Components
            form_vcomp = request.form["v_component"]
            form_scomp = request.form["s_component"]
            form_mcomp = request.form["m_component"]

            if form_mcomp == 1:
                form_materials = request.form["materials"]
            else:
                form_materials = "NULL"

            if form_mcomp == 1 and form_materials == "":
                errorcheck = True
                error = "Please state material components"

            ##Description
            form_desc = request.form["spell_desc"]

            ##Ritual
            form_ritual = request.form["ritual"]

            ##Source and School
            form_source = request.form["spell_source"]
            source_id = models.Source.query.filter_by(SourceName = form_source).first()

            form_school = request.form["spell_school"]
            school_id = models.School.query.filter_by(SchoolName = form_school).first()

            new_spell = models.Spell(
                SpellName = form_name,
                SpellLevel = form_level,
                CastingTime = ctime_string,
                Range = new_spell_range,
                Duration = duration_string,
                Concentration = spl_concentration,
                owner = current_user(),
                school = school_id,
                source = source_id,
                Description = form_desc,
                V = form_vcomp,
                S = form_scomp,
                M = form_mcomp,
                Materials = form_materials,
                Ritual = form_ritual,
            )
            if errorcheck = False:
                db.session.add(new_spell)
                db.session.commit()
            else:
                #Flash error message

            return redirect("/spells")
    else:
        return render_template('userlogin.html', error='Not currently logged in', new_user="")
        #If the user is not logged in, sends them to the login page. This will only happen if they manually type /addspell
    return render_template('addspell.html', schools=schools, sources=sources, users=users)

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