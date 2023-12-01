from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker
import hashlib
import sys
#from flask_login import login_required, LoginManager, current_user, login_user
import home
import search
import manager
import csi3335F2023 as conf

engineStr = ("mysql+pymysql://" +
             conf.mysql['username'] + ":" +
             conf.mysql['password'] + "@" +
             conf.mysql['location'] + ":3306/" +
             conf.mysql['database'])

app = Flask(__name__, template_folder='.')
# login = LoginManager(app)

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/post', methods=['POST'])
def post():
    return "recived: {}".format(request.form)


# potentially add flask login using loginform and login_user
@login_required
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        engine = create_engine(engineStr)
        Session = sessionmaker(bind=engine)
        session = Session()
        username = request.form['username']
        password = encrypt_string(request.form['password'])

    params = {'x': username, 'y': password}
    print(password)
    query = "SELECT username FROM users WHERE username = :x AND password = :y"
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
        for row in result:
            print(row)
            results.append(row)
    if results:
        #return render_template('', username=username)
        return home.home_page(username)
    else:
        return render_template('login.html')


@app.route('/manager/<id>', methods=['GET'])
def managerpage():
    if request.method == 'GET':
        return manager.manager_page(id)
    else:
        return render_template('login.html')

# after adding login info:
# @app.route('/home/<username>')
# @login_required
@app.route('/home')
def search_page():
    name = request.args.get('nm', '')
    print(name)
    return home.home_page(name)


@app.route('/managerInfo/<id>', methods=['GET'])
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
def teamInfo():
    name = request.args.get('nm', '')
    year = request.args.get('year', '')

    params = {'x': name, 'y': year}
    query = "SELECT team_R, teamRank, CONCAT(nameFirst, ' ', nameLast)AS manager_name, playerID FROM teams JOIN managers USING(teamID, yearid) JOIN people USING(playerid) WHERE team_name =:x AND managers.yearID =:y"
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
        for row in result:
            print(row)
            results.append(row)
    return render_template('results.html', name=name, year=year, results=results)


if __name__ == '__main__':
    app.run(debug=True)
