from argparse import Namespace
import logging
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .models import *
from datetime import datetime

urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('base/', include('base.urls')),
    path('admin/', include('admin2.urls')),
    path('register/', include(('register.urls', 'register'), namespace='register')),
    path('index-redirection/', index_redirection, name='index-redirection'),
    path('<page>/', default_view)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.sessions.models import Session
from django.utils import timezone
import threading

class TimerInterval:
    def __init__(self, interval, function, args=None, kwargs=None):
        self.__timer = threading.Timer(interval, self.__operation, args, kwargs)
        self.__function = function

    def __operation(self):
        self.__function()
        self.__timer.run()

    def cancel(self):
        self.__timer.cancel()

    def start(self):
        self.__timer.start()

def clear_session():
    for session in Session.objects.all():
        if session.expire_date <= timezone.now():
            session_decoded = session.get_decoded()
            if 'token' in session_decoded:
                pass
                #eligibility_caretaker.pop(session_decoded['token'])
            
            session.delete()

timer_interval = TimerInterval(300, clear_session)
timer_interval.start()

def clear_connexion():
    if (datetime.now().month == 1 and datetime.now().day == 1):
        connections = Connexion.objects.all()
        for connection in connections :
            user=connection.user
            connection.delete()
            connection=Connexion()
            connection.user=user
            connection.save()
            logging.error("interval fonctionne")


timer_interval2 = TimerInterval(86400, clear_connexion)
timer_interval2.start()