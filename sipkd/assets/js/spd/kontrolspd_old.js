var_ada = false;
$(document).ready(function () {
    $('#kontrol_spd').DataTable( {
        scrollY: 259,
        scrollX: true,
        scrollCollapse: false,
        paging: false,
        // fixedColumns: {
        // leftColumns: 2
        // }
    });
    if($("#semua_checked").length){
        var_ada = true;
    }else{
        var_ada = false;
    }
    ambil_spd();
});

$('#operator').change(function(){
    ambilSPDUser(this.value);
});

function ambil_spd(){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambil_spd_kontrol,
        data :{
            'check_semua':var_ada==true?$('#semua_checked')[0].checked==true ? true : false:'',
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
            $('#kontrol_spd').DataTable( {
                destroy:true,
                "bLengthChange":false, 
                scrollY:259,
                scrollX:true,
                fixedHeader:true,
                paging:false,
                // fixedColumns: {
                // leftColumns: 2
                // },
                data: JSON.parse(data)['list_kontrol_spd'],
                'createdRow':  function (row, data, index) {
                    $('td', row).css({ 'cursor': 'pointer'});
                },
            });
            $(".cover").hide();
        },
        error: function(){
            message_ok('error', 'Proses Gagal !');
            $(".cover").hide();
        }
    });
}

function ambilSPDUser(val){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambil_spd_user,
        data :{
            'user':val,
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
            $('#kontrol_spd').DataTable( {
                destroy:true,
                "bLengthChange":false, 
                scrollY:259,
                scrollX:true,
                fixedHeader:true,
                paging:false,
                // fixedColumns: {
                // leftColumns: 2
                // },
                data: JSON.parse(data)['list_spd_user'],
                'createdRow':  function (row, data, index) {
                },
            });
            $(".cover").hide();
        },
        error: function(){
            message_ok('error', 'Proses Gagal !');
            $(".cover").hide();
        }
    });
}