from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import CustomUser

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.

    This serializer handles the validation and creation of user accounts,
    ensuring that the password is securely hashed before saving.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user (hashed before saving).
        user_type (str): The type of user, either 'Admin' or 'User'.
    """
    
    user_type = serializers.ChoiceField(choices=[('Admin', 'Admin'), ('User', 'User')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'user_type')

    def create(self, validated_data):
        """
        Create a new user instance.

        Args:
            validated_data (dict): A dictionary of validated data for the user.

        Returns:
            CustomUser: The newly created user instance.
        """
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupSerializer, self).create(validated_data)

 
class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    This serializer handles the validation of user login credentials,
    including username and password.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    