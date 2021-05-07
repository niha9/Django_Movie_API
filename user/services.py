from rest_framework import status
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer
from user.utils import generate_jwt_token


class UserService:
    def register(self, data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.create(validated_data=serializer.validated_data)
            # generating JWT token
            token = generate_jwt_token(user)
    
            return Response(
                {
                    'access_token': token
                },
                status=status.HTTP_200_OK
            )
        # response on validation error
        return Response(
            {
                'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

   