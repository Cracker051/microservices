from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import MyUser
from .serializers import MyUserSerializer


class TestAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'ok!'
        }
        return Response(content)


class UserList(APIView):
    def get(self, request, format=None):
        users = MyUser.objects.all()
        serialized_users = MyUserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serialized_user = MyUserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
