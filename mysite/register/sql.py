from atexit import register
from django import forms

#form registration mail
class SqlRegister(forms.Form):
    inputMail = forms.EmailField(label='inputMail', max_length=100)
    inputPass = forms.CharField(label='inputMail', max_length=100)

#form registration code de verification
class Code(forms.Form):
    digit1 = forms.CharField(label='digit1', max_length=100)
    digit2 = forms.CharField(label='digit2', max_length=100)
    digit3 = forms.CharField(label='digit3', max_length=100)
    digit4 = forms.CharField(label='digit4', max_length=100)
    digit5 = forms.CharField(label='digit5', max_length=100)

JURIDICAL_CAPACITY = [('physical','physical'),('moral','moral')]
GENDER = [('male','male'),('female','female')]

class SqlFormLoc(forms.Form):
    physical_moral = forms.CharField(label='physical_moral')
    juridical_form = forms.CharField(label='juridical_form', max_length=100)
    social_reason = forms.CharField(label='social_reason', max_length=100)
    inputSIREN = forms.CharField(label='inputSIREN', max_length=100)
    gender=forms.CharField(label='gender')
    inputName = forms.CharField(label='inputName', max_length=100)
    inputFirstName = forms.CharField(label='inputFirstName', max_length=100)
    inputPhone = forms.CharField(label='inputPhone', max_length=100)
    inputActivity = forms.CharField(label='inputActivity', max_length=100)
    inputWebSite = forms.CharField(label='inputWebSite', max_length=100,required=False)

class SqlFormBail(forms.Form):
    inputAddress = forms.CharField(label='inputAddress', max_length=100)
    inputCode = forms.CharField(label="inputCode")
    inputCity = forms.CharField(label='inputCity', max_length=100)
    mois= forms.IntegerField(label="mois", required=False)
    annee = forms.IntegerField(label="annee", required=False)
    loyer = forms.CharField(label='loyer', max_length=100)
    garantie = forms.CharField(label='garantie', max_length=100)
    garantieMois = forms.IntegerField(label="garantieMois")
    caution = forms.CharField(label='caution', max_length=100)
    cautionMois = forms.IntegerField(label="cautionMois")

class SqlFormGarantie(forms.Form):
    substitution = forms.CharField(label="substitution", max_length=1)

class SqlFormComplete(forms.Form):
    pass

class SqlFormEligibilite(forms.Form):
    incident = forms.CharField(label="incident", max_length=50)
    difficulte = forms.CharField(label="difficulte", max_length=50)
    preavis = forms.CharField(label="preavis", max_length=50)
    echeance = forms.CharField(label="echeance", max_length=50)
    QuietSolution = forms.CharField(label="QuietSolution", max_length=50)
    plusDeuxAns = forms.CharField(label="plusDeuxAns", max_length=50)
    renouveler = forms.CharField(label="renouveler", max_length=50, required=False)
    ca2021 = forms.CharField(label="ca2021", max_length=50, required=False)
    beneficePerte2021 = forms.CharField(label="beneficePerte2021", max_length=50, required=False)
    ca2020 = forms.CharField(label="ca2020", max_length=50, required=False)
    beneficePerte2020 = forms.CharField(label="beneficePerte2020", max_length=50, required=False)
    conges = forms.CharField(label="conges", max_length=50, required=False)
    CC = forms.CharField(label="CC", max_length=50, required=False)
    cautionPerso = forms.CharField(label="cautionPerso", max_length=50, required=False)