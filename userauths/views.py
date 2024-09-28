from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Signup Page
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Homepage:Homepage') 
    else:
        form = UserCreationForm()
    
    return render(request, 'userauths/sign-up.html', {'form': form})

# Login Page
def login_view(request):
    if request.user.is_authenticated:
            return render(request, 'userauths/login.html')  

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} doesn't exist.")
            return render(request, "userauths/sign-in.html")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("Homepage:Homepage")
        else:
            messages.warning(request, "Invalid password. Please try again.")

    return render(request, "userauths/sign-in.html")
