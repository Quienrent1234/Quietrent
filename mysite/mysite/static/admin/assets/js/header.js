function header_notification(){
    $.ajax({
        url: '../ajax_get_message/',
        cache: false,
        contentType: false,
        processData: false,
    }).done(server_data => {
        $('#notification-menu').text('');
        for (elem in server_data){
            switch (server_data[elem].type){
                case "doc":
                    icon="mdi mdi-file-document"
                    break
                case "modif":
                    icon="mdi mdi-information-outline"
                    break
                case "ajout" :
                    icon="mdi mdi-file-download-outline"
                    break
                case "ticket":
                    icon="mdi mdi-ticket-account"
                    break
                default :
                    icon="ti ti-chart-arcs" //default for other
            }            
            html= `<a href="../redirectNotifButton/` + server_data[elem].id + `/" class="dropdown-item py-3">
            <small class="float-end text-muted ps-2">il y a `+server_data[elem].date_message+` min</small>
            <div class="media">
                <div class="avatar-md bg-soft-primary">
                    <i class="`+icon+`" style="color: #4C9082;"></i>
                </div>
                <div class="media-body align-self-center ms-2 text-truncate">
                    <h6 class="my-0 fw-normal text-dark">`+server_data[elem].titre+`</h6>
                    <small class="text-muted mb-0">`+server_data[elem].message+`.</small>
                </div><!--end media-body-->
            </div><!--end media-->
        </a><!--end-item-->`
        $('#notification-menu').append(html);
        }
    }).fail(() => alert("fail"))
}