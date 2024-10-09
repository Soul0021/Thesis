from django.http import HttpResponse
from django.shortcuts import render

def front_view(request):
    return render(request, 'Home/front.html')

def about_us_view(request):
    return render(request , 'Home/aboutus.html')