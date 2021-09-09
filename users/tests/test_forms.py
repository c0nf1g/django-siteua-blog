from django.test import TestCase
from tests import SetupTestData
from users.forms import BlogUserCreationForm, BlogUserChangePasswordForm, BlogUserChangeForm


class BlogUserCreationFormTest(TestCase):
    def test_valid_form_input(self):
        valid_data = {
            'email': 'email@gmail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': '12345678pass',
            'password2': '12345678pass'
        }

        form = BlogUserCreationForm(valid_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.email, 'email@gmail.com')
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.last_name, 'Last')

    def test_invalid_form_input(self):
        form = BlogUserCreationForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])


class BlogUserChangeFormTest(SetupTestData):
    def test_valid_form_input(self):
        valid_data = {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'email': 'new_email@gmail.com'
        }

        form = BlogUserChangeForm(valid_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(form.cleaned_data['first_name'], valid_data['first_name'])
        self.assertEqual(form.cleaned_data['last_name'], valid_data['last_name'])
        self.assertEqual(form.cleaned_data['email'], valid_data['email'])

    def test_invalid_form_input(self):
        form = BlogUserChangeForm({}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])


class BlogUserChangePasswordFormTest(SetupTestData):
    def test_valid_form_input(self):
        valid_data = {
            'old_password': '12345678pass',
            'new_password1': '12345newpass',
            'new_password2': '12345newpass'
        }

        old_password = self.user.password
        form = BlogUserChangePasswordForm(self.user, valid_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertNotEqual(old_password, self.user.password)

    def test_invalid_form_input(self):
        form = BlogUserChangePasswordForm(self.user, {})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'], ['This field is required.'])
        self.assertEqual(form.errors['new_password1'], ['This field is required.'])
        self.assertEqual(form.errors['new_password2'], ['This field is required.'])

    def test_incorrect_old_password(self):
        invalid_data = {
            'old_password': '12345invalidpass',
            'new_password1': '12345newpass',
            'new_password2': '12345newpass'
        }
        form = BlogUserChangePasswordForm(self.user, invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['old_password'].errors, [form.error_messages['password_incorrect']])

    def test_new_passwords_mismatch(self):
        invalid_data = {
            'old_password': '12345678pass',
            'new_password1': '12345differentnewpass',
            'new_password2': '12345newpass'
        }

        form = BlogUserChangePasswordForm(self.user, invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["new_password2"].errors, [str(form.error_messages['password_mismatch'])])