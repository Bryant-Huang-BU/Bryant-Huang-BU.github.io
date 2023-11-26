from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker
import sys
import home
import search
import manager
app = Flask(__name__, template_folder='.')
# login = LoginManager(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post():
    return "recived: {}".format(request.form)


# potentially add flask login using loginform and login_user
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # add login functionality here
        # if login successful, return redirect(url_for('home'))
        # else return render_template('login.html')
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


@app.route('/results')
def results():
    name = request.args.get('nm', '')
    year = request.args.get('year', '')
    return search.search_page(name, year)

@app.route('manager/<id>', methods=['GET'])
def managerInfo():
    params = {'x': id}
    query2 = "SELECT team_name, yearID FROM teams JOIN managers USING(teamID, yearID) JOIN people USING(playerID) WHERE managersID =:x"
    url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="csi3335rocks",
    host="localhost",
    database="QueryQuintet",
    port=3306,)
    print(url_object)
    engine = create_engine(url_object)
    with engine.connect() as conn:
        result = conn.execute(text(query2), params)
        for row in result:
            print(row)
    return result


@app.route('/results', methods=['GET'])
def teamInfo():
    name = request.args.get('nm', '')
    year = request.args.get('year', '')
    params = {'x': name,
              'y': year}
    query1 = "SELECT team_R, teamRank, CONCAT(nameFirst, ' ', nameLast) AS manager_name FROM teams JOIN managers USING(teamID, yearid) JOIN people USING(playerid) WHERE team_name =:x AND managers.yearID =:y"
    url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="csi3335rocks",
    host="localhost",
    database="QueryQuintet",
    port=3306,)
    print(url_object)
    engine = create_engine(url_object)
    with engine.connect() as conn:
        result = conn.execute(text(query1), params)
        for row in result:
            print(row)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
