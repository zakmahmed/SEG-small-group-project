"""Referenced from clucker application"""
"""Unit tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from clubs.forms import SignUpForm
from clubs.models import User

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
            'bio': 'My bio',
            'statement': 'My statement',
            'chess_xp': 100,
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        email_field = form.fields['username']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('statement', form.fields)
        self.assertIn('chess_xp', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    def test_valid_club_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_first_name(self):
        self.form_input['first_name'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_first_name(self):
        self.form_input['first_name'] = 'x' * 60
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_last_name(self):
        self.form_input['last_name'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_last_name(self):
        self.form_input['last_name'] = 'x' * 60
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_bio(self):
        self.form_input['bio'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_club_bio(self):
        self.form_input['bio'] = 'x' * 530
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_statement(self):
        self.form_input['statement'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_club_statement(self):
        self.form_input['statement'] = 'x' * 1010
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_chessxp(self):
        self.form_input['chess_xp'] = ''
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_club_chessxp(self):
        self.form_input['chess_xp'] = -100
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = User.objects.get(username='janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.statement, 'My statement')
        self.assertEqual(user.chess_xp, 100)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
