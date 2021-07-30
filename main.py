from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash, json
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer, String, Boolean
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
import math

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

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
    if request.method == "POST":
        new_spell_name = request.form["spell_name"]
        new_spell_level = request.form["spell_level"]
        new_spell_duration_amount = request.form["spell_duration"]
        new_spell_duration_unit = request.form["spell_duration_unit"]

        new_spell_duration = new_spell_duration_amount + new_spell_duration_unit

        new_spell = models.Spell(
            SpellName = new_spell_name,
            SpellLevel = new_spell_level,
            Duration = new_spell_duration,
            owner=current_user(),
        )

        db.session.add(new_spell)
        db.session.commit()

        return redirect("/")
    return render_template('addspell.html', schools=schools)

if __name__ == "__main__":
    app.run(debug=True)

# For when git doesn't remember my email (everytime)
# git config --global user.email "17441@burnside.school.nz"