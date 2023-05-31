$(document).ready(function() {
    $(function() {
        $.ajaxSetup({
            headers: {"X-CSRFToken": getCookie("csrftoken")}
        });
    });

    $(function() {
        if (getCookie("clicked_id")){
            document.getElementById(getCookie("clicked_id")).click(); 
            console.log("il a clické !!")
        }
    });
    
    $('#echeance-yes').click(function(e) {
        $('#renouveler-hidden').prop("hidden", false);
    });
    $('#echeance-no').click(function(e) {  
        $('#renouveler-hidden').prop("hidden", true);
    })
    $('#conges-yes').click(function(e) {
        $('#conges-yes-hidden').prop("hidden", false);
    });
    $('#conges-no').click(function(e) {  
        $('#conges-yes-hidden').prop("hidden", true);
    })

    $('#plusDeuxAns-yes').click(function(e) {
        $('#plusDeuxAns-Yes-hidden').prop("hidden", false);
        $('#plusDeuxAns-No-hidden').prop("hidden", true);
    });
    $('#plusDeuxAns-no').click(function(e) {  
        $('#plusDeuxAns-Yes-hidden').prop("hidden", true);
        $('#plusDeuxAns-No-hidden').prop("hidden", false);
    })


})

function getCookie(c_name){ 
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1)
                c_end = document.cookie.length;

            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

function switchForButton(key,data){
    switch (data){
        case "yes":
            $("#"+key+"-yes").prop("checked", true);
            $("#"+key+"-no").prop("checked", false);
            break;
        case "no":
            $("#"+key+"-yes").prop("checked", false);
            $("#"+key+"-no").prop("checked", true);
            break;
        default:
            $("#"+key+"-yes").prop("checked", false);
            $("#"+key+"-no").prop("checked", false);
    }
}

function viewbutton(clicked_id){
    console.log(clicked_id)
    $.ajax({
        url: '../ajax_get-demande-super-admin/',
        data: clicked_id,
        type: 'post',
        cache: false,
        contentType: false,
        processData: false,
    }).done(server_data => {
        console.log("info")
        getCookie("clicked_id")
        if (getCookie("clicked_id") != clicked_id){
            document.cookie = "clicked_id="+clicked_id+"; expires=0; path=/";
            location.reload(true);
        }
        var form = $("[name='form-file']");
            console.log("do something")
            console.log(form)
            for (var i = 0, length = form.length; i < length; i++) {
                console.log(form[i])
                $(form[i]).attr('action',"documents_admin_All/"+clicked_id+"/")
            }
        console.log(server_data)
        if (server_data !== "") {
            $("#physical_moral").val(server_data.physical_moral)
            $("#juridical_form").val(server_data.juridical_form)
            $("#social_reason").val(server_data.social_reason)
            $("#inputSIREN").val(server_data.inputSIREN)
            console.log(server_data.gender)
            switch (server_data.gender){
                case "male":
                    $("#gender-monsieur").prop("checked", true);
                    $("#gender-madame").prop("checked", false);
                    break;
                case "female":
                    $("#gender-monsieur").prop("checked", false);
                    $("#gender-madame").prop("checked", true);
                    break;
                default:
                    console.log("passe dans le default")
                    $("#gender-monsieur").prop("checked", false);
                    $("#gender-madame").prop("checked", false);
            }
            $("#inputName").val(server_data.inputName)
            $("#inputFirstName").val(server_data.inputFirstName)
            $("#inputMail").val(server_data.inputMail)
            $("#inputPhone").val(server_data.inputPhone)
            $("#inputActivity").val(server_data.inputActivity)
            $("#inputWebSite").val(server_data.inputWebSite)

            $("#inputAdress").val(server_data.inputAdress)
            $("#inputCode").val(server_data.inputCode)
            $("#inputCity").val(server_data.inputCity)
            $("#mois").val(server_data.mois)
            $("#annee").val(server_data.annee)
            $("#loyer").val(server_data.loyer)
            $("#garantie").val(server_data.garantie)
            $("#garantieMois").val(server_data.garantieMois)
            $("#caution").val(server_data.caution)
            $("#cautionMois").val(server_data.cautionMois)

            console.log(server_data.substitution)
            console.log(typeof server_data.substitution)
            if ((server_data.substitution == 0) || (server_data.substitution == 2)){
                $("#Partenaire").prop("checked",true)
                console.log("pass sub0")
            }
            if ((server_data.substitution == 1) || (server_data.substitution == 2)){
                $("#Courtier").prop("checked",true)
                console.log("pass sub1")
            }
                       
            switchForButton("incident",server_data.incident)
            switchForButton("difficulte",server_data.difficulte)
            switchForButton("preavis",server_data.preavis)
            switchForButton("echeance",server_data.echeance)
            if (server_data.echeance == "yes"){
                $('#renouveler-hidden').prop("hidden", false);
            }
            switchForButton("renouveler",server_data.renouveler)
            switchForButton("plusDeuxAns",server_data.plusDeuxAns)
            switch (server_data.plusDeuxAns){
                case "yes":
                    $('#plusDeuxAns-Yes-hidden').prop("hidden", false);
                    $('#plusDeuxAns-No-hidden').prop("hidden", true);
                    break;
                case "no":
                    $('#plusDeuxAns-Yes-hidden').prop("hidden", true);
                    $('#plusDeuxAns-No-hidden').prop("hidden", false);
                    break;
                default:
                    $('#plusDeuxAns-Yes-hidden').prop("hidden", true);
                    $('#plusDeuxAns-No-hidden').prop("hidden", true);
            }
            $("#ca2021").val(server_data.ca2021)
            $("#beneficePerte2021").val(server_data.beneficePerte2021)
            $("#ca2020").val(server_data.ca2020)
            $("#beneficePerte2020").val(server_data.beneficePerte2020)
            switchForButton("conges",server_data.conges)
            if (server_data.conges == "yes"){
                $('#conges-yes-hidden').prop("hidden", false);
            }
            $("#CC").val(server_data.CC)
            switchForButton("cautionPerso",server_data.cautionPerso)
            switchForButton("QuietSolution",server_data.QuietSolution)

            $("#modifyDemandeLocataire-form").attr('action','./modify-demande-super-admin/'+server_data.id+'/')
            $("#modifyDemandeBail-form").attr('action','./modify-demande-super-admin/'+server_data.id+'/')
            $("#modifyDemandeEligibility-form").attr('action','./modify-demande-super-admin/'+server_data.id+'/')
            
            console.log("server data")
            console.log(server_data)
            for(var key in server_data){
                if(/(adresse_doc)\d+$/.test(key)) {
                    var value=server_data[key];
                    $("#a-adresse_doc-"+key.substring(11,key.length)).attr("href", "../../media/"+value+"/")
                    $("#a-download-adresse_doc-"+key.substring(11,key.length)).attr("href", "../../media/"+value+"/")
                    $("#h6-adresse_doc-"+key.substring(11,key.length)).text(value);
                }
                if(/(type)\d+$/.test(key)) {
                    var value=server_data[key];
                    $("#h6-type-"+key.substring(4,key.length)).text(value);
                }
                if(/(size)\d+$/.test(key)) {
                    var value=server_data[key];
                    $("#small-size-"+key.substring(4,key.length)).text(value);
                }
                if(/(date)\d+$/.test(key)) {
                    var value=server_data[key];
                    const date = new Date(value)
                    console.log(date.toUTCString())
                    $("#small-date-"+key.substring(4,key.length)).text(date.toUTCString());
                }
            }

            // server_data.forEach((key,value) => {
            //     if(!/(test)\d+/.test(key)) {
            //         console.log(key)
            //         console.log(value)
            //     }
            // });
            //$("#h6-adresse_doc-9").text(server_data.adresse_doc9);
        } else {
            throw new Error("Obligatoire");
        }
    }).fail(() => alert("fail"))
}

