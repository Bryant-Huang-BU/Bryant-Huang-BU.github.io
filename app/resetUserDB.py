from app import app, db
from app.models import Users


def reset():
    with app.app_context():
        try:
            db.reflect()
            db.drop_all()
            db.create_all()
        except:
            db.create_all()
