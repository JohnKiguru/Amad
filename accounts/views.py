from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth, User
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import RegistrationForm, UserLoginForm

def home(request):
    return render(request, 'index.html')
def login(request):
    if request.method == 'POST':

        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('shop')
        else:
            print('Something went wrong')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':

        if request.POST['password'] == request.POST['confirm_password']:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, "Email already taken")
            else:
                user = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    #password=set_password(request.POST['first_name']),
                )
                user.set_password(request.POST['password'])
                user.save()
                return redirect('login')
        else:
            messages.error(request, "Passwords don't match")
        print(request.POST)
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('home')