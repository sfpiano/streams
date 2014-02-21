from streams import app, login_manager, db
from .forms import LoginForm, RegistrationForm, RequirementForm
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

from .models import User, Requirement, Project, Issue
from data import query_to_list

@app.before_request
def before_request():
  g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('base.html')

@app.route('/test')
def test():
  test_proj = Project.create(name='proj1')
  test_rq = Requirement.create(
      description='This is a test rq',
      project_id=test_proj.id)

  test_issue = Issue.create(
      title='Test title',
      description='Test desc',
      type=Issue.types.bug)

  test_rq.issues.append(test_issue)
  test_rq.save()

  return render_template('base.html')

@app.route('/issues')
@login_required
def issues():
  data = Issue.query
  results = query_to_list(data)
  return render_template('issues.html', issues=results)

@app.route('/reqs', methods = ['GET', 'POST'])
@login_required
def reqs():
  form = RequirementForm()
  if form.validate_on_submit():
    Requirement.create(
        description=form.data['description'],
        project_id=form.data['project_id'].id)
    flash("Added Requirement")
    return redirect(url_for(".reqs"))
    
  data = Requirement.query
  results = query_to_list(data)
  return render_template('reqs.html', reqs=results, form=form)

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
