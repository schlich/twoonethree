from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']

            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            send_mail('New Contact from the Website', message, sender_email, ['tyler@213group.org','ben@213group.org','austen@213group.org','andrew@213group.org'])
            messages.info(request, 'Your message has been sent!')
            
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()

    return render(request, 'contact/contact-us.html', {'form': form})