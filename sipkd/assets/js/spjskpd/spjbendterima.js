var kd_organisasi = ''
var to_edit = ''
var to_edit_setor = ''
var arr_penerima = []
var arr_setor_bendterima = []

$(document).ready(function () {
    var table = $('#tabel_penerimaan').DataTable( {
        "bLengthChange": false, 
        scrollY:        "150px",
        scrollX:        true,
        fixedHeader: 	true,
        paging:         false,
        "bInfo":false,
    });

    var table = $('#tabel_setor').DataTable( {
        "bLengthChange": false, 
        scrollY:        "150px",
        scrollX:        true,
        fixedHeader: 	true,
        paging:         false,
        "bInfo":false,
    });

    $('#cb_xbulan').val(getBlnToNum(DateNowInd()));
    refreshData();
    $('#btn_tambah').attr('alt','tambah_spjbendterima_terima/add/\'\'/\'\'/pungut/');
    $('#btn_tambah_setor').attr('alt','tambah_spjbendterima_terima/add/\'\'/\'\'/setor/');
    $('#btn_cetak').attr('alt',link_cetak_bendterima);
});

$('#kd_org2').change(function(){
    kd_organisasi = this.value;
    refreshData();
});

$('#cb_xbulan').change(function(){
    refreshData();
});

function refreshData(){
    if (kd_organisasi!='') {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            url: link_refreshdata_spjbendterima,
            data: {kode_organisasi:kd_organisasi,xbulan:$('#cb_xbulan').val()},
            dataType: 'html',
            success: function(data){ 
                render_tabel_penerimaan(JSON.parse(data)['hasil_penerimaan']);
                render_tabel_setor(JSON.parse(data)['hasil_setor']);

                arr_penerima = [];
                arr_setor_bendterima = [];
            },
            error: function(data){
                console.log('gagal');
            }
        });
    }
}

function render_tabel_penerimaan(n) {
    $('#tabel_penerimaan').DataTable( {
        destroy:true,
        "bLengthChange": false, 
        scrollY:        "150px",
        scrollX:        true,
        //scrollCollapse: true,
        fixedHeader: true,
        paging:         false,
        "bInfo": false,
        "ordering": false,
        data: n,
        'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            $('td', row).eq(0).css({ 'text-align': 'center'});
            $('td', row).eq(1).css({ 'text-align': 'center'});
            $('td', row).eq(3).css({ 'text-align': 'center'});
            $('td', row).eq(6).css({ 'text-align': 'center'});
            $('td', row).eq(7).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[7]));
            $('td', row).eq(9).css({ 'text-align': 'center'}).html('<input class="chk_rek_terima" type="checkbox" onClick="cek_uncheck_bendterima(this,\''+data[0]+'\',\''+data[2]+'\',\'terima\',\''+data[9]+'\')"/>');
            
            if (data[9]!='T') {
                $(row).addClass('hijau');
            }else{
                $(row).addClass('kuning');
            }

            $('td', row).eq(8).css({ 'text-align': 'center'}).html('<div class="btn btn-sm btn-info" alt="tambah_spjbendterima_terima/edit/'+data[0]+'/'+data[2].replace(/\s+/g, '^**^').split('/').join('_')+'/pungut/" onClick="showModal(this,\'input_spj_bendterima_terima\')" style="width:80%;" title="Edit Data" id="btn_edit">\
                        <i class="fa fa-pencil"></i>\
                    </div>');
            // for (var i = 2; i <= 6; i++) {
            //     $('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
            // }
        },
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return isNaN(typeof i === 'string' ?
                                i.replace(/[\$,]/g, '')*1 :
                                typeof i === 'number' ?
                                        i : 0)==true?0:typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            // Total over all pages
            total7 = api
                .column( 7 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );
            $( api.column( 7 ).footer() ).html(toRp_WithDesimal(total7.toString()));
            // for (var i = 2; i <= 6; i++) {
            //     total = api
            //     .column( i )
            //     .data()
            //     .reduce( function (a, b) {
            //         return intVal(a) + intVal(b);
            //     }, 0 );
            //     $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
            //  }
       }
    });
}

function render_tabel_setor(n) {
    $('#tabel_setor').DataTable( {
        destroy:true,
        "bLengthChange": false, 
        scrollY:        "150px",
        scrollX:        true,
        //scrollCollapse: true,
        fixedHeader: true,
        paging:         false,
        "bInfo": false,
        "ordering": false,
        data: n,
        'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            $('td', row).eq(0).css({ 'text-align': 'center'});
            $('td', row).eq(1).css({ 'text-align': 'center'});
            $('td', row).eq(3).css({ 'text-align': 'center'});
            $('td', row).eq(5).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[6]));
            $('td', row).eq(7).css({ 'text-align': 'center'}).html('<input class="chk_rek_setor" type="checkbox" onClick="cek_uncheck_bendterima(this,\''+data[0]+'\',\''+data[2]+'\',\'setor\',0)"/>');
            $('td', row).eq(6).css({ 'text-align': 'center'}).html('<div class="btn btn-sm btn-info" alt="tambah_spjbendterima_terima/edit/'+data[0]+'/'+data[2].replace(/\s+/g, '^**^').split('/').join('_')+'/setor/" onClick="showModal(this,\'input_spj_bendterima_terima\')" style="width:80%;" title="Edit Data" id="btn_edit">\
                        <i class="fa fa-pencil"></i>\
                    </div>');
        },
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return isNaN(typeof i === 'string' ?
                                i.replace(/[\$,]/g, '')*1 :
                                typeof i === 'number' ?
                                        i : 0)==true?0:typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            // Total over all pages
            total5 = api
                .column( 6 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );
            $( api.column( 5 ).footer() ).html(toRp_WithDesimal(total5.toString()));
       }
    });
}

