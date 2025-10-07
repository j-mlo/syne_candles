from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """ A view to render home page"""
    
    return render(request, "home/index.html")