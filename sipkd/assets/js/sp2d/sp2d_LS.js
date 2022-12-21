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
  $('#kodeunit').val('');
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

  $("#frm_sumberdana").val('');
  $("#frm_sumberdana_x").val('');

  $('#kunci_sp2d').removeClass('disetujui');
  $('#tgl_sp2d').attr('disabled',false);
  $('#src_kegiatan').css('pointer-events','');
  set_IsLocked('awal');

  loadTabelAfektasi_BARJAS('sp2d');

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2d").focus();
  get_dataBendahara();

  if($('#organisasi').val() != ''){
      generate_nomor_auto_gu_tu_ls();
    }
}

function loadTabelAfektasi_BARJAS(asal){
  var nospm    = $("#no_spm").val();
  var nosp2d   = $("#no_sp2d_x").val();
  var tanggal  = $("#tgl_sp2d").val();
  var skpd     = $("#organisasi").val();
  var kodeunit = $("#kodeunit").val();
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
        data: {skpd:skpd, kodeunit:kodeunit, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kegiatan:kegiatan, asal:asal},
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
        if (hasil['jml_sumdan'] == 1){
          $('#frm_sumberdana').val(hasil['urai_sumdan__']);
          $('#frm_sumberdana_x').val(hasil['kd_sumdan__']);
        }

        if(hasil['jml_sumdan'] > 1){
          $('#div_button_lookup_sumdan').css('display', '');
          $('#btn_lihat_sumberdana').attr('data-subkeg', $('#kegiatan').val());
          $('#btn_lihat_sumberdana').attr('data-skpd', $('#organisasi').val());
        }else{
          $('#div_button_lookup_sumdan').css('display', 'none');
          $('#btn_lihat_sumberdana').attr('data-subkeg', '');
          $('#btn_lihat_sumberdana').attr('data-skpd', '');
        }
        $('#jml_sumdan__').text(hasil['jml_sumdan'])
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
            // $('#norek_bankasal').html(response);
            PilihRekening_sp2d_barjas();
        }
    });
  }
}

// function getSumberDana_BARJAS(){
//   var nospm    = $("#no_spm_x").val();
//   var nosp2d   = $("#no_sp2d").val();
//   var tanggal  = $("#tgl_sp2d").val();
//   var skpd     = $("#organisasi").val();
//   var kegiatan = $("#kegiatan").val();
//   var kdrek    = $("#kd_rekening").val();
//   var aksi     = $('input[name="aksi"]').val();
//   var sumber   = "";

//   $.ajax({
//       headers: { "X-CSRFToken": csrf_token },
//       type: "POST",
//       url: link_sumda,
//       data: {skpd:skpd, nospm_x:nospm, nosp2d_x:nosp2d, tgl:tanggal, kegiatan:kegiatan, kdrek:kdrek, aksi:aksi},
//       async: false,
//       dataType: "json",
//       success: function (hasil) {
//         $('input[name="kd_sumberdana"]').val(hasil['KD_SUMBERDANA']);
//         $('input[name="nm_sumberdana"]').val(hasil['NM_SUMNERDANA']);
//         reksumDana_BARJAS(hasil['KD_SUMBERDANA']);
//       }
//   });

//   function reksumDana_BARJAS(kode){
//     $.ajax({
//         headers: { "X-CSRFToken": csrf_token },
//         type: "POST",
//         url: link_reken,
//         data: {kode:kode},
//         async: false,
//         dataType: "html",
//         timeout: 10000,
//         success: function(response){
//             // $('#norek_bankasal').html(response);
//             PilihRekening_sp2d_barjas();
//         }
//     });
//   }
// }

function PilihRekening_sp2d_barjas(){
  var rekening = $("#norek_bankasal").val().split("|");
  $("#bank_asal").val(rekening[0]);
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

        if (hsl['SUMBERDANA'].split('|').length > 1) {
          $('#frm_sumberdana').val(hsl['SUMBERDANA'].split('|')[1]);
          $('#frm_sumberdana_x').val(hsl['SUMBERDANA'].split('|')[0]);
        }else{
          $('#frm_sumberdana').val(hsl['SUMBERDANA']);
          $('#frm_sumberdana_x').val('');
        }
      }
  });
}

function loadDataSPM_BARJAS(){
  var nospm = $("#no_spm").val();
  var skpd  = $("#organisasi").val();
  var kdunit = $("#kodeunit").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      dataType:"json",
      url: link_spm_c,
      data: {nospm:nospm, skpd:skpd, kdunit:kdunit},
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

        generate_nomor_auto_gu_tu_ls();
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
    var norekbankasal    = $("#norek_bankasal").val();
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

    if(kegiatan == ""){
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
    } else if(norekbankasal == 'Nama Bank Asal'){
        $.alertable.alert("Bank Asal Masih Kosong"); return false;
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

  if(nosp2d == ""){
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

  //if(posisi){
      //if(cekSukses){
         // isCetak = false;
         // SaveSP2D_BARJAS();
      //} else {
          isCetak = posisi;
          cetak_lap_sp2d_barjas();
      //}
  //} else {
    //  isCetak = false;
     // SaveSP2D_BARJAS();
 // }
}

function cetak_lap_sp2d_barjas(){
  var skpd   = $("#organisasi").val();
  var nosp2d = $("#no_sp2d_x").val();
  var nospm  = $("#no_spm_x").val();

  if(nosp2d == ""){ 
    $.alertable.alert("Data SP2D belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SPM belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2d_barjas'); 
  }
}

function LoadBanknya(e){
  modal_searching(e,'nama_bank'); 
}
