from django.shortcuts import render, redirect
from scrap.models import Courdiv, College, ElectivesGroup, Department, Course
from scrap.scrappers import scrappers


def scrap_main(request):
    courdivs = Courdiv.objects.all()
    colleges_major = College.objects.filter(courdiv__name='전공')
    colleges_basic = College.objects.filter(courdiv__name='학문의기초')
    electives_groups = ElectivesGroup.objects.all()
    depts_major = Department.objects.filter(courdiv__name='전공')
    depts_basic = Department.objects.filter(courdiv__name='학문의기초')
    ctx = {
        'courdivs': courdivs,
        'colleges_major': colleges_major,
        'colleges_basic': colleges_basic,
        'electives_groups': electives_groups,
        'depts_major': depts_major,
        'depts_basic': depts_basic,
        }
    return render(request, 'scrap/scrap_main.html', ctx)


def scrap_college(request):
    """Scrap college data (pCol)"""
    courdiv_list = Courdiv.objects.filter(final_opt='dept')
    scrapper = scrappers.CollegeGroupScrapper()

    for courdiv in courdiv_list:
        scrapper.set_data(courdiv_code=courdiv.code)
        scrapped_data = scrapper.scrap()

        for data in scrapped_data:
            existing_college = College.objects.filter(name=data['name'])
            if existing_college:
                existing_college.first().courdiv.add(courdiv)
            else:
                created_college = College.objects.create(
                    name=data['name'],
                    code=data['code'],
                    rowid=data['rowid']
                )
                created_college.courdiv.add(courdiv)

    return redirect('scrap:scrap-main')


def scrap_group(request):
    """Scrap electives group data (pGroupCd)"""
    courdiv = Courdiv.objects.get(name='교양')
    scrapper = scrappers.CollegeGroupScrapper()
    scrapper.set_data()
    scrapped_data = scrapper.scrap()

    existing_group = ElectivesGroup.objects.first()
    if existing_group:
        pass
    else:
        for data in scrapped_data:
            ElectivesGroup.objects.create(
                name=data['name'],
                code=data['code'],
                rowid=data['rowid'],
                courdiv=courdiv
            )

    return redirect('scrap:scrap-main')


def scrap_dept(request):
    """Scrap department data"""
    courdivs = Courdiv.objects.filter(final_opt='dept')
    scrapper = scrappers.DeptScrapper()
    for courdiv in courdivs:
        for college in courdiv.colleges.all():
            scrapper.set_data(college.code, courdiv.code)
            scrapped_data = scrapper.scrap()
            for data in scrapped_data:
                existing_dept = Department.objects.filter(name=data['name'])
                if existing_dept:
                    existing_dept.first().courdiv.add(courdiv)
                else:
                    created_dept = Department.objects.create(
                        name=data['name'],
                        code=data['code'],
                        college=college
                    )
                    created_dept.courdiv.add(courdiv)

    return redirect('scrap:scrap-main')


def scrap_course_dept(request):
    """Scrap course data searched by dept[전공,학문의기초]"""
    courdivs = Courdiv.objects.filter(final_opt='dept')
    scrapper = scrappers.CourseScrapper()
    if Course.objects.filter(courdiv__name='전공'):
        pass
    else:
        for courdiv in courdivs:
            for college in courdiv.colleges.all():
                for dept in college.depts.all():
                    scrapper.set_data(courdiv.code, dept_code=dept.code)
                    scrapped_data = scrapper.scrap()
                    for data in scrapped_data:
                        Course.objects.create(
                            name=data['cour_nm'],
                            courdiv=courdiv,
                            rowid=data['rowid'],
                            campus=data['campus'],
                            dept=data['department'],
                            cour_cd=data['cour_cd'],
                            cour_cls=data['cour_cls'],
                            isu_nm=data['isu_nm'],
                            prof_nm=data['prof_nm'],
                            credit=data['credit'],
                            credit_time=data['time'],
                            time_room=data['time_room'],
                            relative_yn=data['absolute_yn'],
                            lmt_yn=data['lmt_yn'],
                            exch_cor_yn=data['exch_cor_yn'],
                            attend_free_yn=data['attend_free_yn'],
                            no_supervisor_yn=data['no_supervisor_yn'],
                            flexible_term_yn=data['flexible_term'],
                            searched_by_d=dept
                        )

    return redirect('scrap:scrap-main')


def scrap_course_group(request):
    """Scrap course data searched by electives group[교양]"""
    courdiv = Courdiv.objects.get(final_opt='group')
    scrapper = scrappers.CourseScrapper()
    if Course.objects.filter(courdiv__name='교양'):
        pass
    else:
        for group in courdiv.groups.all():
            scrapper.set_data(courdiv.code, group_code=group.code)
            scrapped_data = scrapper.scrap()
            for data in scrapped_data:
                Course.objects.create(
                    name=data['cour_nm'],
                    courdiv=courdiv,
                    rowid=data['rowid'],
                    campus=data['campus'],
                    dept=data['department'],
                    cour_cd=data['cour_cd'],
                    cour_cls=data['cour_cls'],
                    isu_nm=data['isu_nm'],
                    prof_nm=data['prof_nm'],
                    credit=data['credit'],
                    credit_time=data['time'],
                    time_room=data['time_room'],
                    relative_yn=data['absolute_yn'],
                    lmt_yn=data['lmt_yn'],
                    exch_cor_yn=data['exch_cor_yn'],
                    attend_free_yn=data['attend_free_yn'],
                    no_supervisor_yn=data['no_supervisor_yn'],
                    flexible_term_yn=data['flexible_term'],
                    searched_by_g=group
                    )

    return redirect('scrap:scrap-main')


def scrap_course_cd(request):
    """Scrap course data searched by cour_div[교직,군사학,평생교육사]"""
    courdivs = Courdiv.objects.filter(final_opt='courdiv')
    scrapper = scrappers.CourseScrapper()
    if Course.objects.filter(courdiv__name='교직'):
        pass
    else:
        for courdiv in courdivs:
            scrapper.set_data(courdiv.code)
            scrapped_data = scrapper.scrap()
            for data in scrapped_data:
                Course.objects.create(
                    name=data['cour_nm'],
                    courdiv=courdiv,
                    rowid=data['rowid'],
                    campus=data['campus'],
                    dept=data['department'],
                    cour_cd=data['cour_cd'],
                    cour_cls=data['cour_cls'],
                    isu_nm=data['isu_nm'],
                    prof_nm=data['prof_nm'],
                    credit=data['credit'],
                    credit_time=data['time'],
                    time_room=data['time_room'],
                    relative_yn=data['absolute_yn'],
                    lmt_yn=data['lmt_yn'],
                    exch_cor_yn=data['exch_cor_yn'],
                    attend_free_yn=data['attend_free_yn'],
                    no_supervisor_yn=data['no_supervisor_yn'],
                    flexible_term_yn=data['flexible_term'],
                )

    return redirect('scrap:scrap-main')


def delete_data(request):
    """Delete all of data except for courdiv"""
    College.objects.all().delete()
    ElectivesGroup.objects.all().delete()
    Department.objects.all().delete()
    Course.objects.all().delete()
    return redirect('scrap:scrap-main')
