/*
JavaScript untuk modul SP2D
created by Joel Hermawan @GI 2017 
SIPKD Application

===============================================================================================================================
*/

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
  } else {
      $(target1).prop('readonly', true);
  }
}


$("#org_tampilkan").keydown(function(){ return false });
$("#keg_tampilkan").keydown(function(){ return false });
$("#tgl_sp2b").keydown(function(){ return false });
$("#tgl_spm").keydown(function(){ return false });
$("#bank_asal").keydown(function(){ return false });
$("#bank_asal").attr("readonly",true);

function set_IsLocked(cond){
  if(cond == 'Y'){ 
      $('#no_sp2b').attr('readonly',true);
      $('#no_sp2b').keydown(function(){ return false });
      $('.tgl_sp2b').css('pointer-events','none');
      $('#src_spm').css('pointer-events','none');
      $('#status_keperluan').attr('readonly',true);
      $('#status_keperluan').keydown(function(){ return false });
  } else {
      $('#no_sp2b').attr('readonly',false);
      $('#no_sp2b').off('keydown');
      $('.tgl_sp2b').css('pointer-events','');
      $('#src_spm').css('pointer-events','');
      $('#status_keperluan').attr('readonly',false);
      $('#status_keperluan').off('keydown');
  }
}

function cekNoSp2d(nosp2b){
  var digunakan = false;

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_nosp2b,
      data: {nosp2b:nosp2b},
      async: false,
      timeout: 10000,
      success: function(msg){
        if(msg <= 0){ digunakan = false; } else { digunakan = true; }
      }
  });

  return digunakan;
}

// MODAL CARI BENDAHARA / PIHAK KETIGA ======================
$('#src_bend_pihak3').click(function(){
  render_modal('Cari Bendahara / Pihak Ketiga','sp2d_src_bendahara',[]);
});

// MODAL LOAD SP2D ==========================================
$("#btn_lihat_sp2b").click(function(){
  var skpd = $("#organisasi").val();

  switch(form_sp2d){
    case "sp2b_barjas":
      jnsSPM = 'LS';
      break;
  };

  //if(skpd == ''){
     // $.alertable.alert("Organisasi harus dipilih terlebih dahulu !"); return false;
  //} else {
    if(form_sp2d in ['sp2b_barjas','sp2b_gu_kepmen','sp2b_tu_kepmen']){
        render_modal('Cari Data SP2B','btn_lihat_sp2b',[skpd,jnsSPM]);
    } else {
        render_modal_spm_sp2b_barjas('Cari Data SP2B','src_sp2b',[skpd,jnsSPM]);
    }
  //}
});

// MODAL CARI DATA SPM ======================================
$("#src_spm").click(function(){
  var skpd   = $("#organisasi").val();

  switch(form_sp2d){
    case "sp2b_barjas":
      jnsSPM = 'LS';
      break;
  };

  if(skpd == ''){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu !"); return false;
  } else {
    if(form_sp2d in ['sp2b_barjas','sp2b_gu_kepmen','sp2b_tu_kepmen']){
        render_modal('Cari Data SPM','src_spm',[skpd,jnsSPM]);
    } else {
        render_modal_spm_sp2b_barjas('Cari Data SPM','src_spm',[skpd,jnsSPM]);
    }
  }
});

// LOAD FORM CETAK LAPORAN
$("#btn_cetak").click(function(){

  switch(form_sp2d){
    case "sp2b_barjas":
      lap_sp2b_barjas();
      break; 
  }
  
});

// FUNGSI SIMPAN 
$("#btn_simpan").click(function(){
  isCetak = true;

  switch(form_sp2d){
    case "sp2b_barjas":
      SaveSP2D_BARJAS();
      break;
  }
  
});

// FUNGSI EDIT
$("#btn_edit").click(function(){
  switch(form_sp2d){
    case "advis_form":
      EditAdvis_sp2b();
      break;
  }
});

