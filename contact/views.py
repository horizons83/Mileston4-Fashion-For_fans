from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm


# Create your views here.

def contact(request):
    """
    Create contact page for customers to contact Admin.
   """

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        # sends emails to admin and user.
        if contact_form.is_valid():
            user_email = contact_form.cleaned_data['email']
            subject = (" Message Receipt Confirmation: " +
                       contact_form.cleaned_data['subject'])
            body = render_to_string(
                'contact/email/email_body.txt',
                {'contact_email': settings.DEFAULT_FROM_EMAIL})
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user_email]
            )

            if settings.EMAIL_HOST_USER:
                admin_email = settings.DEFAULT_FROM_EMAIL
            else:
                admin_email = settings.DEFAULT_FROM_EMAIL

            # parse the user details from the form.
            last_name = contact_form.cleaned_data['last_name']
            user_name = contact_form.cleaned_data['first_name']
            phone_number = contact_form.cleaned_data['phone_number']
            your_message = contact_form.cleaned_data['your_message']
            admin_body = render_to_string(
                'contact/email/admin_email_body.txt',
                {
                    'sender_email': user_email,
                    'first_name': user_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'subject': subject,
                    'your_message': your_message,
                })
            send_mail(
                subject,
                admin_body,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email]
            )
            contact_form.save()
            messages.success(request, 'Your message was sent successfully !')
            return redirect('products')
        else:
            messages.error(request, 'Oops, looks like there is an error. Please check and try again')

    else:
        contact_form = ContactForm()

    context = {
        'contact_form': contact_form,
    }
    template = 'contact/contact.html'
    return render(request, template, context)
