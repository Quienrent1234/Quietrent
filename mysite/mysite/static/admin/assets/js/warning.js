let dels1 = $('.delete_form1')
for (let del1 of dels1) {
    $(del1).submit(function check3(event) {
    event.preventDefault()
        Swal.fire({
            title: 'Etes-vous sur ?',
            text: "Vous ne pourrez pas revenir en arrière !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, je confirme !',
          }).then(function(result) {
            if (result.isConfirmed) {
              Swal.fire(
                "C'est fait !",
                'Votre document a bien été supprimé.',
                'success'
              )
              $(del1).unbind('submit').submit()
              $(del1).bind('submit', check3)
            }
          })
})
}

let dels2 = $('.delete_form2')
for (let del2 of dels2) {
    $(del2).submit(function check3(event) {
    event.preventDefault()
        Swal.fire({
            title: 'Etes-vous sur ?',
            text: "Vous ne pourrez pas revenir en arrière !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, je confirme !',
          }).then(function(result) {
            if (result.isConfirmed) {
              Swal.fire(
                "C'est fait !",
                'Votre document a bien été supprimé.',
                'success'
              )
              $(del2).unbind('submit').submit()
              $(del2).bind('submit', check3)
            }
          })
})
}

let dels3 = $('.delete_form3')
for (let del3 of dels3) {
    $(del3).submit(function check3(event) {
    event.preventDefault()
        Swal.fire({
            title: 'Etes-vous sur ?',
            text: "Vous ne pourrez pas revenir en arrière !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, je confirme !',
          }).then(function(result) {
            if (result.isConfirmed) {
              Swal.fire(
                "C'est fait !",
                'Votre document a bien été supprimé.',
                'success'
              )
              $(del3).unbind('submit').submit()
              $(del3).bind('submit', check3)
            }
          })
})
}

let dels4 = $('.delete_form4')
for (let del4 of dels4) {
    $(del4).submit(function check3(event) {
    event.preventDefault()
        Swal.fire({
            title: 'Etes-vous sur ?',
            text: "Vous ne pourrez pas revenir en arrière !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, je confirme !',
          }).then(function(result) {
            if (result.isConfirmed) {
              Swal.fire(
                "C'est fait !",
                'Votre document a bien été supprimé.',
                'success'
              )
              $(del4).unbind('submit').submit()
              $(del4).bind('submit', check3)
            }
          })
})
}


let buttons = $('.validate_docs')

for (let button of buttons) {
   $(button).submit(function check3(event) {
    event.preventDefault()
        Swal.fire({
            title: 'Etes-vous sur ?',
            text: "Vous ne pourrez pas revenir en arrière !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Oui, je confirme !',
          }).then(function(result) {
            if (result.isConfirmed) {
              Swal.fire(
                "C'est fait !",
                'Votre document a bien été supprimé.',
                'success'
              )
              $(button).unbind('submit').submit()
              $(button).bind('submit', check3)
            }
          })
})
}
