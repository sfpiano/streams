from streams import app, login_manager, db
from .forms import LoginForm, RegistrationForm
from flask import (render_template,
                   flash,
                   request,
                   redirect,
                   session,
                   url_for,
                   current_app,
                   g)
from flask.ext.login import (login_user,
                             logout_user,
                             current_user,
                             login_required)

from .models import User

@app.before_request
def before_request():
  g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('base.html')

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    login_user(form.user)
    flash("Logged in successfully")
    return redirect(request.args.get('next') or url_for('index'))
  return render_template('login.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User()
    form.populate_obj(user)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('index'))
  return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))
