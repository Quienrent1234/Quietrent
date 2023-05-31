from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core import mail
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
#from pyrsistent import v
import feedparser
from dateutil.relativedelta import *
from pyquery import PyQuery
import re
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from urllib.error import HTTPError
# from django.utils import timezone

import os
import sys
from datetime import datetime, timezone, date, timedelta

# # from requests import request
up1 = os.path.abspath('.')
sys.path.insert(0, up1)

from xhtml2pdf import pisa
from io import BytesIO

from django.contrib.auth import views as auth_views
from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _

import mysite
#from mysite.views import default_view
from multiprocessing import context
import logging
import re
import json
from api_insee import ApiInsee

import jwt
from jose import jws
from cryptography.hazmat.primitives import serialization as crypto_serialization

import time

from docusign_esign import RecipientViewRequest, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient, EnvelopesApi, Text, DateSigned, CarbonCopy
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework import status

import base64
import requests

api = ApiInsee(
    key = "5cBm0pDfweOndd8MoqJVQJqcvVsa",
    secret = "PUnA6IDn7zRbnavSxDROqfnZbRsa"
)

def crm_customers_admin(request):
    """ Permet de d'afficher les utilisateurs (type client) et leurs informations dans la page customers du super admin."""
    context={}
    context["Entreprise"]={}
    AllUser = mysite.models.User.objects.exclude(type=1)
    context["AllUser"]=AllUser
    
    entreprises = mysite.models.Entreprise.objects.values("user","social_reason")
    if request.user.type == '2':
        entreprises = entreprises.filter(user__administrator__id=request.user.id)
    context["AllEntreprise"] = entreprises
    return render(request, './admin/crm-customers-admin.html', context)
 
def crm_leads_admin(request):
    """ Permet de d'afficher les demandes et leurs informations dans la page leads du super admin."""
    context={}
    context["admins"]= mysite.models.User.objects.filter(type="2")
    demandes = mysite.models.Demande.objects.values("id", "inputFirstName", "inputName", "inputMail", "inputPhone", "social_reason", "etat", "user")

    if request.user.type == '2':
        demandes = demandes.filter(user__administrator__id=request.user.id)    
    context["AllDemande"] = demandes
    for i in range(0, len(demandes)):
        if context["AllDemande"][i]["etat"] == 0:
            context["AllDemande"][i]["etat"] = "Rejeté"
        elif context["AllDemande"][i]["etat"] == 1:
            context["AllDemande"][i]["etat"] = "Mise en contact"
        elif context["AllDemande"][i]["etat"] == 2:
            context["AllDemande"][i]["etat"] =  "En cours de traitement"
        elif context["AllDemande"][i]["etat"] == 3:
            context["AllDemande"][i]["etat"] =  "Documents manquants"
        elif context["AllDemande"][i]["etat"] == 4:
            context["AllDemande"][i]["etat"] =  "En cours de complétion"
        elif context["AllDemande"][i]["etat"] == 5:
            context["AllDemande"][i]["etat"] =  "Validé"
        logging.error(demandes[i])
        context["AllDemande"][i]["administrator"] =  mysite.models.User.objects.get(id=demandes[i]["user"]).administrator
        context["AllDemande"][i]["isadministrator"] = mysite.models.User.objects.get(id=demandes[i]["user"]).type
        docForDemande = mysite.models.GestionDoc.objects.filter(id_demande=context["AllDemande"][i]["id"])
        for docs in docForDemande:
            if docs.type in context["AllDemande"][i]:
                context["AllDemande"][i][docs.type][docs.id]=str(docs.id_demande).strip()
            else:
                context["AllDemande"][i][docs.type]={}
                context["AllDemande"][i][docs.type][docs.id]=str(docs.id_demande).strip()
                #context["AllDemande"][i][docs.type][i].append(i)
    return render(request, './admin/crm-leads-admin.html', context)

@login_required(login_url='../../register/login/')
def user_dashboard(request):
    """ Cette vue render en context la liste des demandes, tickets, contrats, factures du User actuellement
     connecté. Ainsi, ces données peuvent être affichées dans la Template Dashboard.
     De plus, il y a des import de flux RSS pour la div Actualités."""
    context = {}
    feeds1 = feedparser.parse('https://www.mesquestionsdargent.fr/flux/Assurance/rss.xml')

    for entry in feeds1.entries:
        context['href1'] = entry.link
        context['title1'] = entry.title
        break

    feeds2 = feedparser.parse('https://www.lefigaro.fr/rss/figaro_assurance.xml')

    for entry in feeds2.entries:
        context['href2'] = entry.link
        context['title2'] = entry.title
        break

    feeds3 = feedparser.parse('https://www.lefigaro.fr/rss/figaro_immobilier.xml')

    for entry in feeds3.entries:
        context['href3'] = entry.link
        context['title3'] = entry.title
        break

    feeds4 = feedparser.parse('https://www.lemonde.fr/immobilier/rss_full.xml')

    for entry in feeds4.entries:
        context['href4'] = entry.link
        context['title4'] = entry.title
        break

    context['user'] = mysite.models.User.objects.get(id=request.user.id)
    context['demandes'] = mysite.models.Demande.objects.filter(user=request.user)
    context['demandes_ok'] = mysite.models.Demande.objects.filter(user=request.user, etat=5)
    context['contrats'] = mysite.models.Contrat.objects.filter(user=request.user)
    context['tickets'] = mysite.models.Ticket.objects.filter(user=request.user)
    context['factures'] = mysite.models.Facture.objects.filter(user=request.user)
    context['open_tickets'] = mysite.models.Ticket.objects.filter(user=request.user, etat='1')
    context['closed_tickets'] = mysite.models.Ticket.objects.filter(user=request.user, etat='0')
    context['done_tickets'] = mysite.models.Ticket.objects.filter(user=request.user, etat='2')
    if context['tickets'].count() > 0:
        context['done_percent'] = 100 * context['done_tickets'].count() // context['tickets'].count()
        context['closed_percent'] = 100 * context['closed_tickets'].count() // context['tickets'].count()
        context['open_percent'] = 100 * context['open_tickets'].count() // context['tickets'].count()
    else:
        context['done_percent'] = 0
        context['closed_percent'] = 0
        context['open_percent'] = 0
    return render(request, './admin/dashboard.html', context)

login_required(login_url='../../register/login/')
def admin_dashboard_ticket(request):
    context = {}
    first_date = date.today() - timedelta(days=1) 
    context['new_tickets'] = mysite.models.Ticket.objects.filter(date_creation__range=(first_date, datetime.now())).count()
    context['open_tickets'] = mysite.models.Ticket.objects.filter(etat='1').count()
    context['closed_tickets'] = mysite.models.Ticket.objects.filter( date_cloture__range=(first_date, datetime.now()), etat='0').count()
    context['done_tickets'] = mysite.models.Ticket.objects.filter(date_cloture__range=(first_date, datetime.now()), etat='2').count()
    context['all_tickets'] = mysite.models.Ticket.objects.values("id","user","objet","service","category","etat").order_by("-date_creation")
    context['all_user'] = mysite.models.User.objects.values("id","first_name","last_name")
    
    first_date2 = date(datetime.now().year, 1, 1)
    context['sumClose']= mysite.models.Ticket.objects.filter( date_cloture__range=(first_date2, datetime.now()), etat='0').count() + mysite.models.Ticket.objects.filter( date_cloture__range=(first_date, datetime.now()), etat='0').count()
    context['sumClose_yesterday']= mysite.models.Ticket.objects.filter( date_cloture__range=(first_date2, first_date), etat='0').count() + mysite.models.Ticket.objects.filter( date_cloture__range=(first_date, first_date), etat='0').count()
    if (context['sumClose'] - context['sumClose_yesterday']) == 0:
        context['pourcentage_close_day'] = 0
    else:    
        context['pourcentage_close_day'] = 100 * context['sumClose_yesterday'] // (context['sumClose'] - context['sumClose_yesterday'])

    return render(request, './admin/dashboard-admin-ticket.html', context)

def admin_dashbord_ticket_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        C = {}
        arrayticket_newByMonth=[]
        arrayticket_closeByMonth=[]
        arrayticket_etatNumber=[]
        arrayticket_category=[]

        for i in range (12):
            arrayticket_newByMonth.append(0)
            arrayticket_closeByMonth.append(0)
        for i in range (3):
            arrayticket_etatNumber.append(0)
        for i in range (3):
            arrayticket_category.append(0)

        first_date = date(datetime.now().year, 1, 1)
        tickets=mysite.models.Ticket.objects.filter(date_creation__range=(first_date, datetime.now()))
        for ticket in tickets:
            arrayticket_newByMonth[ticket.date_creation.month-1]+=1
            if ticket.etat == '0' or ticket.etat =='2':
                arrayticket_closeByMonth[ticket.date_cloture.month-1]+=1
            arrayticket_etatNumber[int(ticket.etat)]+=1
            if ticket.category == "info":
                arrayticket_category[0]+=1
            elif ticket.category == "tech":
                arrayticket_category[1]+=1
            else:
                arrayticket_category[2]+=1
        C["newByMonth"]=arrayticket_newByMonth
        C["etatNumber"]=arrayticket_etatNumber
        C["category"]=arrayticket_category
        C["closeByMonth"]=arrayticket_closeByMonth
        return  JsonResponse(C)
    else :
        return redirect("../../index")

login_required(login_url='../../register/login/')
def admin_dashboard_commercial(request):
    context = {}
    context["date"] = date.today()
    context["datemoismoins1"] = date.today() - relativedelta(months=1)
    # pq = PyQuery(url=f'https://www.linkedin.com/pages-extensions/FollowCompany?id={argv[1]}&counter=bottom')
    # widget_text = pq.text() # equivalent of <document.body.innerText> in JS
    # follower_count = int(re.sub(r'\D', '', widget_text)) # remove everything except digits and cast to int
    #print({ 'raw': widget_text, 'count': follower_count })
    first_date_years = date(datetime.now().year, 1, 1)
    context["newCustomers"]=mysite.models.User.objects.filter(date_joined__range=(first_date_years, datetime.now())).count()
    context["newDeal"]=mysite.models.Demande.objects.filter(date_demande__range=(first_date_years, datetime.now())).count()
    context["newDealConclude"]=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=6).count() + mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=0).count()
    dealsuccess = mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=6).count()
    total = dealsuccess + mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=0).count()
    context["pourcentDealSucces"]= 100 * dealsuccess // total

    return render(request, './admin/dashboard-admin-commercial.html', context)

