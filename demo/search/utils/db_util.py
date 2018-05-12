import os
import sys

current_dir_path = os.path.dirname(os.path.realpath(__file__))
search_dir_path = os.path.join(current_dir_path, os.pardir)
sys.path.insert(0, search_dir_path)

import const

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Transcription

engine = None

def init_db():
    global engine

    if engine != None:
        return

    if not os.path.exists(const.TRANSCRIBED_DATA_PATH):
        os.makedirs(const.TRANSCRIBED_DATA_PATH)
    engine = create_engine('sqlite:///%s' % (const.TRANSCRIBED_SPEECH_SQLITE_DB_PATH))         
    Base.metadata.create_all(bind=engine)

def get_session():
    global engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def add_item(t):
    db_session = get_session()

    db_session.add(t)
    db_session.commit()

def get_item_by_id(id):
    db_session = get_session()

    t = db_session.query(Transcription).filter(Transcription.id == id).one()
    return t

def get_all_items():
    db_session = get_session()
    return db_session.query(Transcription).all()




    