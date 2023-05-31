import { FormValidator } from './form-utils.js'

function check(event) {
    event.preventDefault()

    let data = new Map([
        ['inputAddress', $(this).find("input[name=inputAddress]").val()],
        ['inputCode', $(this).find("input[name=inputCode]").val()],
        ['inputCity', $(this).find("input[name=inputCity]").val()],
        ['loyer', $(this).find("input[name=loyer]").val()],
        ['garantie', $(this).find("input[name=garantie]").val()],
        ['caution', $(this).find("input[name=caution]").val()]
    ])

    if ($(this).find('[name=negotiation]').is(':checked')) {
        $(this).find('select[name=mois]').val('')
        $(this).find('select[name=annee]').val('')
    } else if ($(this).find('select[name=mois]').val() === null || $(this).find('select[name=annee]').val() === null)
        data.set('negotiation', null)

    const verificator = new Map([
        ['loyer', /[0-9]{4,}([.,][0-9]{1,2})?$/],
        ['garantie', /[0-9]{0,}([.,][0-9]{1,2})?$/],
        ['caution', /[0-9]{0,}([.,][0-9]{1,2})?$/]
    ])
    
    if ((data.get('garantie') == '0')) {
        verificator.set('label-garantieMois', /0/)
    }
    else {
        verificator.set('label-garantieMois', /[1-6]/)
    }

    if ((data.get('caution') == '0')) {
        verificator.set('label-cautionMois', /0/)
    }
    else {
        verificator.set('label-cautionMois', /[1-6]/)
    }

    const formValidator = new FormValidator(data)
    formValidator.checkEmptyFields()

    formValidator.add('label-garantieMois', $(this).find("select[name=garantieMois]").val())
    formValidator.add('label-cautionMois', $(this).find("select[name=cautionMois]").val())

    formValidator.check(verificator)

    if ((formValidator.correct)) {
        $(this).unbind('submit').submit()
        $(this).bind('submit', check)
    }
}

$('#form-bail').submit(check)