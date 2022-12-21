var isSimpan = true;
var nosp2d_asli = '';
var isPemberitahuan = false;

$(document).ready(function () {
	$('#tgl_sp2d').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    });

    $('#tgl_spm').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    });

    $('#btn_cetak').attr('alt', link_render_cetak_sp2dup);
    clearForm();
});

$('#kd_org2').change(function(){
	cekdataUP();
});

$('#cari_data_organisasi').click(function(){
  isSimpan=true;
});

$('#btn_tambah_sp2d').click(function(){
	clearForm();
	isSimpan = true;
});
$('#btn_lihat_sp2d').click(function(){
	render_modal('Lihat SP2D', 'sp2d_up', []);
});

$('#cari_bendahara').click(function(){
	render_modal('Pilih Rekening', 'lht_bdhr', []);
});

$('#btn_hapus').click(function(){
  $.alertable.confirm('Apakah anda yakin inginmenghapus SP2D dengan nomor '+$('#no_sp2d').val()+' ?').then(function() {
      hapus_sp2d();
  }, function() {
      message_ok('error', 'Hapus data dibatalkan');
  });
});

$('#norek_bankasal').change(function(){
  ambilbankData();
});

$('#btn_cetak').click(function(){
	var bool = cekTanggal($('#tgl_spm').val(), $('#tgl_sp2d').val())
	if ($('#no_sp2d').val()=='') {
	    message_ok('error', 'NoSP2D tidak boleh kosong !');
	    $('#no_sp2d').focus();
	  }else if($('#no_spm').val()==''){
	    message_ok('error', 'NoSPM tidak boleh kosong !');
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
	    showModal(this, 'cetak_sp2d_up_gu_tu_gunihil');
	  }	
});

function cekdataUP(){
  if (isSimpan) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_cekdataUP,
        data: {'kd_org':$('#kd_org2').val(),},
        dataType: 'html',
        success: function(data){
            hasil = JSON.parse(data)['hasil'][0]['jumlah'];
            if(hasil==0){
              // isSimpan = true;
              cekSKUP();
            }else{
              // isSimpan = false;
              ambilUP('new','',$('#kd_org2').val());
              $.alertable.alert("SP2D sudah dibuat\n UP hanya sekali dalam satu tahun");                        
            }
        }
    });
  }	
}

function cekSKUP(){
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_cekdataSKUP,
      data: {'kd_org':$('#kd_org2').val(),},
      dataType: 'html',
      success: function(data){
          // clearForm();
      	  hasil = JSON.parse(data)['hasil'][0];
      	  // { tahun: "2018", kodeurusan: 1, kodesuburusan: 2, kodeorganisasi: "01  ", noskup: "DDDDD", tanggal: "2018-01-07T00:00:00", jumlah_skup: "5555555.00" }
          if (JSON.parse(data)['hasil'].length>0) {
            $('#jumlah_sp2d').val(toRp_WithDecimal(hasil['jumlah_skup']));
            $('#jml_sp2d').text('Rp. '+toRp_WithDecimal(hasil['jumlah_skup']));
            $('#sp2d_terbilang').text(terbilang(hasil['jumlah_skup']));
      	  }
          $('#btn_simpan').removeAttr('disabled');
      }
  });	
}

function ambilUP(ket,nosp2d, kd_org){
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_ambilUP,
      data: {'kd_org':kd_org,'ket':ket, 'nosp2d':nosp2d},
      dataType: 'html',
      success: function(data){
          // clearForm()
      	  hasil = JSON.parse(data)['hasil'][0];
          
      	  if (hasil['locked']=='T') {
            $('#no_sp2d').val(hasil['nosp2d']);
            nosp2d_asli = hasil['nosp2d'];
            $('#kunci_sp2d').html('(DRAFT)');
            $('#btn_simpan').removeAttr('disabled');
            if (akses!='BELANJA') {
                $('#btn_hapus').removeAttr('disabled');
            }else{
                $('#btn_hapus').attr('disabled','disabled');
            }

            if (isPemberitahuan) {
              $.alertable.alert('SP2D sudah pernah dibuat, anda hanya diperkenankan untuk merubah');
            }
      	  }else{

      	  	$('#no_sp2d').val(hasil['nosp2d']);
      	  	nosp2d_asli = hasil['nosp2d'];
            $('#kunci_sp2d').html('(DISETUJUI)');
      	  	$('#btn_simpan').attr('disabled','disabled');
      	  	$('#btn_hapus').attr('disabled','disabled');
            $.alertable.alert('SP2D Nomor: '+$('#no_sp2d').val()+' telah di ACC oleh pimpinan. Anda tidak diperkenanlkan mengedit dan menghapus SP2D tersebut !');
      	  	// if (cekReport==true) {
      	  	// 	tampilkanFormCetak();
      	  	// }else{
      	  	// 	$.alertable.alert('SP2D Nomor: '+$('#no_sp2d').val()+' telah di ACC oleh pimpinan. Anda tidak diperkenanlkan mengedit dan menghapus SP2D tersebut !');
      	  	// }
      	  }

          $('#tgl_sp2d').val(getTglINDO3(hasil['tanggal_draft']));
          $('#jumlah_sp2d').val(toRp_WithDecimal(hasil['jumlahsp2d'])); 
          $('#jml_sp2d').text('Rp. '+$('#jumlah_sp2d').val());
          $('#sp2d_terbilang').text(terbilang(hasil['jumlahsp2d']));
          $('#no_spm').val(hasil['nospm']);
          $('#status_keperluan').val(hasil['statuskeperluan']);
          
          var rek_bank = hasil['sumberdana']+'|'+hasil['norekbankasal']+'|'+hasil['bankasal']+'|'+hasil['kodesumberdana'];

          // $('#norek_bankasal').val(rek_bank);
          
          $('#bendahara').val(hasil['namayangberhak']);
          $('#norek_bendahara').val(hasil['norekbank']);
          $('#bank_bendahara').val(hasil['bank']);
          $('#npwp_bendahara').val(hasil['npwp']);
          $('#tgl_spm').val(getTglINDO3(hasil['tglspm']));
          isSimpan = false;
      },error: function(){
        $.alertable.alert('Data tidak ditemukan');
      }
  });
}

