var var_nosp2d = '';
var var_nospm = '';
var isSimpan = false;
var dataAfektasi = [];
var array_keg = [];
var array_rinci = [];
var pjg_keg = 0;
var hasil_rekening;
var jumlah_spm = 0;
var jumlah_sp2d = 0;
var array_sumdan = [];
var array_jumlah_sekarang = [];
var dari_keg = false;
var pknospm = '';
var array_jumlah_sekarang_fix = [];
var dari = '';

$(document).ready(function(){
    $('#tabelnya').DataTable( {
        scrollY: 200,
        paging: false,
        "ordering": false
    });
    $('#btn_next').attr('disabled','disabled');
    $('#btn_prev').attr('disabled','disabled');

    // ambilBank();

    $('#tgl_sp2d').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    },
    function(start, end, label) {
        xx = generate_nomor_auto(start.format('YYYY'), $('#no_sp2d'), 'SP2D', start.format('MM'), $('#kd_org2').val().split('.')[0], $('#kd_org2').val().split('.')[1], $('#kd_org2').val().split('.')[2], $('#kd_org2').val().split('.')[3], jenis_modul);
        if(xx){
            getTriwulan('#tgl_sp2d', '#frm_triwull');
        }
    });

    $('#tgl_spm').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    });

    clearForm();

    $('#btn_cetak').attr('alt',link_render_cetak_sp2dgu_tu_nihil);

});

function clearForm(){
    isSimpan = true;
    pknospm = '';
    dari_keg = false;
    $('#kunci_sp2d').text('(DRAFT)');
    $('#tgl_sp2d').val(DateNowInd('yes'));
    $('#tgl_spm').val(DateNowInd('yes'));
    $('#no_spm').val('');
    $('#bendahara').val('');
    $('#norek_bendahara').val('');
    $('#npwp_bendahara').val(''); 

    $('#jns_anggaran').attr('disabled','disabled');
    if (perubahan=='0') {
        $('#jns_anggaran').val('0');
    }else{
        $('#jns_anggaran').val('1');
    }

    // ambilSumberDanaAwal();
    dataAfektasi=[];


    getTriwulan('#tgl_sp2d', '#frm_triwull');
    // ambilKegiatan(function() {});

    $('#btn_simpan').removeAttr('disabled');
    $('#btn_hapus').attr('disabled', 'disabled');

    get_dataBendahara();

    if($('#kd_org2').val() != ''){
      generate_nomor_auto_spm_gu_tu_ls();
    }
}

function ambilSumberDanaAwal(){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambilSumberDanaAwal,
        data :{
   
        },
        dataType: 'html',
        success: function(data){
          hasilnya = JSON.parse(data)['sumdanawal'][0]['rekening'];
          $('#norek_bankasal').val(hasilnya);
          $('#norek_bankasal').trigger('change');
        },
        error: function(){
            message_ok('error', 'Proses ambil data bank gagal !');
        }
    });
}

$('#kd_org2').change(function(){
    clearForm();
    // ambilKegiatan(function() {});
    $('#status_keperluan').val('TU NIHIL pada '+$('#kd_org2_urai').val()+' TA. '+DateNowInd().split(' ')[2]+', sesuai dengan bukti terlampir.'); 
});

$('#norek_bankasal').change(function(){
    ambilBank();
});

$('#cari_bendahara').click(function(){
    render_modal('Lihat Rekenign', 'lht_bdhr',[]);
});

$('#btn_lihat_sp2d').click(function(){
    render_modal('Lihat SP2D', 'sp2d_tunihil', []);
});

$('#btn_tambah_sp2d').click(function(){
    clearForm();
});

$('#btn_simpan').click(function(){
    simpan_tunihil();
});

$('#btn_hapus').click(function(){
    hapus_tunihil();
});

$('#frm_triwull').change(function(){
    if (this.value=='0') {
        ambilKegiatan(function() {});
    }else{
        // ambilRekening(function() {});
    }
});


$('#btn_lihat_spm').click(function(){
    if ($('#kd_org2').val()=='') {
        $.alertable.alert('Kode organisasi tidak boleh kosong !');
      }else{
        render_modal('Lihat SPM', 'spm_sp2d', [$('#kd_org2').val(),'TU_NIHIL']);
      }
});

