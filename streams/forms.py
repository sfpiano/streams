from flask.ext.wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields, TextField, BooleanField
from wtforms.validators import Required, ValidationError, InputRequired

from .models import User

class LoginForm(Form):
  name = TextField('name', validators = [Required()])
  password = TextField('password', validators = [Required()])
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
  password = fields.StringField(validators=[InputRequired()])

  def validate_name(form, field):
    print field.data
    user = User.query.filter(User.name == field.data).first()
    print user
    if user is not None:
      raise ValidationError("Username already exists")
