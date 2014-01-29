from streams import app, lm, db
from forms import LoginForm
from flask import (render_template,
                   flash,
                   request,
                   redirect,
                   session,
                   url_for,
                   g)
from flask.ext.login import (login_user,
                             logout_user,
                             current_user,
                             login_required)

from models import User

@app.before_request
def before_request():
  g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('base.html')

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data

    user = User.query.filter_by(name=form.openid.data).first()
    if user is None:
      name = form.openid.data
      user = User(name = name)
      db.session.add(user)
      db.session.commit()
    remember_me = False
    if 'remember_me' in session:
      remember_me = session['remember_me']
      session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

    return redirect(url_for('index'))
  return render_template('login.html', form = form)
