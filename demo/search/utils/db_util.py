import os
import sys
sys.path.insert(0,os.getcwd()) 

import const

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Transcription

db_session = None

def init_db():
    global db_session

    if db_session != None:
        return

    if not os.path.exists(const.TRANSCRIBED_DATA_PATH):
        os.makedirs(const.TRANSCRIBED_DATA_PATH)
    engine = create_engine('sqlite:///%s' % (const.TRANSCRIBED_SPEECH_SQLITE_DB_PATH))         
    Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    db_session = session

def add_item(t):
    global db_session

    db_session.add(t)
    db_session.commit()

def get_item_by_id(id):
    global db_session

    t = db_session.query(Transcription).filter(Transcription.id == id).one()
    return t

def get_all_items():
    global db_session
    return db_session.query(Transcription).all()