from django.shortcuts import render, redirect
from django.http import HttpResponse

import sys
import os
import logging

up1 = os.path.abspath('.')
sys.path.append(up1)

from django.shortcuts import render, redirect
from django.http import HttpResponse

import sys
import os
import logging

up1 = os.path.abspath('.')
sys.path.insert(0, up1)

import mysite
from register.views import eligibility_caretaker

def contact(request):
    try:
        data = eligibility_caretaker.get_memento(request.session['token'], 0).get_data()
    except Exception:
        name = None
        phone_number = None
    else:
        name = data['inputFirstName'] + " " + data['inputName']
        phone_number = data['inputPhone']
    finally:
        return render(request, 'base/contact-us.html', {
            'name': name,
            'phone_number': phone_number
        })

def contact_verification(request):
    try:
        eligibility_caretaker.pop(request.session.pop('token'))
    except KeyError:
        pass
    finally:
        contact = mysite.models.Contact()

        contact.name = request.POST['name']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone_number']
        contact.msg_subject = request.POST['msg_subject']
        contact.message = request.POST['message']

        contact.save()

        mysite.views.send_email(contact.msg_subject, {
            "Nom": contact.name,
            "Adresse mail": contact.email,
            "Numéro de téléphone": contact.phone_number,
            "\nmessage": contact.message
        })

        return redirect('../../index/')

def view(request, page):
    return mysite.views.default_view(request, 'base/' + page)


up2 = os.path.abspath('..')
sys.path.insert(0, f'{up1}/register')

from register.views import eligibility_caretaker

def contact(request):
    try:
        data = eligibility_caretaker.get_memento(request.session['token'], 0).get_data()
    except Exception:
        name = None
        phone_number = None
    else:
        name = data['inputFirstName'] + " " + data['inputName']
        phone_number = data['inputPhone']
    finally:
        return render(request, 'base/contact-us.html', {
            'name': name,
            'phone_number': phone_number
        })

def contact_verification(request):
    try:
        eligibility_caretaker.pop(request.session.pop('token'))
    except KeyError:
        pass
    finally:
        contact = mysite.models.Contact()

        contact.name = request.POST['name']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone_number']
        contact.msg_subject = request.POST['msg_subject']
        contact.message = request.POST['message']

        contact.save()

        mysite.views.send_email(contact.msg_subject, {
            "Nom": contact.name,
            "Adresse mail": contact.email,
            "Numéro de téléphone": contact.phone_number,
            "\nmessage": contact.message
        })

        return redirect('../../index/')

def view(request, page):
    return mysite.views.default_view(request, 'base/' + page)
