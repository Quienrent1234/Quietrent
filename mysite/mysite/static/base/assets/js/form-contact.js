import { FormValidator } from '../../../register/assets/js/form-utils.js'
import { popup } from './popup.js'

async function check(event) {
    event.preventDefault()

    if ($(this).find('input[name=gridCheck]').is(':not(:checked)')) {
        await popup("Veuillez accepter les conditions d'utilisation")
        return
    }

    const formValidator = new FormValidator(
        new Map([
            ['name', $(this).find("input[name=name]").val()],
            ['email', $(this).find("input[name=email]").val()],
            ['phone_number', $(this).find("input[name=phone_number]").val()],
            ['msg_subject', $(this).find("input[name=msg_subject]").val()],
            ['message', $(this).find("textarea[name=message]").val()]
        ])
    )
    
    formValidator.checkEmptyFields()

    formValidator.check(
        new Map([
            ['email', /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/],
            ['phone_number', /^0[0-9]{9}$/]
        ])
    )

    if (formValidator.correct) {
        $(this).unbind('submit').submit()
        $(this).bind('submit', check)
    }
}

$('#contactForm').submit(check)