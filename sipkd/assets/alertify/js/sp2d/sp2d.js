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

function getNewNoSP2D(skpd,jenis){
  var hasil = "";

  $.ajax({
      type: "POST",
      url: baseUrl+"index.php?route=sp2d/modal_sp2d/getnewnosp2d",
      data: {skpd:skpd, jenis:jenis, form:route},
      async: false,
      timeout: 10000,
      success: function(response){
        hasil = response.replace(/\s/g, '');
      }
  });

  return hasil;
}

$("#org_tampilkan").keydown(function(){ return false });
$("#keg_tampilkan").keydown(function(){ return false });
$("#tgl_sp2d").keydown(function(){ return false });
$("#tgl_spm").keydown(function(){ return false });
$("#bank_asal").keydown(function(){ return false });
$("#bank_asal").attr("readonly",true);

function set_IsLocked(cond){
  if(cond == 'Y'){ 
      $('#no_sp2d').attr('readonly',true);
      $('#no_sp2d').keydown(function(){ return false });
      $('.tgl_sp2d').css('pointer-events','none');
      $('#src_spm').css('pointer-events','none');
      $('#status_keperluan').attr('readonly',true);
      $('#status_keperluan').keydown(function(){ return false });
  } else {
      $('#no_sp2d').attr('readonly',false);
      $('#no_sp2d').off('keydown');
      $('.tgl_sp2d').css('pointer-events','');
      $('#src_spm').css('pointer-events','');
      $('#status_keperluan').attr('readonly',false);
      $('#status_keperluan').off('keydown');
  }
}

function cekNoSp2d(nosp2d){
  var digunakan = false;

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_nosp2d,
      data: {nosp2d:nosp2d},
      async: false,
      timeout: 10000,
      success: function(msg){
        if(msg <= 0){ digunakan = false; } else { digunakan = true; }
      }
  });

  return digunakan;
}

// function LoadKegiatanSP2D(e){
//   var skpd = $("#organisasi").val();

//   if(skpd == 0){
//       $.alertable.alert("Organisasi belum dipilih")
//   } else {
//       showModal(e,'kegiatan');
//   }
// }

// function LoadBedaharaSP2D(e){
//   var skpd = $("#organisasi").val();

//   if(skpd == 0){
//       $.alertable.alert("Organisasi belum dipilih")
//   } else {
//       showModal(e,'bendahara');
//   }
// }

// function LoadModal_SPM(e){
//   var skpd = $("#organisasi").val();

//   if(skpd == 0){
//       $.alertable.alert("Organisasi belum dipilih")
//   } else {
//       showModal(e,'spm');
//   }
// }

// function loadDataSPM(tujuan){
//   switch(tujuan){
//     case "btlppkd": loadDataSPM_btlppkd();
//       break;
//     case "up": loadDataSPM_up();
//       break;
//   }
  
// }

// function loadDataSp2d(tujuan){
//   switch(tujuan){
//     case "btlppkd": loadDataSP2D_btlppkd();
//       break;
//     case "up": getDataSP2D_UP($("#organisasi").val(),$("#no_sp2d").val());
//       break;
//   }
// }

// MODAL CARI BENDAHARA / PIHAK KETIGA ======================
$('#src_bend_pihak3').click(function(){
  render_modal('Cari Bendahara / Pihak Ketiga','sp2d_src_bendahara',[]);
});

// MODAL LOAD SP2D ==========================================
$("#btn_lihat_sp2d").click(function(){
  var skpd = $("#organisasi").val();

  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      jnsSPM = 'LS_PPKD';
      break;
    case "sp2d_gaji":
      jnsSPM = 'GJ';
      break;
    case "sp2d_barjas":
      jnsSPM = 'LS';
      break;
    case "sp2d_nona":
      jnsSPM = 'NON ANGG';
      break;
    case "sp2d_tunihil":
      jnsSPM = 'TU_NIHIL';
      break;
  };

  if(skpd == ''){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu !"); return false;
  } else {
    if(form_sp2d != 'sp2d_barjas'){
        render_modal('Cari Data SP2D','btn_lihat_sp2d',[skpd,jnsSPM]);
    } else {
        render_modal_spm_sp2d_barjas('Cari Data SP2D','src_sp2d',[skpd,jnsSPM]);
    }
  }
});

// MODAL CARI DATA SPM ======================================
$("#src_spm").click(function(){
  var skpd   = $("#organisasi").val();

  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      jnsSPM = 'LS_PPKD';
      break;
    case "sp2d_gaji":
      jnsSPM = 'GJ';
      break;
    case "sp2d_barjas":
      jnsSPM = 'LS';
      break;
    case "sp2d_nona":
      jnsSPM = 'NON ANGG';
      break;
    case "sp2d_tunihil":
      jnsSPM = 'TU_NIHIL';
      break;
  };

  if(skpd == ''){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu !"); return false;
  } else {
    if(form_sp2d != 'sp2d_barjas'){
        render_modal('Cari Data SPM','src_spm',[skpd,jnsSPM]);
    } else {
        render_modal_spm_sp2d_barjas('Cari Data SPM','src_spm',[skpd,jnsSPM]);
    }
  }
});

// LOAD FORM CETAK LAPORAN
$("#btn_cetak").click(function(){

  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      lap_sp2d_btlppkd();
      break;
    case "advis_form":
      Lap_Advis_sp2d();
      break;
    case "sp2d_gaji":
      lap_sp2d_gaji();
      break;
    case "sp2d_barjas":
      lap_sp2d_barjas();
      break; 
    case "sp2d_nona":
      lap_sp2d_NONA();
      break;
    case "sp2d_tunihil":
      lap_sp2d_TU_NIHIL();
      break;
  }
  
});

// FUNGSI SIMPAN 
$("#btn_simpan").click(function(){
  isCetak = true;

  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      SaveSP2D_btlppkd();
      break;
    case "advis_form":
      SaveAdvis_sp2d();
      break;
    case "sp2d_gaji":
      SaveSP2D_gaji();
      break;
    case "sp2d_barjas":
      SaveSP2D_BARJAS();
      break;
    case "sp2d_nona":
      SaveSP2D_NONA();
      break;
    case "sp2d_tunihil":
      SaveSP2D_TU_NIHIL();
      break;
  }
  
});

// FUNGSI EDIT
$("#btn_edit").click(function(){
  switch(form_sp2d){
    case "advis_form":
      EditAdvis_sp2d();
      break;
  }
});

// FUNGSI HAPUS
$("#btn_hapus").click(function(){
  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      Del_sp2d_btlppkd();
      break;
    case "sp2d_gaji":
      Del_sp2d_gaji();
      break;
    case "sp2d_barjas":
      Del_sp2d_BARJAS();
      break;
    case "sp2d_nona":
      Del_sp2d_NONA();
      break;
    case "sp2d_tunihil":
      Del_sp2d_TU_NIHIL();
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
    case "btn_lihat_sp2d":
      get_sp2d_data(e);
      break;
  }
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
    case "sp2d_ppkdbtl":
      loadDataSPM_btlppkd();
      break;

    case "sp2d_gaji":
      loadDataSPM_gaji();
      break;
    case "sp2d_nona":
      loadDataSPM_NONA();
      break;
    case "sp2d_tunihil":
      loadDataSPM_TU_NIHIL();
      break;
  };
}

