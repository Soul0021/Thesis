from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomPasswordChangeForm
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Signup Page
def signup_view(request):
    if request.method == 'POST':
        print("POST request received")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('userauths:dashboard')  # Redirect to dashboard after signup
        else:
            print("Form is invalid:", form.errors)
    else:
        form = UserCreationForm()
    
    return render(request, 'userauths/sign-up.html', {'form': form})

# Login Page
def login_view(request):
    if request.user.is_authenticated:
        return redirect('userauths:dashboard')  # Redirect authenticated users to the dashboard

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # try:
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     messages.warning(request, f"User with {email} doesn't exist.")
        #     return render(request, "userauths/sign-in.html", {"error": "User does not exist"})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("userauths:dashboard")  # Redirect to dashboard after login
        else:
            messages.warning(request, f"User {email} does not exist", {"error": "Invalid password. Please try again."})

    return render(request, "userauths/login.html")

# Dashboard Page
def dashboard_view(request):
    # Ensure the user is logged in to access the dashboard
    if not request.user.is_authenticated:
        return redirect('userauths:login')

    return render(request, 'userauths/dashboard.html', {'user': request.user})

def level_view(request):
    # Ensure the user is logged in to access the level page
    if not request.user.is_authenticated:
        return redirect('userauths:login')

    return render(request, 'userauths/level.html', {'user': request.user})


def logout_view(request):
    logout(request)
    request.session.delete()
    messages.success(request, "Logout Successfully")
    return redirect("userauths:login")



def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'userauths/change_password.html', {'form': form})