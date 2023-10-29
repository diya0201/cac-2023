from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from student.models import DayData, UploadedText, UploadedFile
from core.models import CustomUser
from educator.forms import StudyGroupForm
from educator.models import StudyGroup
from student.models import DayData
from datetime import date


@login_required
def group_list(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.educator = request.user
            group.save()
            return redirect('educator_classes')  # Redirect to the same page after creating the group
    else:
        form = StudyGroupForm()

    groups = StudyGroup.objects.filter(educator=request.user)
    return render(request, 'educator/classes.html', {'groups': groups, 'form': form})


@login_required
def group_detail(request, group_id):
    study_group = StudyGroup.objects.get(id=group_id)
    students = study_group.students.all()
    students_data = []
    for student in students:
        total_time = DayData.objects.filter(user=student).aggregate(total_time=Sum('practice_time'))['total_time'] or 0
        students_data.append({
            'student': student,
            'total_time': int(total_time/60)
        })
    practice_goal = study_group.practice_goal

    return render(request, 'educator/group_detail.html', {'study_group': study_group, 'students_data': students_data, 'practice_goal': practice_goal, 'group_id': group_id})


@login_required
def view_student_calendar(request, student_id, group_id):
    if not request.user.user_type == 'EDUCATOR':
        return HttpResponseForbidden("You don't have permission to access this page.")
    # student = CustomUser.objects.get(id=student_id)
    return render(request, 'educator/student_calendar.html', {'student': student_id, 'group_id': group_id})


@login_required
def get_student_practice_time(request, student_id, group_id, day, month, year):
    start_date = date(int(year), int(month), int(day))
    student = CustomUser.objects.get(id=student_id)
    day_data_records, created = DayData.objects.get_or_create(user=student, date=start_date, group_id=group_id)
    if created:
        practice_time = 0
    else:
        practice_time = day_data_records.practice_time
    group = StudyGroup.objects.get(id=group_id)
    practice_goal = group.practice_goal * 60
    return JsonResponse({'practice_time': practice_time, 'practice_goal': practice_goal}, safe=False)


@login_required
def student_daydetail(request, student_id, group_id, day, month, year):
    start_date = date(int(year), int(month), int(day))
    student = CustomUser.objects.get(id=student_id)
    day_data_records, created = DayData.objects.get_or_create(user=student, date=start_date, group_id=group_id)
    if created:
        practice_time = 0
    else:
        practice_time = day_data_records.practice_time
    group = StudyGroup.objects.get(id=group_id)
    practice_goal = group.practice_goal * 60
    uploaded_files = UploadedFile.objects.filter(user=student, date=start_date, group_id=group_id)
    texts = UploadedText.objects.filter(user=student, date=start_date, group_id=group_id).order_by('-timestamp')
    return render(request, 'educator/student_daydetail.html', {'day': day, 'practice_time': practice_time, 'texts': texts, 'uploaded_files': uploaded_files})
