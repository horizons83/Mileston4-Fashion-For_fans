from django.shortcuts import render, get_object_or_404
from .models import Product, Team
# Create your views here.


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    team = Team.objects.all()

    context = {
        'product': product,
        'team': team,
    }

    return render(request, 'products/product_detail.html', context)
