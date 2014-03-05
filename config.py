from os.path import abspath, dirname, join
from os import environ

_cwd = dirname(abspath(__file__))

class BaseConfiguration(object):
  DEBUG = False
  TESTING = False
  SECRET_KEY = 'iamsecret'

  if environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'app.db')
  else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

  SQLALCHEMY_MIGRATE_REPO = join(_cwd, 'db_repository')
  SQLALCHEMY_ECHO = False
  HASH_ROUNDS = 100000

class TestConfiguration(BaseConfiguration):
  TESTING = True
  WTF_CSRF_ENABLED = False

  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')

  # Since we want our unit tests to run quickly
  # we turn this down - the hashing is still done
  # but the time-consuming part is left out.
  HASH_ROUNDS = 1

class DebugConfiguration(BaseConfiguration):
  DEBUG = True
