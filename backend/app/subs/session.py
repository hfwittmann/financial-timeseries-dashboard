import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from environs import Env

env = Env()


def get_url():

    # settings.py
    MYUSER = env('MYUSER')
    MYPASSWORD = env('MYPASSWORD')
    HOST = env('HOST')
    DATABASE = env('DATABASE')
    PORT = env('PORT')

    sqlalchemy_url = f'postgresql://{MYUSER}:{MYPASSWORD}@{HOST}:{PORT}/{DATABASE}'

    return sqlalchemy_url


def getEngine():
    sqlalchemy_url = get_url()
    engine = create_engine(sqlalchemy_url,
                           echo=False,
                           executemany_mode='batch')

    return engine


def getSession():

    engine = getEngine()

    Session = sessionmaker(bind=engine)
    return Session


def getMetaData():
    engine = getEngine()
    metadata = MetaData(bind=engine)
    metadata.reflect()
    return metadata