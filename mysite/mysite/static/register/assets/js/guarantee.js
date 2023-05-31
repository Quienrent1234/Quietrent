import { FormValidator } from './form-utils.js'

function check(event) {
    console.log("enter")
    event.preventDefault()

    const subs0checked = $(this).find("input[name=DG]").is(':checked')
    const subs1checked = $(this).find("input[name=GAPD]").is(':checked')

    let substitution
    if (subs0checked) {
        if (subs1checked)
            substitution = '2'
        else
            substitution = '0'
    } else if (subs1checked)
        substitution = '1'
    
    $(this).find("input[name=substitution").val(substitution)

    console.log("here")


    const formValidator = new FormValidator(new Map([['garantie', substitution]]))
    formValidator.checkEmptyFields()
    
    console.log(formValidator.correct)


    if (formValidator.correct) {
        $(this).unbind('submit').submit()
        $(this).bind('submit', check)
    }
}

$('#form-garantie').submit(check)