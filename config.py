DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@127.0.0.1:3306/acoustic_pj'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False
CORS_HEADERS = 'Content-Type'
# 16 mb
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SQLALCHEMY_POOL_SIZE = 30
SQLALCHEMY_POOL_TIMEOUT = 300