$('#btn_cetak').click(function(){
var attr = $('#btn_simpan').attr('disabled');
var bool = cekTanggal($('#tgl_spm').val(), $('#tgl_sp2d').val())
    
    if ($('#no_sp2d').val()=='') {
        message_ok('error', 'NO SP2D tidak boleh kosong !');
        $('#no_sp2d').focus();
      }else if($('#no_spm').val()==''){
        message_ok('error', 'NO SPM tidak boleh kosong !');
        $('#no_spm').focus();
      }else if($('#status_keperluan').val()==''){
        message_ok('error', 'Deskripsi tidak boleh kosong !');
        $('#status_keperluan').focus();
      }else if($('#bendahara').val()==''){
        message_ok('error', 'Bendahara tidak boleh kosong !');
        $('#bendahara').focus();
      }else if(bool==false){
        message_ok('error', 'Tanggal SP2D tidak boleh lebih kecil dari tanggal SPM');
        $('#tgl_sp2d').focus();
      }else{
        // if true or if button disabled
        if (typeof attr !== typeof undefined && attr !== false) {
            showModal(this,'cetak_sp2d_up_gu_tu_gunihil');
        }else{
            simpan_tunihil();
            showModal(this,'cetak_sp2d_up_gu_tu_gunihil'); 
        }
      }

});


function ambilRekening(callback){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambilRekening,
        data :{
            'skpd': $('#kd_org2').val(),
            'tgl_sp2d': $('#tgl_sp2d').val(),
            'nosp2d': $('#no_sp2d').val(),
            'tgl_spm':$('#tgl_spm').val(),
            'nospm':pknospm,
            'kegiatan': JSON.stringify(array_keg),
            'jenis':'TU_NIHIL',
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
          array_sumdan = [];
          array_jumlah_sekarang = [];

          hasil_rekening = JSON.parse(data);
          updateJumlah(hasil_rekening);

          if(dari_keg == false){
            $('#btn_prev').removeAttr('disabled'); 
          }

          $('#btn_next').attr('disabled','disabled');
          $(".cover").hide();
          callback();
        },
        error: function(){
            message_ok('error', 'Proses ambil rekening gagal !');
            $(".cover").hide();
        }
    });
}

function ambilKegiatan(callback){
    array_keg = [];
    if ($('#frm_triwull').val()=='0') {
        $.alertable.alert('Triwulan belum dipilih');
    }else{
        if ($('#kd_org2').val()!='') {
            $.ajax({
                type : "POST",
                headers : { "X-CSRFToken": csrf_token },
                url : link_ambilKegiatan,
                data :{
                    'skpd':$('#kd_org2').val(),
                    'tgl_sp2d':$('#tgl_sp2d').val(),
                    'nosp2d':$('#no_sp2d').val(),
                    'nospm':$('#no_spm').val(),
                    'jenis':'TU_NIHIL',
                },
                dataType: 'html',
                beforeSend: function() {
                    $(".cover").show();
                },
                success: function(data){
                    pjg_keg = JSON.parse(data)['hasilnya'].length;
                    dari = 'sp2d';
                    render_tabel_kegiatan(JSON.parse(data)['hasilnya']);
                    callback();
                },
                error: function(){
                    message_ok('error', 'Proses Gagal !');
                    $(".cover").hide();
                }
            });
        } // end if kd_org != ''
    } //end if triwulan
}

