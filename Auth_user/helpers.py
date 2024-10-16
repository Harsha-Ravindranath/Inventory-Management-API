"""from rest_framework_simplejwt.tokens import RefreshToken."""
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a given user.

    Args:
        user: The user instance for which to generate tokens.

    Returns:
        dict: A dictionary containing the refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
