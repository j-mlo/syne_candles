from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages 
from products.models import Product

# Create your views here.
def view_basket(request):
    """ A view to render shopping basket"""
    
    return render(request, "basket/basket.html")

def add_to_basket(request, item_id):
    """ Add a quantity of specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {basket[str(item_id)]}')
    else: 
        basket[item_id] = quantity
        messages.success(request, f'Added {product.name} to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)