function cek_uncek_all(e, chkclass, page){
    $('.'+chkclass+'_'+page).each(function(){ 
        this.checked = e.checked; 
    });


};

function cek_uncheck_bendterima(e, no, no_bukti, jenis, status) {
    
    if(e.checked){
        if (jenis == 'terima') {
            to_edit = no;
            arr_penerima.push(no+'^'+no_bukti+'^'+status);
        } else if (jenis='setor'){
            to_edit_setor = no;
            arr_setor_bendterima.push(no+'^'+no_bukti+'^'+status);
        }

    } else {
        if (jenis == 'terima') {
            to_edit = '';
            arr_penerima.splice(arr_penerima.indexOf(no+'^'+no_bukti+'^'+status), 1);
        } else if (jenis=='setor'){
            to_edit_setor = '';
            arr_setor_bendterima.splice(arr_setor_bendterima.indexOf(no+'^'+no_bukti+'^'+status), 1);
        }
    }
}

$('#btn_edit').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !')    
    }else{
        if (to_edit=='') {
            $.alertable.alert('Centang data yang ingin diedit terlebih dahulu !')    
        }else{
            $(this).removeAttr('alt');

            no_bku = arr_penerima[arr_penerima.length-1].split('^')[0]
            nobukti = arr_penerima[arr_penerima.length-1].split('^')[1].split('/').join('_')
            $(this).attr('alt','tambah_spjbendterima_terima/edit/'+no_bku+'/'+nobukti+'/pungut/')
            showModal($('#btn_edit')['0'],'input_spj_bendterima_terima');
        }      
    }
});

$('#btn_tambah').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !');    
    }else{
        showModal($('#btn_tambah')['0'],'input_spj_bendterima_terima');
    }
});


$('#btn_hapus').click(function(){

    function scrStrInArr(str, inArray){
        for (var i = 0; i < inArray.length; i++) {
            var hasil = inArray[i].split("^");
            if(hasil[2]==str) return i;
        };
        return -1;
    }

    var cek_STR = scrStrInArr('Y',arr_penerima);

    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !');    
    } else if (arr_penerima=='') {
        $.alertable.alert('Data Penerimaan belum ada yang dipilih!');    
    } else if (cek_STR >= 0){
        $.alertable.alert('Data Penerimaan ada yang SUDAH DISETOR!!, Penerimaan yang sudah disetor tidak dapat dihapus.');
    } else {
        $.alertable.confirm('Apakah anda yakin ingin menghapus Data Penerimaan ?').then(function() {
            $.ajax({
                type : "POST",
                headers : { "X-CSRFToken": csrf_token },
                url : link_hapus_spjbendterima,
                data :{
                    'arr_penerima':JSON.stringify(arr_penerima),
                    'jenis':'penerimaan',
                    'skpd':kd_organisasi,
                },
                dataType: 'html',
                success: function(data){
                    refreshData();
                    message_ok('success', 'Proses Hapus Berhasil !');
                    $(".cover").hide();
                },
                error: function(){
                    message_ok('error', 'Proses Gagal !');
                    $(".cover").hide();
                }
            });
        }, function() {
            message_ok('error', 'Hapus data dibatalkan');
        });   
    }
});

$('#btn_cetak').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !');    
    }else{
        showModal($('#btn_cetak')['0'],'cetak_bendterimaskpd');
    }
});

// TOMBOL TABEL SETOR
$('#btn_edit_setor').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !')    
    }else{
        if (to_edit_setor=='') {
            $.alertable.alert('Centang data yang ingin diedit terlebih dahulu !')    
        }else{
            $(this).removeAttr('alt');

            no_bku = arr_setor_bendterima[arr_setor_bendterima.length-1].split('^')[0]
            nobukti = arr_setor_bendterima[arr_setor_bendterima.length-1].split('^')[1].split('/').join('_')
            $(this).attr('alt','tambah_spjbendterima_terima/edit/'+no_bku+'/'+nobukti+'/setor/')
            showModal($('#btn_edit_setor')['0'],'input_spj_bendterima_terima');
        }      
    }
});

$('#btn_tambah_setor').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !')    
    }else{
         showModal($('#btn_tambah_setor')['0'],'input_spj_bendterima_terima');     
    }
});

$('#btn_hapus_setor').click(function(){
    if (kd_organisasi=='') {
        $.alertable.alert('Pilih organisasi terlebih dahulu !')    
    } else if (arr_setor_bendterima=='') {
        $.alertable.alert('Data Setoran belum ada yang dipilih!')    
    } else {
        $.alertable.confirm('Apakah anda yakin ingin menghapus Data Setoran ?').then(function() {
            $.ajax({
                type : "POST",
                headers : { "X-CSRFToken": csrf_token },
                url : link_hapus_spjbendterima,
                data :{
                    'arr_setor_bendterima':JSON.stringify(arr_setor_bendterima),
                    'jenis':'setor',
                    'skpd':kd_organisasi,
                },
                dataType: 'html',
                success: function(data){
                    refreshData();
                    message_ok('success', 'Proses Hapus Berhasil !');
                    $(".cover").hide();
                },
                error: function(){
                    message_ok('error', 'Proses Gagal !');
                    $(".cover").hide();
                }
            }); 

        }, function() {
            message_ok('error', 'Hapus data dibatalkan');
        });  
    }
});
// END TOMBOL SETOR

