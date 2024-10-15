from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .forms import UserCreationForm, CustomPasswordChangeForm
from django.urls import reverse
from .models import UserProgress, Level, RoadmapStep
from django.contrib.auth.decorators import login_required
from .models import Vowel
# Signup Page
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('userauths:dashboard')
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
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("userauths:dashboard")
        else:
            messages.warning(request, "Invalid email or password.")

    return render(request, "userauths/login.html")

# Dashboard Page
@login_required
def dashboard_view(request):
    return render(request, 'Home/dashboard.html', {'user': request.user})

# Level Page
@login_required
def level_view(request):
    return render(request, 'Home/level.html', {'user': request.user})

# Logout Function
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("userauths:login")

# Change Password
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userauths:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'userauths/change_password.html', {'form': form})

# Roadmap View
@login_required
def roadmap_view(request, level):
    level_obj = get_object_or_404(Level, name=level)
    user_progress = UserProgress.objects.filter(user=request.user, level=level_obj)
    roadmap_steps = RoadmapStep.objects.filter(level=level_obj).order_by('id')

    roadmap = []
    for i, step in enumerate(roadmap_steps):
        completed = user_progress.filter(roadmap_step=step, status='completed').exists()
        if i == 0:
            status = 'completed' if completed else 'unlocked'
        else:
            previous_step_completed = user_progress.filter(roadmap_step=roadmap_steps[i - 1], status='completed').exists()
            status = 'completed' if completed else ('locked' if not previous_step_completed else 'unlocked')
        
        roadmap.append({
            'step': step,
            'status': status,
            'quiz_url': reverse('userauths:quiz1', kwargs={'step': step.id})
        })

    return render(request, 'userauths/roadmap.html', {'roadmap': roadmap})

# Combined Quiz View (Rendering `quiz1.html`)
@login_required
def quiz1(request, step=1):
    QUIZ_DATA = [
        {'vowels': [{'symbol': 'ㅣ', 'sound': 'i'}, {'symbol': 'ㅔ', 'sound': 'e'}, {'symbol': 'ㅖ', 'sound': 'ye'}, {'symbol': 'ㅐ', 'sound': 'ae'}, {'symbol': 'ㅡ', 'sound': 'eu'}, {'symbol': 'ㅛ', 'sound': 'yo'}],
         'sounds': [{'label': 'i', 'sound': 'i'}, {'label': 'e', 'sound': 'e'}, {'label': 'ye', 'sound': 'ye'}, {'label': 'ae', 'sound': 'ae'}, {'label': 'eu', 'sound': 'eu'}, {'label': 'yo', 'sound': 'yo'}]
        }
    ]

    if step > len(QUIZ_DATA):
        return redirect('quiz_completed')  # Redirect when quiz is complete

    quiz_data = QUIZ_DATA[step - 1]
    correct_answer = quiz_data['vowels'][0]['sound']

    if request.method == 'POST':
        user_answer = request.POST.get('answer')

        if user_answer.lower() == correct_answer.lower():
            correct = True
        else:
            correct = False
            incorrect = True

        return render(request, 'lesson/b_day1/beginner1.html', {'quiz_data': quiz_data, 'correct': correct, 'incorrect': incorrect, 'correct_answer': correct_answer})
    else:
        return render(request, 'lesson/b_day1/beginner1.html', {'quiz_data': quiz_data})

# Mark quiz as complete and unlock next step
@login_required
def quiz_complete_view(request, step_id):
    step = get_object_or_404(RoadmapStep, id=step_id)
    
    if step.is_quiz:
        progress, created = UserProgress.objects.get_or_create(user=request.user, roadmap_step=step, level=step.level)
        progress.status = 'completed'
        progress.save()

        # Unlock the next step
        next_step = RoadmapStep.objects.filter(level=step.level, order=step.order + 1).first()
        if next_step:
            UserProgress.objects.get_or_create(user=request.user, roadmap_step=next_step, level=step.level, defaults={'status': 'unlocked'})

    return redirect('roadmap', level=step.level.name)


def quiz_view(request):
    if request.method == 'POST':
        selected_vowel = request.POST.get('selected_vowel')
        selected_sound = request.POST.get('selected_sound')

        # Fetch the correct answer from the database for the selected vowel
        vowel = get_object_or_404(Vowel, symbol=selected_vowel)
        correct_sound = vowel.sound

        # Check if the selected sound is correct
        if selected_sound == correct_sound:
            messages.success(request, f'Correct! {selected_vowel} matches with {selected_sound}.')
        else:
            messages.error(request, f'Incorrect. {selected_vowel} does not match with {selected_sound}. The correct sound is {correct_sound}.')

    # Fetch vowels and sounds data from the database
    quiz_data = {
        'vowels': Vowel.objects.all(),
        'sounds': Vowel.objects.values_list('sound', flat=True).distinct()
    }

    return render(request, 'quiz_template.html', {'quiz_data': quiz_data})