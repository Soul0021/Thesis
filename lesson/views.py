from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from userauths.views import *
# Quiz View: Checking answers and updating progress
@login_required
def quiz1(request, step=1):
    QUIZ_DATA = [
        {
            'vowels': [{'symbol': 'ㅣ', 'sound': 'i'}, {'symbol': 'ㅔ', 'sound': 'e'}, {'symbol': 'ㅖ', 'sound': 'ye'}, {'symbol': 'ㅐ', 'sound': 'ae'}, {'symbol': 'ㅡ', 'sound': 'eu'}, {'symbol': 'ㅛ', 'sound': 'yo'}],
            'sounds': [{'label': 'i', 'sound': 'i'}, {'label': 'e', 'sound': 'e'}, {'label': 'ye', 'sound': 'ye'}, {'label': 'ae', 'sound': 'ae'}, {'label': 'eu', 'sound': 'eu'}, {'label': 'yo', 'sound': 'yo'}]
        }
        # Add more quiz data for more steps
    ]
    
    if step > len(QUIZ_DATA):
        return redirect('quiz_completed')  # Redirect when quiz is complete
    
    quiz_data = QUIZ_DATA[step - 1]  # Load data based on step

    if request.method == "POST":
        # Process the answers
        correct_answers = [v['sound'] for v in quiz_data['vowels']]
        user_answers = []

        for i, vowel in enumerate(quiz_data['vowels']):
            user_answer = request.POST.get(f"answer_{i + 1}")
            user_answers.append(user_answer)

        # Check if user answers match the correct answers
        correct = all([user_answers[i] == correct_answers[i] for i in range(len(correct_answers))])

        if correct:
            # Mark step as completed and unlock the next step
            step_obj = get_object_or_404(RoadmapStep, order=step)
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user, roadmap_step=step_obj, level=step_obj.level
            )
            user_progress.status = 'completed'
            user_progress.save()

            # Unlock the next step
            next_step = RoadmapStep.objects.filter(level=step_obj.level, order=step_obj.order + 1).first()
            if next_step:
                UserProgress.objects.get_or_create(
                    user=request.user,
                    roadmap_step=next_step,
                    defaults={'status': 'unlocked'}
                )

            messages.success(request, "Correct! You've completed this step.")
        else:
            messages.error(request, "Incorrect! Try again.")

    context = {
        'quiz_data': quiz_data,
        'step': step,
        'total_steps': len(QUIZ_DATA),
    }

    return render(request, 'lesson/beginner1.html', context)
