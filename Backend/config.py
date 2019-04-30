import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

host = '0.0.0.0'
port = 81
debug = True

SUPPLY_URL = 'http://localhost:80/api/push_key'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DFBDFSFVfsbdrkrdkyrdUGyudf'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_migrate_repo')

