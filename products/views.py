import random
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Team, Category, Review
from .forms import ProductForm
# Create your views here.


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Whoops! You didn't enter any criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details
        and suggested products
     """

    product = get_object_or_404(Product, pk=product_id)
    team = Team.objects.all()
    reviews = Review.objects.filter(product=product)
    category = product.category
    suggestions = Product.objects.filter(category=category)
    suggested_products = list(suggestions)

    # removes current product from suggested products
    for i, item in enumerate(suggested_products):
        if item == product:
            suggested_products.pop(i)
            break

    # pick 3 random products from suggested list
    suggested_products = random.sample(
        suggested_products, min(len(suggested_products), 3))

    # rating math logic.
    if len(reviews) > 0:
        average_rating = 0
        for review in reviews:
            average_rating += review.rating

        average_rating = round(float(average_rating) / float(len(reviews)), 1)
    else:
        average_rating = 'N/A'

    context = {
        'product': product,
        'team': team,
        'reviews': reviews,
        'average_rating': average_rating,
        'suggested_products': suggested_products,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Render form for admin to add product to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Your product was added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Whoops product not added. Please check the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    A view to render a form for admin to edit a
    product in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'{product.name} was updated successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    A View to allow admin to delete
    products from the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product was successfully deleted!')
    return redirect(reverse('products'))
