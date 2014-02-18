from datetime import datetime
from streams import db
from streams.data import CRUDMixin

from random import SystemRandom
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask import current_app
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from collections import namedtuple
def create_named_tuple(*values):
  return namedtuple('NamedTuple', values)(*values)

class User(UserMixin, CRUDMixin, db.Model):
  __tablename__ = 'streams_user'
  name = db.Column(db.String(64), unique = True)
  _password = db.Column(db.LargeBinary(120))
  _salt = db.Column(db.String(120))

  @hybrid_property
  def password(self):
    return self._password

  @password.setter
  def password(self, value):
    if self._salt is None:
      self._salt = bytes(SystemRandom().getrandbits(128))
    self._password = self._hash_password(value)

  def is_valid_password(self, password):
    new_hash = self._hash_password(password)
    return compare_digest(new_hash, self._password)

  def _hash_password(self, password):
    pwd = password.encode("utf-8")
    salt = bytes(self._salt)
    rounds = current_app.config.get("HASH_ROUNDS", 100000)
    buff = pbkdf2_hmac("sha512", pwd, salt, iterations=rounds)
    return bytes(buff)

  def __repr__(self):
    return '<User {0}>'.format(self.name)

class Project(CRUDMixin, db.Model):
  __tablename__ = 'streams_project'
  name = db.Column(db.String(80))
  requirements = db.relationship('Requirement', backref='project', lazy='dynamic')

  def __repr__(self):
    return '<Project {0}>'.format(self.name)

rq_issue_helper = db.Table('rq_issue_helper',
    db.Column('rq_id', db.Integer, db.ForeignKey('streams_rq.id')),
    db.Column('issue_id', db.Integer, db.ForeignKey('streams_issue.id'))
    )

class Requirement(CRUDMixin, db.Model):
  __tablename__ = 'streams_rq'
  description = db.Column(db.Text)
  project_id = db.Column(db.Integer, db.ForeignKey('streams_project.id'))
  issues = db.relationship(
      'Issue',
      secondary=rq_issue_helper,
      backref=db.backref('rqs_query', lazy='dynamic'))

  def __repr__(self):
    return '<RQ {0}>'.format(self.description)

class Issue(CRUDMixin, db.Model):
  __tablename__ = 'streams_issue'

  project_version = create_named_tuple('f', 'alpha', 'beta', 'prod')

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text)
  description = db.Column(db.Text)
  type = db.Column(db.Enum(*project_version._asdict().values(), name='issue_type'))

  requirements = db.relationship(
      'Requirement',
      secondary=rq_issue_helper,
      backref=db.backref('issues_query', lazy='dynamic'))

  def __repr__(self):
    return '<Issue {0}>'.format(self.title)

class Test(CRUDMixin, db.Model):
  __tablename__ = 'streams_test'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text)

  def __init__(self, desc):
    self.description = desc

  def __repr__(self):
    return '<Test {0}>'.format(self.description[0:25])
