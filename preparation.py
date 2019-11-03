"""
This module:
- Downloads a file that is specified by URL, or a place on the disk
- Splits the file into chunks of n seconds
"""

import os
from subprocess import Popen, PIPE
import requests
from urllib.parse import urlparse
import logging

from constants import OUTPUT_DIR, DEFAULT_SEGMENT_LENGTH
from models import BaseAudio, Segment
from database import db
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def download_file(url, file_name=None, output_dir=OUTPUT_DIR, pretty_name=None, segment_length=30):

    filepath = file_name if file_name else urlparse(url).path.split('/')[-1]

    logger.info('Downloading file from %s to be saved at ', url)
    r = requests.get(url)
    obj = BaseAudio(filepath, filepath if not pretty_name else pretty_name, source_url=url, segment_length=segment_length)
    db.add(obj)
    db.commit()
    output_dir_path = '{}/{}'.format(output_dir, obj.id)
    download_path = '{}/{}'.format(output_dir_path, filepath)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        with open(download_path, 'wb') as f:
            f.write(r.content)
        return obj.id, download_path
    raise OSError('The file, or a file with the same name, has already been downloaded')


def split_file(base_id, path, seconds=DEFAULT_SEGMENT_LENGTH):

    if not seconds:
        seconds = DEFAULT_SEGMENT_LENGTH

    logger.info('Splitting file at %s', path)
    split_path = os.path.split(path)
    output_path = "/".join([split_path[0], '{}_{}%04d.mp3'.format(seconds, split_path[1].replace('mp3', ''))])
    args = ['ffmpeg', '-i', path, '-f', 'segment', '-segment_time', str(seconds), '-c', 'copy', output_path]

    proc = Popen(args, stderr=PIPE, stdout=PIPE)
    output, error = proc.communicate()
    logger.debug('Output: %s', str(output))

    if proc.returncode != 0:
        logger.warning(str(error))

    print('listdir: %s' % os.listdir(split_path[0]))
    segments = [s for s in sorted(os.listdir(split_path[0])) if re.match(r'[0-9]{1,4}_', s)]
    print('segments: %r' % segments)
    for idx, f in enumerate(segments):
        logger.debug('%d %s' % (idx, f))
        logger.debug('SAVING %d %s' % (idx, f))
        s = Segment(base_id=base_id, position=idx + 1, transcript=None, confidence=None)
        db.add(s)
        db.commit()
