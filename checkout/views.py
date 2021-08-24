from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "You don't have any items in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JS7UYDCmJwv31im8o2MeHmqiW9ulnCCSLRVlHIDadXKR4hMKnYf1j4v4eAmQX4cnoRBUjqZ52ykDioH70MklvTK00rdDnlBd6',
    }

    return render(request, template, context)
