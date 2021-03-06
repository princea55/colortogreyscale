from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email already exists")
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, "You're are registered!")
                    return redirect('login')
        else:
            messages.error(request, "Both passowrd should be match")
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user= auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, "You're logged in")
            return redirect("upload")
        else:
            messages.error(request, "Invalied Username or Password")
            return redirect("login")
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('upload')
    