function render_tabel_kegiatan(arraynya){
    $('#tabelnya').DataTable( {
        destroy:true,
        "bLengthChange":false, 
        scrollY:200,
        scrollX:true,
        fixedHeader:true,
        paging:false,
        "ordering": false,
        data: arraynya,
        'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});

            if (data[8]=='0') {
                $('td', row).eq(0).html('<input type="checkbox" class="chk_oto_keg" onclick="checkclick_sp2dup_keg(this, \''+index+'\', \'keg\')" id="check_'+index+'">\
                                        <input type="hidden" name="cek_keg" id="cek_keg_'+index+'" value="'+data[8]+'"/>\
                                        <input type="hidden" name="val_keg" id="val_keg_'+index+'" value="'+data[0]+'"/>');
                if (dari=='spm') {
                    if (array_keg.indexOf(data[0])<0) {
                        array_keg.push(data[0]);
                    } 
                    ambilRekening(function() {render_tabel_rekening();});
                }
            }else if(data[8]=='1'){
                $('td', row).eq(0).html('<input type="checkbox" class="chk_oto_keg" onclick="checkclick_sp2dup_keg(this, \''+index+'\', \'keg\')" checked = "checked" id="check_'+index+'">\
                                        <input type="hidden" name="cek_keg" id="cek_keg_'+index+'" value="'+data[8]+'"/>\
                                        <input type="hidden" name="val_keg" id="val_keg_'+index+'" value="'+data[0]+'"/>');
                
                if (dari == 'sp2d') {
                    if (array_keg.indexOf(data[0])<0) {
                        array_keg.push(data[0]);
                    }  
                }
            }

            $('td', row).eq(1).text(data[0]);
            $('td', row).eq(2).text(data[1]);

            $('td', row).eq(3).text(data[2] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[2]));
            $('td', row).eq(4).text(data[3] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[3]));
            $('td', row).eq(5).text(data[4] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[4]));
            $('td', row).eq(6).text(data[5] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[5]));
            $('td', row).eq(7).text(data[6] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[6]));
            $('td', row).eq(8).text(data[7] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[7]));

            for (var i = 3; i <= 8; i++) {
                $('td', row).eq(i).css({ 'text-align': 'right'});
            }

            
            $('td', row).eq(0).css({ 'text-align': 'center'});
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
            for (var i = 3; i <= 8; i++) {
                total = api
                    .column( i-1 )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
                $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
            }
        }
    });
    $(".cover").hide();
    var_nosp2d = '';
    var_nospm = '';
    if (array_keg.length>0) {
        dari_keg = true;
        $('#btn_next').removeAttr('disabled');
        // $('#btn_next').trigger('click');
        // $('#btn_prev').attr('disabled','disabled');
        // if (!isSimpan) {
        //     $('#btn_next').trigger('click');
        // }
    }else{
        $('#btn_next').attr('disabled','disabled');
    }
}

function ambilsp2d(){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambilsp2d,
        data :{
            'skpd':$('#kd_org2').val(),
            'nosp2d':$('#no_sp2d').val(),
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
            if (JSON.parse(data)['hasilnya'].length!=0) {
                hasilnya = JSON.parse(data)['hasilnya'][0];
                pknospm = '';
                isSimpan = false;

                var_nosp2d = hasilnya['nosp2d'];
                var_nospm = hasilnya['nospm'];
                
                $('#tgl_sp2d').val(getTglINDO3(hasilnya['tanggal'])); 
                $('#no_spm').val(hasilnya['nospm']); 
                $('#tgl_spm').val(getTglINDO3(hasilnya['tglspm']));
                $('#status_keperluan').val('TU NIHIL pada Dinas '+$('#kd_org2_urai').val()+''+DateNowInd()+', sesuai dengan bukti terlampir.'); 
                $('#bank_asal').val(hasilnya['bankasal']);
                $('#norek_bankasal').val(hasilnya['norekbankasal']);
                $('#bendahara').val(hasilnya['namayangberhak']);
                $('#norek_bendahara').val(hasilnya['norekbank']);
                $('#bank_bendahara').val(hasilnya['bank']);
                $('#npwp_bendahara').val(hasilnya['npwp']);
                $('#jns_anggaran').val(hasilnya['perubahan']);
                $('#frm_triwull').val(hasilnya['triwulan']);
                jumlah_spm = hasilnya['jumlahspm'];
                jumlah_sp2d = hasilnya['jumlahsp2d'];

                if (hasilnya['locked']=='Y') {
                    $('#kunci_sp2d').text('(DISETUJUI)');
                    $('#btn_simpan').attr('disabled','disabled');
                    $('#btn_hapus').attr('disabled','disabled');
                    $.alertable.alert('SP2D Nomor '+hasilnya['nosp2d']+' telah di ACC oleh pimpinan. Anda tidak diperkenankan mengedit dan menghapus SP2D tersebut!');
                }else{
                    $('#kunci_sp2d').text('(DRAFT)');
                    $('#btn_simpan').removeAttr('disabled');

                    if (akses!='BELANJA') {
                        $('#btn_hapus').removeAttr('disabled');
                    }else{
                        $('#btn_hapus').attr('disabled','disabled');
                    }
                }
            }
            ambilKegiatan(function() {
                if (array_keg.length>0) {
                    if (!isSimpan) {
                        $('#btn_next').trigger('click');
                    }
                }
            });    

            $(".cover").hide();
        },
        error: function(){
            message_ok('error', 'Data SP2D tidak ditemukan !');
            $(".cover").hide();
        }
    });
}

