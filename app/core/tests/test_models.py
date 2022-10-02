from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
#get_user_model is a helpder provided by Django to get the default user model of the User

from core import models


def sample_user(email="test@gmail.com", password="testpassgmail"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@poppoy.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email case insensitive"""
        sample_emails = [
            ['tests23@GMAIL.com', 'tests23@gmail.com'],
            ['cancioffino@gmail.COM', 'cancioffino@gmail.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Test creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', "ciao")

    def test_new_user_invalid_email(self):
        """Test creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "ciao")

    def test_create_super_user(self):
        """Test new superuser"""
        user = get_user_model().objects.create_superuser(
            "email@admin.com",
            "Ciaodk")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representatio"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="meat"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
