from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from tests import SetupTestData


class UserProfileViewTest(SetupTestData):
    def test_get_user_profile_page(self):
        response = self.client.get(reverse('users:profile', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/userProfile.html')

    def test_user_name(self):
        response = self.client.get(reverse('users:profile', kwargs={'user_id': self.user.id}))
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_user_email(self):
        response = self.client.get(reverse('users:profile', kwargs={'user_id': self.user.id}))
        self.assertContains(response, self.user.email)

    def test_user_profile_photo(self):
        response = self.client.get(reverse('users:profile', kwargs={'user_id': self.user.id}))
        self.assertContains(response, self.user.profile_photo)


class RegisterViewTest(TestCase):
    def test_get_register_page(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/register.html')


class LoginViewTest(TestCase):
    def test_get_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/login.html')


class LogoutViewTest(TestCase):
    def test_get_logout_page(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/logout.html')


class EditUserProfileViewTest(SetupTestData):
    def test_get_edit_profile_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/editProfile.html')


class ChangeUserPasswordViewTest(SetupTestData):
    def test_get_change_user_password_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/changePassword.html')