def admin_dashbord_commercial_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        C = {}
        arraycommercial_newCustomersByMonth=[]
        arraycommercial_connexion=[]
        arraycommercial_etat=[]
        arraycommercial_totalCustomersByMonth=[]
        arraycommercial_uniqueCustomerReconnexionByMonth=[]
        arraydemande_encoursByMonth=[]
        arraydemande_clotureByMonth=[]

        for i in range (12):
            arraycommercial_newCustomersByMonth.append(0)
            arraycommercial_connexion.append(0)
            arraycommercial_totalCustomersByMonth.append(0)
            arraycommercial_uniqueCustomerReconnexionByMonth.append(0)
            arraydemande_encoursByMonth.append(0)
            arraydemande_clotureByMonth.append(0)
        for i in range (4):
            arraycommercial_etat.append(0)

        first_date_month = date.today() - relativedelta(months = 1) 
        commercials=mysite.models.Demande.objects.filter(date_demande__range=(first_date_month, datetime.now()))
        for commercial in commercials:
            if (commercial.etat == 2 or commercial.etat == 3):
                arraycommercial_etat[0]+=1
        commercials=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_month, datetime.now()))
        for commercial in commercials:
            if commercial.etat == 0:
                arraycommercial_etat[1]+=1
            elif commercial.etat == 5:
                arraycommercial_etat[2]+=1
            elif commercial.etat == 6:
                arraycommercial_etat[3]+=1 
            
        total = arraycommercial_etat[0] + arraycommercial_etat[1] + arraycommercial_etat[2] + arraycommercial_etat[3]
        arraycommercial_etat[0] =100 * arraycommercial_etat[0] / total
        arraycommercial_etat[1] =100 * arraycommercial_etat[1] / total
        arraycommercial_etat[2] =100 * arraycommercial_etat[2] / total
        arraycommercial_etat[3] =100 * arraycommercial_etat[3] / total


        first_date_years = date(datetime.now().year, 1, 1)
        customers=mysite.models.User.objects.filter(date_joined__range=(first_date_years, datetime.now()))
        for customer in customers:
            arraycommercial_newCustomersByMonth[customer.date_joined.month-1]+=1
        connexions=mysite.models.Connexion.objects.all()
        for connexion in connexions:
            arraycommercial_connexion[0]+=connexion.janv
            if (connexion.janv > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[0]+=1
            arraycommercial_connexion[1]+=connexion.fevr
            if (connexion.fevr > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[1]+=1
            arraycommercial_connexion[2]+=connexion.mars
            if (connexion.mars > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[2]+=1
            arraycommercial_connexion[3]+=connexion.avril
            if (connexion.avril > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[3]+=1
            arraycommercial_connexion[4]+=connexion.mai
            if (connexion.mai > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[4]+=1
            arraycommercial_connexion[5]+=connexion.juin
            if (connexion.juin > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[5]+=1
            arraycommercial_connexion[6]+=connexion.juill
            if (connexion.juill > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[6]+=1
            arraycommercial_connexion[7]+=connexion.aout
            if (connexion.aout > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[7]+=1
            arraycommercial_connexion[8]+=connexion.sept
            if (connexion.sept > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[8]+=1
            arraycommercial_connexion[9]+=connexion.oct
            if (connexion.oct > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[9]+=1
            arraycommercial_connexion[10]+=connexion.nov
            if (connexion.nov > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[10]+=1
            arraycommercial_connexion[11]+=connexion.dec
            if (connexion.dec > 0):
                arraycommercial_uniqueCustomerReconnexionByMonth[11]+=1

        demandes=mysite.models.Demande.objects.filter(date_demande__range=(first_date_years, datetime.now()))
        for demande in demandes:
            if (demande.etat == 2 or demande.etat == 3 or demande.etat == 4 or demande.etat == 5) :
                arraydemande_encoursByMonth[demande.date_demande.month-1]+=1


        demandes2=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=6)
        for demande in demandes2:
            if (demande.etat == 6):
                arraydemande_clotureByMonth[demande.date_demande.month-1]+=1
            
                
        for i in range (12):
            arraycommercial_totalCustomersByMonth[i]=arraycommercial_connexion[i] + arraycommercial_newCustomersByMonth[i]

        C["etat"]=arraycommercial_etat
        C["newCustomersByMonth"]=arraycommercial_newCustomersByMonth
        C["totalCustomersByMonth"]=arraycommercial_totalCustomersByMonth
        C["uniqueCustomerReconnexionByMonth"]=arraycommercial_uniqueCustomerReconnexionByMonth
        C["bounceRate"] = 100 * C["newCustomersByMonth"][datetime.now().month-1] // (C["uniqueCustomerReconnexionByMonth"][datetime.now().month-1]+C["newCustomersByMonth"][datetime.now().month-1])

        C["encoursDemande"]=arraydemande_encoursByMonth
        C["clotureDemande"]=arraydemande_clotureByMonth
        return  JsonResponse(C)
    else :
        return redirect("../../index")

login_required(login_url='../../register/login/')
def admin_dashboard_analytique(request):
    context = {}
    first_date_month = date.today() - relativedelta(months = 1)
    context["dateyearsmoins1"] = date(datetime.now().year, 1, 1)
    context["date"] =datetime.now()
    context["demandeEnCours"]= mysite.models.Demande.objects.filter(Q(etat=2) | Q(etat=3)).count()
    context["contratFinalisé"] = mysite.models.Demande.objects.filter(Q(date_cloture__range=(first_date_month, datetime.now()))).filter(Q(etat=6)).count()
    context["contratEnCours"]= mysite.models.Demande.objects.filter(etat=5).count()
    demandeLastMonth= mysite.models.Demande.objects.filter(Q(date_demande__lte=(first_date_month))).filter(Q(etat=2) | Q(etat=3)).count() + mysite.models.Demande.objects.filter(Q(date_cloture__gte=(first_date_month))).filter(Q(etat=6)).filter(Q(date_demande__lte=(first_date_month))).count()
    count=mysite.models.Demande.objects.filter(Q(date_cloture__gte=(first_date_month))).filter(Q(etat=6)).filter(Q(date_demande__lte=(first_date_month)))
    totalPrime3years = 0.0
    first_date_3years = date(datetime.now().year-2, 1, 1)
    demande_cloturer3ans=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_3years,datetime.now()),etat=6)
    for demande in demande_cloturer3ans:
        if demande.substitution == '0':
            montant=demande.garantie
        elif demande.substitution == '1':               
            montant=demande.caution
        else :
            montant=int(demande.caution) + int(demande.garantie)
        montant = int(montant)
        if demande.plusDeuxAns=='yes':
            totalPrime3years += montant * 0.037 * (demande.date_cloture.year - (datetime.now().year-2))
        else:
            totalPrime3years += montant * 0.035 * (demande.date_cloture.year - (datetime.now().year-2))
    demande_cloturer3ans=mysite.models.Demande.objects.filter(date_cloture__lte=(first_date_3years),etat=6)
    for demande in demande_cloturer3ans:
        if demande.substitution == '0':
            montant=demande.garantie
        elif demande.substitution == '1':               
            montant=demande.caution
        else :
            montant=int(demande.caution) + int(demande.garantie)
        montant = int(montant)
        if demande.plusDeuxAns=='yes':
            totalPrime3years += montant * 0.037 * 3
        else:
            totalPrime3years += montant * 0.035 * 3
    context["allPrimeEver"]=totalPrime3years

    totalPrime=0.0
    totalFrais=0.0
    demande_cloturer=mysite.models.Demande.objects.filter(date_cloture__lte=(datetime.now()),etat=6)
    for demande in demande_cloturer:
        if demande.substitution == '0':
            montant=demande.garantie
        elif demande.substitution == '1':               
            montant=demande.caution
        else :
            montant=int(demande.caution) + int(demande.garantie)
        montant = int(montant)
        if demande.plusDeuxAns=='yes':
            totalPrime += ((montant * 0.037)-(montant * 0.037)*0.09) * 0.13 * 3
            totalFrais += montant * 0.037
        else:
            totalPrime += ((montant * 0.035)-(montant * 0.035)*0.09) * 0.13 * 3
            totalFrais += montant * 0.035
            
    context["totalHonoraire"]= totalPrime + totalFrais
    context["HonoraireMoyen"]= context["totalHonoraire"] / demande_cloturer.count()
    if demandeLastMonth == 0:
        context["variationDemandeEnCours"]="error"
    else:
        context["variationDemandeEnCours"]=100 * ((context["demandeEnCours"] - demandeLastMonth) / demandeLastMonth)
    return render(request, './admin/dashboard-admin-analytique.html', context)

def admin_dashboard_analytique_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        C = {}
        totalPrime=0.0
        totalFrais=0.0
        arraydemande_primeByMonth=[]
        arraydemande_fraisByMonth=[]
        arraydemande_primeByMonthMax=[]
        arraydemande_fraisByMonthMax=[]
        totalMax=[]
        totalDone=[]

        for i in range (12):
            arraydemande_primeByMonth.append(0)
            arraydemande_fraisByMonth.append(0)
            arraydemande_primeByMonthMax.append(0)
            arraydemande_fraisByMonthMax.append(0)
            totalMax.append(0)
            totalDone.append(0)

        first_date_years = date(datetime.now().year, 1, 1)
        first_date_3years = date(datetime.now().year-2, 1, 1)
        demande_encours=mysite.models.Demande.objects.filter(date_demande__range=(first_date_years, datetime.now())).exclude(etat=6).exclude(etat=4)
        demande_cloturer=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_years, datetime.now()),etat=6)
        #demande_cloturer3ans=mysite.models.Demande.objects.filter(date_cloture__range=(first_date_3years,first_date_years),etat=6)
        # for demande in demande_cloturer3ans:
        #     if demande.substitution == '0':
        #         montant=demande.garantie
        #     elif demande.substitution == '1':               
        #         montant=demande.caution
        #     else :
        #         montant=int(demande.caution) + int(demande.garantie)
        #     montant = int(montant)
        #     if demande.plusDeuxAns=='yes':
        #         #arraydemande_primeByMonth3years[demande.date_cloture.month-1] += montant * 0.037
        #         #totalPrime3years += arraydemande_primeByMonth3years[demande.date_cloture.month-1]
        #     else:
        #         #arraydemande_primeByMonth3years[demande.date_cloture.month-1] += montant * 0.035
        #         totalPrime3years += arraydemande_primeByMonth3years[demande.date_cloture.month-1]
        #     logging.error(totalPrime3years)
        # logging.error("------------------total Frais----------------")
        # logging.error(totalPrime3years)
        for demande in demande_cloturer:
            if demande.substitution == '0':
                montant=demande.garantie
            elif demande.substitution == '1':               
                montant=demande.caution
            else :
                montant=int(demande.caution) + int(demande.garantie)
            montant = int(montant)
            if demande.plusDeuxAns=='yes':
                arraydemande_primeByMonth[demande.date_cloture.month-1] += ((montant * 0.037)-(montant * 0.037)*0.09) * 0.13 * 3
                arraydemande_fraisByMonth[demande.date_cloture.month-1] += montant * 0.037
                totalPrime += arraydemande_primeByMonth[demande.date_cloture.month-1]
                totalFrais += arraydemande_primeByMonth[demande.date_cloture.month-1]
            else:
                arraydemande_primeByMonth[demande.date_cloture.month-1] += ((montant * 0.035)-(montant * 0.035)*0.09) * 0.13 * 3
                arraydemande_fraisByMonth[demande.date_cloture.month-1] += montant * 0.035
                totalPrime += arraydemande_primeByMonth[demande.date_cloture.month-1]
                totalFrais += arraydemande_fraisByMonth[demande.date_cloture.month-1]
        for demande in demande_encours:
            if demande.substitution == '0':
                montant=demande.garantie
            elif demande.substitution == '1':               
                montant=demande.caution
            else :
                montant=int(demande.caution) + int(demande.garantie)
            montant = int(montant)
            if demande.plusDeuxAns=='yes':
                arraydemande_primeByMonthMax[demande.date_cloture.month-1] += ((montant * 0.037)-(montant * 0.037)*0.09) * 0.13 * 3
                arraydemande_fraisByMonthMax[demande.date_cloture.month-1] += montant * 0.037
            else:
                arraydemande_primeByMonthMax[demande.date_cloture.month-1] += ((montant * 0.035)-(montant * 0.035)*0.09) * 0.13 * 3
                arraydemande_fraisByMonthMax[demande.date_cloture.month-1] += montant * 0.035
        for i in range (12):
            totalMax[i]=(arraydemande_primeByMonthMax[i]+arraydemande_fraisByMonthMax[i]) #+arraydemande_primeByMonth3yearsMax[i])
            totalDone[i]=(arraydemande_primeByMonth[i]+arraydemande_fraisByMonth[i]) #+arraydemande_primeByMonth3years[i])
        C["totalMax"]=totalMax
        C["totalDone"]=totalDone
        total= totalPrime + totalFrais # + totalPrime3years
        C["totalReccuring"]=100 * (totalPrime) // total
        C["totalOneShot"]= 100 * (totalFrais) // total
        return  JsonResponse(C)
    else :
        return redirect("../../index")

@login_required(login_url='../../register/login/')
def user_profile(request):
    """ Vue reliée à la page profil où l'utilisateur peut changer ses infos perso et celles de ses entreprises.
    Il peut également changer de mdp."""
    context = {}
    context['id'] = request.user.id

    user = mysite.models.User.objects.get(id=context['id'])
    entreprises = mysite.models.Entreprise.objects.filter(user=context['id'])
    context['nb_entreprise'] = entreprises.count()
    context['active'] = entreprises[0].id
    context['entreprises'] = entreprises
    context['user'] = user.id
    context['f1'] = user.first_name[0]
    context['l1'] = user.last_name[0]
    if request.method == 'POST':
        #Si le formulaire 'infoform' est rempli
        if 'infoform' in request.POST:
            user.gender = request.POST.get('gender')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.mobile = request.POST.get('mobile')
            user.email = request.POST.get('email')
            user.save()

        # Si le formulaire 'infoentreprise' est rempli
        for entreprise in entreprises:
            if 'infoentreprise' + str(entreprise.id) in request.POST:
                entreprise.social_reason = request.POST.get('social_reason')
                entreprise.adresse = request.POST.get('adresse')
                entreprise.code_postal = request.POST.get('codepostal')
                entreprise.siren = request.POST.get('siren')
                entreprise.descriptif = request.POST.get('descriptif')
                entreprise.siteweb = request.POST.get('website')
                entreprise.juridical_form = request.POST.get('juridical_form')
                entreprise.inputActivity = request.POST.get('inputActivity')
                entreprise.ville = request.POST.get('ville')
                entreprise.save()

        # Si le formulaire 'infopass' est rempli
        if 'infopass' in request.POST:
            if user.check_password(request.POST.get('currentPass')):
                if request.POST.get('newPass') == request.POST.get('confirmPass'):
                    context['erreur'] = "Mot de passe modifié avec succès"
                    user.password = make_password(request.POST.get('newPass'))
                    user.save()
                    return redirect('/register/auth.login/')
                else:
                    context['erreur'] = "Le nouveau mot de passe ne correspond pas au mot de passe confirmé !"

            else:
                context['erreur'] = "Le mot de passe renseigné est incorrect !"

    return render(request, './admin/pages-profile.html', context)


@login_required(login_url='../../register/login/')
def demande_en_cours_admin(request):
    context = {}
    if request.user.type == '1':
        context['user'] = str(request.user.id)

        demandes = mysite.models.Demande.objects.filter(user__id=request.user.id)
        context['socialReasonDemand'] = False
        for demande in demandes:
            if demande.etat != 4:
                demande.etat =4
                demande.save()
        context['demandes'] = demandes
        return render(request, './admin/pages-demandes-admin.html', context)
    else:
        return redirect ('../demande/')


@login_required(login_url='../../register/login/')
def user_demandes(request):
    """ Vue reliée à la page qui liste les demandes de l'utilisateur, avec leur état."""
    context = {}
    context['user'] = str(request.user.id)

    demandes = mysite.models.Demande.objects.filter(user__id=request.user.id)
    context['socialReasonDemand'] = False
    for demande in demandes:
        if demande.social_reason != demandes[0].social_reason:
            context['socialReasonDemand'] = True

    context['demandes'] = demandes
    return render(request, './admin/pages-demandes.html', context)

def contrats_et_certificats(request):
    """ Vue reliée à la page qui liste les contrats de l'utilisateur, avec leur état."""

    contrats = mysite.models.Contrat.objects.all()
    
    if request.user.type == '0':
        contrats = contrats.filter(user__id=request.user.id)
        return render(request, './admin/pages-contrats-certificats.html', {'contrats': contrats})
    elif request.user.type == '2':
        contrats = contrats.filter(user__administrator__id=request.user.id)

    logging.error(f'\n\n\n{contrats}\n\n\n')

    return render(request, './admin/admin-contrats-certificats.html', {'contrats': contrats})

def factures(request):
    """ Vue reliée à la page qui liste les factures de l'utilisateur, avec leur état."""

    factures = mysite.models.Facture.objects.all()

    if request.user.type == '0':
        factures = factures.filter(user__id=request.user.id)
        return render(request, './admin/pages-factures.html', {'factures': factures})
    elif request.user.type == '2':
        factures = factures.filter(user__administrator__id=request.user.id)
    
    return render(request, './admin/admin-factures.html', {'factures': factures})

def check_invoice(request):
    if request.method == 'POST':
        facture = mysite.models.Facture.objects.get(id=request.POST['choice'])
        facture.payed = True
        facture.save()

        demande = mysite.models.Demande.objects.get(id=facture.demande.id)
        demande.etat += 1
        demande.save()

        return HttpResponse()
    else:
        return redirect('../factures')

def user_autre(request):
    """ Cette vue permet la consultation des documents reçus."""
    context = {}
    demandes = mysite.models.Demande.objects.filter(user=request.user)
    context['active'] = demandes[0].id
    user = mysite.models.User.objects.get(id=request.user.id)
    context['demandes'] = demandes
    autre_docs = mysite.models.AutreDoc.objects.filter(user=user)
    certifs = []
    attests = []
    bulletins = []
    autres = []
    for autre in autre_docs:
        if autre.type == "Certification":
            certifs.append(autre)
            context['certifs'] = certifs
        elif autre.type == "Bulletin":
            bulletins.append(autre)
            context['bulletins'] = bulletins
        elif autre.type == "Attestation":
            attests.append(autre)
            context['attests'] = attests
        else:
            autres.append(autre)
            context['autres'] = autres
    return render(request, './admin/pages-autres.html', context)

@login_required(login_url='../../register/login/')
def tickets(request):
    """ Permet de d'afficher les tickets et leurs informations dans la page ticket du super admin."""
    context = {}
    context['tickets'] = mysite.models.Ticket.objects.all()
    context['open_tickets'] = mysite.models.Ticket.objects.filter(etat='1')
    context['closed_tickets'] = mysite.models.Ticket.objects.filter(etat='0')
    context['done_tickets'] = mysite.models.Ticket.objects.filter(etat='2')

    if context['tickets'].count() > 0:
        context['done_percent'] = 100 * context['done_tickets'].count() // context['tickets'].count()
        context['closed_percent'] = 100 * context['closed_tickets'].count() // context['tickets'].count()
        context['open_percent'] = 100 * context['open_tickets'].count() // context['tickets'].count()
    else:
        context['done_percent'] = 0
        context['closed_percent'] = 0
        context['open_percent'] = 0

    context['demandes'] = mysite.models.Demande.objects.all()
    return render(request, './admin/tickets-consulting-admin.html',context)

@login_required(login_url='../../register/login/')
def demande_consulting(request):
    """ Vue reliée à la page de consultation des infos d'une demande.
    Elle permet de consulter les infos de la demande sélectionnée en fct de l'id de session instanciée
    lors du choix de la demande à consultée."""
    context = {}
    context['id_demande'] = request.session['id_demande_consulting']
    if mysite.models.Demande.objects.get(id=request.session['id_demande_consulting']) in mysite.models.Demande.objects.filter(user=request.user):
        demande = mysite.models.Demande.objects.get(id=request.session['id_demande_consulting'])
        context['demande'] = demande
    return render(request, './admin/pages-consulting.html', context)

@login_required(login_url='../../register/login/')
def consulting_choice(request):
    """ Cette vue permet d'instancier l'id de session permettant la consultation de la demande sélectionnée."""
    if request.method == 'POST':
        request.session['id_demande_consulting'] = request.POST['choice']
        return redirect('../consulting/')
    else:
        return redirect('../demandes/')

@login_required(login_url='../../register/login/')
def upload_choice(request):
    """ Cette vue permet d'instancier l'id de session permettant l'upload de docs pour la demande sélectionnée."""
    if request.method == 'POST':
        request.session['id_demande_upload'] = request.POST['choice']
        request.session['id_demande_of_doc_deleted'] = int(request.POST['choice'])
        return redirect('../upload/')
    else:
        return redirect('../demandes/')

@login_required(login_url='../../register/login/')
def  modify_user_super_admin_choice(request):
    """ 
    Met en session l'id de l'user consulté dans la page customer du super admin afin de le modifier par la suite, pour eviter les 
    instanciation par get, les formulaires dupliqué ou les chemin trop long qui modifirai le header.     
    """
    if request.method == 'POST':
        request.session['user_admin_consulting'] = request.POST['choice']
        return redirect('../modify-user-super-admin/')
    else:
        return redirect('../crm-customers-admin/')

@login_required(login_url='../../register/login/')
def message_choice(request):
    """ 
    Met en session l'id de la demande consulté dans la page lead du super admin afin d'envoyé un message par la suite, pour eviter les 
    instanciation par get, les formulaires dupliqué ou les chemin trop long qui modifirai le header.     
    """
    if request.method == 'POST':
        request.session['id_demande_message'] = request.POST.get('choice',"")
        if request.session['id_demande_message']=="":
            demande=mysite.models.Demande.objects.filter(user=request.POST['choice_user']).order_by("-date_demande")[0].id
            logging.error(demande)
            request.session['id_demande_message'] = demande
        return redirect('../message/')
    else:
        return redirect('../crm-leads-admin/')

@login_required(login_url='../../register/login/')
def upload_docs(request):
    """ Cette vue permet d'upload des docs en fct de la demande sélectionnée.
    Elle contrôle le type de doc ainsi que sa taille."""
    context = {}
    context['error_format'] = False
    context['error_size'] = False
    if ((request.user.type == '1') or (mysite.models.Demande.objects.get(id=request.session['id_demande_upload']) in mysite.models.Demande.objects.filter(user=request.user))):
        if request.method == 'POST':
            for i in range(1, 15):
                gestion_doc = mysite.models.GestionDoc()
                try:
                    uploaded_file = request.FILES['idfile' + str(i)]
                    type = uploaded_file.content_type

                    if re.match("^image/", type) or re.match("application/pdf", type):
                        fs = FileSystemStorage()
                        name = fs.save(uploaded_file.name, uploaded_file)
                        gestion_doc.adresse_doc = name
                        gestion_doc.user = request.user
                        gestion_doc.size = uploaded_file.size // 1024
                        gestion_doc.id_demande = request.session['id_demande_upload']
                        if i < 7:
                            gestion_doc.type = "Piece_identite"
                        elif i == 7:
                            gestion_doc.type = "Kbis"
                        elif i == 8 or i == 9:
                            gestion_doc.type = "Bilan"
                        elif i == 10:
                            gestion_doc.type = "Projet_de_bail_ou_LOI"
                        elif i == 11:
                            gestion_doc.type = "Statut_societe"
                        elif i == 12:
                            gestion_doc.type = "Business_plan"
                        elif i == 13:
                            gestion_doc.type = "Presentation_entreprise"
                        elif i == 14:
                            gestion_doc.type = "Autre_document"
                        if gestion_doc.size < 10240:
                            gestion_doc.save()
                            context['uploaded'] = True
                        else:
                            context['uploaded'] = False
                            context['error_size'] = True
                            return render(request, './admin/pages-upload.html', context)
                    else:
                        context['uploaded'] = False
                        context['error_format'] = True
                        return render(request, './admin/pages-upload.html', context)

                except MultiValueDictKeyError:
                    pass

            if request.user.type == '1':
                if context['uploaded'] == True:
                    return redirect('../crm-leads-admin/')
                else:
                    return redirect('../upload/')
            else:
                if context['uploaded'] == True:
                    return redirect('../upload-success/')
                else:
                    return redirect('../upload/')

    else:
        return redirect('../demandes/')

    return render(request, './admin/pages-upload.html', context)

@login_required(login_url='../../register/login/')
def validate_docs(request, id_demande):
    """ Cette vue permet de valider l'ajout de documents depuis la page 'mes docs'. Une fois les documents validée, les docs ne sont plus supprimables.
    Si le nombre de docs attendus est atteint, la demande correspondante passe à l'état 'en cours'."""
    demande = mysite.models.Demande.objects.get(id=id_demande)
    if demande in mysite.models.Demande.objects.filter(user=request.user):
        docs = mysite.models.GestionDoc.objects.filter(id_demande=id_demande)
        nb_piece_id = 0
        nb_kbis = 0
        nb_bilan = 0
        nb_bail = 0
        nb_statut_societe = 0
        request.session['id_demande_of_doc_deleted'] = id_demande
        for doc in docs:
            doc.deletable = False
            doc.save()
            if doc.type == "Piece_identite":
                nb_piece_id += 1
            elif doc.type == "Kbis":
                nb_kbis += 1
            elif doc.type == "Bilan":
                nb_bilan += 1
            elif doc.type == "Projet_de_bail_ou_LOI":
                nb_bail += 1
            elif doc.type == "Statut_societe":
                nb_statut_societe += 1

        if nb_statut_societe >= 1 and nb_bail >= 1 and nb_bilan >= 2 and nb_kbis >= 1 and nb_piece_id >= 2:
            demande.etat = 2
            demande.save()
    return redirect('../../documents/')

@login_required(login_url='../../register/login/')
def message(request):
    """
    Envois un message (notification) au client concerné par le message
    id de demande en session instancier par message_choice
    """
    context = {}
    context['id_demande']=request.session['id_demande_message']

    context['demande'] = mysite.models.Demande.objects.get(id=request.session['id_demande_message'])
    context['erreur'] = ""
    if request.method == 'POST':
        if request.POST.get('type', False) != False:
            message = mysite.models.Message()
            message.setter = mysite.models.User.objects.get(id=request.user.id)
            message.getter = mysite.models.User.objects.get(id=context['demande'].user)
            message.demande = context['demande']
            message.type = request.POST['type']
            message.titre = request.POST['subject']
            message.message = request.POST['message']
            message.save()
            return redirect('../crm-leads-admin/')
        else:
            context['erreur'] = "Erreur veuillez choisir un type de message"
    return render(request, './admin/send-message-admin.html', context)

@login_required(login_url='../../register/login/')
def delete_docs(request, id_doc):
    """ Cette vue permet de supprimer des docs ajoutés. Ils sont supprimés de la BDD ainsi que du storage."""
    if request.method == 'POST':
        doc = mysite.models.GestionDoc.objects.get(id=id_doc)
        request.session['id_demande_of_doc_deleted'] = doc.id_demande
        doc.delete()
        if os.path.exists("mysite/media/" + str(doc.adresse_doc)):
            os.remove("mysite/media/" + str(doc.adresse_doc))
        else:
            print("The file does not exist")
    return redirect('../../documents/')


@login_required(login_url='../../register/login')
def delete_notif(request, id_notif):
    """ supprime une notification depuis la page pages-notif ou page-notif-admin"""
    if request.method == 'POST':
        notif = mysite.models.Message.objects.get(id=id_notif)
        notif.delete()
    if request.user.type == '1':
        return redirect('../../pages-notif-admin/')
    return redirect('../../pages-notif/')


@login_required(login_url='../../register/login/')
def delete_demande(request, id_demande):
    """ Cette vue permet de supprimer/annuler une demande en cours d'enregistrement."""
    if request.method == 'POST':
        demande = mysite.models.Demande.objects.get(id=id_demande)
        if request.user.type =='1':
            comptEntreprise =0
            try :
                user = mysite.models.User.objects.get(email=demande.inputMail)
            except ObjectDoesNotExist :
                pass
            else:
                demandes=  mysite.models.Demande.objects.filter(user=user)
                entreprises= mysite.models.Entreprise.objects.filter(user=user)
                for entreprise in entreprises :
                    if entreprise.siren == demande.inputSIREN:
                        comptEntreprise +=1 
                if comptEntreprise == 1:
                    entreprise = mysite.models.Entreprise.objects.get(user=user,siren = demande.inputSIREN)
                    entreprise.delete()
                if demandes.count() == 0:
                    connection = mysite.models.Connexion.objects.get(user=user)
                    connection.delete()
                    user.delete()

        demande.delete()
        try:
            request.session['id_demande_new']
        except KeyError:
            pass
        else:
            del request.session['id_demande_new']
    if request.user.type =='1':
        return redirect('../../demande-en-cours-admin/')
    return redirect('../../demandes/')

@login_required(login_url='../../register/login')
def delete_admin_docs(request, id_doc):
    """ Cette vue permet de supprimer un document d'une demande précisé."""
    if request.method == 'POST':
        doc = mysite.models.GestionDoc.objects.get(id=id_doc)
        if os.path.exists("mysite/media/" + str(doc.adresse_doc)):
            os.remove("mysite/media/" + str(doc.adresse_doc))
        else:
            logging.error("The file does not exist")
            logging.error(doc.id)
            logging.error(doc.adresse_doc)
        doc.delete()
    return redirect('../../crm-leads-admin/')


def sub_delete_admin_all_docs(id_demande,type):
    """ Cette vue permet de supprimer plusieurs document d'une demande précisé et d'un ou plusieurs type donné"""
    for i in range(len(type)):
        docs = mysite.models.GestionDoc.objects.filter(type=type[i],id_demande=id_demande)
        for doc in docs :
            if os.path.exists("mysite/media/" + str(doc.adresse_doc)):
                os.remove("mysite/media/" + str(doc.adresse_doc))
                doc.delete()
            else:
                logging.error("The file does not exist")
    return 1

def delete_admin_all_docs(request, id_demande):
    """ initialise le tableau "type" avec les types defini en fonction du boutons dans le modal des leads super admin
        appelle sub_delete_admin_all_docs pour supprimer les documents corespondant
    """
    if request.method == 'POST':
        if 'buttonPiece' in request.POST:
            type=["Piece_identite"]
            sub_delete_admin_all_docs(id_demande,type)
        elif 'buttonKbis' in request.POST:
            type = ["Kbis","Bilan","Projet_de_bail_ou_LOI"]
            sub_delete_admin_all_docs(id_demande,type)
        elif 'buttonStatut' in request.POST :
            type = ["Statut_societe","Business_plan","Presentation_entreprise"]
            sub_delete_admin_all_docs(id_demande,type)
        else:
            type = ["Autre_document"]
            sub_delete_admin_all_docs(id_demande,type)
    return redirect('../../../crm-leads-admin/')

@login_required(login_url='../../register/login/')
def doc_consulting(request):
    """ Cette vue permet la consultation des documents upload."""
    context = {}
    docs_id = []
    docs_immo = []
    docs_entreprise = []
    docs_autre = []

    demandes = mysite.models.Demande.objects.filter(user=request.user)
    try:
        request.session['id_demande_of_doc_deleted']
    except KeyError:
        context['active'] = demandes[0].id
    else:
        context['active'] = request.session['id_demande_of_doc_deleted']

    context['demandes'] = demandes
    docs = mysite.models.GestionDoc.objects.filter(user=request.user)
    for doc in docs:
        if doc.type == "Piece_identite":
            docs_id.append(doc)
            context['docs_id'] = docs_id
        elif doc.type in ["Kbis", "Bilan", "Projet_de_bail_ou_LOI"]:
            docs_immo.append(doc)
            context['docs_immo'] = docs_immo
        elif doc.type == "Autre_document":
            docs_autre.append(doc)
            context['docs_autre'] = docs_autre
        else:
            docs_entreprise.append(doc)
            context['docs_entreprise'] = docs_entreprise
    return render(request, 'admin/mes-documents.html', context)

@login_required(login_url='../../register/login/')
def redirectNotifButton(request,id_notif):
    """
    redirige vers la bonne page lorsque l'on clique sur la notification (admin et client)
    depuis le header ou la page 
    """
    notif= mysite.models.Message.objects.get(id=id_notif)
    notif.etat=1
    notif.save()
    request.session['message']=request.session['message']-1
    if notif.type == 'doc':
        request.session['id_demande_upload'] = notif.demande.id
        return redirect('../../upload/')
    elif notif.type == 'ajout':
        request.session['id_demande_of_doc_deleted'] = notif.demande.id
        return redirect('../../documents/')
    elif notif.type == 'modif':
        request.session['id_demande_consulting'] = notif.demande.id
        return redirect('../../consulting/')
    elif notif.type == 'ticket':
        if request.user.type == '1':
            return redirect('../../tickets/')
        else:
            return redirect('../../tickets-consulting/')
    if request.user.type == '1':
            return redirect('../../pages-notif-admin/')
    return redirect('../../pages-notif/')

@login_required(login_url='../../register/login/')
def return_loc(request, id_demande):
    """ Cette vue redirige l'utilisateur vers la page update de demande s'il appuie sur le button 'Retour'."""
    request.session['id_demande_update'] = id_demande
    if request.user.type == '1':
        return redirect('../../update-demande-loc-admin/')
    return redirect('../../update-demande-loc/')

@login_required(login_url='../../register/login/')
def new_demande_loc(request):
    """ Cette vue permet d'enregistrée les données saisies par l'utilisateur lors de sa nouvelle demande.
     Les données de la demande précedente sont utilisées pour préremplir celle de la nouvelle. Partie locataire."""
    context = {}
    last_demande = mysite.models.Demande.objects.filter(user=request.user).last()
    context['last_demande'] = last_demande
    user = mysite.models.User.objects.get(id=request.user.id)
    demandes = mysite.models.Demande.objects.filter(user=request.user)
    context['user'] = user

    sirens = []
    for dmd in demandes:
        sirens.append(dmd.inputSIREN)

    if request.method == 'POST':
        demande = mysite.models.Demande()

        demande.user = user
        demande.etat = 4
        demande.physical_moral = request.POST['physical_moral']
        demande.juridical_form = request.POST['juridical_form']
        demande.social_reason = request.POST['social_reason']
        demande.inputSIREN = request.POST['inputSIREN']
        demande.gender = request.POST['gender']
        demande.inputName = request.POST['inputName']
        demande.inputFirstName = request.POST['inputFirstName']
        if request.user.type == '1':
            demande.inputMail = request.POST['inputMail']
        else:
            demande.inputMail = request.user.email
        demande.inputPhone = request.POST['inputPhone']
        demande.inputActivity = request.POST['inputActivity']
        demande.inputWebSite = request.POST['inputWebSite']

        if request.user.type == '1':
            demande.save()
            try :
                olddemande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
            except Exception:
                pass
            else:
                olddemande.delete()
            request.session['id_demande_new'] = demande.id
            return redirect('../new-demande-bail-super-admin/')

        if last_demande.etat != 4:
            demande.save()
            request.session['id_demande_new'] = demande.id

            if request.POST['inputSIREN'] not in sirens:
                entreprise = mysite.models.Entreprise()
                entreprise.user = user
                entreprise.social_reason = request.POST['social_reason']
                entreprise.representant = request.POST['inputName'] + request.POST['inputFirstName']
                entreprise.siteweb = request.POST['inputWebSite']
                entreprise.siren = request.POST['inputSIREN']
                entreprise.juridical_form = request.POST['juridical_form']
                entreprise.inputActivity = request.POST['inputActivity']
                entreprise.id_demande = request.session['id_demande_new']
                entreprise.save()

            return redirect('../new-demande-bail/')
        else:
            return redirect('../new-demande-loc/')
    if request.user.type == '1':
        return render(request, './admin/new-demande-loc-super-admin.html', context)
    return render(request, './admin/new-demande-loc.html', context)

def ajax_siret(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        info={}
        # url = "https://api.societe.com/pro/dev/societe/827636507&token=5d99ff69d6ccc15df13fd94643e9f87d&format=json"
        # r = requests.get(url)
        # logging.error("------------------r----------------")
        # logging.error(r)
        # logging.error(r.text)
        info["social-reason"]=""
        info["physical-moral"] = "moral"
        info["categorieJuridiqueUniteLegale"] =""
        x = request.body.decode('utf-8').split(',')
        siret=x[0]
        try:
            data = api.siret(siret).get()
        except HTTPError : 
            info["adresse"]= ""
            info["codePostal"] = ""
            info["commune"] = ""
        else:
            categorieII= int(data["etablissement"]["uniteLegale"]["categorieJuridiqueUniteLegale"]) // 100
            codeActivity = data["etablissement"]["uniteLegale"]["activitePrincipaleUniteLegale"][0:2]
            jsonFile= json.load(open('mysite/mysite/static/register/assets/activityfromcode.json'))
            for i in range (len(jsonFile)):
                if jsonFile[i]["A"] == str(codeActivity):
                    info["activity"]= jsonFile[i]["B"]
                    break
            if "denominationUniteLegale" in dict.keys(data["etablissement"]["uniteLegale"]):
                info["social-reason"]=data["etablissement"]["uniteLegale"]["denominationUniteLegale"]
            if categorieII==10:
                info["physical-moral"] = "physical"
                info["categorieJuridiqueUniteLegale"] = "EI"
                info["nom"] = data["etablissement"]["uniteLegale"]["nomUsageUniteLegale"]
                info["social-reason"]= info["nom"]
                info["sexe"] = data["etablissement"]["uniteLegale"]["sexeUniteLegale"]
                info["prenom"] = data["etablissement"]["uniteLegale"]["prenomUsuelUniteLegale"]
            elif (categorieII<58) and (categorieII>53):
                info["categorieJuridiqueUniteLegale"] = "SC"
            elif categorieII==22:
                info["categorieJuridiqueUniteLegale"] = "EIRL"
            elif categorieII==52:
                info["categorieJuridiqueUniteLegale"] = "SNC"
    return JsonResponse(info)

def getOrElse(x, y):
  return x if x is not None else y


def get_adresse_insee(siret):
    info={}
    if siret:
        try:
            data = api.siret(siret).get()
        except HTTPError : 
            info["adresse"]= ""
            info["codePostal"] = ""
            info["commune"] = ""
        else:
            try :
                info["adresse"]= getOrElse(data["etablissements"][0]["adresseEtablissement"]["numeroVoieEtablissement"],'') +" "+ getOrElse(data["etablissements"][0]["adresseEtablissement"]["typeVoieEtablissement"],'') +" "+ getOrElse(data["etablissement"][0]["adresseEtablissement"]["libelleVoieEtablissement"],'')
                info["codePostal"] = getOrElse(data["etablissements"][0]["adresseEtablissement"]["codePostalEtablissement"],'')
                info["commune"] = getOrElse(data["etablissements"][0]["adresseEtablissement"]["libelleCommuneEtablissement"],'')
            except KeyError:
                info["adresse"]= getOrElse(data["etablissement"]["adresseEtablissement"]["numeroVoieEtablissement"],'')  +" "+ getOrElse(data["etablissement"]["adresseEtablissement"]["typeVoieEtablissement"],'')  +" "+ getOrElse(data["etablissement"]["adresseEtablissement"]["libelleVoieEtablissement"],'')
                info["codePostal"] = getOrElse(data["etablissement"]["adresseEtablissement"]["codePostalEtablissement"],'')
                info["commune"] = getOrElse(data["etablissement"]["adresseEtablissement"]["libelleCommuneEtablissement"],'')
    return info

@login_required(login_url='../../register/login/')
def new_demande_bail(request):
    """ Cette vue permet d'enregistrée les données saisies par l'utilisateur lors de sa nouvelle demande.
    Partie bail."""
    context = {}
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
    context['demande'] = demande
    info = get_adresse_insee(demande.inputSIREN)
    context["adresse"] = info["adresse"]
    context["codePostal"] = info["codePostal"]
    context["city"] = info["commune"]
    if request.method == 'POST':
        demande.inputAddress = request.POST.get('inputAddress')
        demande.inputCode = request.POST.get('inputCode')
        demande.inputCity = request.POST.get('inputCity')
        if request.POST.get('mois') != None: demande.mois = request.POST.get('mois')
        if request.POST.get('annee') != None: demande.annee = request.POST.get('annee')
        demande.loyer = request.POST.get('loyer')
        demande.garantie = request.POST.get('garantie')
        demande.garantieMois = request.POST.get('garantieMois')
        demande.caution = request.POST.get('caution')
        demande.cautionMois = request.POST.get('cautionMois')

        demande.save()
        if request.user.type == '1':
            return redirect('../new-demande-garantie-super-admin/')
        return redirect('../new-demande-garantie/')
    if request.user.type == '1':
        return render(request, './admin/new-demande-bail-super-admin.html', context)
    return render(request, './admin/new-demande-bail.html', context)

@login_required(login_url='../../register/login/')
def new_demande_garantie(request):
    """ Cette vue permet d'enregistrée les données saisies par l'utilisateur lors de sa nouvelle demande.
    Partie garantie."""
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])

    if request.method == 'POST':
        demande.substitution = request.POST.get('substitution')

        demande.save()
        if request.user.type == '1':
            return redirect('../new-demande-eligibilite-super-admin/')
        return redirect('../new-demande-eligibilite/')
        
    if request.user.type == '1':
        return render(request, './admin/new-demande-garantie-super-admin.html')
    return render(request, './admin/new-demande-garantie.html')

@login_required(login_url='../../register/login/')
def new_demande_eligibilite(request):
    """ Cette vue permet d'enregistrée les données saisies par l'utilisateur lors de sa nouvelle demande.
    Partie éligiblité. L'algo contrôle alors si la demande est éligible et défini ainsi l'état de la demande.
    Si non éligible, la demande est supprimée."""
    context = {}
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])

    if request.method == 'POST':
        demande.incident = request.POST.get('incident')
        demande.difficulte = request.POST.get('difficulte')
        demande.preavis = request.POST.get('preavis')
        demande.echeance = request.POST.get('echeance')
        if request.POST.get('echeance') == "yes":
            demande.renouveler = request.POST['renouveler']
        demande.plusDeuxAns = request.POST.get('plusDeuxAns')
        if request.POST.get('plusDeuxAns') == "yes":
            demande.ca2021 = request.POST.get('ca2021')
            demande.beneficePerte2021 = request.POST.get('beneficePerte2021')
            demande.ca2020 = request.POST.get('ca2020')
            demande.beneficePerte2020 = request.POST.get('beneficePerte2020')
            demande.conges = request.POST.get('conges')
            demande.cautionPerso = request.POST.get('cautionPerso')
            if request.POST.get('conges') == "yes":
                demande.CC = request.POST.get('CC')
        else:
            demande.cautionPerso = request.POST.get('cautionPerso')
            demande.QuietSolution = request.POST.get('QuietSolution')
        demande.date_demande = datetime.now()

        if demande.incident == "yes" or demande.difficulte == "yes" or demande.preavis == "yes" or (demande.echeance == "yes" and demande.renouveler == "no"):
            etat = 0

        elif demande.cautionPerso == "no" or demande.QuietSolution == "no":
            etat = 0

        elif demande.plusDeuxAns == "yes":
            benefice = demande.beneficePerte2020 + demande.beneficePerte2021
            if int(benefice) > 0 and int(demande.loyer) < 150000 and int(demande.loyer) >50000:
                etat = 3
            else:
                etat = 1

        else:
            etat = 1
        
        demande.etat = etat
        demande.etat=3

        if request.user.type == '1':
            demande.save()
            return redirect('../new-demande-complete-super-admin/new/')
        if demande.etat != 0:
            demande.save()
        else:
            demande.delete()
            del request.session['id_demande_new']

        return redirect('../new-demande-complete/')
    if request.user.type == '1':
        return render(request, './admin/new-demande-eligibilite-super-admin.html')
    return render(request, './admin/new-demande-eligibilite.html')

@login_required(login_url='../../register/login/')
def new_demande_complete(request):
    """ Cette vue permet d'afficher un message à l'utilisateur en fct de l'état de sa nouvelle demande."""
    context = {}
    try:
        request.session['id_demande_new']
    except KeyError:
        context['etat'] = 0
    else:
        demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
        context['etat'] = demande.etat

    return render(request, './admin/new-demande-complete.html', context)

def ajax_mail_demande_en_cours(request):
    info={}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            request.session['id_demande_new']
        except KeyError:
            info['mail'] = "no"
        else:
            demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
            info['mail'] = demande.inputMail

    return JsonResponse(info)

@login_required(login_url='../../register/login/')
def retour_after_complete_super_admin(request,type):
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
    allUserDemande = mysite.models.Demande.objects.filter(user=demande.user)
    user_demande = mysite.models.User.objects.get(id=demande.user.id)
    if allUserDemande.count ==1 :
        entreprise = mysite.models.Entreprise.objects.get(user=demande.user)
        connection = mysite.models.Connection.objects.get(user=demande.user)
        entreprise.delete()
        connection.delete()
        user_demande.delete()
    if type == "update":
        return redirect("../../update-demande-eligibilite-admin/")
    return redirect("../../new-demande-eligibilite-super-admin/")


@login_required(login_url='../../register/login/')
def new_demande_complete_super_admin(request,type):
    """ Cette vue permet d'afficher un message à l'utilisateur en fct de l'état de sa nouvelle demande."""
    context = {}
    try:
        request.session['id_demande_new']
    except KeyError:
        messages.info(request, "0", extra_tags='etat')
    else:
        demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
        if demande.etat == 0:       #Attention debug a remettre a la mise en prod
            #demande.delete()
            #del request.session['id_demande_update']
            messages.info(request, "0", extra_tags='etat')
        else : 
            try :
                user = mysite.models.User.objects.get(email=demande.inputMail)
            except ObjectDoesNotExist :
                user = mysite.models.User()

                user.email = demande.inputMail
                user.first_name = demande.inputFirstName
                user.last_name = demande.inputName
                user.adresse = demande.inputAddress
                user.code_postal = demande.inputCode
                user.siteweb = demande.inputWebSite
                user.siren = demande.inputSIREN
                user.mobile = demande.inputPhone
                user.physical_moral = demande.physical_moral
                user.gender = demande.gender
                user.password = make_password("abcde")

                user.save()

                connectionCreate = mysite.models.Connexion()
                connectionCreate.user = user
                connectionCreate.save()

                entreprise = mysite.models.Entreprise()
                entreprise.user = user
                entreprise.social_reason = demande.social_reason
                entreprise.representant = demande.inputName + demande.inputFirstName
                entreprise.siteweb = demande.inputWebSite
                entreprise.siren = demande.inputSIREN
                entreprise.juridical_form = demande.juridical_form
                entreprise.inputActivity = demande.inputActivity
                entreprise.id_demande = request.session['id_demande_new']
                entreprise.save()
                messages.info(request, "4", extra_tags='etat')
                if type== "update":
                    redirect("../../get_password_update/")
                return redirect("../../get_password/")
            else :
                demandes = mysite.models.Demande.objects.filter(user=user)
                if demandes.exists():
                    sirens = []
                    for dmd in demandes:
                        sirens.append(dmd.inputSIREN)
                    
                    if demande.inputSIREN not in sirens: 
                        entreprise = mysite.models.Entreprise()
                        entreprise.user = user
                        entreprise.social_reason = demande.social_reason
                        entreprise.representant = demande.inputName + demande.inputFirstName
                        entreprise.siteweb = demande.inputWebSite
                        entreprise.siren = demande.inputSIREN
                        entreprise.juridical_form = demande.juridical_form
                        entreprise.inputActivity = demande.inputActivity
                        entreprise.id_demande = request.session['id_demande_new']
                        entreprise.save()
                else:
                    messages.info(request, "4", extra_tags='etat')
                    if type== "update":
                        redirect("../../get_password_update/")
                    return redirect("../../get_password/")
            demande.user = user
            demande.save()
            messages.info(request, demande.etat, extra_tags='etat')
    if type== "update":
        redirect("../../get_password_update/")
    return redirect("../../get_password/")


from django.urls import reverse_lazy

class PasswordResetForm_extend(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'readonly':True}),
    )

class PasswordResetView_extend(auth_views.PasswordResetView):
    form_class = PasswordResetForm_extend
    success_url = reverse_lazy("password_reset_done_extend")

    def get_initial(self):
        return {'email': mysite.models.Demande.objects.get(id=self.request.session['id_demande_new']).inputMail}

class PasswordResetDoneView_extend(auth_views.PasswordResetDoneView):

    def dispatch(self, request, *args, **kwargs):
        demande = mysite.models.Demande.objects.get(id=request.session['id_demande_new'])
        user = mysite.models.User.objects.get(email=demande.inputMail)
        demande.user = user
        demande.save()
        return super(PasswordResetDoneView_extend, self).dispatch(request, *args, **kwargs)
        


@login_required(login_url='../../register/login/')
def update_choice(request):
    """ Cette vue permet d'instancier l'id de session en fct de la demande à update sélectionnée."""
    if request.method == 'POST':
        request.session['id_demande_update'] = request.POST['choice']
        if request.user.type == '1':
            return redirect ('../update-demande-loc-admin/')
        return redirect('../update-demande-loc/')
    else:
        return redirect('../demandes/')

@login_required(login_url='../../register/login/')
def update_demande_loc(request):
    """ Cette vue permet d'update la demande correspondant à l'id de session actuel.
    Les données déjà saisies sont alors préremplies. Partie locataire."""
    context = {}
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_update'])
    context['demande'] = demande
    demandes = mysite.models.Demande.objects.filter(user=request.user)
    user = mysite.models.User.objects.get(id=request.user.id)

    context['user'] = user

    sirens = []
    for dmd in demandes:
        sirens.append(dmd.inputSIREN)

    if request.method == 'POST':
        if request.POST['inputSIREN'] not in sirens:
            entreprise = mysite.models.Entreprise()
            entreprise.user = user
            entreprise.id_demande = request.session['id_demande_update']
            entreprise.social_reason = request.POST['social_reason']
            entreprise.representant = request.POST['inputName'] + request.POST['inputFirstName']
            entreprise.siteweb = request.POST['inputWebSite']
            entreprise.siren = request.POST['inputSIREN']
            entreprise.juridical_form = request.POST['juridical_form']
            entreprise.inputActivity = request.POST['inputActivity']

            entreprise.save()

        demande.user = user
        demande.etat = 4
        demande.physical_moral = request.POST['physical_moral']
        demande.juridical_form = request.POST['juridical_form']
        demande.social_reason = request.POST['social_reason']
        demande.inputSIREN = request.POST['inputSIREN']
        demande.gender = request.POST['gender']
        demande.inputName = request.POST['inputName']
        demande.inputFirstName = request.POST['inputFirstName']
        demande.inputPhone = request.POST['inputPhone']
        demande.inputActivity = request.POST['inputActivity']
        demande.inputWebSite = request.POST['inputWebSite']
        if request.user.type == '1':
            demande.inputMail = request.POST['inputMail']
    
        demande.save()
        request.session['id_demande_update'] = demande.id
        if request.user.type == '1':
            return redirect('../update-demande-bail-admin/')
        return redirect('../update-demande-bail/')
    if request.user.type == '1':
        return render(request, './admin/update-demande-loc-admin.html',context)
    return render(request, './admin/update-demande-loc.html', context)

@login_required(login_url='../../register/login/')
def update_demande_bail(request):
    """ Cette vue permet d'update la demande correspondant à l'id de session actuel.
    Les données déjà saisies sont alors préremplies. Partie bail."""
    context = {}
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_update'])
    context['demande'] = demande

    if request.method == 'POST':
        demande.InputAddress = request.POST.get('inputAddress')
        demande.inputCode = request.POST.get('inputCode')
        demande.inputCity = request.POST.get('inputCity')
        if request.POST.get('mois') != None: demande.mois = request.POST.get('mois')
        if request.POST.get('annee') != None: demande.mois = request.POST.get('annee')
        demande.loyer = request.POST.get('loyer')
        demande.garantie = request.POST.get('garantie')
        demande.garantieMois = request.POST.get('garantieMois')
        demande.caution = request.POST.get('caution')
        demande.cautionMois = request.POST.get('cautionMois')
        demande.save()

        entreprises = mysite.models.Entreprise.objects.filter(user = demande.user, siren=demande.inputSIREN)
        for entreprise in entreprises:
            entreprise.adresse = demande.inputAddress
            entreprise.code_postal = demande.inputCode
            entreprise.ville = demande.inputCity
            entreprise.save()

        if request.user.type == '1':
            return redirect('../update-demande-garantie-admin/')
        return redirect('../update-demande-garantie/')
    if request.user.type == '1':
        return render(request, './admin/update-demande-bail-admin.html', context)
    return render(request, './admin/update-demande-bail.html', context)

@login_required(login_url='../../register/login/')
def update_demande_garantie(request):
    """ Cette vue permet d'update la demande correspondant à l'id de session actuel.
    Les données déjà saisies sont alors préremplies. Partie garantie."""
    context = {}
    logging.error("enter")
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_update'])
    context['demande'] = demande

    if request.method == 'POST':
        demande.substitution = request.POST.get('substitution')

        demande.save()
        logging.error("pass Post")
        if request.user.type == '1':
            return redirect('../update-demande-eligibilite-admin/')
        return redirect('../update-demande-eligibilite/')
    if request.user.type == '1':
        return render(request, './admin/update-demande-garantie-admin.html', context)
    return render(request, './admin/update-demande-garantie.html', context)

@login_required(login_url='../../register/login/')
def pages_notif_admin(request):
    """ affiche la page avec toute les notifs pour client et super admin dans leurs pages-notif et pages-notif-admin"""
    C={}
    i=0
    user=mysite.models.User.objects.get(id=request.user.id)
    C["message"] = mysite.models.Message.objects.filter(getter=user).order_by("-date_message")
    for message in C["message"]:
        message.etat=1
        message.save()
        i=i+1
        seconde=(datetime.now(timezone.utc) - message.date_message).seconds
        heure=int(seconde/3600)
        minutes = int((seconde - (heure*3600))/60)
        message.date_message= str(heure) + ' h ' + str(minutes)
    request.session['message'] = 0
    if (request.user.type == '1'):
        return render(request, './admin/pages-notif-admin.html', C)
    return render(request, './admin/pages-notif.html', C)


@login_required(login_url='../../register/login/')
def update_demande_eligibilite(request):
    """ Cette vue permet d'update la demande correspondant à l'id de session actuel.
    Les données déjà saisies sont alors préremplies. Partie éligibilité."""
    context = {}
    demande = mysite.models.Demande.objects.get(id=request.session['id_demande_update'])
    context['demande'] = demande

    if request.method == 'POST':
        demande.incident = request.POST.get('incident')
        demande.difficulte = request.POST.get('difficulte')
        demande.preavis = request.POST.get('preavis')
        demande.echeance = request.POST.get('echeance')
        if request.POST.get('echeance') == "yes":
            demande.renouveler = request.POST['renouveler']
        demande.plusDeuxAns = request.POST.get('plusDeuxAns')
        if request.POST.get('plusDeuxAns') == "yes":
            demande.ca2021 = request.POST.get('ca2021')
            demande.beneficePerte2021 = request.POST.get('beneficePerte2021')
            demande.ca2020 = request.POST.get('ca2020')
            demande.beneficePerte2020 = request.POST.get('beneficePerte2020')
            demande.conges = request.POST.get('conges')
            if request.POST.get('conges') == "yes":
                demande.CC = request.POST.get('CC')
        else:
            demande.cautionPerso = request.POST.get('cautionPerso')
            demande.QuietSolution = request.POST.get('QuietSolution')
        demande.date_demande = datetime.now()

        if demande.incident == "yes" or demande.difficulte == "yes" or demande.preavis == "yes" or (demande.echeance == "yes" and demande.renouveler == "no"):
            etat = 0

        elif demande.cautionPerso == "no" or demande.QuietSolution == "no":
            etat = 0

        elif demande.plusDeuxAns == "yes":
            benefice = demande.beneficePerte2020 + demande.beneficePerte2021
            if int(benefice) > 0 and int(demande.loyer) < 150000 and int(demande.loyer) > 50000:
                etat = 3
            else:
                etat = 1

        else:
            etat = 1

        etat = 3
        demande.etat = etat
        if (request.user.type == '1'):
            request.session['id_demande_new'] = request.session['id_demande_update']
            demande.save()
            return redirect('../new-demande-complete-super-admin/update/')

        if demande.etat != 0:
            demande.save()
        else:
            demande.delete()
            del request.session['id_demande_update']
        
        
        return redirect('../update-demande-complete/')
    if (request.user.type == '1'):
        return render(request, './admin/update-demande-eligibilite-admin.html')
    return render(request, './admin/update-demande-eligibilite.html')

class PasswordResetView_extend_update(auth_views.PasswordResetView):
    form_class = PasswordResetForm_extend

    def get_initial(self):
        return {'email': mysite.models.Demande.objects.get(id=self.request.session['id_demande_update']).inputMail}


@login_required(login_url='../../register/login/')
def update_demande_complete(request):
    """ Cette vue est plus ou moins la même que 'new-demande-complete'."""
    context = {}
    try:
        request.session['id_demande_update']
    except KeyError:
        context['etat'] = 0
    else:
        demande = mysite.models.Demande.objects.get(id=request.session['id_demande_update'])
        context['etat'] = demande.etat

    return render(request, './admin/new-demande-complete.html', context)

@login_required(login_url='../../register/login/')
def tickets_consulting(request):
    """ Cette vue permet de calculer toutes les données nécessaires à l'affichage de la page 'Mes tickets'."""
    context = {}
    context['tickets'] = mysite.models.Ticket.objects.filter(user=mysite.models.User.objects.get(id=request.user.id)).order_by('-date_creation')
    context['open_tickets'] = mysite.models.Ticket.objects.filter(user=mysite.models.User.objects.get(id=request.user.id), etat='1')
    context['closed_tickets'] = mysite.models.Ticket.objects.filter(user=mysite.models.User.objects.get(id=request.user.id), etat='0')
    context['done_tickets'] = mysite.models.Ticket.objects.filter(user=mysite.models.User.objects.get(id=request.user.id), etat='2')

    if context['tickets'].count() > 0:
        context['done_percent'] = 100 * context['done_tickets'].count() // context['tickets'].count()
        context['closed_percent'] = 100 * context['closed_tickets'].count() // context['tickets'].count()
        context['open_percent'] = 100 * context['open_tickets'].count() // context['tickets'].count()
    else:
        context['done_percent'] = 0
        context['closed_percent'] = 0
        context['open_percent'] = 0

    context['demandes'] = mysite.models.Demande.objects.filter(user=request.user)
    return render(request, './admin/tickets-consulting.html', context)

class PasswordResetForm_createAdmin(auth_forms.PasswordResetForm):
    first_name = forms.CharField(
        label=_("first_name"),
        max_length=254
    )
    last_name = forms.CharField(
        label=_("last_name"),
        max_length=254
    )
    mobile = forms.CharField(
        label=_("mobile"),
        max_length=254
    )

class PasswordResetView_createAdmin(auth_views.PasswordResetView):
    form_class = PasswordResetForm_createAdmin

    def dispatch(self, *args, **kwargs):
        kwargs.update ({
            "initial": {},
            "prefix": None,
        })

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )            
            try :
                user = mysite.models.User.objects.get(email=kwargs['data']['email'])
            except ObjectDoesNotExist :
                user = mysite.models.User()
                connectionCreate = mysite.models.Connexion()
                connectionCreate.user = user
                connectionCreate.save()

            user.email = kwargs['data']['email']
            user.first_name = kwargs['data']['first_name']
            user.last_name = kwargs['data']['last_name']
            user.mobile = kwargs['data']['mobile']
            user.physical_moral = "moral"
            user.gender = ""
            user.password = make_password("abcde")
            user.type = "2"
            user.save()
        return super().dispatch(*args, **kwargs)



