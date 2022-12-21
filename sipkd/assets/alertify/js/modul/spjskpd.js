/*
JavaScript untuk modul SPJSKPD
created by Kurnianto Tri Nugoroho @GI 2019 
SIPKD Application

===============================================================================================================================
*/
var organisasi = '';

function OnChangeJurnal(){
  array_index = [];
	organisasi = $('#organisasi').val();
  if(organisasi==''){
		$.alertable.alert('Organisasi Belum dipilih');
		$("#jenis_jurnal").val(0);
		// $('#bln_jurnal').val(1);
	}else{
    LoadDataJurnal(organisasi);
	  if ($('#jenis_jurnal').val() == '4') {
      $('#btn_tambah_akrual').attr('disabled','disabled');
    }else{
      $('#btn_tambah_akrual').removeAttr('disabled');
    }
  }	
}

function tambahJurnal(e){
  isSimpancuy = true;

  organisasi = $('#organisasi').val();
  if (organisasi=='') {
    $.alertable.alert('Organisasi Belum dipilih');
  }else{
    showModal($('#btn_tambah_akrual')['0'],'modal_tambah_akrual');
  }
}

function editJurnal(e){
  organisasi = $('#organisasi').val();
  if (organisasi=='') {
    $.alertable.alert('Organisasi Belum dipilih');
  }else{
    isSimpancuy = false;
    noref = e;
    showModal($('#btn_tambah_akrual')['0'],'modal_tambah_akrual');
  }
}

function LoadDataJurnal(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("akrualSKPD");
  var ppkd = 0; 
  var jenisjurnal = $("#jenis_jurnal").val();
  var bulanjurnal = $('#bln_jurnal').val();

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd,
        jenis:jenisjurnal,
        bulan:bulanjurnal
      },
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_jurnal_akrual').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("akrualSKPD");
  } 
}

function postingJurnal(e){  
  var frm = $('#draftJurnal');
  var url = frm.attr('action');
  var skpd = $("#organisasi").val();
  var chekPostingJurnal = $(".checkbox_posting").is(":checked");  

   
  if(array_index.length == 0){
    $.alertable.alert("Silahkan Pilih Data yang Akan di Posting!");
        return false;
  }else{
  	$.alertable.confirm('Anda Yakin ingin Posting Ke Buku Besar?').then(function () {
	    $.ajax({
	      type: "POST",
	      headers: { "X-CSRFToken": csrf_token },
	      url: url,
	      data: {'array_index':JSON.stringify(array_index),'organisasi':$('#organisasi').val(),'act':'posting',},
	      async: false,
	      dataType: "html",
	      timeout: 10000,
	      beforeSend: function() {
	        $(".cover").show();
	      },
	      success: function(response){ 
	        $( "#organisasi" ).trigger( "change" );
	        message_ok('success', response);       
	        $(".cover").hide();
	      }
	    });
    },function() { 
        message_ok('error', 'Data batal di Posting ke Buku Besar !');
    }); 
  }
}

function unpostingJurnal(e){  
  var frm = $('#draftJurnal');
  var url = $('#url_unposting').val();
  var skpd = $("#organisasi").val();
  var chekPostingJurnal = $(".checkbox_posting").is(":checked");  

   
  if(array_index.length == 0){
    $.alertable.alert("Silahkan Pilih Data yang Akan di Un Posting!");
        return false;
  }else{
  	$.alertable.confirm('Anda Yakin ingin Un Posting Data ini?').then(function () {
	    $.ajax({
	      type: "POST",
	      headers: { "X-CSRFToken": csrf_token },
	      url: url,
	      data: {'array_index':JSON.stringify(array_index),'organisasi':$('#organisasi').val(),'act':'unposting',},
	      async: false,
	      dataType: "html",
	      timeout: 10000,
	      beforeSend: function() {
	        $(".cover").show();
	      },
	      success: function(response){ 
	        $( "#organisasi" ).trigger( "change" );
	        message_ok('success', response);       
	        $(".cover").hide();
	      }
	    }); 
    },function() { 
        message_ok('error', 'Data batal di Un Posting !');
    });
  }
}

function deleteJurnal(e){  
  var frm = $('#draftJurnal');
  var url = $('#url_deljurnal').val();
  var skpd = $("#organisasi").val();
  var chekJurnal = $(".checkbox_posting").is(":checked");  

  if(array_index.length == 0){
    $.alertable.alert("Silahkan Pilih Data yang Akan di Hapus!");
        return false;
  }else{
  	$.alertable.confirm('Anda Yakin ingin Menghapus Jurnal?').then(function () {
	    $.ajax({
	      type: "POST",
	      headers: { "X-CSRFToken": csrf_token },
	      url: url,
	      data: {'array_index':JSON.stringify(array_index),'organisasi':$('#organisasi').val(),},
	      async: false,
	      dataType: "html",
	      timeout: 10000,
	      beforeSend: function() {
	        $(".cover").show();
	      },
	      success: function(response){ 
	        $( "#organisasi" ).trigger( "change" );
	        message_ok('success', response);       
	        $(".cover").hide();
	      }
	    }); 
    },function() { 
        message_ok('error', 'Hapus data jurnal dibatalkan!');
    });
  }
}

