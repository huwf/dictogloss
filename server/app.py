# from api.api import app

import csv
import difflib
from urllib.parse import unquote, urlparse

from anki import Collection
from bs4 import BeautifulSoup
import datetime
import pytz
import email.utils
import requests
from flask import request, jsonify, url_for, Flask, redirect, escape
from flask_cors import CORS
import logging
import os

from requests import HTTPError

from server.database import db, init_db
from server.models import BaseAudio, Segment, RSSChannel, RSSTrack, Translation, Article, ParsingRules

app = Flask(__name__)
# app.config.from_object('server.config')
# TODO: Limit CORS to same domain
CORS(app)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.before_first_request
def create_user():
    init_db()
    # u = db.query(User).first()
    # logger.debug('User exists? %r' % u)
    # if not u:
    #     from flask_security.utils import hash_password
    #
    #     user_datastore.create_user(username='testymctestface',
    #                                email=os.environ.get('DEFAULT_EMAIL'),
    #                                password=hash_password(os.environ.get('DEFAULT_PASSWORD')),
    #                                seconds_available=600)
    db.commit()

# @app.route('/')
# def home():
#     return "I'm Ron Burgundy?", 200


@app.route('/ping')
def ping():
    logger.debug('/ping')
    return "I'm a teapot", 418


def _get_url(obj):
    """Internal function to get the URL
    Works out the URL based on the object. Accepts a BaseAudio or a Segment"""

    relative_filename = os.path.join(obj.relative_dir, obj.filename)
    return url_for('static', filename=relative_filename, _external=True)


