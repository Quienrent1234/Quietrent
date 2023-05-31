from django.contrib import admin
from django.urls import path

from . import views

#urlpatterns auto, link with templates so that */<page>/ ---> <page>.html
urlpatterns = [
    path('contact-us/', views.contact),
    path('contact-verification/', views.contact_verification),
    path('<page>/', views.view)
]