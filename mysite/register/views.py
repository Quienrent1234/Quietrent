"""Views for register."""
from calendar import month
import re
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core import mail
from datetime import datetime


from django.template.loader import render_to_string
from django.utils.html import strip_tags

from urllib.error import HTTPError

from . import sql
import requests

import uuid
from random import choice

from abc import ABC

import copy
import json
import random
import string

import logging

import sys
import os

up1 = os.path.abspath('.')
sys.path.insert(0, up1)

import mysite
from api_insee import ApiInsee

api = ApiInsee(
    key = "5cBm0pDfweOndd8MoqJVQJqcvVsa",
    secret = "PUnA6IDn7zRbnavSxDROqfnZbRsa"
)

class Originator(ABC):
    def __init__(self, sqlFormClass, template: str, url_name: str) -> None:
        self.__sqlFormClass = sqlFormClass
        self.__template = template
        self.__url_name = url_name

        self.__history = {}

    def set_history(self, token_id: str, form_data: dict) -> None:
        self.__history[token_id] = form_data

    def clear_data(self, token_id: str) -> None:
        if token_id in self.__history :
            self.__history.pop(token_id)

    def get_sqlFormClass(self):
        return self.__sqlFormClass
    
    def get_url_name(self) -> str:
        return self.__url_name

    def render(self, request: HttpRequest, data={}) -> HttpResponse:
        if request.session['token'] in self.__history:
            logging.error('etre')
            content = self.__history[request.session['token']]
            logging.error(content)
            content.update(data)
            logging.error(content)
        else:
            logging.error('ou ne pas etre')
            content = data
        return render(request, self.__template, content)

class Memento:
    def __init__(self, originator: Originator, data: dict) -> None:
        self.__originator = originator
        self.__data = data

    def get_originator(self) -> Originator:
        return self.__originator

    def get_data(self) -> dict:
        return self.__data

class ConcreteCaretaker():
    def __init__(self, first: Originator) -> None:
        self.__originators = {}
        self.__data = {}
        self.__first = first

    def __create_token(self) -> str:
        token_id = uuid.uuid4().hex
        while token_id in self.__data:
            token_id = uuid.uuid4().hex
        
        return token_id

    def __create_originator(self, token_id) -> None:
        self.__originators[token_id] = self.__first
        self.__data[token_id] = []

    def get_memento(self, token_id: str, i: int) -> Memento:
        return self.__data[token_id][i]
    
    def do(self, request: HttpRequest) -> HttpResponse:
        try:
            originator = self.__originators[request.session['token']]
        except KeyError:
            request.session['token'] = self.__create_token()
            self.__create_originator(request.session['token'])
            originator = self.__first
        finally:
            if request.method == 'POST':
                form = originator.get_sqlFormClass()(request.POST)
                if form.is_valid():
                    try:
                        self.__data[request.session['token']].append(originator.save(form.cleaned_data))
                        originator.clear_data(request.session['token'])
                    except AttributeError:
                        try:
                            originator.save_data(request.session['token'], form.cleaned_data)
                        except ValueError:
                            redirect('../{}'.format(originator.get_url_name()))
                        else:
                            return redirect('../../index/')
                    else:
                        nxt = originator.get_next()
                        self.__originators[request.session['token']] = nxt
                        return redirect('../{}'.format(nxt.get_url_name()))
            
            current_path = originator.get_url_name()
            if request.get_full_path() == '/register/{}'.format(current_path):
                return originator.render(request)
            else:
                return redirect('../{}'.format(current_path))

    def undo(self, request: HttpRequest) -> HttpResponse:
        try:
            if self.__data[request.session['token']] == []:
                token_id = request.session.pop('token')
                self.__data.pop(token_id)
                
                self.__originators.pop(token_id)
                return redirect('../souscription/')
        except KeyError:
            return redirect('../souscription/')
        else:
            memento = self.__data[request.session['token']].pop()
            logging.error(memento)
            logging.error(self.__data)
            logging.error(memento.get_data())
            originator = memento.get_originator()
            self.__originators[request.session['token']] = originator

            originator.set_history(request.session['token'], memento.get_data())

            return redirect('../{}'.format(originator.get_url_name()))

    def pop(self, token_id: str) -> list:
        self.__originators.pop(token_id)
        return self.__data.pop(token_id)