@app.route('/info/languages/speech')
def get_speech_languages():
    logger.debug('/info/languages/speech %s', request.args)
    with open('./server/language_codes.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        # logger.debug('get_speech_languages\n\n\n')
        ret = sorted([{'code': row[1], 'language': row[0]} for row in reader], key=lambda a: a['language'])
        logger.debug(f'get_speech_languages {ret}\n\n\n')
        return {'status': 'ok', 'data': ret}, 200


@app.route('/tools/differ')
def diff():
    try:
        google_answer = request.args.get('google')
        user_answer = request.args.get('user')
        first_arg = request.args.get('first', 'google')
        assert google_answer, 'Parameter google_answer is required'
        assert user_answer, 'Parameter user_answer is required'
        first = google_answer if first_arg == 'google' else user_answer
        second = user_answer if first == google_answer else google_answer

        differ = difflib.Differ()
        comp = differ.compare(escape(first), escape(second))
        ret = []
        string = ''
        # current_symbol = ''
        try:
            char = next(comp)
            current_symbol, char = char[0], char[-1]
            string += char
            while True:
                char = next(comp)
                print(f'char: {char}')
                symbol, char = char[0], char[-1]
                if symbol == current_symbol:
                    string += char
                else:
                    ret.append((current_symbol, string))
                    string = char
                    current_symbol = symbol

        except StopIteration:
            ret.append((current_symbol, string))
            print(ret)
        return {'status': 'OK', 'data': ret}
    except AssertionError as e:
        return {'status': 'error', 'message': str(e)}, 500


@app.route('/rss/<channel>/tracks', methods=['GET'])
def get_tracks_by_channel(channel):
    """Gets all tracks associated with the channel

    Accepts limit, and offset, orders by date (desc)

    :param channel:
    :return:
    """
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    channel_obj = db.query(RSSChannel).filter(RSSChannel.channel_name == channel).first()

    if not channel_obj:
        return {'status': 'error', 'message': f'RSS channel {channel} not found'}, 404

    # TODO: See if it's more efficient to query on channel_obj.tracks
    tracks = db.query(RSSTrack)\
        .filter(RSSTrack.channel == channel_obj) \
        .order_by(RSSTrack.published_date.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

    data = [c.to_json() for c in tracks]
    return {'data': data, 'status': 'ok'}


@app.route('/rss/channels/new', methods=['POST'])
def add_channel():
    data = request.get_json()
    try:
        feed_url = data.get('feed_url')
        resp = requests.head(feed_url)
        resp.raise_for_status()
    except HTTPError:
        return {
            'status': 'error',
            'details': f'Failed to connect to {feed_url} with status code {resp.status_code}'}, resp.status_code
    except ConnectionError:
        return {'status': 'error', 'details': f'Server for url {feed_url} is not available'}, 503

    channel = RSSChannel(
        url=feed_url, channel_name=data.get('feed_name'), channel_description=data.get('feed_description'),
        channel_type=data.get('feed_type'))
    db.add(channel)
    db.commit()
    return {'status': 'ok', 'data': channel.to_json()}, 200


@app.route('/rss/channels')
def get_channels():
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)
    channels = db.query(RSSChannel).limit(limit).offset(offset).all()
    data = [c.to_json() for c in channels]
    return {'data': data, 'status': 'ok'}


@app.route('/rss/channels/<channel_name>')
def get_channel_by_name(channel_name):
    channel_name = unquote(channel_name)
    channel = db.query(RSSChannel).filter(RSSChannel.channel_name == channel_name).first()
    if not channel:
        return {'status': 'error', 'message': f'Channel {channel_name} not found'}, 404
    data = channel.to_json()
    return {'status': 'ok', 'data': data}, 200


@app.route('/rss/parse', methods=['POST'])
def parse_feed():
    """Checks the content of an RSS URL and adds the episodes to the website

    :return:
    """
    data = request.get_json()
    feed_url = data.get('url')
    req = requests.get(feed_url)

    soup = BeautifulSoup(req.content, 'xml')

    channel = db.query(RSSChannel).filter(RSSChannel.url == feed_url).first()
    if not channel:
        name = soup.find('title').text
        description = soup.find('description').text
        channel = RSSChannel(url=feed_url, channel_name=name, channel_description=description)
        db.add(channel)
        db.commit()

    latest_track = db.query(RSSTrack)\
        .filter(RSSTrack.channel == channel)\
        .order_by(RSSTrack.published_date.desc())\
        .first()

    tracks = soup.find_all('item')
    ret = []
    for item in tracks:
        try:
            date_text = item.find('pubDate').text
        except AttributeError:
            date_text = item.find('pubdate').text
        rfc_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(date_text)), pytz.utc)
        if latest_track:
            latest_track.published_date = latest_track.published_date.replace(tzinfo=rfc_date.tzinfo)
            if latest_track.published_date >= rfc_date:
                logger.debug(f'Reached {latest_track.name}, which is already in the database')
                break
        if channel.channel_type == 'audio':
            track_url = item.find('enclosure').get('url')
        elif channel.channel_type == 'text':
            track_url = item.find('link').text
        else:
            raise ValueError('Unrecognised channel type')
        name = item.find('title').text
        description = item.find('description').text
        pub_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(date_text)), pytz.utc)
        track = RSSTrack(channel_id=channel.id, url=track_url, name=name,
                         description=description, published_date=pub_date)
        ret.append(track)
        db.add(track)

    db.commit()
    return {'status': 'OK', 'data': [track.to_json() for track in ret]}, 200


@app.route('/file/upload', methods=['POST'])
def save_file():
    """Downloads the file from the URL specified in POST/PUT body and saves on the filesystem and creates
    a record in the database

    Required fields:
    source_url: The URL to download it from (must be open, no auth will be attempted)
    Optional fields:
    language: BCP 47 language code. See https://cloud.google.com/speech-to-text/docs/languages for supported languages
    Files with more than one language should use string "MULTI"
    pretty_name: The name that the file will be displayed as

    :return: A JSON representation of the file or error message as appropriate
    """
    try:
        data = request.get_json()
        source_url = data.get('source_url')
        pretty_name = data.get('pretty_name')
        language = data.get('language')

        # RSS page field
        track_id = data.get('track_id')

        audio = BaseAudio.get(source_url=source_url)
        if BaseAudio.exists(audio):
            logger.info('Audio file already exists')
            return audio.to_json(), 409

        audio = BaseAudio(source_url=source_url, pretty_name=pretty_name, language=language)
        db.add(audio)
        db.flush()
        audio.save_file()
        db.commit()

        if track_id:
            track = db.query(RSSTrack).filter(RSSTrack.id == track_id).first()
            if track:
                track.is_added = True
                db.commit()

    except Exception as e:
        data = {
            'status': 'error',
            'message': str(e)
        }
        return data, 500
    return audio.to_json(), 201


