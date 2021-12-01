from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from content.models import BlogPost, Category
from .models import Profile

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register_customer')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email ID already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password = password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not matching')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request, profile_slug):
    profile = Profile.objects.get(slug = profile_slug)
    user = User.objects.get(username = profile)
    blogs = BlogPost.objects.filter(author = user)
    context = {
        "blogs": blogs,
        "tags": {
        'Finance': 'Finance',
        'Fashion': 'Fashion',
        'Politics' : 'Politics',
        'Sports' : 'Sports',
        'Travel' : 'Travel',
        'Lifestyle' : 'Lifestyle',
        'Science' : 'Science',
        'Environment' : 'Environment',
        'Technology' : 'Technology',
        },
        "profile_det": profile,
        "user_det": user,
    }
    return render(request, "accounts/profile.html", context)