@login_required(login_url='../../register/login/')
def admin_select(request,id_demande):
    if request.method == 'POST':

        logging.error(request.POST.get('admin'))
        admin = mysite.models.User.objects.get(id=request.POST.get('admin'))
        demande = mysite.models.Demande.objects.get(id=id_demande)
        user = mysite.models.User.objects.get(id=demande.user.id)
        user.administrator = admin
        user.save()

        logging.error("ca passe")
    return redirect('../../crm-leads-admin/')

@login_required(login_url='../../register/login/')
def new_ticket(request):
    """
    Cette vue permet d'enregistrer les données saisies par l'utilisateur lors de la création d'un nouveau ticket ou un admin.
    """
    if request.method == 'POST':
        ticket = mysite.models.Ticket()
        ticket.demande = mysite.models.Demande.objects.get(id=request.POST.get('demande'))
        ticket.user = mysite.models.User.objects.get(id=ticket.demande.user)
        ticket.service = request.POST.get('service')
        ticket.objet = request.POST.get('objet')
        ticket.category = request.POST.get('type')
        ticket.contenu = request.POST.get('contenu')
        ticket.date_creation = str(datetime.now(timezone.utc))
        ticket.etat = 1

        ticket.save()
    if request.user.type == '1':
        return redirect('../tickets/')
    return redirect('../tickets-consulting/')

