var var_id_pejabat = '';

$(document).ready(function () {
    $('#periode_tgl1').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    }, function (start, end, label) {
        // console.log(start.toISOString(), end.toISOString(), label);
    });

    $('#periode_tgl2').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    }, function (start, end, label) {
        // console.log(start.toISOString(), end.toISOString(), label);
    });

    $('#tanggal_cetak').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    }, function (start, end, label) {
        // console.log(start.toISOString(), end.toISOString(), label);
    });

    $('#col_pengguna').addClass('hilang');
    $('#col_kegiatan').addClass('hilang');
    $('#col_rekening').addClass('hilang');
    $('#col_jenis').addClass('hilang');
    $('#col_triwulan').addClass('hilang');
});

$('#cari_pejabat').click(function(){
    render_modal('Lihat Pejabat', 'pejabat_lap_spd',[]);
});
$('#cari_kegiatan').click(function(){
    if ($('#kd_org2').val()=='') {
        $.alertable.alert('Organisasi tidak boleh kosong !');
    }else{
      render_modal('Lihat Kegiatan', 'cari_kegiatan_rkpa',[$('#kd_org2').val()]);  
    }    
});

$('#cari_rekening').click(function(){
    if ($('#frm_kegiatan').val()=='') {
        $.alertable.alert('Kegiatan tidak boleh kosong !');
    }else{
      render_modal('Lihat Rekening', 'rekening_rkpa',[$('#kd_org2').val(),$('#frm_kegiatan').val()]);  
    } 
});


$('#jns_laporan').change(function(){

    if (this.value == 'Kartu Pengawas - Realisasi Anggaran') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Register SPD') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Kartu Kendali Anggaran') {
        $('#col_kegiatan').removeClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Realisasi SP2D') {
        $('#col_kegiatan').removeClass('hilang');
        $('#col_rekening').removeClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Kartu Kontrol SPD') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').removeClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Realisasi Per SKPD Per Rekening') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').removeClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').removeClass('hilang');
    }
    else if (this.value == 'Rekapitulasi Anggaran SKPD') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').addClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
    else if (this.value == 'Rekapitulasi Realisasi Anggaran Per Rekening') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').addClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').removeClass('hilang');
    }
    else if (this.value == 'Rekap Belanja PPKD') {
        $('#col_kegiatan').addClass('hilang');
        $('#col_rekening').addClass('hilang');
        $('#col_organisasi').addClass('hilang');
        $('#col_triwulan').addClass('hilang');
        $('#col_jenis').addClass('hilang');
    }
});

$('#btn_cetak').click(function(){
    var_select = $('#jns_laporan').val();

    if ($('#kd_org2').val()=='') {
        $.alertable.alert('Organisasi belum dipilih');
    }else{
        if (var_select=='Kartu Kendali Anggaran') {
            if ($('#frm_kegiatan').val()=='') {
                $.alertable.alert('Kegiatan belum dipilih');
            }else{
                cetak(var_select);
            }
        }else{
            cetak(var_select);
        }
        
    }    
});

function get_checked(e){
    if(e.checked){
        $('#is_skpkd').val('1');        
    } else {
        $('#is_skpkd').val('0'); 
    }
}

function cetak(jenis_laporan){
    // console.log($('#is_skpkd').val()==undefined?'0':$('#is_skpkd').val())
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_laporan_kpra,
        data: {'kd_org':$('#kd_org').val(),
               'jenis_laporan':jenis_laporan,
                'id_pejabat':var_id_pejabat,
                'nm_pejabat':$('#nama_bendahara').val(),
                'nip_pejabat':$('#nip_bendahara').val(),
                'pangkat_pejabat':$('#pangkat_bendahara').val(),
                'tgl_laporan':$('#tanggal_cetak').val(),
                'isppkd':$('#is_skpkd').val()==undefined?'0':$('#is_skpkd').val(),
                'kegiatan':$('#frm_kegiatan').val(),
                'rekening': $('#frm_rekening').val(),
                'triwulan':$('#cb_triwulan').val(),
                'periode1':$('#periode_tgl1').val(),
                'periode2':$('#periode_tgl2').val(),
                'jenis': $("input[name='optradio']:checked").val(),
              },
        dataType: 'html',
        success: function(data){
          ShowIframeReport(data, jenis_laporan+' '+Thn_log);
        }
    }); 
}

$('#kd_org2').change(function(){
    if (var_skpkd=='1') {
        $('#col_checkbox').html('<label id="cekbok_skpd">\
                                <input type="checkbox" id="is_skpkd" onclick="get_checked(this)" value="1" checked>&nbsp;SKPKD\
                            </label>');
    }else{
         $('#col_checkbox').html('');
    }
});

function fungsi_modal(ini, asal_modal){
    var row     = $(ini).closest('tr'); 
      
    if (asal_modal=='pejabat_lap_spd') {
        $.each(row.find('td:nth-child(1)'), function(){ var_id    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_nama    = $(this).text();});
        $.each(row.find('td:nth-child(3)'), function(){ var_nip    = $(this).text();});
        $.each(row.find('td:nth-child(4)'), function(){ var_pangkat    = $(this).text();});

        var_id_pejabat = var_id;
        $('#nama_bendahara').val(var_nama);
        $('#nip_bendahara').val(var_nip);
        $('#pangkat_bendahara').val(var_pangkat);
    }else if(asal_modal=='cari_kegiatan_rkpa'){
        $.each(row.find('td:nth-child(1)'), function(){ var_kdbidang    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_kdprogram    = $(this).text();});
        $.each(row.find('td:nth-child(3)'), function(){ var_kdkegiatan    = $(this).text();});
        $.each(row.find('td:nth-child(4)'), function(){ var_urai    = $(this).text();});

        $('#frm_kegiatan').val(var_kdbidang+'.'+var_kdprogram+'.'+var_kdkegiatan+' - '+var_urai);
    }else if(asal_modal=='rekening_rkpa'){
        $.each(row.find('td:nth-child(1)'), function(){ var_kode    = $(this).text();});
        $.each(row.find('td:nth-child(2)'), function(){ var_uraian_rekening    = $(this).text();});

        $('#frm_rekening').val(var_kode+'-'+var_uraian_rekening);
    }
}