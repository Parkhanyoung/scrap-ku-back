from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions

from user.serializers import UserSerializer
# Create your views here.


class UserCreateAPIView(APIView):
    """Create user"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserManageAPIView(APIView):
    """Manage authenticated user[retrieve & update]"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Return a currently authenticated user"""
        return self.request.user

    def get(self, request):
        """Retrieve a currently authenticated user"""
        user = self.get_object()
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Partially update a currently authenticated user"""
        user = self.get_object()
        serializer = UserSerializer(user, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