def leads_changement_etats(request):
    """changer l'etat d'une demande dans les leads"""
    if request.method == 'POST':
        x = request.body.decode('utf-8').split(',')
        etat=x[0]
        id_demande=x[1]
        demande = mysite.models.Demande.objects.get(id=id_demande)
        demande.etat = etat
        demande.save()
    return HttpResponse("true")

def modify_user_super_admin(request):
    """modifier user depuis l'espace "modify_user_super_admin grace a l'id de l'user, set par "modify_user_super_admin_choice" 
    en session
    """
    context = {}
    context['id'] = request.session['user_admin_consulting']
    user = mysite.models.User.objects.get(id=request.session['user_admin_consulting'])
    entreprises = mysite.models.Entreprise.objects.filter(user=request.session['user_admin_consulting'])
    context['active'] = entreprises[0].id
    context['entreprises'] = entreprises
    context['user'] = user
    if request.method == 'POST':
        #Si le formulaire 'infoform' est rempli
        if 'infoform' in request.POST:
            user.gender = request.POST.get('gender')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.mobile = request.POST.get('mobile')
            user.email = request.POST.get('email')
            user.save()

        # Si le formulaire 'infoentreprise' est rempli
        for entreprise in entreprises:
            if 'infoentreprise' + str(entreprise.id) in request.POST:
                entreprise.social_reason = request.POST.get('social_reason')
                entreprise.adresse = request.POST.get('adresse')
                entreprise.code_postal = request.POST.get('codepostal')
                entreprise.siren = request.POST.get('siren')
                entreprise.descriptif = request.POST.get('descriptif')
                entreprise.siteweb = request.POST.get('website')
                entreprise.juridical_form = request.POST.get('juridical_form')
                entreprise.inputActivity = request.POST.get('inputActivity')
                entreprise.ville = request.POST.get('ville')
                entreprise.save()
    return render(request, './admin/modify-user-super-admin.html', context)