function get_sp2d_data(e){
  var row   = $(e).closest('tr');
  var $nosp2d  = row.find('td:nth-child(1)');
  $.each($nosp2d, function(){ NoSp2d = $(this).text();});
  document.getElementById('no_sp2d').value = NoSp2d;
  document.getElementById('no_sp2d_x').value = NoSp2d;

  switch(form_sp2d){
    case "sp2d_ppkdbtl":
      loadDataSP2D_btlppkd(); 
      break;
    case "sp2d_gaji":
      loadDataSP2D_gaji();
      break;
    case "sp2d_nona":
      loadDataSP2D_NONA();
      break;
    case "sp2d_tunihil":
      loadDataSP2D_tuNihil();
      break;
  };
}

function getAfektasi(){
  
}

// JS SP2D BTL - PPKD =========================================================================================================

function loadFormSPM_btlppkd(){
  clearForm_btlppkd();
}

function clearForm_btlppkd(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2d").val('');
  $("#no_sp2d_x").val('');
  $("#tgl_sp2d").val(DateNowInd());
  $("#tgl_spm").val(DateNowInd());
  $('#kunci_sp2d').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  $('input[name="inpt_triwulan"]').val($("#triwulan").val());
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());
  getTriwulan('#tgl_sp2d','#triwulan');

  $('#kunci_sp2d').removeClass('disetujui');
  $('#tgl_sp2d').attr('disabled',false);
  set_IsLocked('awal');

  Afektasi_btlppkd('sp2d');

  var skpd = $("#organisasi").val();
  // $("#no_sp2d").val(getNewNoSP2D(skpd,'LS_PPKD'));

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();

}

function Afektasi_btlppkd(asal){
  var nospm   = $("#no_spm").val();
  var nosp2d  = $("#no_sp2d_x").val();
  var tanggal = $("#tgl_sp2d").val();
  var skpd    = $("#organisasi").val();

  var triwul  = $("#triwulan").val();
  var jenis   = $("#perubahan").val();

  if(triwul == 0){
      $.alertable.alert("Triwulan belum dipilih!"); return false;
  } else if(skpd != "" && triwul > 0 && jenis >= 0){
      $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabel,
        data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, asal:asal},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
            $('#tabel_datasp2d').html(response);
            getSumberDana_btlppkd();
            $(".cover").hide();
        }
      });
  }
}

function loadDataSP2D_btlppkd(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sp2d,
      data: {skpd:skpd, nosp2d:nosp2d},
      async: false,
      dataType: "json",
      success: function (hsl) {

        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        $('#kunci_sp2d').text(hsl['KUNCI']);
        $("#tgl_sp2d").val(hsl['TANGGAL']);
        $("#tgl_spm").val(hsl['TGLSPM']);
        $("#no_spm").val(hsl['NOSPM']);
        $("#no_spm_x").val(hsl['NOSPM']);
        $('#status_keperluan').val(hsl['DESKRIPSISPM']);

        loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
        loadPertama('btn_hapus',hsl['BTN_HAPUS']);

        $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
        $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
        $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
        $('input[name="bank_bendahara"]').val(hsl['BANK']);
        $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
        $('input[name="inpt_triwulan"]').val(hsl['TRIWULAN']); 
        $('#triwulan').val(hsl['TRIWULAN']);
        $('#perubahan').val(hsl['PERUBAHAN']); 
        $('input[name="inpt_perubahan"]').val(hsl['PERUBAHAN']);

        Afektasi_btlppkd('sp2d');

        $("#bank_asal").val(hsl['BANKASAL']); 
        $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

        if(hsl['LOCKED'] == 'Y'){ 
            $.alertable.alert(hsl['PESAN']); 
            $('#kunci_sp2d').addClass('disetujui');
        } else {
            $('#kunci_sp2d').removeClass('disetujui');
        }

        set_IsLocked(hsl['LOCKED']);
      }
  });
}

function getSumberDana_btlppkd(){
  var nospm   = $("#no_spm_x").val();
  var nosp2d  = $("#no_sp2d").val();
  var tanggal = $("#tgl_sp2d").val();
  var skpd    = $("#organisasi").val();
  var kdrek   = $("#kd_rekening").val();
  var aksi    = $('input[name="aksi"]').val();
  var sumber  = "";

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sumda,
      data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kdrek:kdrek, aksi:aksi},
      async: false,
      dataType: "json",
      success: function (hasil) {
        $('input[name="kd_sumberdana"]').val(hasil['KD_SUMBERDANA']);
        $('input[name="nm_sumberdana"]').val(hasil['NM_SUMNERDANA']);
        reksumDana_btlppkd(hasil['KD_SUMBERDANA']);
      }
  });

  function reksumDana_btlppkd(kode){
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_reken,
        data: {kode:kode},
        async: false,
        dataType: "html",
        timeout: 10000,
        success: function(response){
            $('#norek_bankasal').html(response);
            PilihRekening_sp2d();
        }
    });
  }
}

function PilihRekening_sp2d(){
  var rekening = $("#norek_bankasal").val().split("|");
  $("#bank_asal").val(rekening[3]);
}

function loadDataSPM_btlppkd(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd},
      async: false,
      success: function(msg){ 

        $('input[name="no_spm_x"]').val(msg['nmrspm']); 
        $('input[name="tgl_spm"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        Afektasi_btlppkd('spm');
        $("#no_sp2d").focus();
      }
  });
}

function SaveSP2D_btlppkd(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var skpd    = $("#organisasi").val();
    var nosp2d  = $("#no_sp2d").val();
    var nosp2dX = $("#no_sp2d_x").val();
    var nospm   = $("#no_spm").val();
    var ktrngn  = $("#status_keperluan").val()
    var bendahr = $("#bendahara").val();
    var norek   = $("#norek_bendahara").val();
    var tanggal = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
    var CKsp2d  = cekNoSp2d(nosp2d);
    var ceked   = [];
    var arrMsg  = [];
    var batas, jumlah;

    function cekValid(){
      // cek afektasi 
      $(".afektasichk:checked").each(function(){
          var pelyu = $(this).attr("alt"); 
          ceked.push(pelyu);

          var row   = $('#dataTable_sp2d td').closest("tr"); 
          otorisasi = toAngka(row.children('td.otorisasi'+pelyu).text());
          anggaran  = toAngka(row.children('td.anggaran'+pelyu).text());
          batas     = toAngka(row.children('td.batas'+pelyu).text());
          jumlah    = toAngka(row.children('td.lalu'+pelyu).text()) + toAngka($('#input_tbl'+pelyu).val());
          rekening  = row.children('td.kode'+pelyu).text()+" "+row.children('td.urai'+pelyu).text();

          cekValidasi(rekening,otorisasi,jumlah,batas,anggaran);
      });
    }
    
    if(aksi == "true"){
        if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
    } else {
        if(nosp2d != nosp2dX){
          if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
        }
    }

    if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(nosp2d == ""){
        $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
    } else if(nospm == ""){
        $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
    } else if(ktrngn == ""){
        $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
    } else if(bendahr == ""){
        $.alertable.alert("Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(norek == ""){
        $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(!tanggal){
        $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
    } else {
      cekValid();
      if(ceked.length == 0){ $.alertable.alert("Data Afektasi belum ada yang dipilih !"); return false;} 
      else if(cekSukses){return false;}
      else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                  if(x['issimpan'] >= 1){
                    $("#no_sp2d_x").val(nosp2d);
                    isSimpan = false;
                    $('input[name="aksi"]').val(isSimpan);
                    loadPertama('btn_hapus','1');
                    loadDataSP2D_btlppkd();
                    if(!isCetak){ cetak_lap_sp2d_btlppkd();}
                  }
                  $.alertable.alert(x['pesan']);
                }
            });

        }, function() {
            message_ok('error', 'Simpan data '+nosp2d+' dibatalkan!');
        });
      } 
    }
}

function Del_sp2d_btlppkd(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi Belum dipilih !"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Data SP2D belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2D Dengan Nomor '+nosp2d+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2d:nosp2d},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_btlppkd(); } 
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!');
      });
  }
}

