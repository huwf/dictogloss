import os

DEFAULT_SEGMENT_LENGTH = 30

DB_CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING', 'sqlite:////usr/src/database.db')
SAVE_DIR = 'server/static'
# To be used with for_static
OUTPUT_DIR_FOR_STATIC = 'mp3'