def modify_demande_super_admin(request,id_demande):
    """
    modifier demande depuis l'espace lead du super admin grace a l'id de la demande
    """
    try:
        context={}
        demande = mysite.models.Demande.objects.get(id=id_demande)
        if request.method == 'POST':
            #Si le formulaire 'infoform' est rempli
            if 'modifyDemandeLocataire' in request.POST:
                demande.physical_moral = request.POST.get('physical_moral')
                demande.juridical_form = request.POST.get('juridical_form')
                demande.social_reason = request.POST.get('social_reason')
                demande.inputSIREN = request.POST.get('inputSIREN')
                demande.gender = request.POST.get('gender')
                demande.inputName = request.POST.get('inputName')
                demande.inputFirstName = request.POST.get('inputFirstName')
                demande.inputMail = request.POST.get('inputMail')
                demande.inputPhone = request.POST.get('inputPhone')
                demande.inputActivity = request.POST.get('inputActivity')
                demande.inputWebSite = request.POST.get('inputWebSite')
                demande.save()

            # Si le formulaire 'infoentreprise' est rempli
            if 'modifyDemandeBail' in request.POST:
                demande.inputCode = request.POST.get('inputCode')
                demande.inputAdress = request.POST.get('inputAdress')
                demande.inputCity = request.POST.get('inputCity')
                if request.POST.get('mois') != None: demande.mois = request.POST.get('mois')
                if request.POST.get('annee') != None: demande.mois = request.POST.get('annee')
                demande.loyer = request.POST.get('loyer')
                demande.garantie = request.POST.get('garantie')
                demande.garantieMois = request.POST.get('garantieMois')
                demande.caution = request.POST.get('caution')
                demande.cautionMois = request.POST.get('cautionMois')
                demande.save()

            if 'modifyDemandeEligibility' in request.POST:
                if 'substitution0' in request.POST:
                    if 'substitution1' in request.POST:
                        demande.substitution = 2
                    else:
                         demande.substitution = 0
                else:
                    demande.substitution = 1
                #demande.substitution = request.POST.get('substitution')
                demande.incident = request.POST.get('incident')
                demande.difficulte = request.POST.get('difficulte')
                demande.preavis = request.POST.get('preavis')
                demande.echeance = request.POST.get('echeance')
                demande.renouveler = request.POST.get('renouveler')
                demande.plusDeuxAns = request.POST.get('plusDeuxAns')
                demande.ca2021 = request.POST.get('ca2021')
                demande.beneficePerte2021 = request.POST.get('beneficePerte2021')
                demande.ca2020 = request.POST.get('ca2020')
                demande.beneficePerte2020 = request.POST.get('beneficePerte2020')
                demande.conges = request.POST.get('conges')
                demande.CC = request.POST.get('CC')
                demande.cautionPerso = request.POST.get('cautionPerso')
                demande.QuietSolution = request.POST.get('QuietSolution')
                demande.save()
    except:
        return redirect('../../../../admin/crm-leads-admin/')

    return redirect('../../../../admin/crm-leads-admin/')

