from django.test import TestCase
from django.contrib.auth import get_user_model


class SetupTestData(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='first_name',
            last_name='last_name',
            email='email@gmail.com',
            password='12345678pass'
        )
