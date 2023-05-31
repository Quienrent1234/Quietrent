""" url pattern for register

    Redirect to the good view 

    For form redirection : create form with the good redirection and models
    than redirect to the view witch correspond with the form class"""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('questionnaire-loc/', views.eligibility_caretaker.do),
    path('questionnaire-bail/', views.eligibility_caretaker.do),
    path('garantie/', views.eligibility_caretaker.do),
    path('eligibilite/', views.eligibility_caretaker.do),
    path('complete/', views.eligibility_caretaker.do),
    path('register/', views.eligibility_caretaker.do),
    path('email-verification/', views.eligibility_caretaker.do),
    path('return/', views.eligibility_caretaker.undo),
    path('remove/', views.remove),
    path('login-client/', views.login_client, name="login-client"),
    path('login-partner/', views.login_partner, name="login-partner"),
    path('login_admin/',views.login_admin, name="login_admin"),
    path('login_admin_bis/',views.login_admin_bis, name="login_admin"),
    path('logout/', views.logout_user, name="logout"),
    path('login/', views.status_choice, name="status"),
    path('ajax-verif-mail/', views.ajax_view_verif_mail),
    path('questionnaire-loc/ajax_siret/',views.ajax_siret,name='ajax_siret'),
    path('<page>/', views.view)
]
