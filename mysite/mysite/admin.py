from django.contrib import admin

from .models import Contact
from .models import GestionDoc
from .models import Demande
from .models import User
from .models import Entreprise
from .models import Message
from .models import Ticket
from .models import Contrat
from .models import Facture
from .models import AutreDoc
from .models import Connexion

admin.site.register(Contact)
admin.site.register(GestionDoc)
admin.site.register(Demande)
admin.site.register(User)
admin.site.register(Entreprise)
admin.site.register(Message)
admin.site.register(Ticket)
admin.site.register(Contrat)
admin.site.register(Facture)
admin.site.register(AutreDoc)
admin.site.register(Connexion)