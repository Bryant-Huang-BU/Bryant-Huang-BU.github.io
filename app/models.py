from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    numberSearches = db.Column(db.Integer)
    managerViews = db.Column(db.Integer)
    logins = db.Column(db.Integer)
    isAdmin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_admin(self):
        return self.isAdmin

    def inc_num_queries(self):
        if self.numberSearches is None:
            self.numberSearches = 0
        self.numberSearches += 1

    def get_username(self):
        return self.username

    def inc_num_searches(self):
        if self.numberSearches is None:
            self.numberSearches = 0
        self.numberSearches += 1
        db.session.commit()

    def inc_num_man_views(self):
        if self.managerViews is None:
            self.managerViews = 0
        self.managerViews += 1
        db.session.commit()

    def inc_logins(self):
        if self.logins is None:
            self.logins = 0
        self.logins += 1
        db.session.commit()

    def get_username(self):
        return self.username

    def get_is_admin(self):
        return self.isAdmin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
