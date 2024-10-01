from django.urls import path
from userauths import views
from django.contrib.auth.views import LogoutView

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.signup_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name='dashboard')
]
