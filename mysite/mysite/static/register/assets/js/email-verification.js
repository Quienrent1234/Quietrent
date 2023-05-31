import { loading } from './timer.js'

function check(event) {
    event.preventDefault()
    loading('Sauvegarde de vos données').then(() => {
        $(this).unbind('submit').submit()
        $(this).bind('submit', check)
    })
}



$('#email-verification-form').submit(check)