@app.route('/text/import', methods=['POST'])
def import_article():
    data = request.get_json()
    logger.info('data: %s', data)

    source_url = data.get('source_url')
    pretty_name = data.get('pretty_name')
    language = data.get('language')
    rss_id = data.get('id')
    track = RSSTrack.get(rss_id)
    try:
        resp = requests.get(track.url)
        resp.raise_for_status()
    except HTTPError as e:
        return {'status': 'error', 'details': str(e)}, resp.status_code

    hostname = urlparse(track.url).hostname

    article = Article(pretty_name=track.name, url=track.url, rss_id=rss_id, language=language)
    parser = ParsingRules.get(hostname)
    # TODO: Save in a better format!
    content = parser.parse(resp.content)
    article.content = content
    db.add(article)
    db.commit()
    return {'status': 'ok', 'article': article.to_json()}, 200


@app.route('/text/anki', methods=['POST'])
def import_to_anki():
    data = request.get_json()
    note_type = data.get('note_type')
    deck = data.get('deck', 'Swedish 2')
    # TODO: Assume only two fields for now and hack the rest
    fields = data.get('fields')
    logger.debug(f'note_type: {note_type} fields: {fields}, deck: {deck} ')
    col = None
    # TODO: Document this better!
    try:
        original_collection = '/home/worker/anki2/User 1/collection.anki2'
        col = Collection(original_collection, server=True)
        model = col.models.byName(note_type)
        if model:
            logger.debug('model: %s', model)
            logger.debug('length: %d', len(model['flds']))

            while len(fields) < len(model['flds']):
                logger.debug('Adding a new blank string to fields')
                fields.append('')
            logger.debug('fields: %s', fields)

        anki_deck = col.decks.byName(deck)
        if not anki_deck:
            return {'status': 'error', 'details': 'The deck entered does not exist'}, 400
        logger.debug('anki_deck %s', anki_deck)
        # col.decks.select(anki_deck['id'])
        # col.models.setCurrent(model)
        # note = col.newNote()
        # note.fields = fields
        # col.addNote(note)
    finally:
        if col:
            col.close()
    return {'status': 'ok'}, 200


@app.route('/text/article/<article_id>')
def get_article(article_id):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return {'status': 'error', 'details': 'Not Found'}, 404
    return {'status': 'ok', 'article': article.to_json()}


