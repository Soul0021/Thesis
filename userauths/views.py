from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout,  get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomPasswordChangeForm
from django.conf import settings
from .models import UserProgress, Level, RoadmapStep
from django.contrib.auth.decorators import login_required

User  = get_user_model()

# Signup Page
def signup_view(request):
    if request.method == 'POST':
        print("POST request received")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('userauths:dashboard') 
        else:
            print("Form is invalid:", form.errors)
    else:
        form = UserCreationForm()
    
    return render(request, 'userauths/sign-up.html', {'form': form})

# Login Page
def login_view(request):
    if request.user.is_authenticated:
        return redirect('userauths:dashboard') 

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # try:
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     messages.warning(request, f"User  with {email} doesn't exist.")
        #     return render(request, "userauths/sign-in.html", {"error": "User  does not exist"})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("userauths:dashboard")  # Redirect to dashboard after login
        else:
            messages.warning(request, f"User  {email} does not exist", {"error": "Invalid password. Please try again."})

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
            return redirect('userauths:dashboard')  # Changed here
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'userauths/change_password.html', {'form': form})


def roadmap_view(request, level):
    if not request.user.is_authenticated:
        return redirect('userauths:login')

    # Fetch the corresponding level object
    try:
        level_obj = Level.objects.get(name=level)
    except Level.DoesNotExist:
        return redirect('userauths:dashboard')  # Redirect if the level doesn't exist

    # Fetch user progress related to the level and the logged-in user
    user_progress = UserProgress.objects.filter(user=request.user, level=level_obj)

    # Prepare the roadmap steps (assuming you have a model for steps)
    roadmap_steps = RoadmapStep.objects.filter(level=level_obj).order_by('id')

    # Create a context that indicates the status of each step
    roadmap = []
    for i, step in enumerate(roadmap_steps):
        if i == 0:  # First lesson unlocked
            status = 'completed' if user_progress.filter(roadmap_step=step, status='completed').exists() else 'unlocked'
        else:
            # All other lessons are locked unless the previous one is completed
            previous_step_completed = user_progress.filter(roadmap_step=roadmap_steps[i - 1], status='completed').exists()
            status = 'completed' if user_progress.filter(roadmap_step=step, status='completed').exists() else 'locked' if previous_step_completed else 'locked'
        
        roadmap.append({
            'step': step,
            'status': status,
        })

    return render(request, 'userauths/roadmap.html', {'roadmap': roadmap})
