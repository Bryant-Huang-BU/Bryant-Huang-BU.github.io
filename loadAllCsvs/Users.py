import hashlib

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, Double
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


csv_file = 'Users.csv'

engineStr = ("mysql+pymysql://" +
             conf.mysql['username'] + ":" +
             conf.mysql['password'] + "@" +
             conf.mysql['location'] + ":3306/" +
             conf.mysql['database'])
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

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

