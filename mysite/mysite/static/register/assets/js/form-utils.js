import { getCookie } from './get-cookie.js'

export class FormValidator {
    #data
    #correct
    #emptyFields
    
    constructor(data) {
        this.#data = data
        this.#correct = true
        this.#emptyFields = []

        $('div.form-remove').remove()
        $('div.insee-remove').remove()
    }

    get correct() {
        return this.#correct
    }

    add(key, value) {
        this.#data.set(key, value)
    }

    checkEmptyFields() {
        for (const [key, value] of this.#data) {
            if ((value === undefined || value === null || value.trim() === '')) {
                $(`#${key}`).after('<div class="form-remove"><span>Champ vide</span></div>')
                this.#emptyFields.push(key)
                this.#correct = false
            }
        }
    }

    check(verificator) {
        for (const [key, regex] of verificator) {
            if (!this.#emptyFields.includes(key)) {
                const value = this.#data.has(key) ? this.#data.get(key) : ''
                if (!regex.test(value)) {
                    $(`#${key}`).after(`<div class="form-remove"><span>${$(`label[for=${key}]`).text()} invalide</span></div>`)
                    this.#correct = false
                }
            }
        }
    }
}

export function readRadioButton(name) {
    const radios = $(`input[name=${name}]`)
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            return radios[i].value
        }
    }
}