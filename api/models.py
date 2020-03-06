import logging
import io
import os
import re
from subprocess import Popen, PIPE
from urllib.parse import urlparse

import requests

from constants import DEFAULT_SEGMENT_LENGTH, OUTPUT_DIR
from database import Base, db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey
# Google API stuff
import google.api_core.exceptions
from google.cloud import speech


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BaseAudio(Base):
    __tablename__ = 'base_audio_file'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    pretty_name = Column(String)
    source_url = Column(String)
    language = Column(String(8), nullable=True)
    hash = Column(String, nullable=True)
    # Allow a user to protect a file if they want to
    protected = Column(Boolean, default=False)
    extension = Column(String(6), default='mp3')
    segments = relationship('Segment')

    def __init__(self, source_url, pretty_name=None, language=None):
        self.pretty_name = pretty_name
        self.source_url = source_url
        self.language = language

    @staticmethod
    def get(id=None, source_url=None):
        if id:
            return db.query(BaseAudio).filter(BaseAudio.id == id).first()
        elif source_url:
            return db.query(BaseAudio).filter(BaseAudio.source_url == source_url).first()
        return None

    @staticmethod
    def exists(obj):
        return obj is not None

    def to_json(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'language': self.language or 'unknown',
            'path': self.get_download_folder(),
            'pretty_name': self.pretty_name,
            'segments': [s.to_json() for s in self.segments]
        }

    def get_download_folder(self):
        return f'{OUTPUT_DIR}/{self.id}'

    def get_download_path(self):
        return f'{self.get_download_folder()}/{self.filename}'

    def save_file(self):
        url = self.source_url
        filename = urlparse(url).path.split('/')[-1]
        self.filename = filename
        if not self.pretty_name:
            self.pretty_name = filename

        logger.info(f'Downloading file from {url}')
        r = requests.get(url)

        output_dir_path = self.get_download_folder()

        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)
            with open(self.get_download_path(), 'wb') as f:
                f.write(r.content)

        # raise OSError('The file, or a file with the same name, has already been downloaded')

    def split_file(self, seconds=DEFAULT_SEGMENT_LENGTH):

        if not seconds:
            seconds = DEFAULT_SEGMENT_LENGTH

        # logger.info('Splitting file at %s', path)
        # split_path = os.path.split(path)
        # output_path = "/".join([split_path[0], f'{seconds}_{split_path[1].rstrip(self.extension)}%04d.mp3'])
        path = self.get_download_folder()
        output_dir = os.path.join(path, str(seconds))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:  # The base has already been split
            return
        ffmpeg_path = os.path.join(output_dir, f'%04d_{self.filename}')

        # TODO: Choice between different tools?
        args = [
            'ffmpeg', '-i', self.get_download_path(),
            '-f', 'segment',
            '-segment_time', str(seconds),
            '-c', 'copy', ffmpeg_path
        ]

        self.ffmpeg(args)

        logger.debug(f'listdir: {output_dir}')
        segments = [s for s in sorted(os.listdir(output_dir))]
        logger.debug('segments: %r' % segments)
        for idx, f in enumerate(segments):
            logger.debug(f'{idx} {f}')
            logger.debug(f'SAVING {idx}, {f}')
            s = Segment(base_id=self.id, position=idx + 1, length=seconds, language=self.language)
            db.add(s)
        db.commit()

    def grab_file(self, start, length):
        meta = SegmentMeta(base_id=self.id, segment_length=length, grab=True)
        input = self.get_download_path()
        output_path = f'{input.rstrip(self.extension)}_grab_{start}_{start+length}.{self.extension}'
        cmd = ['ffmpeg', '-ss', start, '-i', input, '-t', str(length), '-c', 'copy', output_path]
        self.ffmpeg(cmd)
        segment = Segment(meta.id, position=None)

    def ffmpeg(self, args):
        proc = Popen(args, stderr=PIPE, stdout=PIPE)
        output, error = proc.communicate()
        logger.debug(f'Output:{str(output)}')

        if proc.returncode != 0:
            logger.exception(str(error))
            raise Exception('An error occurred splitting the file')

        return output, error


