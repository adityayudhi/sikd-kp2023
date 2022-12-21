/* ==============================================================================================================
JavaScript untuk modul SPJ_SKPD
created by Joel Hermawan @GI 2019 
SIPKD Application
================================================================================================================*/

var isSimpan  = true;
var isTanggal = false;
var url_Form  = $('#myForm').attr('action');
var cekSukses = false;
var isCetak   = true;
var isPemberitahuan = false;
var jnsSPM = '';

function handleClick(cb,target1){
  if(cb.checked == true){
      $(target1).prop('readonly', false);
      $(target1).focus();
  } else { $(target1).prop('readonly', true); }
}

function skrskp_get_tabel_awal(){
	var skpd    = $("#organisasi").val();
	var jenis 	= $("input[name='rdjns_skpskr']:checked").val();

	$.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: $('#tabel_skr_skp').attr('alt'),
      data: {skpd:skpd, jenis:jenis},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(response){
        	$('#tabel_skr_skp').html(response);
        	$(".cover").hide();
      }
  });
}

$("#org_tampilkan").keydown(function(){ return false });
$("input[name='rdjns_skpskr']").click(function(){
    skrskp_get_tabel_awal();
});

$("#btn_tambah").click(function(){
    var skpd = $("#organisasi").val();
    var org  = $("#org_tampilkan").val();

    if(skpd == ""){
        $.alertable.alert("Organisasi belum dipilih !"); return false;
    } else { modal_input_SKPSKR("Input Data SKP / SKR [ "+org+" ]","true"); }
});

$("#btn_edit").click(function(){
    var org  = $("#org_tampilkan").val();

    if(arrPIL.length <= 0){
        $.alertable.alert("Nomor SKP / SKR Belum ada yang dipilih!"); return false;
    } else {
        modal_input_SKPSKR("Edit Data SKP / SKR [ "+org+" ]","false");
    }
});

$("#btn_hapus").click(function(){
    var no_skpskr = $("#check_skpskr").text();
    var skpd      = $("#organisasi").val();

    if(arrCHK.length <= 0){
        $.alertable.alert("Silahkan pilih nomor SKP / SKR yang akan dihapus terlebih dahulu!"); return false;
    } else {
        $.alertable.confirm('Apakah anda yakin ingin menghapus data SKP / SKR dengan Nomor : '+no_skpskr+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: frm_aksi,
                data: {skpd:skpd, nomer:no_skpskr},
                dataType:"json",
                success: function(z){
                    skrskp_get_tabel_awal();
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data SKP / SKR dibatalkan!');
        });
    }
});

function modal_input_SKPSKR(judul,act){
  var skpd = $("#organisasi").val();
  var data = ""; 

  if(act == "false"){
      data = "&dt="+$("#check_skpskr_edit").text().toUpperCase().replace(/\//g,'_').replace(/\ /g,'+');
  }

  var tautan  = link_modal_skpskr+"?ax="+act+"&id="+skpd+data;
  document.getElementById("ModalskpskrLabel").innerHTML = judul;  
  $("#Modalskpskr").modal();
  $(".modal-body-skpskr").load(tautan);
  $(".modal-skpskr").css('width', '900px');
}


// JS FOR AKUNTANSI ==================================================================
// JOEL 20 MEI 2019 ==================================================================
function change_AKUN(){
    var kdakun = $("#jenis_akun").val();

    if(kdakun == 5){ $('#radio_belanja').show(); }
    else{ $('#radio_belanja').hide(); }
    koreak_get_tabel_awal();
}

function koreak_get_tabel_awal(){
  var jns_belanja = $("input[name='rdjns_belanja']:checked").val(); 
  var jns_akun    = $("#jenis_akun").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: $('#tabel_koreak').attr('alt'),
      data: {jns_belanja:jns_belanja, jns_akun:jns_akun},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(response){
          $('#tabel_koreak').html(response);
          $(".cover").hide();
      }
  });
}

$("input[name='rdjns_belanja']").click(function(){
  change_AKUN();
});

function get_konpiu_load(){
  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: $('#tabel_konpiu').attr('alt'),
      data: {id:'piutang'},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(response){
        $('#tabel_konpiu').html(response);
        $(".cover").hide();
      }
  });
}