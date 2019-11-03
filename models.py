from api import get_transcript
from database import Base, db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey


class BaseAudio(Base):
    __tablename__ = 'base_audio_file'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    pretty_name = Column(String)
    source_url = Column(String)
    segment_length = Column(Integer)
    segments = relationship('Segment')

    def __init__(self, filename, pretty_name, source_url, segment_length):
        self.filename = filename
        self.pretty_name = pretty_name
        self.source_url = source_url
        self.segment_length = segment_length


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


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    # For trials and stuff, allow a certain amount free
    seconds_available = Column(Integer, default=0)
    # Setup roles later...
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


def get_base_info(id):
    """:rtype: BaseAudio"""
    return db.query(BaseAudio).filter(BaseAudio.id == id).first()


# TODO: Implement filter/sort option
def get_downloads(filter=None, sort=None):
    query = db.query(BaseAudio).order_by(BaseAudio.pretty_name)
    if filter:
        pass
    if sort:
        pass
    return query.all()


def get_segment(obj, file_id, position, update=False):
    full_filename = get_full_filename(obj, position)
    segment = db.query(Segment).filter(Segment.base_id == file_id, Segment.position == position).first()

    if segment.transcript is None and update:
        transcript, confidence = get_transcript('./static/{}'.format(full_filename))
        segment.transcript = transcript
        segment.confidence = confidence
        db.commit()

    return segment


def get_full_filename(obj, position):
    dirname = '{}/{}'.format('mp3', obj.id)
    # TODO: Hardcoded length
    # position -1 because ffmpeg starts splitting on 0000
    filename = obj.filename.replace('.mp3', '.{:04}'.format(int(position) - 1))
    return '{}/{}.mp3'.format(dirname, '{}_{}'.format(obj.segment_length, filename))
