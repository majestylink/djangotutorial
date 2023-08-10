from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User


def signup(request):
    if request.method == 'POST':
        data = request.POST
        if data['password1'].strip() != data['password2'].strip():
            return redirect('recipe:index')
        email = data['email'].strip()
        username = data['username'].strip()
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        password = data['password1'].strip()
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        return redirect('recipe:index')
    return redirect('recipe:index')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            username = data['username'].strip()
            password = data['password'].strip()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipe:index')
        return redirect('recipe:index')
    else:
        return redirect('recipe:index')


def logout_view(request):
    logout(request)
    return redirect('recipe:index')