class FormValidation(Originator):
    def __init__(self, nxt: Originator, sqlFormClass, template: str, path: str) -> None:
        super().__init__(sqlFormClass, template, path)

        self.__next = nxt

    def get_next(self):
        return self.__next

    def save(self, form_data: dict) -> Memento:
        return Memento(self, form_data)

class FormBail(FormValidation):
    def __init__(self, nxt: Originator, sqlFormClass, template: str, path: str) -> None:
        super().__init__(nxt, sqlFormClass, template, path)

    def render(self, request: HttpRequest, data={}) -> HttpResponse:
        try :
            logging.error(eligibility_caretaker.get_memento(request.session['token'], 0).get_data())
            siret = eligibility_caretaker.get_memento(request.session['token'], 0).get_data()['inputSIREN']
        except IndexError :
            siret=""
        return super().render(request, data=get_adresse_insee(siret))
        
class EligibilityFormValidation(FormValidation):
    def __init__(self, nxt: Originator, sqlFormClass, template: str, path: str) -> None:
        super().__init__(nxt, sqlFormClass, template, path)

    def __are_you_eligible(self, data):
        # if data['incident'] == "yes" or data['difficulte'] == "yes" or data['preavis'] == "yes" or (data['echeance'] == "yes" and data['renouveler'] == "no"):
        #     return 0
        
        # elif data['cautionPerso'] == "no" or data['QuietSolution'] == "no":
        #     return 0
        
        # elif data['plusDeuxAns'] == "no":
        #     return 1
        
        # try:
        #     benefice = float(data['beneficePerte2021'].replace(',', '.')) + float(data['beneficePerte2020'].replace(',', '.'))
        #     if benefice < 0 or float(data['loyer'].replace(',', '.')) > 150000:
        #         return 1
        # except Exception:
        #     return 1
        
        return 2

    def save(self, form_data: dict) -> Memento:
        form_data.update({'eligibilite': self.__are_you_eligible(form_data)})
        logging.error(form_data)
        return super().save(form_data)

class Complete(FormValidation):
    def __init__(self, nxt: Originator, sqlFormClass, template: str, path: str) -> None:
        super().__init__(nxt, sqlFormClass, template, path)

    def render(self, request: HttpRequest) -> HttpResponse:
        eligibility = eligibility_caretaker.get_memento(request.session['token'], -1).get_data()['eligibilite']
        logging.error("eligibility state")
        logging.error(eligibility_caretaker.get_memento(request.session['token'], -1).get_data()['eligibilite'])
        return super().render(request, {'state': eligibility})

class Register(FormValidation):
    def __init__(self, nxt: Originator, sqlFormClass, template: str, path: str) -> None:
        super().__init__(nxt, sqlFormClass, template, path)
    
    def save(self, form_data: dict) -> Memento:
        code = ''.join([choice(string.digits) for i in range(5)])

        msg_html = render_to_string('register/email-templates-basic.html', {'code': code})
        plain_message = strip_tags(msg_html)

        # from django.core.mail import EmailMultiAlternatives

        # subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        msg = mail.EmailMultiAlternatives(
            "Code de validation", plain_message, '', [form_data['inputMail']],
            connection = mail.get_connection()
        )
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        
        form_data.update({'code': code})
        return super().save(form_data)

