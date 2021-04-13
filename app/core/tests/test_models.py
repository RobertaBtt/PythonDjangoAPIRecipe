from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@poppoy.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email case insensitive"""
        email = "test@POPPOY.com"
        user = get_user_model().objects.create_user(email, "Test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "ciao")

    def test_create_super_user(self):
        """Test new super user"""
        user = get_user_model().objects.create_superuser(
            "email@admin.com",
            "Ciaodk")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