function lap_sp2d_btlppkd(){
  var posisi = $("#btn_simpan").is("[disabled]");

  if(posisi){
      if(cekSukses){
          isCetak = false;
          SaveSP2D_btlppkd();
      } else {
          isCetak = posisi;
          cetak_lap_sp2d_btlppkd();
      }

  } else {
      isCetak = false;
      SaveSP2D_btlppkd();
  }
}

function cetak_lap_sp2d_btlppkd(){
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(nosp2d == ""){ 
      $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
      $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
      showModalLaporan('lap_sp2d_ppkdbtl'); 
  }
}

// JS SP2D BARANG DAN JASA [BARJAS] Joel - 11 Feb 2019 ==================================================================

function render_modal_spm_sp2d_barjas(header,asal,js_arg){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: modal_spm_sp2d,
    data: {'asal':asal,'js_arg':JSON.stringify(js_arg),},
    dataType: 'html',
    beforeSend: function() {
      $(".cover").show();
    },
    success: function(data){
      $('#myModalLabel').html(header);
      $("#showModal").modal();
      $(".modal-body-showmodal").html(data);
      $(".modal-dialog").css('width', '800px');
      $(".cover").hide();
    }
  });
}


function clearForm_BARJAS(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2d").val('');
  $("#no_sp2d_x").val('');
  $("#keg_tampilkan").val('');
  $("#kegiatan").val('');
  $("#kegiatan").attr('alt','');
  $("#tgl_sp2d").val(DateNowInd());
  $("#tgl_spm").val(DateNowInd());
  $('#kunci_sp2d').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  $('input[name="inpt_triwulan"]').val($("#triwulan").val());
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());
  getTriwulan('#tgl_sp2d','#triwulan');

  $('#kunci_sp2d').removeClass('disetujui');
  $('#tgl_sp2d').attr('disabled',false);
  $('#src_kegiatan').css('pointer-events','');
  set_IsLocked('awal');

  loadTabelAfektasi_BARJAS('sp2d');

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();

}

function loadTabelAfektasi_BARJAS(asal){
  var nospm    = $("#no_spm").val();
  var nosp2d   = $("#no_sp2d_x").val();
  var tanggal  = $("#tgl_sp2d").val();
  var skpd     = $("#organisasi").val();
  var kegiatan = $("#kegiatan").val();
  var triwul   = $("#triwulan").val();
  var jenis    = $("#perubahan").val();

  if(triwul == 0){
      $.alertable.alert("Triwulan belum dipilih!"); return false;
  } else if(triwul > 0 && jenis >= 0){

      $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabel,
        data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kegiatan:kegiatan, asal:asal},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
          $('#tabel_datasp2d').html(response);
          getSumberDana_BARJAS();
          getPotongan_sp2d(asal);
          $(".cover").hide();
        }
      });
  }
}

function getSumberDana_BARJAS(){
  var nospm    = $("#no_spm_x").val();
  var nosp2d   = $("#no_sp2d").val();
  var tanggal  = $("#tgl_sp2d").val();
  var skpd     = $("#organisasi").val();
  var kegiatan = $("#kegiatan").val();
  var kdrek    = $("#kd_rekening").val();
  var aksi     = $('input[name="aksi"]').val();
  var sumber   = "";

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sumda,
      data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kegiatan:kegiatan, kdrek:kdrek, aksi:aksi},
      async: false,
      dataType: "json",
      success: function (hasil) {
        $('input[name="kd_sumberdana"]').val(hasil['KD_SUMBERDANA']);
        $('input[name="nm_sumberdana"]').val(hasil['NM_SUMNERDANA']);
        reksumDana_BARJAS(hasil['KD_SUMBERDANA']);
      }
  });

  function reksumDana_BARJAS(kode){
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_reken,
        data: {kode:kode},
        async: false,
        dataType: "html",
        timeout: 10000,
        success: function(response){
            $('#norek_bankasal').html(response);
            PilihRekening_sp2d();
        }
    });
  }
}

function loadDataSP2D_BARJAS(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sp2d,
      data: {skpd:skpd, nosp2d:nosp2d},
      async: false,
      dataType: "json",
      success: function (hsl) {

        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        $('#kunci_sp2d').text(hsl['KUNCI']);
        $("#tgl_sp2d").val(hsl['TANGGAL']);
        $("#tgl_spm").val(hsl['TGLSPM']);
        $("#no_spm").val(hsl['NOSPM']);
        $("#no_spm_x").val(hsl['NOSPM']);
        $('#status_keperluan').val(hsl['DESKRIPSISPM']);

        loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
        loadPertama('btn_hapus',hsl['BTN_HAPUS']);

        $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
        $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
        $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
        $('input[name="bank_bendahara"]').val(hsl['BANK']);
        $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
        $('input[name="inpt_triwulan"]').val(hsl['TRIWULAN']); 
        $('#triwulan').val(hsl['TRIWULAN']);
        $('#perubahan').val(hsl['PERUBAHAN']); 
        $('input[name="inpt_perubahan"]').val(hsl['PERUBAHAN']);

        loadTabelAfektasi_BARJAS('sp2d');

        $("#bank_asal").val(hsl['BANKASAL']); 
        $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

        if(hsl['LOCKED'] == 'Y'){ 
            $.alertable.alert(hsl['PESAN']); 
            $('#kunci_sp2d').addClass('disetujui');
            $('#src_kegiatan').css('pointer-events','none');
        } else {
            $('#kunci_sp2d').removeClass('disetujui');
            $('#src_kegiatan').css('pointer-events','');
        }

        set_IsLocked(hsl['LOCKED']);
      }
  });
}

function loadDataSPM_BARJAS(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd},
      async: false,
      success: function(msg){ 

        $('input[name="no_spm_x"]').val(msg['nmrspm']); 
        $('input[name="tgl_spm"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        loadTabelAfektasi_BARJAS('spm');
        $("#no_sp2d").focus();
      }
  });
}

function SaveSP2D_BARJAS(){
    var frm      = $("#myForm");
    var aksi     = $("#aksi").val();
    var skpd     = $("#organisasi").val();
    var nosp2d   = $("#no_sp2d").val();
    var nosp2dX  = $("#no_sp2d_x").val();
    var kegiatan = $("#kegiatan").val();
    var nospm    = $("#no_spm").val();
    var ktrngn   = $("#status_keperluan").val()
    var bendahr  = $("#bendahara").val();
    var norek    = $("#norek_bendahara").val();
    var tanggal  = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
    var CKsp2d   = cekNoSp2d(nosp2d);
    var ceked    = [];
    var arrMsg   = [];
    var batas, jumlah;

    function cekValid(){
      // cek afektasi 
      $(".afektasichk:checked").each(function(){
          var pelyu = $(this).attr("alt"); 
          ceked.push(pelyu);

          var row   = $('#dataTable_sp2d td').closest("tr"); 
          otorisasi = toAngka(row.children('td.otorisasi'+pelyu).text());
          anggaran  = toAngka(row.children('td.anggaran'+pelyu).text());
          batas     = toAngka(row.children('td.batas'+pelyu).text());
          jumlah    = toAngka(row.children('td.lalu'+pelyu).text()) + toAngka($('#input_tbl'+pelyu).val());
          rekening  = row.children('td.kode'+pelyu).text()+" "+row.children('td.urai'+pelyu).text();

          cekValidasi(rekening,otorisasi,jumlah,batas,anggaran);

      });
    }

    if(aksi == "true"){
        if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
    } else {
        if(nosp2d != nosp2dX){
          if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
        }
    }

    if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(kegiatan == ""){
        $.alertable.alert("Kegiatan harus diisi terlebih dahulu!"); return false;
    } else if(nosp2d == ""){
        $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
    } else if(nospm == ""){
        $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
    } else if(ktrngn == ""){
        $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
    } else if(bendahr == ""){
        $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
    } else if(norek == ""){
        $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(!tanggal){
        $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
    } else {
        cekValid();
        if(ceked.length == 0){ $.alertable.alert("Data Afektasi belum ada yang dipilih !"); return false; } 
        else if(cekSukses){ return false;}
        else {
          $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                  
                  if(x['issimpan'] >= 1){
                    $("#no_sp2d_x").val(nosp2d);
                    isSimpan = false;
                    $('input[name="aksi"]').val(isSimpan);
                    loadPertama('btn_hapus','1');
                    loadDataSP2D_BARJAS();
                    if(!isCetak){ cetak_lap_sp2d_barjas();}
                  }
                  $.alertable.alert(x['pesan']);
                }
            });
          }, function() {
              message_ok('error', 'Simpan data '+nosp2d+' dibatalkan!');
          });
        }
    }
}

