from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash

def home(request):
    return render(request, 'board/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('projecthub')
        else:
            messages.error(request, "Invalid username or password")
     
           
   
    return render(request, 'board/login.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not full_name or not email or not username or not password:
            messages.error(request, "All fields are required")
            return render(request, 'board/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'board/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login') 

    return render(request, 'board/register.html')


def projecthub(request):
    return render(request, 'board/projecthub.html')


def profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')

        password = request.POST.get('password')
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully")

    return render(request, 'board/profile.html')

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect('home') 