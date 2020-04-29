from django.shortcuts import render, redirect
from .models import UserDetails
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserDetails
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
import re 



# Create your views here.

def index(request):
    users = []
    if request.user.is_authenticated :
        username = request.user.username
        # print('authentication success !! for {}'.format(request.user.username))
        users = UserDetails.objects.filter(username = username)
    print(users)
    return render(request, 'homepage.html', {'users':users})


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        print(password1)

        if password1 == password2:
            if(string_check.search(password1) != None):
                messages.info(request, 'Password must not have special characters')
                return redirect('register')
            elif len(password1) < 8:
                messages.info(request, 'Password length is too short')
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif UserDetails.objects.filter(email = email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif len(phone) != 10:
                messages.info(request, 'Phone no. must have 10 digits')
                return redirect('register')
            elif UserDetails.objects.filter(phone = phone).exists():
                messages.info(request, 'Phone number already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password = password1)
                user.save()
                userd = UserDetails()
                userd.name = name 
                userd.email = email 
                userd.phone = phone 
                userd.username = username
                userd.save()
                print('user userd saved')
                return redirect('login')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('register')

    return render(request, 'register.html')


# def register(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         username = request.POST['username']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         messages = []
#         if password1 == password2:
#         elif User.objects.filter(username = username).exists():
#             messages.info(request, 'Username already exists')
#             return redirect('register')
#         elif UserDetails.objects.filter(email = email).exists():
#             messages.info(request, 'Email already exists')
#             return redirect('register')
#         elif UserDetails.objects.filter(phone = phone).exists():
#             messages.info(request, 'Phone already exists')
#             return redirect('register')
#         else:
#             user = User.objects.create_user(username = username, password = password1)
#             user.save()
#             userd = UserDetails()
#             userd.name = name 
#             userd.email = email 
#             userd.phone = phone 
#             userd.username = username
#             userd.save()
#             print('user saved')
#             return redirect('login')
        # else:
        #     messages.info(request, 'Passwords not matching')
        #     return redirect('register')

    # return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    logout_user(request)
    return redirect('index')
    
    

