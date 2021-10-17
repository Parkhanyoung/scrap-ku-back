from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from scrap.models import Courdiv, College, ElectivesGroup, Course, Department
from scrap.serializers import CourdivSerializer, CollegeSerializer, \
                                GroupSerializer, DeptSerializer


class SearchBaseAPIView(APIView):
    """Base APIView for searching categories"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_seri_data(self, obj, courdiv=None, college=None):
        """Return appropriate serializer data according to obj"""
        if obj == 'courdiv':
            objs = Courdiv.objects.all()
            serializer = CourdivSerializer(objs, many=True)
        if obj == 'college':
            objs = College.objects.filter(courdiv__name=courdiv)
            serializer = CollegeSerializer(objs, many=True)
        if obj == 'group':
            objs = ElectivesGroup.objects.all()
            serializer = GroupSerializer(objs, many=True)
        if obj == 'dept':
            objs = Department.objects.filter(courdiv__name=courdiv)
            objs = objs.filter(college__name=college)
            serializer = DeptSerializer(objs, many=True)

        return serializer.data


class SearchCourdivAPIView(SearchBaseAPIView):
    """Return a list of courdivs"""

    def get(self, request):
        data = self.get_seri_data('courdiv')
        return Response(data, status=status.HTTP_200_OK)


class SearchCollegeAPIView(SearchBaseAPIView):
    """Return a list of colleges"""

    def get(self, request):
        courdiv = request.query_params.get('courdiv')
        if not courdiv:
            msg = {"QuerystringError": "Courdiv info is not given"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        data = self.get_seri_data('college', courdiv)
        return Response(data, status=status.HTTP_200_OK)


class SearchGroupAPIView(SearchBaseAPIView):
    """Return a list of electivesgroup"""

    def get(self, request):
        data = self.get_seri_data('group')
        return Response(data, status=status.HTTP_200_OK)


class SearchDeptAPIView(SearchBaseAPIView):
    """Return a list of dept"""

    def get(self, request):
        courdiv = request.query_params.get('courdiv')
        college = request.query_params.get('college')
        if not (courdiv and college):
            msg = {"QuerystringError": "courdiv or college are not given"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        data = self.get_seri_data('dept', courdiv, college)
        return Response(data, status=status.HTTP_200_OK)