class EmailVerification(Originator):
    def __init__(self, sqlFormClass, template: str, path: str) -> None:
        super().__init__(sqlFormClass, template, path)

    def save_data(self, token_id, form_data) -> None:
        logging.error(''.join(form_data.values()))
        logging.error(eligibility_caretaker.get_memento(token_id, -1).get_data()['code'])
        if ''.join(form_data.values()) == eligibility_caretaker.get_memento(token_id, -1).get_data()['code']:
            all_data = {}
            for memento in eligibility_caretaker.pop(token_id):
                all_data.update(memento.get_data())
            
            user = mysite.models.User()

            user.email = all_data['inputMail']
            user.first_name = all_data['inputFirstName']
            user.last_name = all_data['inputName']
            user.adresse = all_data['inputAddress']
            user.code_postal = all_data['inputCode']
            user.siteweb = all_data['inputWebSite']
            user.siren = all_data['inputSIREN']
            user.mobile = all_data['inputPhone']
            user.physical_moral = all_data['physical_moral']
            user.gender = all_data['gender']
            user.password = make_password(all_data['inputPass'])

            user.save()

            connectionCreate = mysite.models.Connexion()
            connectionCreate.user = user
            connectionCreate.save()


            demande = mysite.models.Demande()

            demande.user = user
            demande.physical_moral = all_data['physical_moral']
            demande.juridical_form = all_data['juridical_form']
            demande.social_reason = all_data['social_reason']
            demande.inputSIREN = all_data['inputSIREN']
            demande.gender = all_data['gender']
            demande.inputName = all_data['inputName']
            demande.inputFirstName = all_data['inputFirstName']
            demande.inputMail = all_data['inputMail']
            demande.inputPhone = all_data['inputPhone']
            demande.inputActivity = all_data['inputActivity']
            if 'inputWebSite' in all_data: demande.inputWebSite = all_data['inputWebSite']
            demande.inputAddress = all_data['inputAddress']
            demande.inputCode = all_data['inputCode']
            demande.inputCity = all_data['inputCity']
            if all_data['mois'] != None: demande.mois = all_data['mois']
            if all_data['annee'] != None: demande.annee = all_data['annee']
            demande.loyer = all_data['loyer']
            demande.garantie = all_data['garantie']
            demande.garantieMois = all_data['garantieMois']
            demande.caution = all_data['caution']
            demande.cautionMois = all_data['cautionMois']
            demande.substitution = all_data['substitution']
            demande.incident = all_data['incident']
            demande.difficulte = all_data['difficulte']
            demande.preavis = all_data['preavis']
            demande.echeance = all_data['echeance']
            demande.renouveler = all_data['renouveler']
            demande.plusDeuxAns = all_data['plusDeuxAns']
            demande.ca2021 = all_data['ca2021']
            demande.beneficePerte2021 = all_data['beneficePerte2021']
            demande.ca2020 = all_data['ca2020']
            demande.beneficePerte2020 = all_data['beneficePerte2020']
            demande.conges = all_data['conges']
            demande.CC = all_data['CC']
            demande.cautionPerso = all_data['cautionPerso']
            demande.QuietSolution = all_data['QuietSolution']
            demande.etat = all_data['eligibilite']
            
            demande.save()

            entreprise = mysite.models.Entreprise()

            entreprise.user = user
            entreprise.id_demande = demande.id
            entreprise.social_reason = all_data['social_reason']
            entreprise.adresse = all_data['inputAddress']
            entreprise.ville = all_data['inputCity']
            entreprise.code_postal = all_data['inputCode']
            if 'inputWebSite' in all_data: entreprise.siteweb = all_data['inputWebSite']
            entreprise.siren = all_data['inputSIREN']  
            entreprise.juridical_form = all_data['juridical_form']
            entreprise.inputActivity = all_data['inputActivity']

            entreprise.save()

            if all_data['inputWebSite'] == '':
                website = "je ne dispose pas de site web"
            else:
                website = all_data['inputWebSite']

            if all_data['physical_moral'] == 'phisical':
                juridic_capacity = 'physique'
            else:
                juridic_capacity = 'morale'

            if all_data['juridical_form'] == 'EI':
                juridical_form = "entreprise individuelle"
            elif all_data['juridical_form'] == 'EIRL':
                juridical_form = "entreprise individuelle à responsabilité limitée"
            elif all_data['juridical_form'] == 'EURL':
                juridical_form = "entreprise unipersonnelle à responsabilité limitée"
            elif all_data['juridical_form'] == 'SC':
                juridical_form = "société de capitaux"
            else:
                juridical_form = "société en nom collectif"

            if all_data['gender'] == 'male':
                gender = "homme"
            else:
                gender = 'femme'

            if all_data['mois'] == '1':
                month = 'janvier'
            elif all_data['mois'] == '2':
                month = 'février'
            elif all_data['mois'] == '3':
                month = 'mars'
            elif all_data['mois'] == '4':
                month = 'avril'
            elif all_data['mois'] == '5':
                month = 'mai'
            elif all_data['mois'] == '6':
                month = 'juin'
            elif all_data['mois'] == '7':
                month = 'juillet'
            elif all_data['mois'] == '8':
                month = 'août'
            elif all_data['mois'] == '9':
                month = 'septembre'
            elif all_data['mois'] == '10':
                month = 'octobre'
            elif all_data['mois'] == '11':
                month = 'novembre'
            else:
                month = 'décembre'

            if all_data['substitution'] == '0':
                substitution = 'partenaire'
            elif all_data['substitution'] == '1':
                substitution = 'courtier'
            else:
                substitution = 'partenaire & courtier'

            if all_data['incident'] == 'yes':
                incident = 'oui'
            else:
                incident = 'non'

            if all_data['difficulte'] == 'yes':
                difficulte = 'oui'
            else:
                difficulte = 'non'

            if all_data['preavis'] == 'yes':
                preavis = 'oui'
            else:
                preavis = 'non'

            if all_data['echeance'] == 'yes':
                echeance = 'oui'
            else:
                echeance = 'non'

            data = {
                "Nom": all_data['inputName'],
                "Prénom": all_data['inputFirstName'],
                "Adresse mail": all_data['inputMail'],
                "Raison sociale": all_data['social_reason'],
                "Adresse": all_data['inputAddress'],
                "Code postal": all_data['inputCode'],
                "Site web": website,
                "Siren": all_data['inputSIREN'],
                "Numéro de téléphone": all_data['inputPhone'],
                "Capacité juridique": juridic_capacity,
                "Forme juridique": juridical_form,
                "Sexe": gender,
                "Secteur d'activité": all_data['inputActivity'],
                "Ville": all_data['inputCity'],
                "Date d'effet du bail": 'en ' + month + ' ' + str(all_data['annee']),
                "loyer": all_data['loyer'] + ' ' + '€',
                "Montant de la garantie": all_data['garantie'] + ' ' + '€',
                "Nombre de mois de loyer correspondnant au montant de la garantie": all_data['garantieMois'],
                "Montant de la caution": all_data['caution'] + ' ' + '€',
                "Nombre de mois de loyer correspondnat au montant de la caution": all_data['cautionMois'],
                "Substitution à mettre en place": substitution,
                "Y'a-t-il eu un incident de paiement ou litige avec le bailleur ?": incident,
                "Coresponds-je au critère de société en difficulté (fonds propres négatifs) ?": difficulte,
                "Ai-je reçu/donné un préavis de congé portant sur le bail visé par la présente étude d'éligibilité ?": preavis,
                "Ai-je une échéance triennale au cours des 12 prochains mois ?": echeance
            }

            if all_data['renouveler'] == 'yes':
                data['Renouvelement de contrat de bail'] = 'oui'
            elif all_data['renouveler'] == 'no':
                data['Renouvelement de contrat de bail'] = 'non'

            if all_data['plusDeuxAns'] == 'yes':
                data["Votre entreprise à t'elle plus de deux ans ?"] = 'oui'
            else:
                data["Votre entreprise à t'elle plus de deux ans ?"] = 'non'

            if all_data['ca2021'] != '':
                data["Chiffre d'affaire de mon entreprise sur l'année 2021"] = all_data['ca2021'] + ' ' + '€'
            
            if all_data['beneficePerte2021'] != '':
                if int(all_data['beneficePerte2021']) >= 0:
                    data["Bénéfice sur l'année 2021"] = all_data['beneficePerte2021'] + ' ' + '€'
                elif int(all_data['beneficePerte2021']) < 0:
                    data["Perte sur l'année 2021"] = all_data['beneficePerte2021'] + ' ' + '€'

            if all_data['ca2020'] != '':
                data["Chiffre d'affaire de mon entreprise sur l'année 2021"] = all_data['ca2021'] + ' ' + '€'
            
            if all_data['beneficePerte2020'] != '':
                if int(all_data['beneficePerte2020']) >= 0:
                    data["Bénéfice sur l'année 2020"] = all_data['beneficePerte2021'] + ' ' + '€'
                elif int(all_data['beneficePerte2020']) < 0:
                    data["Perte sur l'année 2020"] = all_data['beneficePerte2021'] + ' ' + '€'

            if all_data['conges'] == 'yes':
                data['Ai-je des congés sur mes locaux actuellement loué ?'] = 'oui'
            elif all_data['conges'] == 'no':
                data['Ai-je des congés sur mes locaux actuellement loué ?'] = 'non'
            
            if all_data['CC'] != '':
                data['Mon loyer avec charges comprises est de'] = all_data['CC'] + ' ' + '€'

            if all_data['cautionPerso'] == 'yes':
                data["Ai-je la possibilité d'emettre une caution personelle ou d'une entreprise de plus de 2 ans solvable ?"] = 'oui'
            elif all_data['cautionPerso'] == 'no':
                data["Ai-je la possibilité d'emettre une caution personelle ou d'une entreprise de plus de 2 ans solvable ?"] = 'non'
                
            if all_data['QuietSolution'] == 'yes':
                data['Mon bailleur a-t-il déjà accepté la solution QuietRent ?'] = 'oui'
            elif all_data['QuietSolution'] == 'no':
                data['Mon bailleur a-t-il déjà accepté la solution QuietRent ?'] = 'non'

            mysite.views.send_email("demande d'éligibilité", data)

        else:
            raise ValueError()
    
    def render(self, request: HttpRequest) -> HttpResponse:
        email = eligibility_caretaker.get_memento(request.session['token'], -1).get_data()
        return super().render(request, {'email': email})

