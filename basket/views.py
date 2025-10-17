from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages 
from products.models import Product

# Create your views here.
def view_basket(request):
    """ A view to render shopping basket"""
    
    return render(request, "basket/basket.html")

def add_to_basket(request, item_id):
    """ Add a quantity of specified product to the shopping basket """

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


def update_basket(request, item_id):
    """ Updates the quantity of specified product to the shopping basket with quantity input"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
    else: 
        basket.pop(item_id)
    
    request.session['basket'] = basket
    messages.success(request, f'{product.name} quantity has been updated')
    return redirect('basket')


def remove_from_basket(request, item_id):
    """ Removes item from the shopping basket"""

    try: 
        product = get_object_or_404(Product, pk=item_id)
        basket = request.session.get('basket', {})

        basket.pop(item_id)

        request.session['basket'] = basket
        messages.success(request, f'{product.name} has been removed')
        return HttpResponse(status=200)
    
    except Exception as e:
        messages.error(request, 'There has been an error, please try again!')
        return HttpResponse(status=500)