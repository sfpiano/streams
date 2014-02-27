from flask.ext.wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields, TextField, BooleanField
from wtforms.validators import Required, ValidationError, InputRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import User, Project, Issue, Requirement, Release

class LoginForm(Form):
  name = TextField('name', validators = [Required()])
  password = fields.PasswordField('password', validators = [Required()])
  remember_me = BooleanField('remember_me', default = False)

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

class RegistrationForm(Form):
  name = fields.StringField("Display Name")
  password = fields.PasswordField(validators=[InputRequired()])

  def validate_name(form, field):
    print field.data
    user = User.query.filter(User.name == field.data).first()
    print user
    if user is not None:
      raise ValidationError("Username already exists")

def project_query():
  return Project.query
def req_query():
  return Requirement.query
def release_query():
  return Release.query

class RequirementForm(Form):
  description = fields.StringField(validators=[Required()])
  project_id = QuerySelectField(query_factory=project_query)

class IssueForm(Form):
  title = fields.StringField(validators=[Required()])
  description = fields.TextAreaField(validators=[Optional()])
  type = fields.SelectField('Type', choices=Issue.Types._asdict().items(), validators=[Required()])
  release = QuerySelectField(query_factory=release_query)
  req = QuerySelectField(query_factory=req_query)

class ReleaseForm(Form):
  name = fields.StringField(validators=[Required()])
  date = fields.DateField('Date: m/d/yy', validators=[Required()], format='%m/%d/%y')

class TestForm(Form):
  pass
