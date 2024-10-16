from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import SignupAPIView, LoginAPIView


urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]