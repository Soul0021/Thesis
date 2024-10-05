from django.urls import path
from Home.views import front
from userauths import views

app_name = "Homepage"

urlpatterns = [
   
   path('', front, name='root'),  # Define a URL pattern for the root URL
   path('Home/', front, name='Homepage'),
   path('Home/login/', views.login_view, name='login')
]