function fungsi_modal(ini, asal_modal){
	var var_nospd, var_skpd;
    var row     = $(ini).closest('tr'); 
    var tglnya = '';

    var $nospd  = row.find('td:nth-child(1)');
    var $tgl = row.find('td:nth-child(2)');
    var $skpd = row.find('td:nth-child(3)');

    $.each($nospd, function(){ var_nospd    = $(this).text();}); 
    $.each($tgl, function(){ tglnya  = $(this).text();}); 
    $.each($skpd, function(){ var_skpd  = $(this).text();}); 

    var var_skpd2 = var_skpd.split('.');
    
    $.get(is_skpkd_js(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2])).done(
	    function(){ 
	    	
	    }
	   );  
    if (asal_modal=='spm_sp2d') {
      $.each(row.find('td:nth-child(1)'), function(){ var_nospm    = $(this).text();});
      $.each(row.find('td:nth-child(3)'), function(){ var_kd_org    = $(this).text();});

      ambil_spm(var_nospm,var_kd_org);
    }else if(asal_modal=='sp2d_up'){
    	$.each(row.find('td:nth-child(1)'), function(){ var_nosp2d    = $(this).text();});
      	$.each(row.find('td:nth-child(5)'), function(){ var_nospm    = $(this).text();});
      	$.each(row.find('td:nth-child(3)'), function(){ var_kd_org    = $(this).text();});
      	ambilUP('not_new',var_nosp2d,var_kd_org.split('-')[0]);
      	$('#kd_org').val(var_kd_org.split('-')[0]+' - '+var_kd_org.split('-')[1]);
      	$('#kd_org2').val(var_kd_org.split('-')[0]);
      	$('#kd_org2_urai').val(var_kd_org.split('-')[1]);
        isPemberitahuan = false;
    }else if (asal_modal=='lht_bdhr') {
    	$.each(row.find('td:nth-child(1)'), function(){ var_norekbank    = $(this).text();});
      	$.each(row.find('td:nth-child(2)'), function(){ var_bank    = $(this).text();});
      	$.each(row.find('td:nth-child(3)'), function(){ var_npwp    = $(this).text();});
      	$.each(row.find('td:nth-child(4)'), function(){ var_bendahara    = $(this).text();});
    	$('#bendahara').val(var_bendahara);
    	$('#norek_bendahara').val(var_norekbank);
    	$('#bank_bendahara').val(var_bank);
    	$('#npwp_bendahara').val(var_npwp);
    }
}

function ambil_spm(no_spm, kd_org){
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_ambil_spm,
      data: {'kd_org':kd_org,'no_spm':no_spm,},
      dataType: 'html',
      success: function(data){
        hasil = JSON.parse(data)['hasil'][0];

        $('#jumlah_sp2d').val(toRp_WithDecimal(hasil['jumlahspm'])); 
        $('#jml_sp2d').text('Rp. '+$('#jumlah_sp2d').val());
        // $('#sp2d_terbilang').text(terbilang(hasil['jumlahsp2d']));
        $('#no_spm').val(hasil['nospm']);
        $('#status_keperluan').val(hasil['statuskeperluan']);
        $('#bank_asal').val('');
        
        $('#bendahara').val(hasil['namayangberhak']);
        $('#norek_bendahara').val(hasil['norekbank']);
        $('#bank_bendahara').val(hasil['bank']);
        $('#npwp_bendahara').val(hasil['npwp']);
        $('#tgl_spm').val(getTglINDO3(hasil['tanggal']));
        ambilbankData();
      }
  }); 
}

