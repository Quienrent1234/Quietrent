from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from datetime import datetime, timezone
from datetime import date as DateFromDatetime

#Creation de la class CustomUserManager
class CustomUserManager(BaseUserManager):
    def __create_user(self, email, password, first_name, last_name, type, mobile, date_joined, last_login, physical_moral, gender, **extra_fields):
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            type = type,
            mobile = mobile,
            date_joined = date_joined,
            last_login = last_login,
            physical_moral = physical_moral,
            gender = gender,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, type, mobile, date_joined, last_login, physical_moral, gender, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self.__create_user(email, password, first_name, last_name, type, mobile, date_joined, last_login, physical_moral, gender, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, type, mobile, date_joined, last_login, physical_moral, gender, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.__create_user(email, password, first_name, last_name, type, mobile, date_joined, last_login, physical_moral, gender, **extra_fields)

#Créeation d'une table user customisée
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=240, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')

    type = models.CharField(max_length=255, default='0')
    mobile = models.CharField(max_length=255, blank=True, default='')
    date_joined = models.DateTimeField(blank=True, default=datetime.now(timezone.utc))
    last_login = models.DateTimeField(blank=True, default=datetime.now(timezone.utc))
    physical_moral = models.CharField(max_length=255, blank=True, default="")
    gender = models.CharField(max_length=255, blank=True, default="")
    administrator = models.ForeignKey('User', on_delete=models.CASCADE, null=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'type', 'mobile', 'date_joined', 'last_login', 'physical_moral', 'gender', 'administrator']
    USERNAME_FIELD = 'email'

class GestionDoc(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    id_demande = models.IntegerField(blank=True)
    adresse_doc = models.FileField()
    type = models.CharField(max_length=100)
    upload_date = models.DateTimeField(blank=True, default=datetime.now(timezone.utc))
    size = models.CharField(max_length=255)
    deletable = models.BooleanField(default=True)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    msg_subject = models.TextField()
    message = models.TextField()
    etat = models.CharField(max_length=255, default="En cours")

    def __str__(self):
        return self.name

class Demande(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    physical_moral = models.CharField(max_length=255,blank=True,default="")
    juridical_form = models.CharField(max_length=255,blank=True,default="")
    social_reason = models.CharField(max_length=255,blank=True,default="")
    inputSIREN = models.CharField(max_length=255,blank=True,default="")
    gender = models.CharField(max_length=255,blank=True,default="")
    inputName = models.CharField(max_length=255,blank=True,default="")
    inputFirstName = models.CharField(max_length=255,blank=True,default="")
    inputMail = models.CharField(max_length=255,blank=True,default="")
    inputPhone = models.CharField(max_length=255,blank=True,default="")
    inputActivity = models.CharField(max_length=255,blank=True,default="")
    inputWebSite = models.CharField(max_length=255,blank=True,default="")
    inputAddress = models.CharField(max_length=255,blank=True,default="")
    inputCode = models.CharField(max_length=255,blank=True,default="")
    inputCity = models.CharField(max_length=255,blank=True,default="")
    mois = models.CharField(max_length=255,blank=True,default="")
    annee = models.CharField(max_length=255,blank=True,default="")
    loyer = models.CharField(max_length=255,blank=True,default="")
    garantie = models.CharField(max_length=255,blank=True,default="")
    garantieMois = models.CharField(max_length=255,blank=True,default="")
    caution = models.CharField(max_length=255,blank=True,default="")
    cautionMois = models.CharField(max_length=255,blank=True,default="")
    substitution = models.CharField(max_length=255, blank=True, default=-1)
    incident = models.CharField(max_length=255,blank=True,default="")
    difficulte = models.CharField(max_length=255,blank=True,default="")
    preavis = models.CharField(max_length=255,blank=True,default="")
    echeance = models.CharField(max_length=255,blank=True,default="")
    renouveler = models.CharField(max_length=255,blank=True,default="")
    plusDeuxAns = models.CharField(max_length=255,blank=True,default="")
    ca2021 = models.CharField(max_length=255,blank=True,default="")
    beneficePerte2021 = models.CharField(max_length=255,blank=True,default="")
    ca2020 = models.CharField(max_length=255,blank=True,default="")
    beneficePerte2020 = models.CharField(max_length=255,blank=True,default="")
    conges = models.CharField(max_length=255,blank=True,default="")
    CC = models.CharField(max_length=255,blank=True,default="")
    cautionPerso = models.CharField(max_length=255,blank=True,default="")
    QuietSolution = models.CharField(max_length=255,blank=True,default="")
    etat = models.IntegerField(blank=True, default=0)
    date_demande = models.DateTimeField(max_length=255,blank=True,default=datetime.now(timezone.utc))
    date_cloture = models.DateTimeField(max_length=255,blank=True,default=datetime.now())
    # 0 si rejeté, 1 si en cours de validation et 2 si validé

class Entreprise(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    id_demande = models.IntegerField()
    social_reason = models.CharField(max_length=255, blank=True, default="")
    adresse = models.CharField(max_length=255, blank=True, default='')
    ville = models.CharField(max_length=255, blank=True, default='')
    code_postal = models.CharField(max_length=255, blank=True, default='')
    representant = models.CharField(max_length=255, blank=True, default='')
    siteweb = models.CharField(max_length=255, blank=True, default='')
    siren = models.CharField(max_length=255, blank=True, default='')
    descriptif = models.TextField(max_length=3000, blank=True, default='')
    logo = models.CharField(max_length=255, blank=True, default='')
    rcs = models.CharField(max_length=255, blank=True, default='')
    juridical_form = models.CharField(max_length=255, blank=True, default="")
    inputActivity = models.CharField(max_length=255, blank=True, default="")

class Message(models.Model):
    setter = models.ForeignKey('User',on_delete=models.CASCADE,related_name='setter')
    getter = models.ForeignKey('User',on_delete=models.CASCADE,related_name='getter')
    demande = models.ForeignKey('Demande',on_delete=models.CASCADE,related_name='demande')
    type =  models.CharField(max_length=255, blank=True, default="")
    titre = models.CharField(max_length=255, blank=True, default="")
    message = models.TextField(blank=True, default='')
    etat = models.IntegerField(default=0)
    date_message = models.DateTimeField(max_length=255,blank=True,default=datetime.now(timezone.utc))

class Ticket(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    demande = models.ForeignKey('Demande',on_delete=models.CASCADE)
    service = models.CharField(max_length=255, blank=True)
    objet = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    contenu = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=datetime.now())
    date_cloture = models.DateTimeField(default=datetime.now())
    etat = models.CharField(max_length=255)

class Contrat(models.Model): # renommer la table
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    adresse_doc = models.FileField()
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=datetime.now())
    user_has_signed = models.BooleanField(default=False)
    admin_has_signed = models.BooleanField(default=False)

class Facture(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    adresse_doc = models.FileField()
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=datetime.now())
    payed = models.BooleanField(default=False)

class AutreDoc(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    demande = models.ForeignKey('Demande', on_delete=models.CASCADE)
    name = models.FileField()
    type = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=datetime.now())
    size = models.CharField(max_length=255)

class Connexion(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    janv = models.IntegerField( default=0)
    fevr = models.IntegerField( default=0)
    mars = models.IntegerField( default=0)
    avril = models.IntegerField( default=0)
    mai = models.IntegerField( default=0)
    juin = models.IntegerField( default=0)
    juill = models.IntegerField( default=0)
    aout = models.IntegerField( default=0)
    sept = models.IntegerField( default=0)
    oct = models.IntegerField(default=0)
    nov = models.IntegerField( default=0)
    dec = models.IntegerField( default=0)
    