function Del_sp2d_BARJAS(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi Belum dipilih !"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Data SP2D belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2D Dengan Nomor '+nosp2d+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2d:nosp2d},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_BARJAS(); }
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!');
      });
  }
}

function lap_sp2d_barjas(){
  var posisi = $("#btn_simpan").is("[disabled]");

  if(posisi){
      if(cekSukses){
          isCetak = false;
          SaveSP2D_BARJAS();
      } else {
          isCetak = posisi;
          cetak_lap_sp2d_barjas();
      }
  } else {
      isCetak = false;
      SaveSP2D_BARJAS();
  }
}

function cetak_lap_sp2d_barjas(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(skpd == ""){ 
    $.alertable.alert("Data Organisasi belum dipilih !"); return false; 
  } else if(nosp2d == ""){ 
    $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2d_barjas'); 
  }
}

// JS SP@D GAJI [GJ] Joel - 6 Feb 2019 ==================================================================

function clearForm_GJ(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2d").val('');
  $("#no_sp2d_x").val('');
  $("#tgl_sp2d").val(DateNowInd());
  $("#tgl_spm").val(DateNowInd());
  $('#kunci_sp2d').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  $('input[name="inpt_triwulan"]').val($("#triwulan").val());
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());
  getTriwulan('#tgl_sp2d','#triwulan');

  $('#kunci_sp2d').removeClass('disetujui');
  $('#tgl_sp2d').attr('disabled',false);
  set_IsLocked('awal');

  loadTabelAfektasi_GJ('sp2d');

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();

}

function loadTabelAfektasi_GJ(asal){
  var nospm   = $("#no_spm").val();
  var nosp2d  = $("#no_sp2d_x").val();
  var tanggal = $("#tgl_sp2d").val();
  var skpd    = $("#organisasi").val();

  var triwul  = $("#triwulan").val();
  var jenis   = $("#perubahan").val();

  if(triwul == 0){
      $.alertable.alert("Triwulan belum dipilih!"); return false;
  } else if(triwul > 0 && jenis >= 0){

      $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabel,
        data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, asal:asal},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
          $('#tabel_datasp2d').html(response);
          getSumberDana_gaji();
          getPotongan_sp2d(asal);
          $(".cover").hide();
        }
      });
  }
}

function getPotongan_sp2d(asal){
  var nospm   = $("#no_spm").val();
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d").val();

  $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    type: "POST",
    url: link_tbl_pot,
    data: {skpd:skpd, nospm:nospm, nosp2d:nosp2d, asal:asal},
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){
      $('#tabel_potongansp2d').html(response);
    }
  });
}

function getSumberDana_gaji(){
  var nospm   = $("#no_spm_x").val();
  var nosp2d  = $("#no_sp2d").val();
  var tanggal = $("#tgl_sp2d").val();
  var skpd    = $("#organisasi").val();
  var kdrek   = $("#kd_rekening").val();
  var aksi    = $('input[name="aksi"]').val();
  var sumber  = "";

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sumda,
      data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kdrek:kdrek, aksi:aksi},
      async: false,
      dataType: "json",
      success: function (hasil) {
        $('input[name="kd_sumberdana"]').val(hasil['KD_SUMBERDANA']);
        $('input[name="nm_sumberdana"]').val(hasil['NM_SUMNERDANA']);
        reksumDana_gaji(hasil['KD_SUMBERDANA']);
      }
  });

  function reksumDana_gaji(kode){
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_reken,
        data: {kode:kode},
        async: false,
        dataType: "html",
        timeout: 10000,
        success: function(response){
            $('#norek_bankasal').html(response);
            PilihRekening_sp2d();
        }
    });
  }
}

function loadDataSP2D_gaji(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sp2d,
      data: {skpd:skpd, nosp2d:nosp2d},
      async: false,
      dataType: "json",
      success: function (hsl) {

        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        $('#kunci_sp2d').text(hsl['KUNCI']);
        $("#tgl_sp2d").val(hsl['TANGGAL']);
        $("#tgl_spm").val(hsl['TGLSPM']);
        $("#no_spm").val(hsl['NOSPM']);
        $("#no_spm_x").val(hsl['NOSPM']);
        $('#status_keperluan').val(hsl['DESKRIPSISPM']);

        loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
        loadPertama('btn_hapus',hsl['BTN_HAPUS']);

        $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
        $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
        $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
        $('input[name="bank_bendahara"]').val(hsl['BANK']);
        $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
        $('input[name="inpt_triwulan"]').val(hsl['TRIWULAN']); 
        $('#triwulan').val(hsl['TRIWULAN']);
        $('#perubahan').val(hsl['PERUBAHAN']); 
        $('input[name="inpt_perubahan"]').val(hsl['PERUBAHAN']);

        loadTabelAfektasi_GJ('sp2d');

        $("#bank_asal").val(hsl['BANKASAL']); 
        $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

        if(hsl['LOCKED'] == 'Y'){ 
            $.alertable.alert(hsl['PESAN']); 
            $('#kunci_sp2d').addClass('disetujui');
        } else {
            $('#kunci_sp2d').removeClass('disetujui');
        }

        set_IsLocked(hsl['LOCKED']);
      }
  });
}

function loadDataSPM_gaji(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd},
      async: false,
      success: function(msg){ 

        $('input[name="no_spm_x"]').val(msg['nmrspm']); 
        $('input[name="tgl_spm"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        loadTabelAfektasi_GJ('spm');
        $("#no_sp2d").focus();
      }
  });
}

