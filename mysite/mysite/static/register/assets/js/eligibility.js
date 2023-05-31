import { FormValidator, readRadioButton } from './form-utils.js'
import { loading } from './timer.js'

function setMinusIfNecessary(year) {
    if ($(`#loss${year}`).is(':checked')) {
        const beneficePerte = $(`#beneficePerte${year}`).val()
        if (beneficePerte[0] != '-') {
            $(`#beneficePerte${year}`).val('-'+beneficePerte)
        }
    }
}

function check(event) {
    event.preventDefault()
    
    setMinusIfNecessary('2020')
    setMinusIfNecessary('2021')

    const data = new Map([
        ['incident', readRadioButton('incident')],
        ['difficulte', readRadioButton('incident')],
        ['preavis', readRadioButton('preavis')],
        ['echeance', readRadioButton('echeance')],
        ['plusDeuxAns', readRadioButton('plusDeuxAns')],
        ['QuietSolution', readRadioButton('QuietSolution')]
    ])

    const verificator = new Map()

    if ((data.get('plusDeuxAns') === 'yes')) {
        data.set('ca2021', $(this).find("input[name=ca2021]").val())
        verificator.set('ca2021', /[0-9]{1,}([.,][0-9]{1,2})?$/)

        data.set('beneficePerte2021', $(this).find("input[name=beneficePerte2021]").val())
        verificator.set('beneficePerte2021', /-?[0-9]{1,}([.,][0-9]{1,2})?$/)

        data.set('ca2020', $(this).find("input[name=ca2020]").val())
        verificator.set('ca2020', /[0-9]{1,}([.,][0-9]{1,2})?$/)

        data.set('beneficePerte2020', $(this).find("input[name=beneficePerte2020]").val())
        verificator.set('beneficePerte2020', /-?[0-9]{1,}([.,][0-9]{1,2})?$/)
    } else
        data.set('cautionPerso', readRadioButton('cautionPerso'))
    
    const formValidator = new FormValidator(data)
    formValidator.checkEmptyFields()
    formValidator.check(verificator)

    if (formValidator.correct) {
        loading('Vérification de votre éligibilié').then(() => {
            $(this).unbind('submit').submit()
            $(this).bind('submit', check)
        })
    }
}

$(document).ready(function(e) {
    $('#YEcheance').click(function(e) {
        $('#ifYEcheance').css("display", "block")
        $('#YRenouveler').prop('required', true)
        $('#NRenouveler').prop('required', true)
    })

    $('#NEcheance').click(function(e) {  
        $('#ifYEcheance').css("display", "none")
        $('#YRenouveler').prop('required', false)
        $('#NRenouveler').prop('required', false)
    })

    $('#YplusDeuxAns').click(function(e) {
        $(`label[for=cautionPerso]`).text("Souhaitez vous ajouter une caution personelle a ce bail ?")
        $('#ifYplusDeuxAns').css("display", "block")
        $('#ifNplusDeuxAns').css("display", "block")
        $('#ca2021').prop('required', true)
        $('#beneficePerte2021').prop('required', true)
        $('#ca2020').prop('required', true)
        $('#beneficePerte2020').prop('required', true)
        $('#Yconges').prop('required', true)
        $('#Nconges').prop('required', true)
        $('#YcautionPerso').prop('required', true)
        $('#NcautionPerso').prop('required', true)
    })
    
    $('#NplusDeuxAns').click(function(e) { 
        $(`label[for=cautionPerso]`).text("Avez-vous la possibilité d'emettre une caution personelle ou d'une entreprise de plus de 2 ans solvable ?")
        $('#ifYplusDeuxAns').css("display", "none")
        $('#ifNplusDeuxAns').css("display", "block")
        $('#YcautionPerso').prop('required', true)
        $('#NcautionPerso').prop('required', true)
        $('#ca2021').prop('required', false)
        $('#beneficePerte2021').prop('required', false)
        $('#ca2020').prop('required', false)
        $('#beneficePerte2020').prop('required', false)
        $('#Yconges').prop('required', false)
        $('#Nconges').prop('required', false)
  
    })
    $('#Yconges').click(function() {  
        $('#ifYconges').css("display", "block")
        $('#CC').prop('required', true)
    })

    $('#Nconges').click(function() {  
        $('#ifYconges').css("display", "none")
        $('#CC').prop('required', false)
    })
})

$('#eligibiliteSubmit').submit(check)