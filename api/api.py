from database import db, init_db
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from api.models import BaseAudio, Segment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
# TODO: Limit CORS to same domain
CORS(app)


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

@app.route('/info/languages/speech')
def get_speech_languages():
    with open('language_codes.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        ret = [{'code': row[1], 'language': row[0]} for row in reader]
        return {'status': 'ok', 'data': ret }, 200


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

        audio = BaseAudio.get(source_url=source_url)
        if BaseAudio.exists(audio):
            logger.info('Audio file already exists')
            return audio.to_json(), 409

        audio = BaseAudio(source_url=source_url, pretty_name=pretty_name, language=language)
        db.add(audio)
        db.flush()
        audio.save_file()
        db.commit()

    except Exception as e:
        data = {
            'status': 'error',
            'message': str(e)
        }
        return data, 500
    return audio.to_json(), 201


@app.route('/file/<file_id>')
def get_file(file_id):
    """Returns the URL of a file by its ID
    """
    try:
        f = BaseAudio.get(id=file_id)
        # f = db.query(BaseAudio).filter(BaseAudio.id == file_id).first()
        if not f:
            return {'status': 'error', 'message': 'File not found'}, 404
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


@app.route('/segment/<id>')
def get_segment(id):
    """Returns a segment object requested by ID

    :param id:
    :return:
    """
    segment = Segment.get(id)
    if not segment:
        data = {
            'status': 'error',
            'message': 'This segment ID does not exist'
        }
        return data, 404
    return {'data': segment.to_json(), 'status': 'ok'}, 200


@app.route('/segment/<id>/transcript', methods=['GET', 'POST'])
def transcription(id):
    """Gets or sets the transcript for segment <id>

    For a GET request, the ID is the ID of the segment which is passed in the route.

    For a POST request, the following may be set in the request body:
    encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                            sample_rate=44100, language_code='sv-SE', automatic_punctuation=True
    """
    segment = Segment.get(id)
    if not segment:
        data = {
            'status': 'error',
            'message': 'This segment ID does not exist'
        }
        return data, 404

    if request.method == 'POST':
        kwargs = {
            'encoding': request.form.get('encoding'),
            'sample_rate': request.form.get('sample_rate'),
            'language_code': request.form.get('language_code'),
            'automatic_punctuation': request.form.get('automatic_punctuation')
        }
        segment.retrieve_transcript(**kwargs)

    data = {
        'status': 'ok',
        'data': {
            'transcript': segment.transcript, 'confidence': segment.confidence
        }
    }

    return data, 200



@app.route('/user/<id>/assign_ownership')
def assign_ownership(id):
    """This function will assert the user <<id>> has an ownership (e.g. has paid) for a particular
    entity.

    A user can protect a file (or not), or the specific set of segments of a file.

    :param id:
    :return:
    """
    pass