function ambilSPM(){
    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambilspm,
        data :{
            'skpd':$('#kd_org2').val(),
            'nospm':$('#no_spm').val(),
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
            hasilnya = JSON.parse(data)['hasilnya'][0];
            pknospm = hasilnya['nospm'];
            $('#no_spm').val(hasilnya['nospm']); 
            $('#tgl_spm').val(getTglINDO3(hasilnya['tanggal']));
            $('#status_keperluan').val('TU NIHIL pada Dinas '+$('#kd_org2_urai').val()+''+DateNowInd()+', sesuai dengan bukti terlampir.'); 
            $('#bendahara').val(hasilnya['namayangberhak']);
            $('#norek_bendahara').val(hasilnya['norekbank']);
            $('#bank_bendahara').val(hasilnya['bank']);
            $('#npwp_bendahara').val(hasilnya['npwp']);
            $('#jns_anggaran').val(hasilnya['perubahan']);
            $('#frm_triwull').val(hasilnya['triwulan']);
            ambilKegiatan_spm();
            $(".cover").hide();
        },
        error: function(){
            message_ok('error', 'Proses Gagal !');
            $(".cover").hide();
        }
    });
}

function ambilKegiatan_spm(){
    if ($('#frm_triwull').val()=='0') {
        $.alertable.alert('Triwulan belum dipilih');
    }else{
        if ($('#kd_org2').val()!='') {
            $.ajax({
                type : "POST",
                headers : { "X-CSRFToken": csrf_token },
                url : link_ambilKegiatan_spm,
                data :{
                    'skpd':$('#kd_org2').val(),
                    'tgl_sp2d':$('#tgl_sp2d').val(),
                    'tgl_spm':$('#tgl_spm').val(),
                    'nospm':$('#no_spm').val(),
                    'nosp2d':$('#no_sp2d').val(),
                    'jenis':'TU_NIHIL',
                },
                dataType: 'html',
                beforeSend: function() {
                    $(".cover").show();
                },
                success: function(data){
                    pjg_keg = JSON.parse(data)['hasilnya'].length;
                    dari = 'spm';
                    render_tabel_kegiatan(JSON.parse(data)['hasilnya']);
                },
                error: function(){
                    message_ok('error', 'Proses Gagal !');
                    $(".cover").hide();
                }
            });
        } // end if kd_org != ''
    } //end if triwulan
}

function cek_uncek_all_sp2dtunihil(e, chkclass, page){
    $('.'+chkclass+'_'+page).each(function(){ 
        this.checked = e.checked; 
    });

    array_keg=[];

    if(e.checked){
        $('#frm_sp2dtunihil input[name=cek_'+page+']').val('1');
        for (var i = 0; i < pjg_keg; i++) {
            if ($("#val_"+page+"_"+i+"").val()!=undefined) {
                array_keg.push($("#val_"+page+"_"+i+"").val());     
            }
        }
        
    } else {
        $('#frm_sp2dtunihil input[name=cek_'+page+']').val('0');
        for (var i = 0; i < pjg_keg; i++) {
            array_keg.splice(array_keg.indexOf($("#val_"+page+"_"+i+"").val()), 1);
        }
    }

    if (array_keg.length>0) {
        $('#btn_next').removeAttr('disabled');
    }else{
        $('#btn_next').attr('disabled','disabled');
    }
    // console.log(array_keg);
    // console.log(array_rinci);
}

function checkclick_sp2dup_keg(e, urutan, tabel){
    if(e.checked){
        $("#cek_"+tabel+"_"+urutan+"").val('1');
        if (tabel=='keg') {
            array_keg.push($("#val_"+tabel+"_"+urutan+"").val()); 
        }else if (tabel=='rinci'){
            array_rinci.push($("#val_"+tabel+"_"+urutan+"").val());
            array_sumdan.push($("#val_sumdan_"+urutan+"").val());
            array_jumlah_sekarang.push($("#val_"+tabel+"_"+urutan+"").val()+'^'+parseFloat(toAngkaDec($("#sekarang_"+urutan+"").val()))+'^'+parseFloat(toAngkaDec($("#anggaran_"+urutan+"").val()))+'^'+$("#otorisasi_"+urutan+"").val());
        }
    } else {
        $("#cek_"+tabel+"_"+urutan+"").val('0');
        if (tabel=='keg') {
            array_keg.splice(array_keg.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1); 
        }else if (tabel=='rinci'){
            array_rinci.splice(array_rinci.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1);
            array_sumdan.splice(array_sumdan.indexOf($("#val_sumdan_"+urutan+"").val()), 1);
            array_jumlah_sekarang.splice(array_jumlah_sekarang.indexOf($("#val_"+tabel+"_"+urutan+"").val()+'^'+parseFloat(toAngkaDec($("#sekarang_"+urutan+"").val()))+'^'+parseFloat(toAngkaDec($("#anggaran_"+urutan+"").val()))+'^'+$("#otorisasi_"+urutan+"").val()), 1);
        }
    }
    if (array_keg.length>0) {
        $('#btn_next').removeAttr('disabled');
    }else{
        $('#btn_next').attr('disabled','disabled');
    }
    // console.log(array_keg);
    // console.log(array_rinci);
    // console.log(array_sumdan);
    // console.log(array_jumlah_sekarang);
}

