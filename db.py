from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, String, Integer, Float, Text

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)

Base = declarative_base()


class BaseAudio(Base):
    __tablename__ = 'base_audio_file'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    pretty_name = Column(String)
    source_url = Column(String)
    segments = relationship('Segment')

    def __init__(self, filename, pretty_name, source_url):
        self.filename = filename
        self.pretty_name = pretty_name
        self.source_url = source_url


class Segment(Base):
    __tablename__ = 'segment'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey('base_audio_file.id'))
    position = Column(Integer)
    transcript = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)

    def __init__(self, base_id, position, transcript, confidence):
        self.base_id = base_id
        self.position = position
        self.transcript = transcript
        self.confidence = confidence

    def __lt__(self, other):
        return self.position < other.position

    def __gt__(self, other):
        return self.position > other.position


Base.metadata.create_all(engine)
db = Session()  # scoped_session(sessionmaker(bind=engine))


def get_base_info(id):
    return db.query(BaseAudio).filter(BaseAudio.id == id).first()


def get_segment(base, position):
    return db.query(Segment).filter(Segment.base_id == base).filter(Segment.position == position).first()
