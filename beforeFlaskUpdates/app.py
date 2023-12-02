from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker
import hashlib
#from flask_login import login_required, LoginManager, current_user, login_user
import home
import manager
import csi3335F2023 as conf
from forms import RegistrationForm
from loadAllCsvs.Users import Users

engineStr = ("mysql+pymysql://" +
             conf.mysql['username'] + ":" +
             conf.mysql['password'] + "@" +
             conf.mysql['location'] + ":3306/" +
             conf.mysql['database'])

app = Flask(__name__)
# login = LoginManager(app)

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

@app.route('/', methods=['GET'])
def index():
    return render_template('loginPrevious.html')


@app.route('/post', methods=['POST'])
def post():
    return "recived: {}".format(request.form)


# potentially add flask login using loginform and login_user
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        engine = create_engine(engineStr)
        Session = sessionmaker(bind=engine)
        session = Session()
        username = request.form['username']
        password = encrypt_string(request.form['password'])

    results = Users.check_password(Users, username, password)
    if results:
        #return render_template('', username=username)
        return home.home_page(username)
    else:
        return render_template('loginPrevious.html')


@app.route('/manager/<id>', methods=['GET'])
def managerpage():
    if request.method == 'GET':
        return manager.manager_page(id)
    else:
        return render_template('loginPrevious.html')

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)
