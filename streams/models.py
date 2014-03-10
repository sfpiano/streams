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

################################################################################
################################################################################
class User(UserMixin, CRUDMixin, db.Model):
  __tablename__ = 'streams_user'
  name = db.Column(db.String(64), unique = True)
  current_project_id = db.Column(db.Integer, db.ForeignKey('streams_project.id'))

  _password = db.Column(db.LargeBinary(120))
  _salt = db.Column(db.String(120))

  @property
  def current_project(self):
    try:
      return Project.query.get(self.current_project_id)
    except Exception:
      return None

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

################################################################################
################################################################################
class Project(CRUDMixin, db.Model):
  __tablename__ = 'streams_project'
  name = db.Column(db.String(80))
  requirements = db.relationship('Requirement', backref='project', lazy='dynamic')

  def __repr__(self):
    return '<Project {0} {1}>'.format(self.id, self.name)

rq_issue_helper = db.Table('rq_issue_helper',
    db.Column('rq_id', db.Integer, db.ForeignKey('streams_rq.id')),
    db.Column('issue_id', db.Integer, db.ForeignKey('streams_issue.id'))
    )

################################################################################
################################################################################
class RQCategory(CRUDMixin, db.Model):
  __tablename__ = 'streams_rq_cat'

  name = db.Column(db.String(32))

  def __repr__(self):
    return '<Cat {0} {1}>'.format(self.id, self.name)

################################################################################
################################################################################
class Requirement(CRUDMixin, db.Model):
  __tablename__ = 'streams_rq'

  description = db.Column(db.Text)
  category_id = db.Column(db.Integer, db.ForeignKey('streams_rq_cat.id'))
  project_id = db.Column(db.Integer, db.ForeignKey('streams_project.id'))
  external_id = db.Column(db.Integer)

  issues = db.relationship(
      'Issue',
      secondary=rq_issue_helper,
      backref=db.backref('rqs_query', lazy='dynamic'))

  @property
  def category(self):
    try:
      return RQCategory.query.get(self.category_id)
    except Exception:
      return None

  def __repr__(self):
    try:
      return '{0} {1} {2}{3}'.format(
          self.category.name,
          self.external_id,
          self.description[:50],
          '...' if len(self.description) > 50 else "")
    except Exception:
      return '<RQ {0} {1}>'.format(self.id, self.description)

################################################################################
################################################################################
class Issue(CRUDMixin, db.Model):
  __tablename__ = 'streams_issue'

  Types = create_named_tuple('bug', 'en')
  Status = create_named_tuple('open', 'closed', 'invalid')

  release_id = db.Column(db.Integer, db.ForeignKey('streams_release.id'))
  requirement_id = db.Column(db.Integer, db.ForeignKey('streams_rq.id'))
  assignee_id = db.Column(db.Integer, db.ForeignKey('streams_user.id'))

  title = db.Column(db.Text)
  description = db.Column(db.Text)
  type = db.Column(db.Enum(*Types._asdict().values(), name='issue_type'))
  status = db.Column(db.Enum(*Status._asdict().values(), name='issue_status'))

  @property
  def assignee(self):
    try:
      return User.query.get(self.assignee_id)
    except Exception:
      pass

  @property
  def release(self):
    try:
      return Release.query.get(self.release_id)
    except Exception:
      pass

  @property
  def req(self):
    try:
      return Requirement.query.get(self.requirement_id)
    except Exception:
      pass

  def __repr__(self):
    return '<{0} {1}>'.format(self.id, self.title)

################################################################################
################################################################################
class Test(CRUDMixin, db.Model):
  __tablename__ = 'streams_test'

  description = db.Column(db.Text)
  issue_id = db.Column(db.Integer, db.ForeignKey('streams_issue.id'))

  def __repr__(self):
    return '<{0} {1}>'.format(self.id, self.description[0:25])

################################################################################
################################################################################
class Release(CRUDMixin, db.Model):
  __tablename__ = 'streams_release'

  issues = db.relationship('Issue', backref='release')

  name = db.Column(db.Text)
  date = db.Column(db.Date)

  def __repr__(self):
    return '<{0} {1}>'.format(self.id, self.name)
