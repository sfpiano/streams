from datetime import datetime
from streams import db
from streams.data import CRUDMixin

from random import SystemRandom
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask import current_app
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

class User(UserMixin, CRUDMixin, db.Model):
  id = db.Column(db.Integer, primary_key = True)
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
    return '<User %r>' % (self.name)

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  requirements = db.relationship('Requirement', backref='project', lazy='dynamic')

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return '<Project %r>' % self.name

class Requirement(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

  def __init__(self, desc):
    self.description = desc

class Issue(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text)
  description = db.Column(db.Text)

  def __init__(self, title):
    self.title = title

class Test(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text)

  def __init__(self, desc):
    self.description = desc
