import unittest
from django.contrib.auth import get_user_model


class ModelTests(unittest.TestCase):

    def test_create_user_with_email(self):
        """test creating a new user with an email is successful"""
        email = 'mikerock@gmail.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # def test_new_user_email_normalized(self):
    #    """test the email for a new user is normalized"""
    #    email = 'mikerock@GMAIL.COM'
    #    password = 'test123'
    #    user = get_user_model().objects.create_user(
    #        email=email,
    #        password=password
    #    )
    #    self.assertEqual(user.email, email)

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    # def test_create_new_super_user(self):
    #    """test creating a new super user"""
    #    user = get_user_model().objects.create_superuser(
    #        'mikerock@gmail.com',
    #       'test123'
    #   )
    #    self.assertTrue(user.is_superuser)
    #    self.assertTrue(user.is_staff)


if __name__ == '__main__':
    unittest.main()
