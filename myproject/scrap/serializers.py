from .models import Courdiv, College, ElectivesGroup, Department, Course

from rest_framework import serializers


class CourdivSerializer(serializers.ModelSerializer):
    """Serializer for Courdiv objects"""

    class Meta:
        model = Courdiv
        fields = ('name', 'code', 'final_opt', 'id')
        read_only_fields = ('id',)


class CollegeSerializer(serializers.ModelSerializer):
    """Serializer for College objects"""

    class Meta:
        model = College
        fields = ('name', 'code', 'courdiv', 'id')
        read_only_fields = ('id',)


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for ElectivesGroup objects"""

    class Meta:
        model = ElectivesGroup
        fields = ('name', 'code', 'courdiv', 'id')
        read_only_fields = ('id',)


class DeptSerializer(serializers.ModelSerializer):
    """Serializer for Department objects"""

    class Meta:
        model = Department
        fields = ('name', 'code', 'courdiv', 'college', 'id')
        read_only_fields = ('id',)


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course objects"""

    class Meta:
        model = Course
        fields = ('campus', 'cour_cd', 'cour_cls', 'isu_nm', 'dept', 'name',
                  'prof_nm', 'credit_time', 'time_room', 'relative_yn',
                  'lmt_yn', 'exch_cor_yn', 'attend_free_yn',
                  'no_supervisor_yn', 'flexible_term_yn', 'id')
        read_only_fields = ('id',)
