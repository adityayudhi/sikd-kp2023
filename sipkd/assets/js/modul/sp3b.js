var isSimpan  = true;
var hslCKsp3b = "";

function CekNoSP3B(URL,skpd,nosp3b){ 
	if(nosp3b){
		$.ajax({
		    type: "POST",
		    headers: { "X-CSRFToken": csrf_token },
		    url: URL,
		    dataType: "json",
		    data: {skpd:skpd, nosp3b:nosp3b},
		    async: false,
		    success: function(msg){
		      	hslCKsp3b = msg['nosp3b'];
		    }
		});
	} else { $.alertable.alert("Nomor SP3B masih kosong !"); }
	return hslCKsp3b;
}

function clearForm_SP3B(e){
	$("#no_sp3b").attr('readonly',false);
	$('#kode_unit').val('');
	$('#kode_bidang').val('');
	$('#kode_program').val('');
	$('#kode_kegiatan').val('');
	$('#kode_subkegiatan').val('');
	$('#urai_kegiatan').val('');
	$('#nomor_dpa').val('');
	$('#no_sp3b').val('');
	$('#no_sp3b_lama').val('');
	$('#tanggal_sp3b').val(DateNowInd());
	$('#status_keperluan').val('');
	$('#saldo_awal').val('0,00');

	$('#kd_akun').val('');
	$('#kd_kelompok').val('');
	$('#kd_jenis').val('');
	$('#kd_objek').val('');
	$('#kd_rcobjek').val('');
	$('#kd_subrcobjek').val('');
	$('#kd_rekening').val('');
	$('#urai_pendapatan').val('');
	$('#jum_pendapatan').val('0,00');

	$('#bendahara').val('');
	$('#norek_bendahara').val('');
	$('#nama_bank').val('');
	$('#nama_rekening_bank').val('');
	$('#npwp_bendahara').val('');
	$('#bend_jabatan').val('');

	$("#jenis_rekening option:eq(0)").prop('selected','true');
	isSimpan = true;
	$('#aksi').val(isSimpan);

	getPotongan_sp3b();
	ambilAfektasi_sp3b();
	jnsRek_chnage();
};

function InputOnFokus(e, target){
	document.getElementById(target).value = toAngkaDec(e);
}
function InputOnBlur(e, target){
	var nilai;
	if(e == ''){ nilai  = parseInt(0); } 
	else { nilai  = e; }
	document.getElementById(target).value = toRp_WithDecimal(nilai);;
}

function jnsRek_chnage(){
	var jnsRek = $("#jenis_rekening option:selected").text();
	$("#nm_jns_rekening").val(jnsRek);
}

function org_change_sp3b(e){
	getPotongan_sp3b();
	ambilAfektasi_sp3b();
	if(!isSimpan){ load_dataSP3B(); }
}

function LoadPendapatanSP3B(e){
	if($("#organisasi").val() == 0){
		$.alertable.alert("Organisasi belum dipilih")
	} else {
		tampilkanModals(e,'sp3b_pendapatan');
	}
};

function LoadBedaharaSP3B(e){
  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      tampilkanModals(e,'pihak_ketiga');
  }
}

function loadSP3B(e){
  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      tampilkanModals(e,'sp3b_load');
  }
}

function tampilkanModals(e,modal){
	var url_load  = "";
	var loadModal = "";
	var linkLoad  = $(e).attr('alt');
	var act       = getUrlVars(linkLoad)["act"];
	var widthnya = '800px'

	switch(modal) {
		case "sp3b_pendapatan":
	        var skpd  = $("#organisasi").val().split("-");
	        loadModal = "Cari Pendapatan";
	        url_load  = linkLoad+"?id="+skpd[0];
	        break; 

	    case "pihak_ketiga":
	        var skpd  = $("#organisasi").val().split("-");
	        loadModal = "Cari Data Pihak Ketiga";
	        url_load  = linkLoad+"?id="+skpd[0];
	        break; 

	    case "sp3b_load":
	        var skpd  = $("#organisasi").val().split("-");
	        loadModal = "Cari Data SP3B";
	        url_load  = linkLoad+"?id="+skpd[0];
	        break; 

	    case "laporan_sp3b":
	        var skpd  = $("#organisasi").val().split("-");
	        loadModal = "Cetak Laporan Data SP3B";
	        url_load  = linkLoad+"?id="+skpd[0];
	        break; 
	}
	document.getElementById("myModalLabel").innerHTML = loadModal;
	$("#showModal").modal();
	$(".modal-body-showmodal").load(url_load);
	$(".modal-dialog").css('width', widthnya);
};