$('#btn_next').click(function(){
    $('.judul-tabel').text('Daftar Belanja');
    array_rinci = [];
    ambilRekening(function() {render_tabel_rekening();});
});

$('#btn_prev').click(function(){
    $('.judul-tabel').text('Daftar Kegiatan');
    array_keg = [];
    ambilKegiatan(function() {});
    // if(dari_keg==false){
    //     $('.judul-tabel').text('Daftar Kegiatan');
    //     array_keg = [];
    //     ambilKegiatan();
    // }
});

function render_tabel_rekening(){
    pjg_row = hasil_rekening['rekening'].length;
    $('#tabelnya').DataTable( {
        destroy:true,
        "bLengthChange":false, 
        scrollY:200,
        scrollX:true,
        fixedHeader:true,
        paging:false,
        "ordering": false,
        data: hasil_rekening['rekening'],
        'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            //Inisialisasi Nilai
            anggaran = data[3] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[3]);
            batas = data[4] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[4]);
            lalu = data[5] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[5]);
            sekarang = data[6] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[6]);
            jumlah = data[7] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[7]);
            sisa = data[8] == 'None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[8]);

            if (data[0]=='0') {
                if (data[1].split('-').length>1) {
                    $('td', row).eq(0).html('<input type="checkbox" class="chk_oto_keg" onclick="checkclick_sp2dup_keg(this, \''+index+'\', \'rinci\')" id="check_'+index+'">\
                                        <input type="hidden" name="cek_rinci" id="cek_rinci_'+index+'" value="'+data[0]+'"/>\
                                        <input type="hidden" name="val_rinci" id="val_rinci_'+index+'" value="'+data[1]+'"/>\
                                        <input type="hidden" name="val_sumdan" id="val_sumdan_'+index+'" value="'+data[9]+'"/>');
                }else{
                    $('td', row).eq(0).html('');
                }
            }else if(data[0]=='1'){
                $('td', row).eq(0).html('<input type="checkbox" class="chk_oto_keg" onclick="checkclick_sp2dup_keg(this, \''+index+'\', \'rinci\')" checked = "checked" id="check_'+index+'">\
                                        <input type="hidden" name="cek_rinci" id="cek_rinci_'+index+'" value="'+data[0]+'"/>\
                                        <input type="hidden" name="val_rinci" id="val_rinci_'+index+'" value="'+data[1]+'"/>\
                                        <input type="hidden" name="val_sumdan" id="val_sumdan_'+index+'" value="'+data[9]+'"/>');
                if (array_rinci.indexOf(data[1])<0) {
                    array_rinci.push(data[1]);
                }

                // if (array_sumdan.indexOf(data[9])<0) {
                //     array_sumdan.push(data[9]);
                // }
                array_sumdan.push(data[9]);
                array_jumlah_sekarang.push(data[1]+'^'+parseFloat(data[6])+'^'+parseFloat(data[3])+'^'+data[10]);
            }

            $('td', row).eq(3).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="anggaran" id="anggaran_'+index+'" style="text-align:right;" value="'+anggaran+'">');
            $('td', row).eq(4).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="batas" id="batas_'+index+'" style="text-align:right;" value="'+batas+'">');
            $('td', row).eq(5).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="lalu" id="lalu_'+index+'" style="text-align:right;" value="'+lalu+'">');
            if (data[1].split('-').length>1) {
                $('td', row).eq(6).html('<input type="text" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" onblur="action_sp2dsekarang(this,'+index+', '+pjg_row+')" name="sekarang" id="sekarang_'+index+'" style="text-align:right;" value="'+sekarang+'">');
            }else{
                $('td', row).eq(6).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="sekarang" id="sekarang_'+index+'" style="text-align:right;" value="'+sekarang+'">');
            }
            
            $('td', row).eq(7).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="jumlah" id="jumlah_'+index+'" style="text-align:right;" value="'+jumlah+'">');
            $('td', row).eq(8).html('<input type="text" readonly = "true" disabled="disabled" class="input-dlm-tabel paste" onkeydown="isNumberKey(event)" name="sisa" id="sisa_'+index+'" style="text-align:right;" value="'+sisa+'">\
                                    <input type="hidden" readonly = "true" disabled="disabled" class="input-dlm-tabel" name="otorisasi" id="otorisasi_'+index+'" value="'+data[10]+'">');
            
            for (var i = 3; i <= 8; i++) {
                $('td', row).eq(i).css({ 'text-align': 'right'});
            }

            
            $('td', row).eq(0).css({ 'text-align': 'center'});
        },
        footerCallback: function ( row, data, start, end, display ) {
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
            for (var i = 3; i <= 8; i++) {
             total = api
                    .column( i )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );
                $( api.column( i ).footer() ).html('<span id="footer_'+i+'">'+toRp_WithDesimal(total.toString())+'</span>');
            }
        }
    });
}