@app.route('/file/<file_id>')
def get_file(file_id):
    """Returns the URL of a file by its ID

    Fields can be specified by
    """
    try:
        f = BaseAudio.get(id=file_id)

        # f = db.query(BaseAudio).filter(BaseAudio.id == file_id).first()
        if not f:
            return {'status': 'error', 'message': 'File not found'}, 404

        f.url = _get_url(f)
        return {'data': f.to_json(), 'status': 'ok'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 200



@app.route('/file/<id>/split', methods=['POST'])
def split_file(id):
    """Splits a file into equal segments of `segment_length` seconds

    The POST body requires the following fields as JSON:
    segment_length: The length of each segment
    :return:
    """
    # TODO: Handle the args properly
    segment_length = request.form.get('segment_length', 30)
    base = BaseAudio.get(id=id)
    if not base:
        return {'status': 'error', 'message': 'File not found'}, 404

    base.split_file(seconds=segment_length)
    data = {
        'status': 'ok',
        'data': [s.to_json() for s in base.segments],
    }
    return jsonify(data), 200

@app.route('/file/<id>/url')
def file_url(id):
    return '', 200


@app.route('/file/grab', methods=['POST'])
def grab_file():
    """Assumes a file exists on the server and makes a single segment of it

    POST body should have:
    * id
    * segment_length
    * start_point

    :return:
    """
    pass


@app.route('/file/downloads')
def get_downloads():
    downloads = BaseAudio.get_all()
    for d in downloads:
        d.url = _get_url(d)
    data = {
        'status': 'ok',
        'data': [d.to_json(['id', 'url', 'pretty_name']) for d in downloads]
    }
    return data, 200


@app.route('/segment/<id>')
def get_segment(id):
    """Returns a segment object requested by ID

    :param id:
    :return:
    """
    return redirect(url_for('find_segment', id=id), 301)


# TODO: refactor so there's only one segment route with optional attributes to return
@app.route('/segment')
def find_segment():
    """Search for a segment object

    Currently supported: id, file_id, position
    """
    params = request.args
    id = params.get('id')

    if id:
        segment = Segment.get(id)
    else:
        file_id = params.get('file_id')
        position = params.get('position')
        if not (file_id and position):
            return {
                'status': 'error',
                'message': 'Invalid request. Must contain either `id` for segment or `file_id` and `position`'
            }, 400
        segment = BaseAudio.get(file_id).get_segment(position)
    if not segment:
        data = {
            'status': 'error',
            'message': 'This segment does not exist'
        }
        return data, 404

    # Decide what fields to return
    fields = request.args.get('fields')
    if isinstance(fields, str):
        fields = [f.lower() for f in fields.split(',')]

    data = segment.to_json(fields)
    # Include the URL unless specified otherwise
    if 'url' in data:
        data['url'] = _get_url(segment)

    return {'data': data, 'status': 'ok'}, 200


def _transcribe(segment):

    if not segment:
        data = {
            'status': 'error',
            'message': 'This segment ID does not exist'
        }
        return data, 404

    if request.method == 'PUT':
        kwargs = {
            'encoding': request.form.get('encoding'),
            'sample_rate': request.form.get('sample_rate'),
            'language_code': request.form.get('language_code'),
            'automatic_punctuation': request.form.get('automatic_punctuation')
        }
        segment.retrieve_transcript(**kwargs)

    data = {
        'status': 'ok',
        'data': segment.to_json(['transcript', 'confidence'])
    }
    logger.debug('Completed transcription')
    return data, 200


@app.route('/transcript/<file>/<position>', methods=['GET', 'PUT'])
def transcription_by_position(file, position):
    logger.debug(f'file: {file}')
    segment = BaseAudio.get(file).get_segment(position)
    return _transcribe(segment)


@app.route('/segment/<id>/transcript', methods=['GET', 'PUT'])
def transcription(id):
    """Gets or sets the transcript for segment <id>

    For a GET request, the ID is the ID of the segment which is passed in the route.

    For a PUT request, the following may be set in the request body:
    encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                            sample_rate=44100, language_code='sv-SE', automatic_punctuation=True
    """
    segment = Segment.get(id)
    return _transcribe(segment)


def _translate(text, target, obj):
    translation = Translation.retrieve_translation(text, target_language=target, source_language=obj.language)
    if isinstance(obj, Article):
        translation.article = obj
    elif isinstance(obj, Segment):
        translation.segment = obj

    return translation

@app.route('/translate/<file>/<position>', methods=['GET', 'POST'])
def translate_segment(file, position):
    # NOTE: This does not necessarily translate a whole segment, merely a part.
    # To translate a whole part, we may end up translating some bits twice
    # so we'll have to do something a bit more clever
    data = request.get_json(force=True)
    target = data.get('target', 'en-GB')
    text = data.get('text')
    logger.debug(f'translate file {file} position {position} text {text}')
    segment = BaseAudio.get(file).get_segment(position)
    logger.debug(f'translate segment: {segment.to_json()}')

    translation = _translate(text, target, segment)
    db.add(translation)
    db.commit()
    ret = {'status': 'ok', 'translation': translation.to_json(segment)}

    return ret, 200


# @app.route('/translate/text', methods=['GET', 'POST'])
# def translate_text()



@app.route('/user/<id>/assign_ownership')
def assign_ownership(id):
    """This function will assert the user <<id>> has an ownership (e.g. has paid) for a particular
    entity.

    A user can protect a file (or not), or the specific set of segments of a file.

    :param id:
    :return:
    """
    pass

if __name__ == "__main__":
    app.run(debug=True)
