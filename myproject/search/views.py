from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from django.shortcuts import get_object_or_404

from scrap.models import Courdiv, College, ElectivesGroup, Department, Course 
from scrap.serializers import CourdivSerializer, CollegeSerializer, \
                              GroupSerializer, DeptSerializer, CourseSerializer


class SearchBaseAPIView(APIView):
    """Base APIView for searching categories"""
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get_seri_data(self, obj, courdiv=None, college=None):
        """Return appropriate serialized data according to obj"""
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
            msg = {"QuerystringError": "courdiv or college is not given"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        data = self.get_seri_data('dept', courdiv, college)
        return Response(data, status=status.HTTP_200_OK)


class SearchCourseAPIView(APIView):
    """Return a list of courses which meet the conditions"""
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes  = (permissions.IsAuthenticated,)

    def first_filter_default(self, courdiv_nm=None,
                             dept_nm=None, group_nm=None):
        """filters course objects[이수구분] and returns the queryset"""
        if  dept_nm:
            courses = Course.objects.filter(searched_by_d__name=dept_nm)
            courses = courses.filter(courdiv__name=courdiv_nm)
            return courses
        elif group_nm:
            courses = Course.objects.filter(searched_by_g__name=group_nm)
            return courses
        elif courdiv_nm:
            courses = Course.objects.filter(courdiv__name=courdiv_nm)
            return courses

    def first_filter_optional(self, cour_cd=None, cour_nm=None):
        """Filter course objects[학수번호 및 교과목명] and returns the queryset"""
        if (cour_cd and cour_nm):
            courses = Course.objects.filter(cour_cd__contains=cour_cd)
            courses = courses.filter(name__contains=cour_nm)
            return courses
        elif cour_cd:
            courses = Course.objects.filter(cour_cd__contains=cour_cd)
            return courses
        elif cour_nm:
            courses = Course.objects.filter(name__contains=cour_nm)
            return courses

    def second_filter(self, queryset, credit=None, day=None,
                      prof_nm=None, cour_cls=None):
        """Secondarily filter course objects and returns the queryset"""
        courses = queryset
        if credit:
            courses = courses.filter(credit=credit)
        if day:
            courses = courses.filter(time_room__contains=day)
        if prof_nm:
            courses = courses.filter(prof_nm__contains=prof_nm)
        if cour_cls:
            courses = courses.filter(cour_cls=cour_cls)

        serializer = CourseSerializer(courses, many=True)
        return serializer.data

    def get(self, request):
        """Return a list of courses meets all the conditions"""
        courdiv_nm = request.query_params.get('courdiv')
        group_nm = request.query_params.get('group')
        dept_nm = request.query_params.get('dept')
        cour_cd = request.query_params.get('cour_cd')
        cour_nm = request.query_params.get('cour_nm')
        if (cour_cd or cour_nm):
            courses = self.first_filter_optional(cour_cd, cour_nm)
        elif (courdiv_nm or group_nm):
            courses = self.first_filter_default(courdiv_nm, dept_nm, group_nm)
        elif not (cour_cd or cour_nm or courdiv_nm or group_nm):
            msg = {'QuerystringError': 'Querystring is not appropriate'}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        credit = request.query_params.get('credit')
        day = request.query_params.get('day')
        prof_nm = request.query_params.get('prof_nm')
        cour_cls = request.query_params.get('cour_cls')
        courses_data = self.second_filter(
            courses, credit, day, prof_nm, cour_cls
            )
        return Response(courses_data, status=status.HTTP_200_OK)


class RetrieveCourseAPIView(APIView):
    """Retrieve a course with primary key"""
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes  = (permissions.IsAuthenticated,)
    def get_object(self, pk):
        return Course.objects.filter(pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        if course:
            serializer = CourseSerializer(course, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
