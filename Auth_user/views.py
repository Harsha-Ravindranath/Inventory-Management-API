from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer, LoginSerializer
from .models import CustomUser
from .helpers import get_tokens_for_user


class SignupAPIView(APIView):
    """
    API View for user signup.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle user signup.

        Args:
            request: The HTTP request containing user signup data.

        Returns:
            Response: A response object with the status and message.
        """
        print(request.data)
        if not request.data:
            return Response({'message': 'Provide data for registration'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = SignupSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.validated_data['email']

                if CustomUser.objects.filter(email=email).exists():
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Email already exists'
                    }, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'User registered successfully',
                    'status': status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    """
    API View for user login.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle user login.

        Args:
            request: The HTTP request containing login credentials.

        Returns:
            Response: A response object indicating the success or failure of the login attempt.
        """
        if not request.data:
            return Response({'message': 'Required data not provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                response_data = get_tokens_for_user(user)

                response = {
                    "message": "Login successful",
                    "data": response_data,
                    
                }
                return Response(response, status=status.HTTP_200_OK)

            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid username or password"
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Bad request",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