emailVerification = EmailVerification(sql.Code, './register/email-verification.html', 'email-verification/')
register = Register(emailVerification, sql.SqlRegister, './register/register.html', 'register/')
complete = Complete(register, sql.SqlFormComplete, './register/complete.html', 'complete/')
form_eligibilite = EligibilityFormValidation(complete, sql.SqlFormEligibilite, './register/eligibilite.html', 'eligibilite/')
form_garantie = FormValidation(form_eligibilite, sql.SqlFormGarantie, './register/garantie.html', 'garantie/')
form_bail = FormBail(form_garantie, sql.SqlFormBail, './register/questionnaire-bail.html', 'questionnaire-bail/')
form_loc = FormValidation(form_bail, sql.SqlFormLoc, './register/questionnaire-loc.html', 'questionnaire-loc/')
eligibility_caretaker = ConcreteCaretaker(form_loc)

def remove(request):
    try:
        eligibility_caretaker.pop(request.session.pop('token'))
    except KeyError:
        pass
    finally:
        return redirect('../../index/')

def status_choice(request):
    context = {}
    return render(request, './register/status-choice.html', context)

def switch_login(request):
    month= datetime.now().month
    logging.error(month)
    user = mysite.models.User.objects.get(id=request.user.id)
    connection=mysite.models.Connexion.objects.get(user=user)
    if (month==1):
        connection.janv+=1
    elif (month==2):
        connection.fevr+=1
    elif (month==3):
        connection.mars+=1
    elif (month==4):
        connection.avril+=1
    elif (month==5):
        connection.mai+=1
    elif (month==6):
        connection.juin+=1
    elif (month==7):
        connection.juill+=1
    elif (month==8):
        connection.aout+=1
    elif (month==9):
        connection.sept+=1
    elif (month==10):
        connection.oct+=1
    elif (month==11):
        connection.nov+=1
    else:
        connection.dec+=1
    connection.save()