function ambilAfektasi_sp3b(){
	var skpd = $("#organisasi").val();  
	var no_sp3b = $("#no_sp3b").val();
	var tanggal = $("#tanggal_sp3b").val();
	var url  = $("#url_afektasi_sp3b").val();
	var jenis = $("#jenis").val(); 
	var kd_unit = $("#kode_unit").val();
	var kd_bidang = $("#kode_bidang").val();
	var kd_program = $("#kode_program").val();
	var kd_kegiatan = $("#kode_kegiatan").val();  
	var kd_subkegiatan = $("#kode_subkegiatan").val(); 	

	if(skpd==0) { skpd = '0.0.0.0'; } 
	else if(skpd=='') { skpd = '0.0.0.0'; }  

	if(kd_bidang == ''){
		kd_bidang = '';
		kd_program = 0;
		kd_kegiatan = 0;
		kd_subkegiatan = 0;	
    }

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: url,
        data: {
          skpd:skpd,
          nosp3b:no_sp3b,
          tgl:tanggal,
          kdunit:kd_unit,
          bidang:kd_bidang,
          program:kd_program,
          kegiatan:kd_kegiatan,
          subkegiatan:kd_subkegiatan,
          jenis:jenis,
        },
        dataType: 'html',
        timeout: 10000,
        beforeSend: function() {
          	$(".cover").show();
        },
        success: function(response){  
          	adjust_datatable();
            $('#tabel_sp3b_afektasi').html(response); 
          	$(".cover").hide();
        }
    });
};

function getPotongan_sp3b(){
	var nosp3b = $("#no_sp3b").val();
	var skpd   = $("#organisasi").val();

	$.ajax({
		headers: { "X-CSRFToken": csrf_token },
		type: "POST",
		url: $('#tabel_sp3b_potongan').attr('alt'),
		data: {skpd:skpd, nosp3b:nosp3b},
		async: false,
		dataType: "html",
		timeout: 10000,
		success: function(response){
		  	$('#tabel_sp3b_potongan').html(response);
		}
	});
}

function load_dataSP3B(){
	var nosp3b_old = $("#no_sp3b_lama").val();
	var skpd = $("#organisasi").val();
	var uerel = $("#url_ambilsp3b").val();

	$.ajax({
        type: "GET",
        url: uerel,
        data: {id:skpd,tk:nosp3b_old},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function() {
          	$(".cover").show();
        },
        success: function(data){        
        	dtx = JSON.parse(data);      
          	$('#saldo_awal').val(dtx[0].saldoawal);
          	$('#jum_pendapatan').val(dtx[0].pendapatan);

			$('#kd_akun').val(dtx[0].kodeakun);
			$('#kd_kelompok').val(dtx[0].kodekelompok);
			$('#kd_jenis').val(dtx[0].kodejenis);
			$('#kd_objek').val(dtx[0].kodeobjek);
			$('#kd_rcobjek').val(dtx[0].koderincianobjek);
			$('#kd_subrcobjek').val(dtx[0].kodesubrincianobjek);
			$('#kd_rekening').val(dtx[0].kd_rekening);
			$('#urai_pendapatan').val(dtx[0].uraian);

			$('#bendahara').val(dtx[0].bendaharapenerima);
			$('#norek_bendahara').val(dtx[0].norekbank);
			$('#nama_bank').val(dtx[0].namabank);
			$('#nama_rekening_bank').val(dtx[0].namarekeningbank);
			$('#npwp_bendahara').val(dtx[0].npwp);
			$('#bend_jabatan').val(dtx[0].jabatan);

			$("#jenis_rekening").val(dtx[0].kodesumberdana_kasda);
			isSimpan = false;
			$('#aksi').val(isSimpan);

	      	$(".cover").hide();
        }
    }); 
}

