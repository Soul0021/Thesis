from django.urls import path
from userauths import views


app_name = "userauths"

urlpatterns = [
    path('', views.login_view, name='root'),  # Define a URL pattern for the root URL
    path("sign-up/", views.signup_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('level/', views.level_view, name='level'),
    path('roadmap/<str:level>/', views.roadmap_view, name='roadmap'), 
    path('change_password/', views.change_password, name='change_password'),
    path('home/',views.logout_view , name='logout'),
    path('quiz/<int:step>/', views.quiz1, name='quiz1'),  # Quiz navigation
    path('quiz-completed/', views.quiz_complete_view, name='quiz_completed'),
]
