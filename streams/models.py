from datetime import datetime
from streams import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), unique = True)
  email = db.Column(db.String(120), unique = True)
  #role = db.Column(db.SmallInteger, default = ROLE_USER)
  #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % (self.name)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80))
  body = db.Column(db.Text)
  pub_date = db.Column(db.DateTime)

  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  category = db.relationship('Category',
      backref=db.backref('posts', lazy='dynamic'))

  def __init__(self, title, body, category, pub_date=None):
    self.title = title
    self.body = body
    if pub_date is None:
        pub_date = datetime.utcnow()
    self.pub_date = pub_date
    self.category = category

  def __repr__(self):
    return '<Post %r>' % self.title


class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return '<Category %r>' % self.name