function cekSimpanSP3B(url){ 
	var nosp3b = $("#no_sp3b").val();
	var nosp3b_old = $("#no_sp3b_lama").val();
	var skpd   = $("#organisasi").val();
	var kdbidang = $('#kode_bidang').val();
	var keperluan = $('#status_keperluan').val();
	var saldo = $('#saldo_awal').val();
	var kdakun = $('#kd_akun').val();
	var pendapatan = $('#jum_pendapatan').val();
	var bendh = $('#bendahara').val();
	var norek = $('#norek_bendahara').val();
	var nmbank = $('#nama_bank').val();

	CekNoSP3B(url,skpd,nosp3b);
	if(isSimpan == true){      
		if(hslCKsp3b > 0){
		  	$.alertable.alert("Nomor SP3B : "+nosp3b+", sudah digunakan.");
		  	return false;
		}
	}

	if(skpd == 0){
		$.alertable.alert('Organisasi belum dipilih'); return false;
	} else if(kdbidang == ""){
		$.alertable.alert('Sub Kegiatan belum dipilih'); return false;
	} else if(nosp3b == ""){
		$.alertable.alert('Nomor SP3B belum diisi'); return false;
	} else if(keperluan == ""){
		$.alertable.alert('Status Keperluan belum diisi'); return false;
	} else if(saldo == ""){
		$.alertable.alert('Saldo Awal belum diisi'); return false;
	} else if(kdakun == ""){
		$.alertable.alert('Rekening Pendapatan belum dipilih'); return false;
	} else if(pendapatan == ""){
		$.alertable.alert('Pendapatan belum diisi'); return false;
	} else if(bendh == ""){
		$.alertable.alert('Pihak Ketiga belum diisi'); return false;
	}  else if(norek == ""){
		$.alertable.alert('Nomor Rekening belum diisi'); return false;
	}  else if(nmbank == ""){
		$.alertable.alert('Nama Bank belum diisi'); return false;
	} else {

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
          $.alertable.confirm("Rekening "+rekening
            +". Belum di Otorisasi Bidang Anggaran! Harap Hubungi Bidang Anggaran.").then(function() {          
            cekBatas_SP3B();                     
          });
        } else {
          var chekOto = $(".afektasichk").is(":checked");
          if(chekOto==false){
              $.alertable.confirm("Rekening Belum ada yang dipilih");
          } else {
              cekBatas_SP3B();
          }              
        }    
	}
}

function cekBatas_SP3B(){  
	var val = []; var sekarang = [];  
	var lalu = []; var batas = [];
	var koderekening = []; var urai = []; var loloskan = [];
	var batas_rekening = '';    
	var jenis = $("#jenis").val();

	$(':checkbox:checked').each(function(i){
		val[i] = $(this).val().split('|'); 

		koderekening[i] = val[i][0];
		sekarang[i] = val[i][1];
		urai[i] = val[i][3];     
		lalu[i] = val[i][4]; 
		batas[i] = val[i][5];    
		loloskan[i] = parseInt(val[i][6]);   

		if((eval(toAngkaDec(sekarang[i]))+eval(toAngkaDec(lalu[i])))>eval(toAngkaDec(batas[i]))){
		if(loloskan[i] != 1){
		  batas_rekening = batas_rekening +', '+ koderekening[i]+' '+urai[i];   
		}         

		}     
	});

	batas_rekening = batas_rekening.substr(1,batas_rekening.length); 

	if(batas_rekening != ''){
		$.alertable.alert("Rekening "+batas_rekening+" melebihi batas. Harap Ubah Anggaran Kas dan Perbaiki SPD di Bidang Anggaran!"); return false;
	} else {
		simpanDataSP3B();
	} 
}

function simpanDataSP3B(){
	var frm = $('#frmSP3B');

	$.ajax({
		headers: { "X-CSRFToken": csrf_token },
		type: frm.attr('method'),
		url: frm.attr('action'),
		data: frm.serialize(),
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
			isSimpan = false;
			$('input[name="aksi"]').val(isSimpan);
			$("#no_sp3b_lama").val($("#no_sp3b").val());
		}
	}); 
}

function deleteSP3B(e){
	var skpd  = $('#organisasi').val();
    var nosp3b = $('#no_sp3b').val();
    var urlxx = $(e).attr('alt');

    if(skpd == 0){
      	$.alertable.alert('Organisasi Belum dipilih');
    } else if(nosp3b == ''){
      	$.alertable.alert('Nomor SP3B masih kosong');
    } else {
      	$.alertable.confirm("Anda yakin akan menghapus data SP3B dengan Nomor : "+nosp3b+" ?").then(function() {            
			$.ajax({
				headers: { "X-CSRFToken": csrf_token },
				type: "POST",
				url: urlxx,
				data: {         
					'nosp3b':nosp3b,
					'org':skpd,
				},
				dataType: 'html',
				success: function (data) {                   
					message_ok("success",data);
					clearForm_SP3B('');                                                                 
				}
			});
		}, function() {
			 message_ok('error', 'Anda telah membatalkan menghapus data SP3B');          
      	});
    }
}

function cekLaporanSP3B(e){
	if($('#organisasi').val() == 0){
      	$.alertable.alert("Organisasi belum dipilih")
  	} else if($('#no_sp3b').val()==''){
		$.alertable.alert('Nomor SP3B belum diisi'); 
	} else if($('#bendahara').val()==""){
		$.alertable.alert('Nama Bendahara belum diisi');
	} else{                
		tampilkanModals(e,'laporan_sp3b');
	}      
}