function SaveSP2D_gaji(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var skpd    = $("#organisasi").val();
    var nosp2d  = $("#no_sp2d").val();
    var nosp2dX = $("#no_sp2d_x").val();
    var nospm   = $("#no_spm").val();
    var ktrngn  = $("#status_keperluan").val()
    var bendahr = $("#bendahara").val();
    var norek   = $("#norek_bendahara").val();
    var tanggal = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
    var CKsp2d  = cekNoSp2d(nosp2d);
    var ceked   = [];
    var arrMsg  = [];
    var batas, jumlah;

    function cekValid(){
      // cek afektasi 
      $(".afektasichk:checked").each(function(){
          var pelyu = $(this).attr("alt"); 
          ceked.push(pelyu);

          var row   = $('#dataTable_sp2d td').closest("tr"); 
          otorisasi = toAngka(row.children('td.otorisasi'+pelyu).text());
          anggaran  = toAngka(row.children('td.anggaran'+pelyu).text());
          batas     = toAngka(row.children('td.batas'+pelyu).text());
          jumlah    = toAngka(row.children('td.lalu'+pelyu).text()) + toAngka($('#input_tbl'+pelyu).val());
          rekening  = row.children('td.kode'+pelyu).text()+" "+row.children('td.urai'+pelyu).text();

          cekValidasi(rekening,otorisasi,jumlah,batas,anggaran);
      });
    }

    if(aksi == "true"){
        if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
    } else {
        if(nosp2d != nosp2dX){
          if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
        }
    }

    if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(nosp2d == ""){
        $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
    } else if(nospm == ""){
        $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
    } else if(ktrngn == ""){
        $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
    } else if(bendahr == ""){
        $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
    } else if(norek == ""){
        $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(!tanggal){
        $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
    } else {
      cekValid();
      if(ceked.length == 0){ $.alertable.alert("Data Afektasi belum ada yang dipilih !"); return false; }
      else if(cekSukses){ return false; } 
      else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                  if(x['issimpan'] >= 1){
                    $("#no_sp2d_x").val(nosp2d);
                    isSimpan = false;
                    $('input[name="aksi"]').val(isSimpan);
                    loadPertama('btn_hapus','1');
                    loadDataSP2D_gaji();
                    if(!isCetak){ cetak_lap_sp2d_gaji();}
                  }
                  $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data '+nosp2d+' dibatalkan!');
        });
      }
    }
}

function Del_sp2d_gaji(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi Belum dipilih !"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Data SP2D belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2D Dengan Nomor '+nosp2d+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2d:nosp2d},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_GJ(); }
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!');
      });
  }
}

function lap_sp2d_gaji(){
  var posisi = $("#btn_simpan").is("[disabled]");

  if(posisi){
      if(cekSukses){
          isCetak = false;
          SaveSP2D_gaji();
      } else {
          isCetak = posisi;
          cetak_lap_sp2d_gaji();
      }
  } else {
      isCetak = false;
      SaveSP2D_gaji();
  }
}

function cetak_lap_sp2d_gaji(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(skpd == ""){ 
    $.alertable.alert("Data Organisasi belum dipilih !"); return false; 
  } else if(nosp2d == ""){ 
    $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2d_gaji'); 
  }
}

// JS SP2D NON ANGGARAN (BTL NON ANGG) JOEL 14 Feb 2019 =========================================================

function clearForm_NONA(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2d").val('');
  $("#no_sp2d_x").val('');
  $("#tgl_sp2d").val(DateNowInd());
  $("#tgl_spm").val(DateNowInd());
  $('#kunci_sp2d').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());

  $('#kunci_sp2d').removeClass('disetujui');
  $('#tgl_sp2d').attr('disabled',false);
  set_IsLocked('awal');

  loadTabelAfektasi_NONA('sp2d');

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();

}

function loadTabelAfektasi_NONA(asal){
  var nospm    = $("#no_spm").val();
  var nosp2d   = $("#no_sp2d_x").val();
  var tanggal  = $("#tgl_sp2d").val();
  var skpd     = $("#organisasi").val();
  var jenis    = $("#perubahan").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi masih kosong!"); return false;
  } else {

    $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_tabel,
      data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, asal:asal},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(response){
        $('#tabel_datasp2d').html(response);
        getSumberDana_NONA();
        $(".cover").hide();
      }
    });
  }
}

function getSumberDana_NONA(){
  var nospm    = $("#no_spm_x").val();
  var nosp2d   = $("#no_sp2d").val();
  var tanggal  = $("#tgl_sp2d").val();
  var skpd     = $("#organisasi").val();
  var kdrek    = $("#kd_rekening").val();
  var aksi     = $('input[name="aksi"]').val();
  var sumber   = "";

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sumda,
      data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kdrek:kdrek, aksi:aksi},
      async: false,
      dataType: "json",
      success: function (hasil) {
        $('input[name="kd_sumberdana"]').val(hasil['KD_SUMBERDANA']);
        $('input[name="nm_sumberdana"]').val(hasil['NM_SUMNERDANA']);
        reksumDana_NONA(hasil['KD_SUMBERDANA']);
      }
  });

  function reksumDana_NONA(kode){
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_reken,
        data: {kode:kode},
        async: false,
        dataType: "html",
        timeout: 10000,
        success: function(response){
            $('#norek_bankasal').html(response);
            PilihRekening_sp2d();
        }
    });
  }
}

function loadDataSP2D_NONA(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sp2d,
      data: {skpd:skpd, nosp2d:nosp2d},
      async: false,
      dataType: "json",
      success: function (hsl) {

        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        $('#kunci_sp2d').text(hsl['KUNCI']);
        $("#tgl_sp2d").val(hsl['TANGGAL']);
        $("#tgl_spm").val(hsl['TGLSPM']);
        $("#no_spm").val(hsl['NOSPM']);
        $("#no_spm_x").val(hsl['NOSPM']);
        $('#status_keperluan').val(hsl['DESKRIPSISPM']);

        loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
        loadPertama('btn_hapus',hsl['BTN_HAPUS']);

        $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
        $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
        $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
        $('input[name="bank_bendahara"]').val(hsl['BANK']);
        $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
        $('#perubahan').val(hsl['PERUBAHAN']); 
        $('input[name="inpt_perubahan"]').val(hsl['PERUBAHAN']);

        loadTabelAfektasi_NONA('sp2d');

        $("#bank_asal").val(hsl['BANKASAL']); 
        $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

        if(hsl['LOCKED'] == 'Y'){ 
            $.alertable.alert(hsl['PESAN']); 
            $('#kunci_sp2d').addClass('disetujui');
        } else {
            $('#kunci_sp2d').removeClass('disetujui');
        }

        set_IsLocked(hsl['LOCKED']);
      }
  });
}

function loadDataSPM_NONA(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd},
      async: false,
      success: function(msg){ 

        $('input[name="no_spm_x"]').val(msg['nmrspm']); 
        $('input[name="tgl_spm"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        loadTabelAfektasi_NONA('spm');
        $("#no_sp2d").focus();
      }
  });
}

function SaveSP2D_NONA(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var skpd    = $("#organisasi").val();
    var nosp2d  = $("#no_sp2d").val();
    var nosp2dX = $("#no_sp2d_x").val();
    var nospm   = $("#no_spm").val();
    var ktrngn  = $("#status_keperluan").val()
    var bendahr = $("#bendahara").val();
    var norek   = $("#norek_bendahara").val();
    var tanggal = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
    var CKsp2d  = cekNoSp2d(nosp2d);
    var ceked   = [];
    var arrMsg  = [];
    var batas, jumlah;

    if(aksi == "true"){
        if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
    } else {
        if(nosp2d != nosp2dX){
          if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
        }
    }

    $(".afektasichk:checked").each(function(){
        var pelyu = $(this).attr("alt"); 
        ceked.push(pelyu);
    });

    if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(nosp2d == ""){
        $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
    } else if(nospm == ""){
        $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
    } else if(ktrngn == ""){
        $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
    } else if(bendahr == ""){
        $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
    } else if(norek == ""){
        $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(!tanggal){
        $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
    } else if(ceked.length == 0){
        $.alertable.alert("Data Afektasi belum ada yang dipilih !"); return false;
    } else if(cekSukses){
        return false;
    } else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                  if(x['issimpan'] >= 1){
                    $("#no_sp2d_x").val(nosp2d);
                    isSimpan = false;
                    $('input[name="aksi"]').val(isSimpan);
                    loadPertama('btn_hapus','1');
                    loadDataSP2D_NONA();
                    if(!isCetak){ cetak_lap_sp2d_NONA();}
                  }
                  $.alertable.alert(x['pesan']);
                }
            });

        }, function() {
            message_ok('error', 'Simpan data '+nosp2d+' dibatalkan!');
        });
    }
}

