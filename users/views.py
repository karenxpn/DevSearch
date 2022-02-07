from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm


def login_user(request):
    context = {'page': 'login'}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

        print(request.POST)
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.error(request, 'User was successfully logged out!')
    return redirect('login')


def register_user(request):
    form = CustomUserCreationForm()
    context = {'page': 'register',
               'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Your account was successfully created!')

            login(request, user)
            return redirect('profiles')

        else:
            messages.error(request, 'An error has occurred during registration')

    return render(request, 'users/login_register.html', context)


def profiles(request):
    all_profiles = Profile.objects.all()
    context = {'profiles': all_profiles}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/user-profile.html', context)