function attribuer(clicked_id){
    console.log(clicked_id)
    $("#form-admin-select").attr('action','../admin-select/'+clicked_id+'/')
}

function WarningConfirm(int,elemid){
    data=[];
    data[0]=int;
    data[1]=elemid;
    console.log(int);
    console.log(elemid);
    Swal.fire({
        title: 'Etes vous sur ?',
        text: "Cela va envoyer un mail au client et un message au courtier en charge",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, Change la demande !',
    }).then(function(result) {
        if (result.isConfirmed) {
            $.ajax({
                url: './change/',
                data: data,
                type: 'post',
                cache: false,
                dataType: 'json',
                contentType: false,
                processData: false,
            }).done(server_data => {
                Swal.fire({
                    icon: 'success',
                    title: 'Validation',
                    text: 'La demande à été validé',
                    showCancelButton: false,
                    confirmButtonText: 'Yes !',
                }).then(function(result){
                    if (result.isConfirmed) {
                        location.reload(true);
                    }
                })
                
                //location.reload(true);
            }).fail(() => Swal.fire(
                'Fail',
                'Nothing as been done',
                'error'
            ))
           
        }
    })
}

function ChangerEtatContact(etat,elemid){
    data=[];
    data[0]=etat;
    data[1]=elemid;
    console.log(etat);
    console.log(elemid);
    $.ajax({
        url: './ajax-change-etat-contact/',
        data: data,
        type: 'post',
        cache: false,
        dataType: 'json',
        contentType: false,
        processData: false,
    }).done(server_data => {
        $("#status-"+elemid).text(etat)
        if (etat == "Fermer"){
            Swal.fire({
                title: 'Vous venez de fermer une demande de contact',
                text: "Voulez vous supprimer ce message ?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Supprimer',
            }).then(function(result) {
                if (result.isConfirmed) {
                    data[0]="supprimer";
                    $.ajax({
                        url: './ajax-change-etat-contact/',
                        data: data,
                        type: 'post',
                        cache: false,
                        dataType: 'json',
                        contentType: false,
                        processData: false,
                    }).done(server_data => {
                        location.reload(true);
                    }).fail(() => Swal.fire(
                        'Fail',
                        'nothing has been done',
                        'error'
                    ))

                }
            })
        }
    }).fail(() => Swal.fire(
        'Fail',
        'nothing has been done',
        'error'
    ))
}