function Del_sp2d_NONA(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi Belum dipilih !"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Data SP2D belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2D Dengan Nomor '+nosp2d+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2d:nosp2d},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_NONA(); }
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!');
      });
  }
}

function lap_sp2d_NONA(){
  var posisi = $("#btn_simpan").is("[disabled]");

  if(posisi){
      if(cekSukses){
          isCetak = false;
          SaveSP2D_NONA();
      } else {
          isCetak = posisi;
          cetak_lap_sp2d_NONA();
      }
  } else {
      isCetak = false;
      SaveSP2D_NONA();
  }
}

function cetak_lap_sp2d_NONA(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(skpd == ""){ 
    $.alertable.alert("Data Organisasi belum dipilih !"); return false; 
  } else if(nosp2d == ""){ 
    $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2d_nona'); 
  }
}


// // JS SP2D UP =================================================================================================================

// function pageLoadSP2D_UP(){
//   PilihRekening_sp2d();
//   clearFormSP2D_UP(0);
// }

// function clearFormSP2D_UP(skpd){
//   isPemberitahuan = false;
//   isSimpan = true;
//   $('input[name="aksi"]').val(isSimpan);

//   $("#organisasi").val(skpd);
//   $("#no_sp2d").val('');
//   $("#no_sp2d_x").val('');
//   $('#kunci_sp2d').html('(DRAFT)');
//   $("#tgl_sp2d").val(DateNowInd());
//   $("#jumlah_sp2d").val('0,00');
//   OnBlur_sp2d();
//   $("#no_spm").val('');
//   $("#no_spm_x").val('');
//   $("#tgl_spm").val(DateNowInd());
//   $('#status_keperluan').val('');
//   $("#bendahara").val('');
//   $("#norek_bendahara").val('');
//   $("#bank_bendahara").val('');
//   $("#npwp_bendahara").val('');

//   loadPertama('btn_simpan','1');
//   loadPertama('btn_cetak','-1');
//   loadPertama('btn_hapus','-1');
// }

// function loadSKPD_sp2d_UP(){
//   var skpd  = $("#organisasi").val();

//     $.ajax({
//       type: 'POST',
//       url: baseUrl+"index.php?route=sp2d/modal_sp2d/cek_data_sp2d",
//       data: {skpd:skpd, form:route},
//       beforeSend: function(){ $(".cover").show(); },
//       success: function(dt){
//         if(dt <= 0){ 
//             clearFormSP2D_UP(skpd);
//             cekSK_UP(skpd); 
//             $("#no_sp2d").val(getNewNoSP2D(skpd,'UP')); 
//         } else {
//             ambil_UP(skpd);
//             $.alertable.alert("SP2D sudah dibuat, UP hanya sekali dalam satu tahun.");
//         }
//         $(".cover").hide();
//       }
//     });
// }

// function cekSK_UP(skpd){
//   $.ajax({
//     type: 'POST',
//     url: baseUrl+"index.php?route=sp2d/modal_sp2d/cek_skup",
//     data: {skpd:skpd, form:route},
//     success: function(dt){
//       $("#jumlah_sp2d").val(toRp(dt));
//       $("#jml_sp2d").html(toRp(dt)); 
//       $("#sp2d_terbilang").html(terbilang(dt,3));
//     }
//   });
// }

// function ambil_UP(skpd){
//   $.ajax({
//     type: 'POST',
//     dataType: "json",
//     url: baseUrl+"index.php?route=sp2d/modal_sp2d/ambil_up",
//     data: {skpd:skpd, form:route},
//     success: function(dt){
//       getDataSP2D_UP(dt['SKPD'],dt['NOSP2D']);
//     }
//   });
// }

// function getDataSP2D_UP(skpd,sp2d){

//   $.ajax({
//     type: 'POST',
//     dataType: "json",
//     url: baseUrl+"index.php?route=sp2d/up/get_sp2d_up",
//     data: {skpd:skpd, nosp2d:sp2d, form:route},
//     success: function(hsl){

//         isSimpan = false;
//         $('input[name="aksi"]').val(isSimpan);
//         $("#no_sp2d").val(hsl['NOSP2D']);
//         $("#no_sp2d_x").val(hsl['NOSP2D']);
//         $('#kunci_sp2d').text(hsl['KUNCI']);
//         $("#tgl_sp2d").val(hsl['TANGGAL']);
//         $("#tgl_spm").val(hsl['TGLSPM']);
//         $("#no_spm").val(hsl['NOSPM']);
//         $("#no_spm_x").val(hsl['NOSPM']);
//         $('#status_keperluan').val(hsl['DESKRIPSISPM']);

//         $("#jumlah_sp2d").val(hsl['JUMLAHSP2D']);
//         OnBlur_sp2d();

//         loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
//         loadPertama('btn_hapus',hsl['BTN_HAPUS']);
//         loadPertama('btn_cetak','1');

//         $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
//         $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
//         $('input[name="bank_bendahara"]').val(hsl['BANK']);
//         $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
//         $("#bank_asal").val(hsl['BANKASAL']); 
//         $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

//         if(hsl['LOCKED'] == 'Y'){ $.alertable.alert(hsl['PESAN']); } else {
//           if(isPemberitahuan){
//             $.alertable.alert("SP2D sudah dibuat. Anda hanya diperkenankan untuk merubah");
//           }
//         }
//     }
//   });
// }

// function loadDataSPM_up(){
//   var skpd  = $("#organisasi").val();
//   var nospm = $("#no_spm").val();

//   $.ajax({
//     type: 'POST',
//     dataType: "json",
//     url: baseUrl+"index.php?route=sp2d/up/load_spm",
//     data: {skpd:skpd, nospm:nospm, form:route},
//     success: function(hsl){

//       $("#no_spm").val(hsl['NOSPM']);
//       $("#no_spm_x").val(hsl['NOSPM']);
//       $("#tgl_spm").val(hsl['TANGGAL']);
//       $("#jumlah_sp2d").val(hsl['JUMLAHSPM']);
//       $('#status_keperluan').val(hsl['INFORMASI']);
//       $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
//       $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
//       $('input[name="bank_bendahara"]').val(hsl['BANK']);
//       $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 

//       OnBlur_sp2d();
//     }
//   });
// }

// function SimpanSP2D_up(){

//   var frm     = $("#myForm");
//   var aksi    = $("#aksi").val();
//   var skpd    = $("#organisasi").val();
//   var nosp2d  = $("#no_sp2d").val();
//   var nosp2dX = $("#no_sp2d_x").val();
//   var nospm   = $("#no_spm").val();
//   var status  = $('#status_keperluan').val();
//   var bendahr = $('input[name="bendahara"]').val();
//   var tanggal = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
//   var CKsp2d  = cekNoSp2d(nosp2d);



//   if(aksi == "true"){ 
//       if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
//   } else {
//       if(nosp2d != nosp2dX){
//         if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
//       }
//   }

//   if(skpd == 0){
//       $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
//   } else if(nosp2d == ""){
//       $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
//   } else if(nospm == ""){
//       $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
//   } else if(status == ""){
//       $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
//   } else if(bendahr == ""){
//       $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
//   } else if(!tanggal){
//       $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
//   } else {
//       alertify.confirm('Anda yakin akan menyimpan data?', function (e) {
//         if (e) {
//           $.ajax({
//               type: frm.attr('method'),
//               url: frm.attr('action'),
//               data: frm.serialize(),
//               success: function (data) {
//                 getDataSP2D_UP(skpd,nosp2d);
//                 $.alertable.alert('Data SP2D - UP berhasil disimpan');
//               }
//           });

