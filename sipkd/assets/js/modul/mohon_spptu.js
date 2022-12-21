// JavaScript untuk Permohonan SPP TU
// Created By. JOEL 18 OCT 2022 - GI
// ============================================================================================

var NoSPP     = "";
var isSimpan  = true;
var isTambah  = true;
var SumNoSPP  = "";
var cekSukses = false;
var check_sumberdana = [];
var isMdl_Potongan  = 'false';

function loadSPPTU_mohon(e){
  var skpd = $("#organisasi").val();  

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'spp');
  }
  
}

function SaveSPPTU_mohon(url){    
	var skpd  = $('#organisasi').val();
	var noSPP = $('#no_spp').val();
	var jenis = $('#jenis').val();  

	CekNoSPP(url,skpd,noSPP);
	if(isSimpan==true){    
		if(NoSPP != noSPP){      
			if(SumNoSPP > 0){
				$.alertable.alert("Nomor SPP : "+noSPP+", sudah digunakan.");
				return false;
			}
		}
	}   
  
	if($('#organisasi').val() == 0){
		$.alertable.alert('Organisasi Belum dipilih');
	} else if($('#no_spp').val() == ""){
		$.alertable.alert('Nomor SPP belum diisi');
	} else if($('#tanggal_spp').val() == ""){
		$.alertable.alert('Tanggal SPP belum diisi');
	} else if($('#bendahara').val() == ""){
		$.alertable.alert('Nama Bendahara belum diisi');
	} else if($('#norek_bendahara').val() == ""){
		$.alertable.alert('Nomor Rekening Bank belum diisi');
	} else if($('#nama_rekening_bank').val() == ""){
		$.alertable.alert('Nama Pemilik Rekening belum diisi');
	} else if($('#nama_bank').val() == ""){
		$.alertable.alert('Nama Bank belum diisi');
	} else if($('#npwp_bendahara').val() == ""){
		$.alertable.alert('NPWP belum diisi');
	} else if($('#status_keperluan').val() == ""){
		$.alertable.alert('Status Keperluan Belum diisi');
	} else {      
		if(jenis=='tu'){        
			var val = []; 
			var otorisasi = []; 
			var urai = [];       
			var rekening = ''; 
			var count = 0;   

			$(':checkbox:checked').each(function(i){
				val[i] = $(this).val().split('|');             
				otorisasi[i] = val[i][2];
				urai[i] = val[i][3];      

				if(otorisasi[i]==0){
					rekening = rekening +', '+ urai[i];
					count = count+1;              
				}        
			});       

			rekening = rekening.substr(1,rekening.length);           

			if (count != 0){
				$.alertable.confirm("Rekening "+rekening+". Belum di Otorisasi Bidang Anggaran! Harap Hubungi Bidang Anggaran.").then(function() {          
					cekBatas_SPP(); 
				});
			} else {
				var chekOto = $(".afektasichk").is(":checked");
				if(chekOto==false){
					$.alertable.confirm("Rekening Belum ada yang dipilih");
				} else {
					cekBatas_SPP();
				}      
			} 
		}
  	}
}

function deleteSPP_TUP(){
    var skpd  = $('#organisasi').val();
    var nospp = $('#no_spp').val();
    var url = $('#deletespptu_p').val();
    var jenis = $('#jenis').val().toUpperCase();
    var kdunit = $('#kode_unit').val();

    if(skpd == 0){
      $.alertable.alert('Organisasi Belum dipilih');
    }else{
      $.alertable.confirm("Anda yakin akan menghapus data Permohonan SPP-"+jenis+" dengan Nomor : "+nospp+" ?").then(function() {            
          $.ajax({
                  type: "POST",
                  headers: { "X-CSRFToken": csrf_token },
                  url: url,
                  data: {         
                    'nospp':nospp,
                    'org':skpd,
                    'kdunit':kdunit                      
                  },
                  dataType: 'html',
                  success: function (data) {                   
                      message_ok("success",data);
                      if(jenis=='UP'){
                        clearFormSPP_UP(skpd);
                      }else{
                        clearFormSPP_PPKD(skpd);
                      }                                                                  
                  }
              }); 
          }, function() {
              message_ok('error', 'Anda telah membatalkan menghapus data Permohonan SPP-'+jenis+'');          
      });
    }
}

function LoadDataSPP_TU_P(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("persetujuanSPP");
  var ppkd = 0; 

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spp').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("persetujuanSPP");
  } 
}