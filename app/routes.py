from flask import render_template, flash, redirect, url_for
from sqlalchemy import URL, create_engine, text

from app import app, db
import pymysql
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Users
from flask import request
from urllib.parse import urlparse
from app import csi3335F2023 as conf


# create database if it does not exist
@app.before_request
def before_login():
    try:
        print('before login request')
        db.session.query(Users).all()
    except:
        db.create_all()
        user = Users()
        user.username = 'admin'
        user.set_password('admin')
        user.isAdmin = True
        db.session.add(user)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('search_page')
        user.inc_logins()
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('search_page'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route('/index')
@login_required
def search_page():
    return render_template('index.html', title='Home')


@app.route('/managerInfo/<id>', methods=['GET'])
@login_required
def managerInfo(id):
    params = {'x': id}
    name_query = "SELECT CONCAT(nameFirst, ' ', nameLast)AS manager_name FROM people WHERE playerID = :x"
    query = "SELECT teams.team_name, managers.yearID FROM managers JOIN teams ON managers.teamID = teams.teamID AND managers.yearID = teams.yearID WHERE managers.playerID = :x ORDER BY managers.yearID DESC"
    url_object = URL.create(
        "mysql+pymysql",
        username=conf.mysql['username'],
        password=conf.mysql['password'],
        host=conf.mysql['location'],
        database=conf.mysql['database'],
        port=3306,)
    engine = create_engine(url_object)

    manager_name = ''
    with engine.connect() as conn:
        result = conn.execute(text(name_query), params)
        name_row = result.fetchone()
        if name_row:
            manager_name = name_row.manager_name

    results = []
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        for row in result:
            results.append(row)
            print(row)

    return render_template('manager.html', manager_name=manager_name, results=results)


@app.route('/results', methods=['GET'])
@login_required
def teamInfo():
    name = request.args.get('nm', '')
    year = request.args.get('year', '')
    user = Users.query.filter_by(username=current_user.get_username()).first()
    user.inc_num_man_views()

    params = {'x': name, 'y': year}
    query = "SELECT team_projW, team_projL, team_R, teamRank, CONCAT(nameFirst, ' ', nameLast)AS manager_name, playerID FROM teams JOIN managers USING(teamID, yearid) JOIN people USING(playerid) WHERE team_name =:x AND managers.yearID =:y"
    url_object = URL.create(
        "mysql+pymysql",
        username=conf.mysql['username'],
        password=conf.mysql['password'],
        host=conf.mysql['location'],
        database=conf.mysql['database'],
        port=3306,)
    engine = create_engine(url_object)
    results = []
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        if result is None:
            flash('Invalid team name or year')
            return redirect(url_for('search_page'))
        user_id = current_user.get_id()
        user = Users.query.filter_by(id=user_id).first()
        user.inc_num_searches()
        for row in result:
            results.append(row)
    return render_template('results.html', name=name, year=year, results=results)

@app.route('/user_counts', methods=['GET'])
@login_required
def user_counts():
    query = "SELECT username, numberSearches, managerViews, logins FROM users"
    url_object = URL.create(
        "mysql+pymysql",
        username=conf.mysql['username'],
        password=conf.mysql['password'],
        host=conf.mysql['location'],
        database=conf.mysql['database'],
        port=3306,)
    engine = create_engine(url_object)
    results = []
    with engine.connect() as conn:
        user_id = current_user.get_id()
        user = Users.query.filter_by(id=user_id).first()

        if user.get_admin is None:
            flash('You are not an admin')
            return redirect(url_for('search_page'))
        result = conn.execute(text(query))
        for row in result:
            results.append(row)
            print(row)
    return render_template('user_info.html', results=results)