class Segment(Base):
    __tablename__ = 'segment'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey('base_audio_file.id'))
    base = relationship('BaseAudio')
    position = Column(Integer, nullable=True)
    length = Column(Integer, nullable=False)
    # If language is null, then get from base_audio
    # If it is not there, then will get less accurate results
    language = Column(String(8), nullable=True)
    transcript = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    protected = Column(Boolean, default=False)
    # If we want to get a single part of the file and save it
    grab = Column(Boolean, default=False)
    # TODO: start position and end position
    translations = relationship('Translation', back_populates='segment')

    @staticmethod
    def get(id):
        return db.query(Segment).filter(Segment.id == id).first()

    def to_json(self):
        return {
            'position': self.position,
            'length': self.length,
            'transcript': self.transcript,
            'language': self.language,
            'confidence': self.confidence,
            'protected': self.protected,
        }

    def __lt__(self, other):
        return self.position < other.position

    def __gt__(self, other):
        return self.position > other.position

    @property
    def filepath(self):
        dir = os.path.join(self.base.get_download_folder(), str(self.length))
        prefix = '{0:04d}'.format(self.position - 1)
        return os.path.join(dir, f'{prefix}_{self.base.filename}')

    def retrieve_transcript(self, **kwargs):

        encoding = kwargs.get('encoding') or speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
        sample_rate = kwargs.get('encoding') or 44100
        language_code = kwargs.get('language_code') or self.language
        automatic_punctuation = kwargs.get('automatic_punctuation') or True

        client = speech.SpeechClient()

        with io.open(self.filepath, 'rb') as f:
            content = f.read()

        audio = speech.types.RecognitionAudio(content=content)
        config = speech.types.RecognitionConfig(encoding=encoding, enable_automatic_punctuation=automatic_punctuation,
                                                sample_rate_hertz=sample_rate, language_code=language_code)
        result = client.recognize(config, audio)

        transcript = ''
        confidence = 0
        for r in result.results:
            confidence = r.alternatives[0].confidence
            transcript += r.alternatives[0].transcript

        self.confidence = confidence
        self.transcript = transcript
        db.commit()
        return transcript, confidence

    def get_full_filename(self):
        if self.grab:
            return self._grab_filename()
        elif not self.position:
            raise Exception('Programmer error: position needed to get "position" full name')
        return self.position_filename()

    def _grab_filename(self):
        raise NotImplementedError('Grab has not been implemented yet')

    def position_filename(self):
        base = self.base
        dirname = base.get_download_folder()
        position = '.{:04}'.format(int(self.position) - 1)
        filename = f'{self.length}_{base.filename.rstrip(base.extension)}.{position}.{base.extension}'

        return f'{dirname}/{filename}'


class SegmentUsers(Base):
    __tablename__ = 'segment_users'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segment.id'))
    segment = relationship('Segment')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


class Translation(Base):
    __tablename__ = 'translation'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segment.id'))
    segment = relationship('Segment', back_populates='translations')
    translation = Column(Text)
    language = Column(String(2))
    protected = Column(Boolean, default=False)


class TranslationUsers(Base):
    __tablename__ = 'transcript_user'
    id = Column(Integer, primary_key=True)
    translation_id = Column(Integer, ForeignKey('translation.id'))
    translation = relationship('Translation')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


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
    password = Column(String(512))
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


# def get_segment(obj, file_id, position, update=False):
#     full_filename = get_full_filename(obj, position)
#     segment = db.query(Segment).filter(Segment.meta_id == file_id, Segment.position == position).first()
#
#     if segment.transcript is None and update:
#         transcript, confidence = get_transcript('./static/{}'.format(full_filename))
#         segment.transcript = transcript
#         segment.confidence = confidence
#         db.commit()
#
#     return segment


