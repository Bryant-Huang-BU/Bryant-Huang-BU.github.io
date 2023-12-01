from sqlalchemy import URL
import csi3335F2023 as conf


class Config(object):
    SQLALCHEMY_DATABASE_URI = URL.create(
        "mysql+pymysql",
        username=conf.mysql['username'],
        password=conf.mysql['password'],
        host=conf.mysql['location'],
        database=conf.mysql['database'],
        port=3306,)
