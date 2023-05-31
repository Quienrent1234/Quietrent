export async function loading(title) {
    await Swal.fire({
        title: title,
        html: '<b></b>',
        timer: 3000,
        timerProgressBar: true,
        didOpen: () => Swal.showLoading()
    })
}