def login_client(request):
    """ Cette vue permet de se connecter en tant que client"""
    context = {}
    context['status'] = "client"
    if request.method == 'POST':
        email = request.POST.get('inputMail')
        password = request.POST.get('inputPass')

        try:
            user = mysite.models.User.objects.get(email=email)
        except:
            context['error'] = "Utilisateur introuvable..."

        # user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.type == '0':
                message=mysite.models.Message.objects.filter(getter=user)
                request.session['message'] = len(message)
                login(request, user)
                switch_login(request)
                request.session['id'] = user.id
                return redirect('../../admin/dashboard/')
            else:
                context['error'] = "E-mail ou mot de passe incorrect...."
        else:
            context['error'] = "E-mail ou mot de passe incorrect..."

    return render(request, './register/login.html', context)

def login_partner(request):
    """ Cette vue permet de se connecter en tant que partner"""
    context = {}
    context['status'] = "partner"
    if request.method == 'POST':
        email = request.POST.get('inputMail')
        password = request.POST.get('inputPass')

        try:
            user = mysite.models.User.objects.get(email=email)
        except:
            context['error'] = "Utilisateur introuvable..."

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.type == '0':
                message=mysite.models.Message.objects.filter(getter=user)
                request.session['message'] = len(message)
                login(request, user)
                switch_login(request)
                request.session['id'] = user.id
                return redirect('../../admin/dashboard/')
            else:
                context['error'] = "E-mail ou mot de passe incorrect..."
        else:
            context['error'] = "E-mail ou mot de passe incorrect..."

    return render(request, './register/login.html', context)