def crm_contact_admin(request):
    """
    afficher les demande de contact depuis le formulaire de contact du site vitrine (pas de compte utilisateur)
    """
    context={}
    context["Contact"] = mysite.models.Contact.objects.all()
    return render(request, './admin/crm-contacts-admin.html', context)


#---------------------------------------faire des commentaire !!!
def ajax_change_etat_contact(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        x = request.body.decode('utf-8').split(',')
        etat=x[0]
        id_contact=x[1]
        if etat == "supprimer":
            contact = mysite.models.Contact.objects.get(id=id_contact)
            contact.delete()
        else :
            contact = mysite.models.Contact.objects.get(id=id_contact)
            contact.etat = etat
            contact.save()
    return HttpResponse("true")


def ajax_change_etat_tickets(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        x = request.body.decode('utf-8').split(',')
        etat=x[0]
        id_ticket=x[1]
        ticket = mysite.models.Ticket.objects.get(id=id_ticket)
        if ticket.etat != etat:
            ticket.etat = etat
            if etat == '0' or etat == '2':
                ticket.date_cloture = datetime.now()
            ticket.save()
            message = mysite.models.Message()
            message.setter = mysite.models.User.objects.get(id=request.user.id)
            message.getter = ticket.user
            message.demande = ticket.demande
            message.type = "ticket"
            message.titre = "Votre ticket à bien été traité."
            message.message = "Votre ticket à bien été traité. Pour plus de précision, nous vous invitons a consulté vos mails. N'hésitez pas à créer un nouveau tickets si vous rencontré d'autres difficulté "
            message.save()
    return HttpResponse("true")

def leads_changement_etats(request):
    if request.method == 'POST':
        x = request.body.decode('utf-8').split(',')
        etat=x[0]
        id_demande=x[1]
        demande = mysite.models.Demande.objects.get(id=id_demande)
        demande.etat = etat
        demande.save()
    return HttpResponse("true")


def ajax_get_demande_super_admin(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_demande = request.body.decode('utf-8')
        demande=mysite.models.Demande.objects.get(id=id_demande)
        docs=mysite.models.GestionDoc.objects.filter(id_demande=id_demande)
        C=model_to_dict(demande)
        for doc in docs:
            C["type"+str(doc.id)]=doc.type
            C["adresse_doc"+str(doc.id)]=str(doc.adresse_doc)
            C["size"+str(doc.id)]=doc.size
            C["date"+str(doc.id)]=doc.upload_date
        return  JsonResponse(C)
    else :
        return redirect("../../index")

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """

    sUrl = settings.STATIC_URL        # Typically /static/
    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL         # Typically /media/
    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        
    return path

@login_required(login_url='../../register/login')
def download_doc(request, name):
    if request.method == 'POST':
        demande = mysite.models.Demande.objects.get(id=request.POST['choice'])
        
        file_name = '{}-{}.pdf'.format(name, request.POST['choice'])
        url = '../../../media/{}'.format(file_name)

        if not default_storage.exists(file_name):
            html = render_to_string('admin/pdfs/{}.html'.format(name), {'demande': demande})

            result = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=result, link_callback=link_callback)

            if pisa_status.err:
                return HttpResponse('Erreur dans la création du document')
            else:
                fs = FileSystemStorage()
                fs.save(file_name, result)

                if name.startswith('facture'):
                    facture = mysite.models.Facture()
                    
                    facture.user = request.user
                    facture.adresse_doc = file_name
                    facture.demande = demande
                    facture.type = name

                    facture.save()

                else:
                    contrat = mysite.models.Contrat()
                    contrat.user = request.user
                    contrat.adresse_doc = file_name
                    contrat.demande = demande
                    contrat.type = name

                    contrat.save()

        return redirect(url)
        
    else:
        return redirect('../../demandes/')

def create_jwt_grant_token():
    iat = time.time()
    exp = iat + 10800

    with open(os.path.join(settings.BASE_DIR, 'admin2/private_key.pem'), "rb") as key_file:
        private_key = crypto_serialization.load_pem_private_key(key_file.read(), password=None)

    key = private_key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
    token = jws.sign({
        "iss": settings.CLIENT_AUTH_ID,
        "sub": settings.CLIENT_USER_ID,
        "iat": iat, # session start_time
        "exp": exp, # session end_time
        "aud": "account-d.docusign.com",
        "scope": "signature impersonation"
    }, key, algorithm='RS256')

    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'

    r = requests.post(base_url, data=post_data)
    return r.json()

def docusign_signature(request):
    if request.method == 'POST':
        token = create_jwt_grant_token()

        # get contrat

        request.session['contrat_id'] = request.POST['choice']
        file_name = mysite.models.Contrat.objects.get(id=request.POST['choice']).adresse_doc.name

        # document that are to be signed

        with open(os.path.join(settings.MEDIA_ROOT, file_name), 'rb') as file: # Your docusign file path
            content_bytes = file.read()

        base64_file_content = base64.b64encode(content_bytes).decode('ascii')

        # Create the document model
        document = Document( # create the DocuSign document object
            document_base64 = base64_file_content,
            name = 'Example document', # can be different from actual file name
            file_extension = 'pdf', # many different document types are accepted
            document_id = '1' # a label used to reference the doc
        )

        if file_name.startswith('certificat-eligibilite'):
            page = '1'

            sign_here_x = '402'
            sign_here_y = '626'

            sign_date_x = '388'
            sign_date_y = '670'

            text_name_x = '438'
            text_name_y = '670'

            text_email_x = '388'
            text_email_y = '680'

        elif file_name.startswith('bulletin-adhesion'):
            page = '3'

            sign_here_x = '412'
            sign_here_y = '125'

            sign_date_x = '74'
            sign_date_y = '127'

            text_name_x = '423'
            text_name_y = '168'

            text_email_x = '398'
            text_email_y = '178'

        else:
            page = '5'

            if request.user.type == '0':
                sign_here_x = '442'
                sign_date_x = '428'
                text_name_x = '478'
                text_email_x = '428'
            
            else:
                sign_here_x = '80'
                sign_date_x = '66'
                text_name_x = '116'
                text_email_x = '66'
                
            sign_here_y = '626'
            sign_date_y = '670'
            text_name_y = '670'
            text_email_y = '680'

        sign_here = SignHere(
            document_id = '1',
            page_number = page,
            recipient_id = '1',
            tab_label = 'SignHereTab',
            x_position = sign_here_x,
            y_position = sign_here_y
        )

        today = date.today()
        curr_date = today.strftime("%d/%m/%Y")
        sign_date = DateSigned(
            document_id = '1',
            page_number = page,
            recipient_id = '1',
            tab_label = 'Date',
            font = 'helvetica',
            bold = 'true',
            value = curr_date,
            tab_id = 'date',
            font_size = 'size8',
            x_position = sign_date_x,
            y_position = sign_date_y
        )

        text_name = Text(
            document_id = '1',
            page_number = page,
            recipient_id = '1',
            tab_label = 'Name',
            font = 'helvetica',
            bold = 'true',
            value = f'{request.user.first_name} {request.user.last_name}',
            tab_id = 'name',
            font_size = 'size8',
            x_position = text_name_x,
            y_position = text_name_y
        )

        text_email = Text(
            document_id = '1',
            page_number = page,
            recipient_id = '1',
            tab_label = 'Email',
            font = 'helvetica',
            bold = 'true',
            value = request.user.email,
            tab_id = 'email',
            font_size = 'size8',
            x_position = text_email_x,
            y_position = text_email_y
        )

        text_tabs=[text_name, text_email, sign_date]

        if file_name == 'bulletin-adhesion':
            text_place = Text(
                document_id = '1',
                page_number = '3',
                recipient_id = '1',
                tab_label = 'Email',
                font = 'helvetica',
                bold = 'true',
                value = request.user.email,
                tab_id = 'email',
                font_size = 'size8',
                x_position = '81',
                y_position = '101',
            )
            
            text_tabs.append(text_place)

        signer_tab = Tabs(sign_here_tabs=[sign_here], text_tabs = text_tabs)
        signer = Signer(
            email = request.user.email,
            name = f'{request.user.first_name} {request.user.last_name}',
            recipient_id = '1',
            routing_order = '1',
            client_user_id = settings.CLIENT_USER_ID,
            tabs = signer_tab
        )

        # Next, create the top level envelope_definition and populate it.

        envelope_definition = EnvelopeDefinition(
            email_subject = "Please sign this document sent from the Python SDK",
            documents = [document],
            # The Recipients object wants arrays for each recipient type
            recipients = Recipients(signers=[signer]),
            status = "sent" # requests that the envelope be created and sent.
        )

        # STEP-2 create/send envelope

        api_client = ApiClient()
        api_client.host = "https://demo.docusign.net/restapi"
        api_client.set_default_header('Authorization', 'Bearer ' + token['access_token'])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id = settings.ACCOUNT_ID, envelope_definition = envelope_definition)

        # Create the Recipient View request object
        recipient_view_request = RecipientViewRequest(
            authentication_method = 'email',
            client_user_id = settings.CLIENT_USER_ID,
            recipient_id = '1',
            return_url = 'http://127.0.0.1:8000/admin/get-envelope-status/{}/'.format(results.envelope_id), # Your redirected URL
            user_name = f'{request.user.first_name} {request.user.last_name}',
            email = request.user.email
        )

        # Obtain the recipient view url for the signing ceremony
        # Exceptions will be caught by the calling function

        results = envelope_api.create_recipient_view(settings.ACCOUNT_ID, results.envelope_id, recipient_view_request = recipient_view_request)
        return redirect(results.url)

    else:
        return redirect('../contrats-certificats/')

def get_envelope_status(request, envelope_id):
    contrat = mysite.models.Contrat.objects.get(id=request.session['contrat_id'])

    token = create_jwt_grant_token()

    api_client = ApiClient()
    api_client.host = "https://demo.docusign.net/restapi"
    api_client.set_default_header('Authorization', 'Bearer ' + token['access_token'])

    envelope_api = EnvelopesApi(api_client)

    temp_file = envelope_api.get_document(settings.ACCOUNT_ID, '1', envelope_id)
    os.replace(temp_file, os.path.join(settings.MEDIA_ROOT, contrat.adresse_doc.name))
    
    if request.user.type == '0':
        contrat.user_has_signed = True
    else:
        contrat.admin_has_signed = True

    contrat.save()

    return redirect('../../contrats-certificats')

def send_payment_link(request):
    if request.method == 'POST':
        demande = mysite.models.Demande.objects.get(id=request.POST['choice'])

        with mail.get_connection() as connection:
            html = render_to_string('admin/emails/paiement.html', {'demande': demande})

            email = mail.EmailMultiAlternatives(
                "Mail Insor", html, '', ['miel.licorne@gmail.com'],
                connection = connection
            )

            email.attach_alternative(html, 'text/html')

            email.send()
        
        return HttpResponse()
    else:
        return redirect('../test')

def consulting_docs(request):
    if request.method == 'POST':
        return redirect('../../../media/{}'.format(request.POST['file_name']))
    else:
        return HttpResponse()

def ajax_get_message(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        C = {}
        user=mysite.models.User.objects.get(id=request.user.id)
        messages=mysite.models.Message.objects.filter(getter=user,etat=0).order_by("-date_message")
        for message in messages:
            C[str(message.id)]=model_to_dict(message)
            seconde=(datetime.now(timezone.utc) - message.date_message).seconds
            heure=int(seconde/3600)
            minutes = int((seconde - (heure*3600))/60)
            C[str(message.id)]["date_message"]= str(heure) + ' h ' + str(minutes)
        return  JsonResponse(C)
    else :
        return redirect("../../index")

# Here for administrators

@login_required(login_url='../../register/login/')
def dashboard_for_admin(request):
    return render(request, 'admin/dashboard-admin-bis.html')

# endHere

def view(request, page):
    return mysite.views.default_view(request, 'admin/' + page)