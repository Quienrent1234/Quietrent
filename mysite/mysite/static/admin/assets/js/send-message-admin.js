$(document).ready(function() {
    var select = document.querySelector('#alertType')
    select.addEventListener('change',function(){
        onchangeSelect($(this).children("option:selected").val())
    });
})

function onchangeSelect (type){
    switch (type) {
        case "doc":
            titre="Documents manquant"
            text=`Votre demande est incomplete. Nous avons besoin de documents supplementaires.
Nous vous rappellons que les documents suivant sont obligatoires : Pièce d'identité, KBis, 2 derniers Bilans, Projet de Bail ou loi, Statut de société.
Certaines demandes de garanties neccessites des documents supplémentaires.
Nous vous remercions de votre confiance.`
            break
        case "ajout":
            titre="Ajout de documents"
            text="L'un de nos administrateur a ajouter des documents a votre demande"
            break
        case "modif":
            titre="Modification des informations"
            text=`L'un de nos administrateur a modifié certaines de vos informations ou les informations de votre demande`
            break
        case "other": 
            titre="Message de QuietRent"
            break
    }
    $("#subject").val(titre)
    if (text){
        $("#message").val(text)
    }

}