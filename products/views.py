from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product

# Create your views here.
def all_products(request):
    """Displays all products, including sorting and search queries"""

    products = Product.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        # Query search 
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter search criteria')
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(subtitle__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
            
        # Product sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            direction = request.GET.get('direction', 'asc')
    
            if sortkey == 'name':
                products = products.annotate(lower_name=Lower('name'))
                sortkey = 'lower_name'
            elif sortkey == 'price':
                 sortkey = 'price'
            elif sortkey == 'rating':
                 sortkey = 'rating'

            if direction == 'desc':
                sortkey = f'-{sortkey}'
    
            products = products.order_by(sortkey)

    current_sorting = f"{request.GET.get('sort', 'None')}_{request.GET.get('direction', 'None')}"

    context = {
        'products': products,
        'search_term': query,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """Displays individual product details, including description and reviews"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)