from django.contrib.auth import get_user_model
from django.test import TestCase


class BlogUserManagerTests(TestCase):
    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(email='test_email@gmail.com',
                                              first_name='TestFirstName',
                                              last_name='TestLastName',
                                              password='testpassword12345')
        self.assertEqual(user.email, 'test_email@gmail.com')
        self.assertEqual(user.first_name, 'TestFirstName')
        self.assertEqual(user.last_name, 'TestLastName')
        self.assertTrue(user.check_password('testpassword12345'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email='',
                                           first_name='',
                                           last_name='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='',
                                           first_name='test_first_name',
                                           last_name='test_last_name',
                                           password='testpassword12345')

    def test_create_super_user(self):
        user_model = get_user_model()
        super_user = user_model.objects.create_super_user(email='test_email@gmail.com',
                                                          first_name='TestFirstName',
                                                          last_name='TestLastName',
                                                          password='testpassword12345')
        self.assertEqual(super_user.email, 'test_email@gmail.com')
        self.assertEqual(super_user.first_name, 'TestFirstName')
        self.assertEqual(super_user.last_name, 'TestLastName')
        self.assertTrue(super_user.check_password('testpassword12345'))
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

        try:
            self.assertIsNone(super_user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(ValueError):
            user_model.objects.create_super_user(email='test_super@gmail.com',
                                                 first_name='test_first_name',
                                                 last_name='test_last_name',
                                                 password='testpassword12345',
                                                 is_superuser=False)
