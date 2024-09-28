
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def front(request):
    return render(request,'Home/front.html')