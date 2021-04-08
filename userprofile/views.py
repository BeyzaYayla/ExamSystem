from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group

# Create your views here.
from exam.models import Exam

# creates new user with the input from form
# if the user_type is true assigns the user to 'instructor' group
# if false assigns the user to 'student' group
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_type = form.cleaned_data.get('user_type')

            if user_type:
                group = Group.objects.get(name='instructor')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='student')
                user.groups.add(group)

            user.save()

            messages.success(request, 'Account was created for ' + username)

            login(request, user)

            return redirect('frontpage')
    else:
        form = RegisterForm()

    return render(request, 'userprofile/register.html', {'form': form})

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('myaccount')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'userprofile/login.html', context)

# shows user profile if the user is an instructor shows the created exams too
@login_required
def myaccount(request):
    exams = Exam.objects.filter(instructor=request.user)
    return render(request, 'userprofile/myaccount.html', {'exams': exams})
