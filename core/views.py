from django.shortcuts import render, redirect
from educator.models import StudyGroup
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate


def welcome(request):
    return render(request, 'core/welcome.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            join_code = form.cleaned_data.get('join_code')
            if join_code == '000000':
                login(request, user)
            else:
                group = StudyGroup.objects.filter(join_code=join_code).first()
                if group:
                    login(request, user)
                    group.students.add(user)
                    return redirect('welcome')
                else:
                    form.add_error('join_code', 'Invalid join code.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'STUDENT':
                return redirect('student_dashboard')
            elif user.user_type == 'EDUCATOR':
                return redirect('educator_classes')
            else:
                return redirect('register')
        else:
            # Invalid authentication
            pass
    return render(request, 'core/signin.html')
