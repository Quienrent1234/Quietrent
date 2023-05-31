from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.template.exceptions import TemplateDoesNotExist
from django.core import mail

from abc import ABC, abstractmethod

# class Caretaker(ABC):
#     @abstractmethod
#     def do(self, request: HttpRequest) -> HttpResponse:
#         pass

#     @abstractmethod
#     def undo(self, request: HttpRequest) -> HttpResponse:
#         pass

def send_email(object, data):
    message = ''
    for key, value in data.items():
        message += '{} : {}\n'.format(key, value)
    with mail.get_connection() as connection:
        mail.EmailMessage(
            object, message, 'moimeme', ['miel.licorne@gmail.com'],
            connection=connection
        ).send()

def default_view(request, page):
    try:
        return render(request, page + '.html')

    except TemplateDoesNotExist:
        return render(request, '404.html')

def index_redirection(request):
    return redirect('http://127.0.0.1:8000/index/')