from django.urls import path
from Home.views import front_view, about_us_view
from userauths import views

app_name = "Homepage"

urlpatterns = [
    path('', front_view, name='root'),
    path('Home/', front_view, name='Homepage'),
    path('Home/login/', views.login_view, name='login'),
    path('aboutus.html/', about_us_view, name='about_us'),
]