def login_admin(request):
    """ Permet de se connecter dans le module super admin (accessible a partir de la page /admin/login_admin) avec un user de type 1"""
    context = {}
    context['status'] = "admin"
    if request.method == 'POST':
        email = request.POST.get('inputMail')
        password = request.POST.get('inputPass')

        try:
            user = mysite.models.User.objects.get(email=email)
        except:
            context["error"]= 'Utilisateur introuvable...'
        else:
            # user = authenticate(request, email=email, password=password)

            if user is not None and user.type == '1' :
                message=mysite.models.Message.objects.filter(getter=user,etat=0)
                request.session['message'] = len(message)
                login(request, user)
                switch_login(request)
                request.session['id'] = user.id
                return redirect('../../admin/super-profil/') #render la template "super-profil"
            else:
                context["error"] = 'E-mail ou mot de passe incorrect... Ici c''est pour les admin'
    
    return render(request, './register/login.html', context)

def login_admin_bis(request):
    """ Permet de se connecter dans le module super admin (accessible a partir de la page /admin/login_admin) avec un user de type 1"""
    context = {}
    context['status'] = "admin"
    if request.method == 'POST':
        email = request.POST.get('inputMail')
        password = request.POST.get('inputPass')

        try:
            user = mysite.models.User.objects.get(email=email)
        except:
            context["error"] = 'Utilisateur introuvable...'

        # user = authenticate(request, email=email, password=password)
        
        if user is not None and user.type == '2' :
            message=mysite.models.Message.objects.filter(getter=user,etat=0)
            request.session['message'] = len(message)
            login(request, user)
            switch_login(request)
            request.session['id'] = user.id
            return redirect('../../admin/admin-profil/') #render la template "super-profil"
        else:
            context["error"]= 'E-mail ou mot de passe incorrect... Ici ne peuvent se connecter que les administrateurs.'
    return render(request, './register/login.html', context)

def logout_user(request):
    """ Cette vue permet de se déconnecter"""
    logout(request)
    return redirect('../../index')

def ajax_view_verif_mail(request):
    body_unicode = request.body.decode('utf-8')
    try:
        mysite.models.User.objects.get(email=body_unicode)
    except:
        return HttpResponse('true')
    else:
        return HttpResponse('false')

def getOrElse(x, y):
  return x if x is not None else y

def get_adresse_insee(siret):
    info={}
    if siret:
        logging.error(siret)
        try:
            data = api.siret(siret).get()
        except HTTPError : 
            info["inputAddress"]= ""
            info["inputCode"] = ""
            info["inputCity"] = ""
        else:
            try :
                info["inputAddress"]= getOrElse(data["etablissements"][0]["adresseEtablissement"]["numeroVoieEtablissement"],'') +" "+ getOrElse(data["etablissements"][0]["adresseEtablissement"]["typeVoieEtablissement"],'') +" "+ getOrElse(data["etablissement"][0]["adresseEtablissement"]["libelleVoieEtablissement"],'')
                info["inputCode"] = getOrElse(data["etablissements"][0]["adresseEtablissement"]["codePostalEtablissement"],'')
                info["inputCity"] = getOrElse(data["etablissements"][0]["adresseEtablissement"]["libelleCommuneEtablissement"],'')
            except KeyError:
                info["inputAddress"]= getOrElse(data["etablissement"]["adresseEtablissement"]["numeroVoieEtablissement"],'')  +" "+ getOrElse(data["etablissement"]["adresseEtablissement"]["typeVoieEtablissement"],'')  +" "+ getOrElse(data["etablissement"]["adresseEtablissement"]["libelleVoieEtablissement"],'')
                info["inputCode"] = getOrElse(data["etablissement"]["adresseEtablissement"]["codePostalEtablissement"],'')
                info["inputCity"] = getOrElse(data["etablissement"]["adresseEtablissement"]["libelleCommuneEtablissement"],'')
        logging.error(info)
    return info


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
        data = api.siret(siret).get()
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


def view(request, page):
    """ Default view for register
    :param QueryDict request : server request
    :param str page : html name of the page we want to access
    :return redirect to default_view in my site with path to te template (register)
    """
    return mysite.views.default_view(request, 'register/' + page)

