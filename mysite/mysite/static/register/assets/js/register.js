import { FormValidator } from './form-utils.js'
import { getCookie } from './get-cookie.js'

function check(event) {
    event.preventDefault()
    const email = $(this).find("input[name=inputMail]").val()

    const formValidator = new FormValidator(
        new Map([
            ['inputMail', email],
            ['inputPass', $(this).find("input[name=inputPass]").val()]
        ])
    )
    
    formValidator.checkEmptyFields()
    formValidator.check(new Map([['inputMail', /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/]]))

    $.ajax({
        url: '../ajax-verif-mail/',
        data: email,
        type: 'post',
        cache: false,
        contentType: false,
        processData: false
    }).done(result => {
        if (result === 'true') {
            if (formValidator.correct) {
                $(this).unbind('submit').submit()
                $(this).bind('submit', check)
            }
        } else
            $(`#inputMail`).after(`<div class="form-remove"><span>Cette adresse mail est déjà utilisée</span></div>`)
    })
}

$(document).ready(function() { 
    $.ajaxSetup({headers: {'X-CSRFToken': getCookie('csrftoken')}}) 
})

$('#register-form').submit(check)