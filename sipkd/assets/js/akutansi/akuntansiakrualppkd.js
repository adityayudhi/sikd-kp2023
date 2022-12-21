var kd_organisasi = ''
var to_edit = ''
var to_edit_setor = ''
var arr_penerima = []
var arr_setor_bendterima = []
$(document).ready(function () {
    var table = $('#tabel_penerimaan').DataTable( {
        "bLengthChange": false, 
        scrollY:        "350px",
        scrollX:        true,
        fixedHeader: 	true,
        paging:         false,
        "bInfo":false,
    });
});
