"""Unit tests for the `PrivilegeUserSerializer` class."""

from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.users.serializers import PrivilegeUserSerializer


class Validate(TestCase):
    """Test data validation via the `validate` method."""

    def setUp(self) -> None:
        """Define dummy user data."""

        self.user_data = {
            'username': 'testuser',
            'password': 'Password123!',
            'email': 'testuser@example.com',
        }

    def test_validate_password_is_hashed(self) -> None:
        """Test the password is hashed during validation."""

        serializer = PrivilegeUserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(check_password('Password123!', serializer.validated_data['password']))

    def test_validate_password_invalid(self) -> None:
        """Test an invalid password raises a `ValidationError`."""

        self.user_data['password'] = '123'  # Too short
        serializer = PrivilegeUserSerializer(data=self.user_data)
        with self.assertRaises(DRFValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_without_password(self) -> None:
        """Test validation fails when a password is not provided."""

        del self.user_data['password']
        serializer = PrivilegeUserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
