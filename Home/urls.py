from django.urls import path
from Home.views import front
app_name = "Homepage"

urlpatterns = [
   
   path('', front, name='Homepage')
]   