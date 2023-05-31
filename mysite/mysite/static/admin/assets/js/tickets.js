
$(document).ready(function() {
    $(function() {
        $.ajaxSetup({
            headers: {"X-CSRFToken": getCookie("csrftoken")}
        });
    });
})


function getCookie(c_name){ 
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1)
                c_end = document.cookie.length;

            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}


function ChangeEtatTicket(etat,elemid){
    data=[];
    data[0]=etat;
    data[1]=elemid;
    console.log(etat);
    console.log(elemid);
    $.ajax({
        url: './ajax-change-etat-tickets/',
        data: data,
        type: 'post',
        cache: false,
        dataType: 'json',
        contentType: false,
        processData: false,
    }).done(server_data => {
        texte="erreur"
        switch (etat){
            case 0 :
                texte="Clos"
                removeClass1="badge badge-soft-success border-0 font-12"
                removeClass2="badge badge-soft-pink border-0 font-12"
                addClass="btn btn-outline-dark border-0 font-12"
                break;
            case 1 :
                texte="En Cours"
                removeClass1="btn btn-outline-dark border-0 font-12"
                removeClass2="badge badge-soft-success border-0 font-12"
                addClass= "badge badge-soft-pink border-0 font-12"
                break;
            case 2:
                texte="Résolu"
                removeClass1="btn btn-outline-dark border-0 font-12"
                removeClass2="badge badge-soft-pink border-0 font-12"
                addClass= "badge badge-soft-success border-0 font-12"
                break;
        }
        $("#ticket-button-"+elemid).text(texte)
        $("#ticket-button-"+elemid).removeClass(removeClass1);
        $("#ticket-button-"+elemid).removeClass(removeClass2);
        $("#ticket-button-"+elemid).removeClass(removeClass1);
        $("#ticket-button-"+elemid).addClass(addClass);

    }).fail(() => Swal.fire(
        'Fail',
        'Nothing as been done',
        'error'
    ))
}