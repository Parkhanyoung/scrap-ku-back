from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from scrap.models import Courdiv, College, ElectivesGroup, Course, Department
from scrap.serializers import CourdivSerializer, CollegeSerializer, \
                                GroupSerializer, DeptSerializer


class SearchCategoryAPIView(APIView):
    """Retrieve categories for searching"""
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

    def get(self, request):
        obj = request.query_params.get('obj')
        courdiv = request.query_params.get('courdiv')
        college = request.query_params.get('college')

        if obj == 'college' and not courdiv:
            msg = {'QuerystringError': '/obj=college&courdiv=XX'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        elif obj == 'dept' and not (courdiv and college):
            msg = {'QuerystringError': '/obj=dept&courdiv=XX&college=XX'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if obj == 'college':
            data = self.get_seri_data(obj, courdiv)
        elif obj == 'dept':
            data = self.get_seri_data(obj, courdiv, college)
        elif obj == 'courdiv' or obj == 'group':
            data = self.get_seri_data(obj)
        else:
            msg = {'QuerystringError': '/obj=[courdiv/college/group/dept]'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)