function fungsi_modal(ini, asal_modal){
    var row     = $(ini).closest('tr'); 
      
    if (asal_modal=='sp2d_tunihil') {
        $.each(row.find('td:nth-child(1)'), function(){ var_nosp2d    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_tgl_sp2d    = $(this).text();});
        $.each(row.find('td:nth-child(3)'), function(){ var_organisasi    = $(this).text();});
        $.each(row.find('td:nth-child(4)'), function(){ var_keperluan    = $(this).text();});
        $.each(row.find('td:nth-child(5)'), function(){ var_nospm    = $(this).text();});
        $.each(row.find('td:nth-child(6)'), function(){ var_jumlah    = $(this).text();});

        $('#no_sp2d').val(var_nosp2d);
        $('#where_nosp2d').val(var_nosp2d);
        $('#kd_org').val(var_organisasi.split('-')[0]+' - '+var_organisasi.split('-')[1]);
        $('#kd_org2').val(var_organisasi.split('-')[0]);
        $('#kd_org2_urai').val(var_organisasi.split('-')[1]);

        ambilsp2d();
        console.log('cekcok')
    }else if(asal_modal == 'spm_sp2d'){
        $.each(row.find('td:nth-child(1)'), function(){ var_nospm    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_tgl_spm    = $(this).text();});
        $.each(row.find('td:nth-child(3)'), function(){ var_organisasi    = $(this).text();});
        $.each(row.find('td:nth-child(4)'), function(){ var_keperluan    = $(this).text();});

        $('#no_spm').val(var_nospm);
        $('#kd_org').val(var_organisasi.split('-')[0]+' - '+var_organisasi.split('-')[1]);
        $('#kd_org2').val(var_organisasi.split('-')[0]);
        $('#kd_org2_urai').val(var_organisasi.split('-')[1]);

        ambilSPM();
    }else if (asal_modal=='lht_bdhr') {
        $.each(row.find('td:nth-child(1)'), function(){ var_norekbank    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_bank    = $(this).text();});
        $.each(row.find('td:nth-child(3)'), function(){ var_npwp    = $(this).text();});
        $.each(row.find('td:nth-child(4)'), function(){ var_namayangberhak    = $(this).text();});

        $('#bendahara').val(var_namayangberhak);
        $('#norek_bendahara').val(var_norekbank);
        $('#bank_bendahara').val(var_bank);
        $('#npwp_bendahara').val(var_npwp);
    }
}