//         } else { message_ok('error', 'Simpan data SP2D - UP dibatalkan!'); }
//       });
//   }
// }

// function DelSP2D_up(url){
//   var skpd    = $("#organisasi").val();
//   var nosp2d  = $("#no_sp2d_x").val();

//   if(skpd == ""){
//       $.alertable.alert("Organisasi Belum dipilih !"); return false;
//   } else if(nosp2d == ""){
//       $.alertable.alert("Data SP2D belum dipilih !"); return false;
//   } else {
//       alertify.confirm("Apakah anda Yakin Untuk Menghapus Data SP2D Dengan no. "+nosp2d+" ?", function (e) {
//         if (e){
//             $.ajax({
//                 type: 'POST',
//                 url: url,
//                 data: {skpd:skpd, nosp2d:nosp2d},
//                 success: function (data) {
//                     pageLoadSP2D_UP();
//                     $.alertable.alert('Data SP2D Dengan no. '+nosp2d+', berhasil dihapus');
//                 }
//             });
  
//         } else { message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!'); }
//       });
//   }
// }




// JS LAPORAN SP2D ============================================================================================================

function getLapDataPejabat(){
	var data  = $("#pejabat").val().split("|");

  $("#id_pejabat").val(data[0]);
	$("#nama_pejabat").val(data[1]);
	$("#nip_pejabat").val(data[2]);
	$("#pangkat_pejabat").val(data[3]);
}

// function getCekedPPKD(){
//   var ceked = $("#skpkd_checked").is(":checked");

//   if(ceked){
//       $('input[name="is_skpkd"]').val('1');
//   } else {
//       $('input[name="is_skpkd"]').val('0');
//   }
// }



// function pilihSKPDLaporan(){
//   var isSKPKD = $("#organisasi option:selected").attr("alt");
//   var jnsLap  = $("#jns_laporan").val();
//   var felyu   = $("#organisasi option:selected").attr("mydata").split("|");

//   $('input[name="kd_urusan"]').val(felyu[0]);
//   $('input[name="kd_suburusan"]').val(felyu[1]);
//   $('input[name="kd_organisasi"]').val(felyu[2]);
//   $('input[name="urai_organisasi"]').val(felyu[3]);

//   $("#kode_bidang").val('');
//   $("#kode_program").val('');
//   $("#kode_kegiatan").val('');
//   $("#urai_kegiatan").val('');
//   $('#skpkd_checked').prop('checked', false);

//   if(jnsLap == 3 || jnsLap == 4 || jnsLap == 12){
//       if(isSKPKD == 1){
//           $('#cek_ppkd').css('display','');
//       } else { $('#cek_ppkd').css('display','none'); }
//   } else { $('#cek_ppkd').css('display','none'); }
// }

// function lapPilihSumDana(){
//   var kode = $("#sumber_dana option:selected").text();
//   $('input[name="urai_sumberdana"]').val(kode);
// }

// function setLapJenisSPJ(){
//   var jnsspj = $("#jenis_spj option:selected").attr("alt"); 
//   var jenis  = "";

//   if(jnsspj == 0){ jenis  = "SEMUA"; }
//   else if(jnsspj == 1){ jenis  = "GU"; } 
//   else if(jnsspj == 2){ jenis  = "TU"; }

//   $('input[name="id_jenis_spj"]').val(jenis);
// }

// function cetakLaporanSP2D(){

//   var frm       = $("#myForm");
//   var jnslap    = $("#jns_laporan").val();
//   var skpd      = $("#organisasi").val();
//   var kegiatan  = $("#urai_kegiatan").val();

//   getCekedPPKD();
//   lapPilihSumDana();
//   setLapJenisSPJ();
//   setPPKDtoSKPD(jnslap);

//   if(jnslap == 2 || jnslap == 3 || jnslap == 4 || jnslap == 5 || jnslap == 12 || jnslap == 14 || 
//     jnslap == 17 || jnslap == 18 || jnslap == 19 || jnslap == 20 || jnslap == 21){
//       if(skpd == 0){
//           $.alertable.alert("Organisasi belum dipilih !"); return false;
//       } else if(jnslap == 5 && kegiatan == ""){
//           $.alertable.alert("Kegiatan belum dipilih"); return false;
//       } else { cetak(); }

//   } else {
//       cetak();
//   }

//   function cetak(){
//     $.ajax({
//       type: frm.attr('method'),
//       url: frm.attr('action'),
//       data: frm.serialize(),
//       async: false,
//       timeout: 10000,
//       success: function(res){
//         ShowIframeReport(res, "Report SP2D");
//       }
//     });
//   }

//   function setPPKDtoSKPD(jenis){
//     if(jenis == 6 || jenis == 7 || jenis == 8 || jenis == 9){
//         var skpkd = $("#skpkd").val().split("|");

//         $('input[name="kd_urusan"]').val(skpkd[0]);
//         $('input[name="kd_suburusan"]').val(skpkd[1]);
//         $('input[name="kd_organisasi"]').val(skpkd[2]);
//         $('input[name="urai_organisasi"]').val(skpkd[3]);
//     }
//   }
// }

// PERSETUJUAN SP2D - JOEL 27 Jan 2019 ==========================================================
function load_draft_sp2d(e){

  if(e != ''){
      var tgl = $('#per_tgl_sp2d').val();
  } else {
      var tgl = $('#tabel_persetujuan').attr('alt');
  }

  var usr = $('#us_skpd').val();

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_draft_sp2d,
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
function load_draft_advis_sp2d(){
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
    url: link_advis_sp2d,
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

  load_draft_spj_sp2d();
}

function load_draft_spj_sp2d(){
  var skpd = $('#organisasi').val();
  var usr  = $('#us_skpd').val();

  $.ajax({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
    url: link_draft_sp2d,
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

// JS TU NIHIL - joel 18 Apr 2019 =============================================================
// pertama load js......

function clearForm_TUNIHIL(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);
  arrKEG   = [];
  arrREK   = [];

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2d").val('');
  $("#no_sp2d_x").val('');
  $("#no_lpj_skpd").val('');
  $("#no_lpj_skpd_x").val('');
  $("#tgl_sp2d").val(DateNowInd());
  $("#tgl_spm").val(DateNowInd());
  $('#kunci_sp2d').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  $('input[name="inpt_triwulan"]').val($("#triwulan").val());
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());
  $("input[name='kd_sumberdana']").val('');
  $("input[name='nm_sumberdana']").val('');
  getTriwulan('#tgl_sp2d','#triwulan');

  $('#kunci_sp2d').removeClass('disetujui');
  $('#no_sp2d').attr('readonly',false);
  $('#tgl_sp2d').attr('disabled',false);
  $('#src_spm').css('pointer-events','');

  loadTabelAfektasi_TUNIHIL('sp2d');
  PilihRekening_tunihil();
  load_rekening();

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();

}

function loadTabelAfektasi_TUNIHIL(asal){
  var nospm   = $("#no_spm").val();
  var nosp2d  = $("#no_sp2d_x").val();
  var tanggal = $("#tgl_sp2d").val();
  var skpd    = $("#organisasi").val();
  var organ   = $("#organisasi").attr('alt');
  var triwul  = $("#triwulan").val();
  var jenis   = $("#perubahan").val();
  var too;

  if(asal == 'get_sp2d'){ too = 'rekening'; } else { too = 'kegiatan'; }
  if(triwul == 0){
      $.alertable.alert("Triwulan belum dipilih!"); return false;
  } else if(triwul > 0 && jenis >= 0){
      $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabel,
        data: {skpd:skpd, nospm:nospm, nosp2d:nosp2d, tgl:tanggal, too:too, asal:asal},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
          $('#tabel_datasp2d').html(response);
          if(skpd != ""){
            $("#status_keperluan").val("TU NIHIL pada "+organ+" TA. "+Thn_log+", sesuai dengan bukti yang terlampir.");
          } $(".cover").hide();
        }
      });
  }
}

