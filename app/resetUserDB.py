from app import app, db
from app.models import Users


def reset():
    with app.app_context():
        try:
            print("Trying to drop table if it exists")
            Users.__table__.drop(db.engine)
            print("Table dropped")
            db.create_all()
            print("Create correct table")
        except:
            print("Creating new table")
            db.create_all()