function simpan_tunihil() {
    count = 0;
    rekening = '';
    if($('#kd_org2').val()==''){
        message_ok('error', 'Kode Organisasi tidak boleh kosong !');
    }else if($('#no_sp2d').val()==''){
        message_ok('error', 'Nomor SP2D tidak boleh kosong !');
    }else if($('#no_spm').val()==''){
        message_ok('error', 'Nomor SPM tidak boleh kosong !');
    }else if($('#status_keperluan').val()==''){
        message_ok('error', 'Status Keperluan tidak boleh kosong !');
    }
    // else if($('#bendahara').val()==''){
    //     message_ok('error', 'Bendahara tidak boleh kosong !');
    // }else if($('#norek_bendahara').val()==''){
    //     message_ok('error', 'Nomor Rekening Bendahara tidak boleh kosong !');
    // }
    else if(cekTanggal($('#tgl_spm').val(), $('#tgl_sp2d').val())==false){
        message_ok('error', 'Tanggal SP2D tidak boleh kurang dari tanggal SPM !');
    }else{
        if (array_jumlah_sekarang.length!=0) {
            for (var i = 0; i < array_jumlah_sekarang.length; i++) {
                // console.log(array_jumlah_sekarang[i].split('^')[3]);
                if (array_jumlah_sekarang[i].split('^')[3]=='0') {
                    rekening = rekening + ', ' +array_jumlah_sekarang[i].split('^')[0];
                    count= count+1;
                }
            }
            if (count!=0) {
                $.alertable.confirm('Rekening '+ rekening +' belum diotorisasi Bidang Anggaran! Jika ingin melanjutkan data rekening tersebut tidak tersimpan. ').then(function() {
                    simpan_oce_tunihil()
                }, function() {
                    message_ok('error', 'Simpan data dibatalkan.');
                });
            }else{
                simpan_oce_tunihil()
            }
        }else{
            $.alertable.alert('Tidak ada rekening yang dipilih!');
        }
    }
}

function simpan_oce_tunihil() {
    array_jumlah_sekarang_fix = [];
    for (var i = 0; i < array_jumlah_sekarang.length; i++) {
        
        if (array_jumlah_sekarang[i].split('^')[3]!='0') {
            array_jumlah_sekarang_fix.push(array_jumlah_sekarang[i]);
        }
    }

    $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_simpan_tunihil,
        data :{
            'skpd': $('#kd_org2').val(),
            'tgl_sp2d': $('#tgl_sp2d').val(),
            'nosp2d': $('#no_sp2d').val(),
            'where_nosp2d':$('#where_nosp2d').val(),
            'nospm': $('#no_spm').val(),
            'kegiatan': JSON.stringify(array_keg),
            'rinci': JSON.stringify(array_rinci),
            'isSimpan':isSimpan,

            'TGLSPM':$('#tgl_spm').val(),
            'jumlahspm':jumlah_spm,

            'pemegangkas':$('#bendahara').val(),
            'sumberdana':JSON.stringify(array_sumdan),
            'namayangberhak':$('#bendahara').val(),
            'triwulan':$('#frm_triwull').val(),
            'informasi':$('#status_keperluan').val(),
            'deskripsispm':$('#status_keperluan').val(),
            'perubahan':$('#jns_anggaran').val(),
            'statuskeperluan':$('#status_keperluan').val(),
            'jumlahsp2d':toAngkaDec($('#jml_sp2d').text()),
            'bankasal':$('#bank_asal').val(),
            'norekbank':$('#norek_bendahara').val(),
            'norekbankasal':$('#norek_bankasal').val(),
            'bank':$('#bank_bendahara').val(),
            'NPWP':$('#npwp_bendahara').val(),
            'jumlah':JSON.stringify(array_jumlah_sekarang_fix),
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
            ambilsp2d();              
            $(".cover").hide();
            message_ok('success', data);
        },
        error: function(){
            $(".cover").hide();
            message_ok('error', 'Simpan gagal !');
        }
    });
}

function hapus_tunihil() {
    if ($('#kd_org2').val()=='') {
        $.alertable.alert('Organisasi belum dipilih!');
    }else if($('#no_sp2d').val()==''){
        $.alertable.alert('Nomor SP2D tidak boleh kosong!');
    }else{
        $.alertable.confirm('Apakah anda yakin ingin menghapus data SP2D '+$('#no_sp2d').val()+' ?').then(function() {
             $.ajax({
                type : "POST",
                headers : { "X-CSRFToken": csrf_token },
                url : link_hapus_tunihil,
                data :{
                    'skpd': $('#kd_org2').val(),
                    'nosp2d': $('#no_sp2d').val(),
                },
                dataType: 'html',
                beforeSend: function() {
                    $(".cover").show();
                },
                success: function(data){
                  message_ok('success', data);
                  location.reload();
                  $(".cover").hide();
                },
                error: function(){
                    message_ok('error', 'Hapus data gagal.');
                    $(".cover").hide();
                }
            });   
        }, function() {
            message_ok('error', 'Hapus data dibatalkan.');
        });
    }
}