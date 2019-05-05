import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

host = '0.0.0.0'
port = 81
debug = True
UPLOAD_FOLDER = './photos/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DFBDFSFVfsbdrkrdkyrdUGyudf'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_migrate_repo')