from flask import url_for
from flask.ext.login import current_user

from streams.test_base import BaseTestCase
from .models import User, Project, Requirement, Issue

class BasicModelsTests(BaseTestCase):
  def test_relate_proj_rq(self):
    test_proj = Project.create(name='proj1')
    test_rq = Requirement.create(
        description='This is a test rq',
        project_id=test_proj.id)

    self.assertEqual(test_proj.requirements.one(), test_rq)

    test_issue = Issue.create(
        title='Test title',
        description='Test desc')

    test_rq.issues.append(test_issue)
    test_rq.save()

    self.assertEqual(
        Requirement.query.filter_by(id=test_rq.id).first().issues[0].id,
        test_issue.id)
    self.assertEqual(
        Issue.query.filter_by(id=test_issue.id).first().requirements[0].id,
        test_rq.id)

class UserViewsTests(BaseTestCase):
  def test_user_can_login(self):
    test_name = 'Steve'
    test_pass = 'pass'
    User.create(name=test_name, password=test_pass)

    # Needed to keep the thread-local 'current_user' var alive after
    # the post completes
    with self.client:
      response = self.client.post(
          url_for('login'),
          data={'name': test_name, 'password': test_pass})

      self.assert_redirects(response, url_for('index'))
      self.assertTrue(current_user.name == test_name)
      self.assertFalse(current_user.is_anonymous())

  def test_users_can_logout(self):
    test_name = 'Steve'
    test_pass = 'pass'
    User.create(name=test_name, password=test_pass)

    with self.client:
      self.client.post(
          url_for('login'),
          data={'name': test_name, 'password': test_pass})
      self.client.get(url_for('logout'))

      self.assertTrue(current_user.is_anonymous())

  def test_invalid_password_is_rejected(self):
    test_name = 'Steve'
    test_pass = 'pass'
    User.create(name=test_name, password=test_pass)

    with self.client:
      response = self.client.post(
          url_for("login"),
          data={'name': test_name,
                "password": "*****"})

      self.assertTrue(current_user.is_anonymous())
      self.assert_200(response)
      self.assertIn("Invalid password", response.data)

  def test_user_can_register_account(self):
    with self.client:
      response = self.client.post(url_for("register"),
                                  data={"password": "5555"})

      self.assert_redirects(response, url_for("index"))
      self.assertFalse(current_user.is_anonymous())

  #def test_user_is_redirected_to_index_from_logout(self):
  #  with self.client:
  #    response = self.client.get(url_for("logout"))

  #    self.assert_redirects(response, url_for("login"))
  #    self.assertTrue(current_user.is_anonymous())
