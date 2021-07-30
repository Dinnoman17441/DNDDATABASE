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
        new_username = request.form["username"]
        new_userpassword = generate_password_hash(request.form.get('password'), salt_length = 10)
        new_user = models.User(username = new_username, password = new_userpassword)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template('usercreate.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('useron'):
        return redirect('/')
    if request.method == "POST":
        useron = models.User.query.filter(models.User.username == request.form.get('login_username')).first()
        if useron and check_password_hash(useron.password, request.form.get('login_password')):
            session['useron'] = useron.UserID
            return redirect("/")
        else:
            return render_template('userlogin.html', error = 'username or password incorrect')
    return render_template('userlogin.html')

@app.route('/logout')
def logout():
    try:
        session.pop('useron')
    except:
        return redirect('/login', error = 'not currently logged in')
    return redirect('/')

@app.route('/')
def contents():
    return render_template('contents.html')

@app.route('/spells')
def spells():
    spells = models.Spell.query.all()
    return render_template('spells.html', spells=spells)

@app.route('/items')
def items():
    items = models.Item.query.all()
    return render_template('items.html', items=items)

@app.route('/addspell', methods = ["GET", "POST"])
def addspell():
    schools = models.School.query.all()
    sources = models.Source.query.all()
    if request.method == "POST":
        new_spell_name = request.form["spell_name"]
        new_spell_level = request.form["spell_level"]
        new_spell_duration_amount = request.form["spell_duration"]
        new_spell_duration_unit = request.form["spell_duration_unit"]

        new_spell_duration = new_spell_duration_amount + new_spell_duration_unit

        new_spell_school = request.form["spell_school"]
        new_spell_school_id = models.School.query.filter_by(SchoolName = new_spell_school).first()

        new_spell_source = request.form["spell_source"]
        new_spell_source_id = models.Source.query.filter_by(SourceName = new_spell_source).first()
        
        new_spell = models.Spell(
            SpellName = new_spell_name,
            SpellLevel = new_spell_level,
            Duration = new_spell_duration,
            owner = current_user(),
            school = new_spell_school_id,
            source = new_spell_source_id,
        )

        db.session.add(new_spell)
        db.session.commit()

        return redirect("/")
    return render_template('addspell.html', schools=schools, sources=sources)

@app.route('/additem', methods = ["GET", "POST"])
def additem():
    sources = models.Source.query.all()
    types = models.Type.query.all()
    if request.method == "POST":
        new_item_name = request.form["item_name"]
        new_item_rarity = request.form["item_rarity"]

        new_item_type = request.form["item_type"]
        new_item_type_id = models.Type.query.filter_by(TypeName = new_item_type).first()

        new_item_source = request.form["item_source"]
        new_item_source_id = models.Source.query.filter_by(SourceName = new_item_source).first()
        
        new_item = models.Item(
            ItemName = new_item_name,
            ItemRarity = new_item_rarity,
            owner = current_user(),
            type = new_item_type_id,
            source = new_item_source_id,
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect("/")
    return render_template('additem.html', sources=sources, types=types)

if __name__ == "__main__":
    app.run(debug=True)

# For when git doesn't remember my email (everytime)
# git config --global user.email "17441@burnside.school.nz"