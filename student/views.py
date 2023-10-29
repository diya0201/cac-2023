from django.http import JsonResponse
from django.contrib import messages
from core.models import CustomUser
from educator.models import StudyGroup
from .models import DayData, UploadedText, UploadedFile
from django.shortcuts import render, redirect
import calendar
from .forms import TextUploadForm, FileUploadForm, JoinGroupForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.utils import timezone
import random


def save_day_data(request):
    if request.method == "POST" and request.is_ajax():
        day_date = request.POST.get('date')
        data = request.POST.get('data')
        day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date)
        day_data.data = data
        day_data.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})


def calendar_view(request, group_id):
    return render(request, 'student/calendar.html', {'group_id': group_id})


@login_required
def daydetail(request, day, month, year, group_id):
    current_month = int(month)  # for example, October
    current_year = int(year)  # for example, year 2023
    day_date = date(current_year, current_month, int(day))
    day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date, group_id=group_id)

    if request.method == 'POST':
        form = TextUploadForm(request.POST)
        if form.is_valid():
            text_instance = form.save(commit=False)
            text_instance.user = request.user
            text_instance.date = day_date
            text_instance.group_id = group_id
            text_instance.save()
            return redirect('daydetail', day=int(day), month=current_month, year=current_year, group_id=group_id)
    else:
        form = TextUploadForm()

    # Fetch all texts uploaded by the user for this day
    texts = UploadedText.objects.filter(user=request.user, date=day_date, group_id=group_id).order_by('-timestamp')

    file_form = FileUploadForm(request.POST, request.FILES or None)
    if file_form.is_valid():
        file_instance = file_form.save(commit=False)
        file_instance.user = request.user
        file_instance.date = day_date
        file_instance.group_id = group_id
        file_instance.save()

    uploaded_files = UploadedFile.objects.filter(user=request.user, date=day_date, group_id=group_id)
    practice_time = day_data.practice_time

    return render(request, 'student/daydetail.html', {'day': day, 'form': form, 'texts': texts, 'file_form': file_form, 'uploaded_files': uploaded_files, 'practice_time': practice_time, 'group_id': group_id, 'month': current_month, 'year': current_year})


@method_decorator(csrf_exempt, name='dispatch')
class SavePracticeTimeView(View):
    def post(self, request, day, month, year, **kwargs):
        current_month = int(month)  # for example, October
        current_year = int(year)  # for example, year 2023
        day_date = date(current_year, current_month, day)
        day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date)
        data = json.loads(request.body)
        practice_time = data.get('practice_time')
        day_data.practice_time += int(practice_time)
        day_data.save()

        return JsonResponse({'message': 'Time saved successfully!'})


@login_required
def analytics(request, group_id, month, year):
    current_time = timezone.now()
    if month == current_time.month and year == current_time.year:
        day = current_time.day
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        day = 31
    elif month in [4, 6, 9, 11]:
        day = 30
    elif (year % 400) == 0:
        day = 29
    elif (year % 100) == 0:
        day = 28
    elif (year % 4) == 0:
        day = 29
    else:
        day = 28
    current_month = month
    current_year = year
    day_date = date(current_year, current_month, day)
    day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date, group_id=group_id)
    total = 0
    practice_times = []
    dates = []
    for i in range(1, day+1):
        dates.append(i)
        day_date = date(current_year, current_month, i)
        day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date, group_id=group_id)
        practice_times.append(day_data.practice_time)
        total += day_data.practice_time
    return render(request, 'student/analytics.html', {'total': total, 'practice_times': practice_times, 'dates': dates})


@login_required
def student_dashboard(request):
    day_date = timezone.now().date()
    day_data, created = DayData.objects.get_or_create(user=request.user, date=day_date)
    student_groups = StudyGroup.objects.filter(students__username=request.user)
    if not day_data.small_claimed:
        print('hi')
        for student_group in student_groups:
            if day_data.practice_time > 0:
                day_data.small_claimed = True
                request.user.profile.save()
                request.user.profile.coins += 10
                request.user.profile.save()
    if not day_data.big_claimed:
        for student_group in student_groups:
            if day_data.practice_time >= student_group.practice_goal:
                day_data.big_claimed = True
                request.user.profile.save()
                request.user.profile.coins += 30
                request.user.profile.save
    print(request.user.profile.coins)
    if request.method == 'POST':
        form = JoinGroupForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data['join_code']
            group = StudyGroup.objects.filter(join_code=join_code).first()
            if group:
                group.students.add(request.user)
                messages.success(request, 'Successfully joined the group!')
            else:
                messages.error(request, 'Invalid join code. Please try again.')
    else:
        form = JoinGroupForm()
    user_pk = request.user.pk
    user_instance = CustomUser.objects.get(pk=user_pk)
    groups = user_instance.student_groups.all()
    return render(request, 'student/dashboard.html', {'groups': groups, 'form': form})


@login_required
def get_practice_time(request, day, month, year, group_id):
    start_date = date(int(year), int(month), int(day))
    day_data_records, created = DayData.objects.get_or_create(user=request.user, date=start_date, group_id=group_id)
    if created:
        practice_time = 0
    else:
        practice_time = day_data_records.practice_time
    group = StudyGroup.objects.get(id=group_id)
    practice_goal = group.practice_goal * 60
    return JsonResponse({'practice_time': practice_time, 'practice_goal': practice_goal}, safe=False)


@login_required
def beat_the_met(request):
    if int(request.user.profile.coins) >= 10:
        print('can play!')
        high_score = request.user.profile.high_score_met
        target = random.randint(90, 150)
        return render(request, 'student/beat_the_met.html', {'high_score_met': high_score, 'target': target})
    else:
        return redirect('student_dashboard')


@login_required
def update_high_score_met(request):
    request.user.profile.coins -= 10
    request.user.profile.save()
    new_score = int(request.POST.get('new_score', 0))
    high_score = int(request.user.profile.high_score_met)
    target = random.randint(90, 150)

    if new_score > high_score:
        request.user.profile.high_score_met = new_score
        request.user.profile.save()
    print(request.user.profile.coins)
    return redirect('beat_the_met')



