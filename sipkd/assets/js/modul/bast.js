let isSimpan  = true;
let isTanggal = false;
let url_Form  = $('#myForm').attr('action');
let cekSukses = false;
let isCetak   = true;
let isPemberitahuan = false;
let jnsSPM = '';

function get_tabel_bast(){
	let opd    = $("#organisasi").val();
  
	$.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: $('#tabel_bast').attr('alt'),
      data: {skpd:opd},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(response){
        	$('#tabel_bast').html(response);
        	$(".cover").hide();
      }
  });
}

function modal_input_bast(judul,act){
  var skpd = $("#organisasi").val();
  let data = ""; 

  if(act == "false"){
      // data = "&dt="+$("#check_bast_edit").text().toUpperCase().replace(/\//g,'_').replace(/\ /g,'+');
      data = "&dt="+encodeURIComponent(arrPIL[0].toUpperCase());
  }

  let tautan  = link_modal_bast+"?ax="+act+"&id="+skpd+data;
  document.getElementById("modal-bastLabel").innerHTML = judul;  
  $("#modal-bast").modal();
  $(".modal-bast-body").load(tautan);
  $(".modal-bast-div").css('width', '900px');
}

function LoadKontrak(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'list_kontrak');
  }
}

$("#btn_tambah").click(function(){
  let skpd = $("#organisasi").val();
  let org  = $("#org_tampilkan").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi belum dipilih !"); return false;
  } else { 
    modal_input_bast(`Input Data BAST [ ${org} ]`,`true`); 
  }
});

$("#btn_edit").click(function(){
  var org  = $("#org_tampilkan").val();
  if(arrPIL.length <= 0){
      $.alertable.alert("Nomor BAST Belum ada yang dipilih!"); return false;
  } else if(arrPIL.length > 1) {
      $.alertable.alert("Nomor BAST Tidak bisa lebih dari satu!"); return false;
  } else {
    modal_input_bast("Edit Data BAST [ "+org+" ]","false");
  }
});

$("#btn_hapus").click(function(){
  var nobast = $("#check_bast").text();
  var skpd      = $("#organisasi").val();

  if(arrCHK.length <= 0){
      $.alertable.alert("Silahkan pilih nomor BAST yang akan dihapus terlebih dahulu!"); return false;
  } else {
      $.alertable.confirm('Apakah anda yakin ingin menghapus data BAST dengan Nomor : '+nobast+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nobast:nobast},
              dataType:"json",
              success: function(z){
                get_tabel_bast();
                  $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data BAST dibatalkan!');
      });
  }
});

function ambilAfektasiKontrak(){    
    var skpd = $("#skpd").val();  
    var nokontrak = $("#nokontrak").val();
    var tanggal = $("#tgl_mulai").val();
    var url  = $("#url_afektasi_kontrak").val();
    var kd_unit = $("#kode_unit").val();
    var kd_bidang = $("#kode_bidang").val(); 
    var kd_program = $("#kode_program").val();
    var kd_kegiatan = $("#kode_kegiatan").val();
    var kd_subkegiatan = $("#kode_subkegiatan").val();   
    data_type = 'html';
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: url,
        data: {
          skpd:skpd,
          nokontrak:nokontrak,
          tgl:tanggal,
          kdunit:kd_unit,
          bidang:kd_bidang,
          program:kd_program,
          kegiatan:kd_kegiatan,
          subkegiatan:kd_subkegiatan,
          jenis:'bast',
        },
        dataType: data_type,
        timeout: 10000,
        beforeSend: function() {
          $(".cover").show();
        },
        success: function(response){  
          $('#tabel_kontrak_afektasi').html(response);
          $(".cover").hide();
        }
      });
  }