from sqlalchemy import Column, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    media_id = Column(String(50), nullable=False)
    media_type = Column(String(50), nullable=False)
    time_start = Column(Float(), nullable=False)
    time_end = Column(Float(), nullable=False)
    transcription = Column(Text(), nullable=False)

    def __repr__(self):
        return '<Transcription %s %s %.2f %.f>' % (self.media_type, self.media_id, self.time_start, self.time_end)


