from streams import app, login_manager, db
from flask import (
    render_template,
    flash,
    request,
    redirect,
    session,
    url_for,
    current_app,
    g)
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required)

from .forms import (
    LoginForm,
    RegistrationForm,
    RequirementForm,
    IssueForm,
    ProjectForm,
    ReleaseForm,
    TestForm)
from .models import (
    User,
    Requirement,
    Project,
    Issue,
    Release,
    Test)
from .data import query_to_list

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.before_request
def before_request():
  g.user = current_user

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/favicon.ico')
def fav():
  return render_template('base.html')

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template('base.html')

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/projects', methods = ['GET', 'POST'])
@login_required
def projects():
  form = ProjectForm()
  if form.validate_on_submit():
    project = Project.create(**form.data)

    flash("Added Project")
    return redirect(url_for(".projects"))

  results = Project.query.all()
  return render_template('projects.html', projects=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/setproj/<int:id>')
@login_required
def set_project(id):
  current_user.current_project_id = id
  current_user.save()
  return redirect(url_for('index'))

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/issues', methods = ['GET', 'POST'])
@login_required
def issues():
  form = IssueForm()
  if form.validate_on_submit():
    issue = Issue.create(
        title=form.data['title'],
        description=form.data['description'],
        release_id=form.data['release'].id,
        requirement_id=form.data['req'].id,
        type=form.data['type'],
        status=form.data['status'],
        assignee_id=form.data['assignee'].id)

    flash("Added Issue")
    return redirect(url_for(".issues"))

  results = Issue.query.all()
  return render_template('issues.html', action='Add', issues=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/issues/r/<int:req_id>', methods = ['GET', 'POST'])
@login_required
def issue_from_req(req_id):
  from wtforms.ext.sqlalchemy.fields import QuerySelectField
  from forms import req_query

  class F(IssueForm):
    pass

  setattr(F, 'req',
    QuerySelectField(
      query_factory=req_query,
      default=Requirement.query.get(req_id)))

  form = F()
  if form.validate_on_submit():
    issue = Issue.create(
        title=form.data['title'],
        description=form.data['description'],
        release_id=form.data['release'].id,
        requirement_id=form.data['req'].id,
        type=form.data['type'],
        status=form.data['status'],
        assignee_id=form.data['assignee'].id)
    flash("Added Issue")
    return redirect(url_for(".issues"))

  results = Issue.query.all()
  return render_template('issues.html', action='Add', issues=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/issues/d/<int:issue_id>', methods = ['GET', 'POST'])
@login_required
def del_issue(issue_id):
  issue = Issue.query.get(issue_id)
  Issue.delete(issue)
  flash("Deleted Issue")
  return redirect(url_for(".issues"))

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/issues/<int:issue_id>', methods = ['GET', 'POST'])
@login_required
def edit_issue(issue_id):
  issue = Issue.query.get(issue_id)
  form = IssueForm(obj=issue)
  if form.validate_on_submit():
    issue.title=form.data['title']
    issue.description=form.data['description']
    issue.release_id=form.data['release'].id
    issue.requirement_id = form.data['req'].id
    issue.assignee_id=form.data['assignee'].id
    issue.type=form.data['type']
    issue.status=form.data['status']

    issue.save()
    flash("Updated Issue")
    return redirect(url_for(".issues"))

  results = Issue.query.all()
  return render_template('issues.html',
      action='Edit',
      issues=results,
      form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/releases', methods = ['GET', 'POST'])
@login_required
def releases():
  form = ReleaseForm()
  if form.validate_on_submit():
    Release.create(
      name=form.data['name'],
      date=form.data['date'])
    flash("Added Release")
    return redirect(url_for(".releases"))

  results = Release.query.order_by(Release.date).all()
  return render_template('releases.html', releases=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/reqs', methods = ['GET', 'POST'])
@login_required
def reqs():
  form = RequirementForm()
  if form.validate_on_submit():
    Requirement.create(
        description=form.data['description'],
        project_id=current_user.current_project_id,
        category_id=form.data['category'].id,
        external_id=form.data['external_id'])
    flash("Added Requirement")
    return redirect(url_for(".reqs"))
    
  results = Requirement.query.all()
  return render_template('reqs.html', reqs=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/reqs/d/<int:req_id>', methods = ['GET', 'POST'])
@login_required
def del_req(req_id):
  req = Requirement.query.get(req_id)
  Requirement.delete(req)
  flash("Deleted Requirement")
  return redirect(url_for(".reqs"))

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/reqs/<int:req_id>', methods = ['GET', 'POST'])
@login_required
def edit_req(req_id):
  req = Requirement.query.get(req_id)
  form = RequirementForm(obj=req)
  if form.validate_on_submit():
    req.description=form.data['description']
    req.category_id=form.data['category'].id
    req.external_id=form.data['external_id']

    req.save()
    flash("Updated requirement")
    return redirect(url_for(".reqs"))

  results = req.query.all()
  return render_template('reqs.html',
      action='Edit',
      reqs=results,
      form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/tests', methods = ['GET', 'POST'])
@login_required
def tests():
  form = TestForm()
  if form.validate_on_submit():
    Test.create(
        description=form.data['description'],
        issue_id=form.data['issue'].id)
    flash("Added Test")
    return redirect(url_for(".tests"))
    
  results = Test.query.all()
  return render_template('tests.html', tests=results, form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/login', methods = ['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    login_user(form.user)
    flash("Logged in successfully")
    return redirect(request.args.get('next') or url_for('index'))
  return render_template('login.html', form=form)

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
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
