import hashlib

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, Double, URL, text
import csi3335F2023 as conf
import pandas as pd
class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    ID = Column(Integer, primary_key=True)
    username = Column(String(512))
    password = Column(String(512))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = encrypt_string(password)

    def check_password(self, username, password):
        params = {'x': username, 'y': password}
        print(password)
        query = "SELECT username FROM users WHERE username = :x AND password = :y"
        url_object = URL.create(
            "mysql+pymysql",
            username=conf.mysql['username'],
            password=conf.mysql['password'],
            host=conf.mysql['location'],
            database=conf.mysql['database'],
            port=3306, )
        engine = create_engine(url_object)
        results = []
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            for row in result:
                print(row)
                results.append(row)
        return results


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature



def loadFromCSV():
    csv_file = 'Users.csv'
    engineStr = ("mysql+pymysql://" +
                 conf.mysql['username'] + ":" +
                 conf.mysql['password'] + "@" +
                 conf.mysql['location'] + ":3306/" +
                 conf.mysql['database'])

    # Creating the Database Engine and Tables
    engine = create_engine(engineStr)
    Base.metadata.create_all(engine)

    # Creating a Session to Interact with the Database
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(csv_file)
    allUsers = session.query(Users).all()

    for index, row in df.iterrows():
        foundMatch = False
        # Replace NaN values with None
        row = row.where(pd.notna(row), None)

        # Create a new object of the class with data from the row
        new_row = Users(**row.to_dict())
        new_row.password = encrypt_string(new_row.password)

        # Remove the previous instance of the player
        for person in allUsers:
            if new_row.ID == person.ID:
                foundMatch = True
                session.delete(person)
                break

        # Add the new object to the session
        session.add(new_row)
        if not foundMatch:
            if new_row.username is not None and new_row.password is not None:
                print(new_row.username + " " + new_row.password)

    session.commit()

