from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Transcription

import const

import os

if not os.path.exists(const.TRANSCRIBED_DATA_PATH):
    os.makedirs(const.TRANSCRIBED_DATA_PATH)


engine = create_engine('sqlite:///%s' % (const.TRANSCRIBED_SPEECH_SQLITE_DB_PATH))
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(bind=engine)



DBSession = sessionmaker(bind=engine)
session = DBSession()

t = Transcription(media_type="test", media_id="4gdfgdf2", time_start=0, time_end=1.51, transcription="test")
session.add(t)
session.commit()