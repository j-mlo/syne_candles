from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def view_basket(request):
    """ A view to render home page"""
    
    return render(request, "basket/basket.html")