// FUNGSI HAPUS
$("#btn_hapus").click(function(){
  switch(form_sp2d){
    case "sp2b_barjas":
      Del_sp2b_BARJAS();
      break;
  }
})


function fungsi_modal(e,asal){
  $('#showModal').modal('hide');

  switch(asal) {
    case "sp2d_src_bendahara":
      src_bendahara(e);
      break;
    case "src_spm":
      src_noSPM(e);
      break;
    case "btn_lihat_sp2b":
      get_sp2b_data(e);
      break;
    case "ambil_sumdan_":
      select_sumberdana(e);
      break;
  }
}

function select_sumberdana(e){
  var row   = $(e).closest('tr'); 
  var $kode_sumdan   = row.find('td:nth-child(1)');
  var $urai_sumdan   = row.find('td:nth-child(2)');
  $.each($kode_sumdan, function(){ var_kodesumdan_  = $(this).text();}); 
  $.each($urai_sumdan, function(){ var_uraiansumdan_  = $(this).text();}); 
  $('#frm_sumberdana').val(var_uraiansumdan_);
  $('#frm_sumberdana_x').val(var_kodesumdan_);
}

function src_bendahara(e){
  var row   = $(e).closest('tr'); 
  var $nama   = row.find('td:nth-child(4)');
  var $norek  = row.find('td:nth-child(1)');
  var $bank   = row.find('td:nth-child(2)');
  var $npwp   = row.find('td:nth-child(3)');

    $.each($nama, function(){ Nama  = $(this).text();}); 
    $.each($norek, function(){ NoRek = $(this).text();}); 
    $.each($bank, function(){ Bank  = $(this).text();}); 
    $.each($npwp, function(){ NPWP  = $(this).text();});  

    var noPajak;
    if(NPWP == "-" || NPWP == ""){ noPajak = "00.000.000.0-000.000";} else { noPajak = NPWP;}

    document.getElementById('bendahara').value = Nama;
    document.getElementById('norek_bendahara').value = NoRek;
    document.getElementById('bank_bendahara').value = Bank;
    document.getElementById('npwp_bendahara').value = noPajak;
}

function src_noSPM(e){
  var row   = $(e).closest('tr');
  var $nospm  = row.find('td:nth-child(1)');
  $.each($nospm, function(){ NoSPM = $(this).text();});
  document.getElementById('no_spm').value = NoSPM;

  switch(form_sp2d){
    case "sp2b_ppkdbtl":
      loadDataSPM_btlppkd();
      break;

    case "sp2b_gaji":
      loadDataSPM_gaji();
      break;
    case "sp2b_nona":
      loadDataSPM_NONA();
      break;
    case "sp2b_tunihil":
      loadDataSPM_TU_NIHIL();
      break;
  };
}

function get_sp2b_data(e){
  var row   = $(e).closest('tr');
  var $nosp2b  = row.find('td:nth-child(1)');
  $.each($nosp2b, function(){ NoSp2d = $(this).text();});
  document.getElementById('no_sp2b').value = NoSp2d;
  document.getElementById('no_sp2b_x').value = NoSp2d;

  switch(form_sp2d){
    case "sp2b_ppkdbtl":
      loadDataSP2D_btlppkd(); 
      break;
    case "sp2b_gaji":
      loadDataSP2D_gaji();
      break;
    case "sp2b_nona":
      loadDataSP2D_NONA();
      break;
    case "sp2b_tunihil":
      loadDataSP2D_tuNihil();
      break;
  };
}

function getAfektasi(){
  
}


function getPotongan_sp2b(asal){
  var nospm   = $("#no_spm").val();
  var skpd    = $("#organisasi").val();
  var nosp2b  = $("#no_sp2b").val();
  var kodeunit = $("#kodeunit").val();

  $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    type: "POST",
    url: link_tbl_pot,
    data: {skpd:skpd, nospm:nospm, nosp2b:nosp2b, asal:asal,kodeunit:kodeunit},
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){
      $('#tabel_potongansp2b').html(response);
    }
  });
}


 
// JS LAPORAN SP2D ============================================================================================================

