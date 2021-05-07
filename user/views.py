from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.services import UserService
user_service = UserService()


class UserRegisterationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return user_service.register(data=request.data)





