import { getCookie } from './get-cookie.js'
import { FormValidator, readRadioButton } from './form-utils.js'

$(document).ready(function() {
    $(function() {
        $.ajaxSetup({
            headers: {"X-CSRFToken": getCookie("csrftoken")}
        });
    });
    $('#form-loc').submit(check)
    $('#buttonInsee').click(insee)
})


function insee(event) {
    const siren = $('#inputSIREN').val()
    let data=[];
    $('div.insee-remove').remove()
    data[0]=siren;
    if ((/^[0-9]{14}$/).test(siren)){
        $.ajax({
            url: './ajax_siret/',
            data : data,
            type: 'post',
            cache: false,
            contentType: false,
            processData: false
            
        }).done(result => {
            console.log(Object.keys(result))
            $('div.insee-remove').remove()
            $('div.form-remove').remove()
            $('#'+result["physical-moral"]).prop( "checked", true );
            $('#social_reason').val(result["social-reason"])
            $('#'+result["categorieJuridiqueUniteLegale"]).prop( "selected", true );
            $('#inputName').val(result["nom"])
            $('#inputFirstName').val(result["prenom"])
            if ("sexe" in Object.keys(result)){
                if (result["sexe"]='F'){$('#Gfemale').prop( "checked", true );}
                else{
                    $('#Gmale').prop( "checked", true );
                }
            }
            $('#inputActivity').val(result["activity"])
        }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
            $(`#inputSIREN`).after(`<div class="insee-remove"><span> SIRET non enregister à l'INSEE</span></div>`)
        })
    }else{$(`#inputSIREN`).after(`<div class="insee-remove"><span> SIRET invalide</span></div>`)}
}


function check(event) {
    event.preventDefault()

    const formValidator = new FormValidator(
        new Map([
            ['juridical_form', $(this).find("select[name=juridical_form]").val()],
            ['social_reason', $(this).find("input[name=social_reason]").val()],
            ['inputSIREN', $(this).find("input[name=inputSIREN]").val()],
            ['inputName', $(this).find("input[name=inputName]").val()],
            ['inputFirstName', $(this).find("input[name=inputFirstName]").val()],
            ['inputPhone', $(this).find("input[name=inputPhone]").val()],
            ['inputActivity', $(this).find("input[name=inputActivity]").val()],
            ['physical_moral', readRadioButton('physical_moral')],
            ['gender', readRadioButton('gender')]
        ])
    )
    
    formValidator.checkEmptyFields()

    formValidator.add('inputWebSite', $(this).find("input[name=inputWebSite]").val())

    formValidator.check(
        new Map([
            ['inputSIREN', /^[0-9]{14}$/],
            ['inputPhone', /^0[0-9]{9}$/],
            ['inputWebSite', /^(|((https?\:\/\/)?[a-zA-Z0-9_/\-.]+(?:\.[a-zA-Z0-9_/\-]+)*))$/]
        ])
    )

    if (formValidator.correct) {
        $(this).unbind('submit').submit()
        $(this).bind('submit', check)
    }
}

