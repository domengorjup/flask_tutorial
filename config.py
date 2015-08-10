WTF_CSRF_ENABLED = True
SECRET_KEY = 'secretkey'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
	
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Search configuration
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# mail server settings
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('Y_MAIL_USERNAME')   # SET USER VARIABLE!
MAIL_PASSWORD = os.environ.get('Y_MAIL_PASSWORD')

# administrator list
ADMINS = ['domengorjup@yahoo.com', 'domen_gorjup@hotmail.com']

# pagination
POSTS_PER_PAGE = 3