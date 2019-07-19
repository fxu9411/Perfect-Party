import os
SECRET_KEY = 'secret'
DATA_BACKEND = 'cloudsql'PROJECT_ID = 'cs-348'
CLOUDSQL_USER = 'admin'
CLOUDSQL_PASSWORD = 'password'
CLOUDSQL_DATABASE = 'bookshelf'CLOUDSQL_CONNECTION_NAME = 'cs-348:us-central1:library'##
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
MONGO_URI = \
    'mongodb://user:password@host:27017/database'