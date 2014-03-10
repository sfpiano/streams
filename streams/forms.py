from flask.ext.wtf import Form
from flask.ext.login import current_user
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields 
from wtforms.validators import (
    Required,
    ValidationError,
    InputRequired,
    Optional)
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import User, Project, Issue, Requirement, Release, RQCategory

def project_query():
  return Project.query
def proj_req_query():
  return Requirement.query.filter(
    Requirement.project_id == current_user.current_project_id)
def release_query():
  return Release.query
def issue_query():
  return Issue.query
def rq_cat_query():
  return RQCategory.query
def assignee_query():
  return User.query

################################################################################
################################################################################
class LoginForm(Form):
  name = fields.TextField('name', validators = [Required()])
  password = fields.PasswordField('password', validators = [Required()])

  def validate_password(form, field):
    try:
      user = User.query.filter(User.name == form.name.data).one()
    except (MultipleResultsFound, NoResultFound):
      raise ValidationError("Invalid user")

    if user is None:
      raise ValidationError("Invalid user")
    if not user.is_valid_password(form.password.data):
      raise ValidationError("Invalid password")

    form.user = user

################################################################################
################################################################################
class RegistrationForm(Form):
  name = fields.TextField("Display Name")
  password = fields.PasswordField(validators=[InputRequired()])

  def validate_name(form, field):
    print field.data
    user = User.query.filter(User.name == field.data).first()
    print user
    if user is not None:
      raise ValidationError("Username already exists")

################################################################################
################################################################################
class RequirementForm(Form):
  description = fields.TextAreaField(validators=[Required()])
  category = QuerySelectField(query_factory=rq_cat_query)
  external_id = fields.IntegerField(validators=[Optional()])

################################################################################
################################################################################
class IssueForm(Form):
  title = fields.TextField(validators=[Required()])
  description = fields.TextAreaField(validators=[Optional()])
  type = fields.SelectField(
    'Type',
    choices=Issue.Types._asdict().items(),
    validators=[Required()])
  status = fields.SelectField(
    'Status',
    choices=Issue.Status._asdict().items(),
    validators=[Required()])
  assignee = QuerySelectField(query_factory=assignee_query)
  release = QuerySelectField(query_factory=release_query)
  req = QuerySelectField(query_factory=proj_req_query)

################################################################################
################################################################################
class ReleaseForm(Form):
  name = fields.TextField(validators=[Required()])
  date = fields.DateField(
    'Date: m/d/yy',
    validators=[Required()],
    format='%m/%d/%y')

################################################################################
################################################################################
class ProjectForm(Form):
  name = fields.TextField(validators=[Required()])

################################################################################
################################################################################
class TestForm(Form):
  issue = QuerySelectField(query_factory=issue_query)
  description = fields.TextAreaField(validators=[Required()])
