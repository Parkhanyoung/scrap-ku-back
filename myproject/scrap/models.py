from django.db import models


class Courdiv(models.Model):
    """Courdiv information (pCourDiv)"""
    final_opt_choices = (
        ('dept', 'dept'),
        ('group', 'group'),
        ('courdiv', 'courdiv')
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    rowid = models.CharField(max_length=10)
    final_opt = models.CharField(max_length=255, choices=final_opt_choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('rowid',)


class College(models.Model):
    """College data (pCol)"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    rowid = models.CharField(max_length=255)
    courdiv = models.ManyToManyField('Courdiv', related_name='colleges')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ElectivesGroup(models.Model):
    """Group data of Electives (pGroupCd)"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    rowid = models.CharField(max_length=255)
    courdiv = models.ForeignKey(
        'Courdiv',
        on_delete=models.CASCADE,
        related_name='groups'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Department(models.Model):
    """Department data (pDept)"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    courdiv = models.ManyToManyField('Courdiv', related_name='depts')
    college = models.ForeignKey(
        'College',
        on_delete=models.CASCADE,
        related_name='depts'
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Course(models.Model):
    """Course data"""
    name = models.CharField(max_length=255)
    courdiv = models.ForeignKey(
    'Courdiv', on_delete=models.CASCADE, related_name='courses'
    )
    rowid = models.CharField(max_length=5)
    campus = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    cour_cd = models.CharField(max_length=255)
    cour_cls = models.CharField(max_length=255)
    isu_nm = models.CharField(max_length=255)
    prof_nm = models.CharField(max_length=255)
    credit = models.CharField(max_length=5)
    credit_time = models.CharField(max_length=255)
    time_room = models.CharField(max_length=255)
    relative_yn = models.CharField(max_length=5)
    lmt_yn = models.CharField(max_length=5)
    exch_cor_yn = models.CharField(max_length=5)
    attend_free_yn = models.CharField(max_length=5)
    no_supervisor_yn = models.CharField(max_length=5)
    flexible_term_yn = models.CharField(max_length=5)
    searched_by_d = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='courses',
        blank=True,
        null=True
        )
    searched_by_g = models.ForeignKey(
        'ElectivesGroup',
        on_delete=models.CASCADE,
        related_name='courses',
        blank=True,
        null=True
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