function getLapDataPejabat(){
	var data  = $("#pejabat").val().split("|");

  $("#id_pejabat").val(data[0]);
	$("#nama_pejabat").val(data[1]);
	$("#nip_pejabat").val(data[2]);
	$("#pangkat_pejabat").val(data[3]);
}


// PERSETUJUAN SP2D - JOEL 27 Jan 2019 ==========================================================
function load_draft_sp2b(e){

  if(e != ''){
      var tgl = $('#per_tgl_sp2b').val();
  } else {
      var tgl = $('#tabel_persetujuan').attr('alt');
  }

  var usr = $('#us_skpd').val();

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_draft_sp2b,
    data: {tgl:tgl,usr:usr},
    async: false,
    dataType: 'html',
    timeout: 10000,
    beforeSend: function(){ $(".cover").show(); },
    success: function(datax){
      $('#tabel_persetujuan').html(datax);
      $(".cover").hide();
    }
  });
}

// ADVIS - JOEL 31-JAN-2019 ==========================
// DRAFT ADVIS
function load_draft_advis_sp2b(){
  var tgl = $('#per_tgl_advis').val();

  $('#label_advis').html('ADVIS SP2D TANGGAL '+$('#per_tgl_advis option:selected').text());

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: get_no_advis,
    async: false,
    dataType: 'json',
    timeout: 10000,
    success: function(datax){
      $("#no_advis").val(datax['hasil']);
      $("#advis_urut").val(datax['urutan']);

      isAkses = datax['pisibel'];
      loadPertama('btn_edit',datax['pisibel']);
    }
  });

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_draft_advis,
    data: {tgl:tgl},
    async: false,
    dataType: 'html',
    timeout: 10000,
    beforeSend: function(){ $(".cover").show(); },
    success: function(datax){
      $('#div_draft_advis').html(datax);
    }
  });

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_advis_sp2b,
    data: {tgl:tgl},
    async: false,
    dataType: 'html',
    timeout: 10000,
    success: function(datax){
      $('#div_advis').html(datax);
      $(".cover").hide();
    }
  });
}

// ADVIS - JOEL 19-FEB-2019 ==========================
// PERSETUJUAN SPJ SP2D PER SKPD
function clrs_frm_lock(){ 
  $('#org_tampilkan').val('');
  $('#organisasi').val('');
  $('#organisasi').attr('alt','');

  load_draft_spj_sp2b();
}

function load_draft_spj_sp2b(){
  var skpd = $('#organisasi').val();
  var usr  = $('#us_skpd').val();

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_draft_sp2b,
    data: {skpd:skpd,usr:usr},
    async: false,
    dataType: 'html',
    timeout: 10000,
    beforeSend: function(){ $(".cover").show(); },
    success: function(datax){
      $('#tabel_persetujuan').html(datax);
      $(".cover").hide();
    }
  });
}


function enable_disable_tabs(keg,rek){
  loadPertama('btn_tab_kegiatan',keg);
  loadPertama('btn_tab_rekening',rek);

  if(keg == "1" && rek == "0"){
    loadPertama('btn_simpan',0);
    loadPertama('btn_back',0);
    loadPertama('btn_next',1);
    $("#tab_kegiatan").removeClass('hidden');
    $("#tab_rekening").addClass('hidden');
    $("#tabs_tujuan").html('rekening');
  } else {
    loadPertama('btn_simpan',1);
    loadPertama('btn_back',1);
    loadPertama('btn_next',0);
    $("#tab_kegiatan").addClass('hidden');
    $("#tab_rekening").removeClass('hidden');
    $("#tabs_tujuan").html('kegiatan');
  }
}