function clearForm(){
  isSimpan = true;
  isPemberitahuan = false;
  $('#no_sp2d').val('');
  $('#kunci_sp2d').text('(DRAFT)');
  $('#tgl_sp2d').val(tgl_sekarang);
  $('#jumlah_sp2d').val('0,00');
  $('#no_spm').val('');
  $('#tgl_spm').val(tgl_sekarang);
  $('#status_keperluan').val('');
  $('#bank_asal').val('');
  $('#norek_bankasal').val('DAU|900.01.10.06.00011-1 ( RUTIN )|BANK PAPUA CAB. NABIRE|1');
  $('#bendahara').val('');
  $('#norek_bendahara').val('');
  $('#bank_bendahara').val('');
  $('#npwp_bendahara').val('');
  $('#jml_sp2d').text('Rp. 0,00');
  $('#sp2d_terbilang').text('Nol Rupiah');
  ambilbankData();
}

$('#btn_lihat_spm').click(function(){
  if ($('#kd_org2').val()=='') {
    $.alertable.alert('Kode organisasi tidak boleh kosong !');
  }else{
    render_modal('Lihat SPM','spm_sp2d',[$('#kd_org2').val(),'UP']);
  }
});

$('#btn_simpan').click(function(){
  simpan_sp2d();
});

function simpan_sp2d(){
  var bool = cekTanggal($('#tgl_spm').val(), $('#tgl_sp2d').val())
  var no_spm = $('#no_spm').val();
  var kd_org = $('#kd_org2').val()

  if ($('#no_sp2d').val()=='') {
    message_ok('error', 'NoSP2D tidak boleh kosong !');
    $('#no_sp2d').focus();
  }else if($('#no_spm').val()==''){
    message_ok('error', 'NoSPM tidak boleh kosong !');
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
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_simpan_sp2d,
        data: {'kd_org':kd_org,
        		'no_spm':no_spm,
        		'isSimpan':isSimpan,
        		'nosp2d':$('#no_sp2d').val(),
				'tanggal':$('#tgl_sp2d').val(),
				'tanggal_draft':$('#tgl_sp2d').val(),
				'tglspm':$('#tgl_spm').val(),
				'jumlahspm':toAngkaDec($('#jumlah_sp2d').val()),
				'pemegangkas':$('#bendahara').val(),
				'namayangberhak':$('#bendahara').val(),
				'triwulan':'1',
				'sumberdana':'DAU',
				'lastupdate':'NOW',
				'informasi':$('#status_keperluan').val(),
				'deskripsispm':$('#status_keperluan').val(),
				'perubahan':'0',
				'statuskeperluan':$('#status_keperluan').val(),
				'jumlahsp2d':toAngkaDec($('#jumlah_sp2d').val()),
				'bankasal':$('#bank_asal').val(),
				'norekbank':$('#norek_bendahara').val(),
				'norekbankasal':$('#norek_bankasal').val(),
				'bank':$('#bank_bendahara').val(),
				'npwp':$('#npwp_bendahara').val(),
				'nosp2d_asli' : nosp2d_asli,},
        dataType: 'html',
        success: function(data){
          message_ok('success', data);
          if (data != 'Nomor SP2D sudah ada !') {
            ambilUP('new','',$('#kd_org2').val());
          }          
        },
        error: function(data){
          message_ok('error', 'Data gagal disimpan');
        }
    });
  }
}

function hapus_sp2d(){
  if ($('#no_sp2d').val()=='') {
    message_ok('error', 'NoSP2D tidak boleh kosong !');
    $('#no_sp2d').focus();
  }else if($('#kd_org').val()==''){
    message_ok('error', 'Kode organisasi tidak boleh kosong !');
    $('#kd_org').focus();
  }else{
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_hapus_sp2d,
        data: {'kd_org':$('#kd_org2').val(),'nosp2d':$('#no_sp2d').val(),},
        dataType: 'html',
        success: function(data){
          message_ok('success', 'Data berhasil dihapus !')
          cekdataUP();
          location.reload();
        }
    }); 
  }
   
}

function ambilbankData() {
  $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_ambilbankData,
        data: {'norek':$('#norek_bankasal').val(),},
        dataType: 'html',
        success: function(data){
          $('#bank_asal').val(JSON.parse(data)['hasil_bank'][0]['bank']);
          $('#bank_bendahara').val();
        },
        error: function(argument) {
          message_ok('error', 'Data bank tidak ditemukan!');
        }
    }); 
}