function loadDataSP2D_tuNihil(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    type: "POST",
    url: link_sp2d,
    data: {skpd:skpd, nosp2d:nosp2d},
    async: false,
    dataType: "json",
    success: function (hsl) {

      isSimpan = false;
      $('input[name="aksi"]').val(isSimpan);
      $('#kunci_sp2d').text(hsl['KUNCI']);
      $("#tgl_sp2d").val(hsl['TANGGAL']);
      $("#tgl_spm").val(hsl['TGLSPM']);
      $("#no_spm").val(hsl['NOSPM']);
      $("#no_spm_x").val(hsl['NOSPM']);
      $('#status_keperluan').val(hsl['DESKRIPSISPM']);

      loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
      loadPertama('btn_hapus',hsl['BTN_HAPUS']);

      $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
      $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
      $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
      $('input[name="bank_bendahara"]').val(hsl['BANK']);
      $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
      $('#perubahan').val(hsl['PERUBAHAN']); 
      $('input[name="inpt_perubahan"]').val(hsl['PERUBAHAN']);

      // loadTabelAfektasi_TUNIHIL('get_sp2d');
      loadTabelAfektasi_TUNIHIL('sp2d');

      $("#bank_asal").val(hsl['BANKASAL']); 
      $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

      if(hsl['LOCKED'] == 'Y'){ 
          $.alertable.alert(hsl['PESAN']); 
          $('#kunci_sp2d').addClass('disetujui');
      } else {
          $('#kunci_sp2d').removeClass('disetujui');
      }

      set_IsLocked(hsl['LOCKED']);
      $('#status_keperluan').attr('readonly',true);
      $('#status_keperluan').keydown(function(){ return false });
      get_keg_tunihil();
    }
  });
}

function loadDataSPM_TU_NIHIL(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd},
      async: false,
      success: function(msg){ 

        $("#no_sp2d").val('');
        $("#no_sp2d_x").val('');
        $("#no_lpj_skpd").val('');
        $("#no_lpj_skpd_x").val('');
        
        $('input[name="no_spm_x"]').val(msg['nmrspm']); 
        $('input[name="tgl_spm"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        loadTabelAfektasi_TUNIHIL('spm');
        get_keg_tunihil();
        $("#no_sp2d").focus();
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

function Back_kegiatan_tu_nihil(){
  loadTabelAfektasi_TUNIHIL('{{from}}');
  enable_disable_tabs('1', '0');
  check_kegiatan(arrKEG);
}

function Next_rekening_tu_nihil(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d").val();
  var nospm  = $("#no_spm").val();
  var urai   = $("#uraian_informasi").val();
  var kdKeg  = $("#check_kegiatan").text();
  var tgl    = $("#tgl_spm").val();
  var too    = "rekening";
  var aksi   = $('input[name="aksi"]').val();
  var pilih  = arrKEG.length;

  if(skpd == ""){
    $.alertable.alert("Organisasi masih kosong !"); return false;
  } else if(nosp2d == ""){
    $.alertable.alert("Nomor SP2D masih kosong !"); return false;
  } else if(nospm == ""){
    $.alertable.alert("Nomor SPM masih kosong !"); return false;
  } else if(urai == ""){
    $.alertable.alert("Uraian masih kosong !"); return false;
  } else if(pilih < 1){
    $.alertable.alert("Belum ada kegiatan yang dipilih !"); return false;
  } else {
    $.ajax({
      headers: { 'X-CSRFToken': csrf_token },
      type: 'POST',
      url: link_reken,
      data: {asal:'{{from}}',skpd:skpd,nosp2d:nosp2d,nospm:nospm,tgl:tgl,keg:kdKeg,too:too,aksi:aksi},
      async: false,
      dataType: 'html',
      timeout: 10000,
      beforeSend: function(){ $(".cover").show(); },
      success: function(datax){
        $(".cover").hide();
        $('#tabel_datasp2d').html(datax);
        get_rek_tunihil();
      }
    });
  }
}

function SaveSP2D_TU_NIHIL(){
  var frm     = $("#myForm");
  var aksi    = $("#aksi").val();
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d").val();
  var nosp2dX = $("#no_sp2d_x").val();
  var nospm   = $("#no_spm").val();
  var ktrngn  = $("#status_keperluan").val()
  var bendahr = $("#bendahara").val();
  var norek   = $("#norek_bendahara").val();
  var tanggal = cekTanggal($("#tgl_spm").val(), $("#tgl_sp2d").val());
  var CKsp2d  = cekNoSp2d(nosp2d);
  var ceked   = [];
  var batas, jumlah;

  if(aksi == "true"){
      if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
  } else {
      if(nosp2d != nosp2dX){
        if(CKsp2d){ $.alertable.alert("Nomor SP2D Sudah digunakan!"); return false; }
      }
  }

  $(".chk_rekening:checked").each(function(){
      var pelyu = $(this).attr("value"); 
      ceked.push(pelyu);
  });

  if(skpd == ""){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Nomor SP2D harus diisi terlebih dahulu!"); return false;
  } else if(nospm == ""){
      $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
  } else if(ktrngn == ""){
      $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
  } else if(bendahr == ""){
      $.alertable.alert("Nama Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
  } else if(norek == ""){
      $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
  } else if(!tanggal){
      $.alertable.alert("Tanggal SP2D tidak boleh kurang dari tanggal SPM !"); return false;
  } else if(ceked.length == 0){
      $.alertable.alert("Data Afektasi belum ada yang dipilih !"); return false;
  } else if(cekSukses){
      return false;
  } else {
      $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
          $.ajax({
              type: frm.attr('method'),
              url: frm.attr('action'),
              data: frm.serialize(),
              dataType:"json",
              success: function(x){
                
                if(x['issimpan'] >= 1){
                  $("#no_sp2d_x").val(nosp2d);
                  isSimpan = false;
                  $('input[name="aksi"]').val(isSimpan);
                  loadPertama('btn_hapus','1');
                  loadDataSP2D_tuNihil();
                  if(!isCetak){ cetak_lap_sp2d_TU_NIHIL();}
                }
                $.alertable.alert(x['pesan']);
              }
          });

      }, function() {
          message_ok('error', 'Simpan data '+nosp2d+' dibatalkan!');
      });
  }
}

function Del_sp2d_TU_NIHIL(){
  var skpd    = $("#organisasi").val();
  var nosp2d  = $("#no_sp2d_x").val();

  if(skpd == ""){
      $.alertable.alert("Organisasi Belum dipilih !"); return false;
  } else if(nosp2d == ""){
      $.alertable.alert("Data SP2D belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2D Dengan Nomor '+nosp2d+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2d:nosp2d},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_TUNIHIL(); }
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2d+' dibatalkan!');
      });
  }
}

function lap_sp2d_TU_NIHIL(){
  var posisi = $("#btn_simpan").is("[disabled]");

  if(posisi){
      if(cekSukses){
          isCetak = false;
          SaveSP2D_TU_NIHIL();
      } else {
          isCetak = posisi;
          cetak_lap_sp2d_TU_NIHIL();
      }
  } else {
      isCetak = false;
      SaveSP2D_TU_NIHIL();
  }
}

function cetak_lap_sp2d_TU_NIHIL(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(skpd == ""){ 
    $.alertable.alert("Data Organisasi belum dipilih !"); return false; 
  } else if(nosp2d == ""){ 
    $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2d_tu_nihil'); 
  }
}


