from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.serializers import UserSerializer
# Create your views here.


class UserCreateAPIView(APIView):
    """function for creating and listing user"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
