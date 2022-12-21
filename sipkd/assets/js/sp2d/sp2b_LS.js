// JS SP2D BARANG DAN JASA [BARJAS] Joel - 11 Feb 2019 ==================================================================

function render_modal_spm_sp2b_barjas(header,asal,js_arg){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: modal_spm_sp2b,
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


function clearForm_SP2B(){
  isCetak  = true;
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  $("#no_spm").val('');
  $("#no_spm_x").val('');
  $("#no_sp2b").val('');
  $("#no_sp2b_x").val('');
  $('#kodeunit').val('');
  $("#keg_tampilkan").val('');
  $("#kegiatan").val('');
  $("#kegiatan").attr('alt',''); 
  $("#frm_sumberdana").val('');
  $("#frm_sumberdana_x").val('');
  $("#tgl_sp2b").val(DateNowInd());
  $("#tgl_sp3b").val(DateNowInd());
  $('#kunci_sp2b').html('(DRAFT)');
  $('#status_keperluan').val('');
  $("#bendahara").val('');
  $("#norek_bendahara").val('');
  $("#bank_bendahara").val('');
  $("#npwp_bendahara").val('');
  try{
    $('#norek_bankasal').val('Nama Bank Asal');
  }
  catch{
    
  }
  $('input[name="inpt_triwulan"]').val($("#triwulan").val());
  $('input[name="inpt_perubahan"]').val($("#perubahan").val());
  getTriwulan('#tgl_sp2b','#triwulan');

  $('#kunci_sp2b').removeClass('disetujui');
  $('#tgl_sp2b').attr('disabled',false);
  $('#src_kegiatan').css('pointer-events','');
  set_IsLocked('awal');

  loadTabelAfektasi_SP2B('sp2b');

  var skpd = $("#organisasi").val();

  loadPertama('btn_simpan','1');
  loadPertama('btn_hapus','-1');

  $("#no_sp2b").focus();

}

function loadTabelAfektasi_SP2B(asal){
  var nospm    = $("#no_spm").val();
  var nosp2b   = $("#no_sp2b_x").val();
  var tanggal  = $("#tgl_sp2b").val();
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
        data: {skpd:skpd, kodeunit:kodeunit, nospm_x:nospm, nosp2b_x:nosp2b, tgl:tanggal, kegiatan:kegiatan, asal:asal},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
          $('#tabel_datasp2b').html(response);
          // getSumberDana_BARJAS();
          getPotongan_sp2b(asal);
          $(".cover").hide();
        }
      });
  }
}

// function getSumberDana_BARJAS(){
//   var nospm    = $("#no_spm_x").val();
//   var nosp2b   = $("#no_sp2b").val();
//   var tanggal  = $("#tgl_sp2b").val();
//   var skpd     = $("#organisasi").val();
//   var kegiatan = $("#kegiatan").val();
//   var kdrek    = $("#kd_rekening").val();
//   var aksi     = $('input[name="aksi"]').val();
//   var sumber   = "";

//   $.ajax({
//       headers: { "X-CSRFToken": csrf_token },
//       type: "POST",
//       url: link_sumda,
//       data: {skpd:skpd, nospm_x:nospm, nosp2b_x:nosp2b, tgl:tanggal, kegiatan:kegiatan, kdrek:kdrek, aksi:aksi},
//       async: false,
//       dataType: "json",
//       success: function (hasil) {
//         if (hasil['jml_sumdan'] == 1){
//           $('#frm_sumberdana').val(hasil['urai_sumdan__']);
//           $('#frm_sumberdana_x').val(hasil['kd_sumdan__']);
//         }

//         if(hasil['jml_sumdan'] > 1){
//           $('#div_button_lookup_sumdan').css('display', '');
//           $('#btn_lihat_sumberdana').attr('data-subkeg', $('#kegiatan').val());
//           $('#btn_lihat_sumberdana').attr('data-skpd', $('#organisasi').val());
//         }else{
//           $('#div_button_lookup_sumdan').css('display', 'none');
//           $('#btn_lihat_sumberdana').attr('data-subkeg', '');
//           $('#btn_lihat_sumberdana').attr('data-skpd', '');
//         }
//         $('#jml_sumdan__').text(hasil['jml_sumdan'])
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
//             PilihRekening_sp2b();
//         }
//     });
//   }
// }

function PilihRekening_sp2b(){
  var rekening = $("#norek_bankasal").val().split("|");
  $("#bank_asal").val(rekening[0]);
}

function loadDataSP2D_BARJAS(){
  var skpd    = $("#organisasi").val();
  var nosp2b  = $("#no_sp2b_x").val();

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_sp2b,
      data: {skpd:skpd, nosp2b:nosp2b},
      async: false,
      dataType: "json",
      success: function (hsl) {
        console.log(hsl);
        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        $('#kunci_sp2b').text(hsl['KUNCI']);
        $("#tgl_sp2b").val(hsl['TANGGAL']);
        $("#tgl_sp3b").val(hsl['TGLSP3B']);
        $("#no_sp3b").val(hsl['NOSPM']);
        $("#no_spm_x").val(hsl['NOSPM']);
        $('#status_keperluan').val(hsl['URAI']);

        loadPertama('btn_simpan',hsl['BTN_SIMPAN']);
        loadPertama('btn_hapus',hsl['BTN_HAPUS']);

        $('input[name="nm_sumberdana"]').val(hsl['SUMBERDANA']);
        $('input[name="bendahara"]').val(hsl['NAMAYANGBERHAK']);
        $('input[name="norek_bendahara"]').val(hsl['NOREKBANK']);
        $('input[name="bank_bendahara"]').val(hsl['BANK']);
        $('input[name="npwp_bendahara"]').val(hsl['NPWP']); 
        $('input[name="inpt_triwulan"]').val(hsl['TRIWULAN']); 
        $('#triwulan').val(hsl['TRIWULAN']);
        $('#saldo_awal').val(hsl['SALDOAWAL']);
        $('#pendapatan').val(hsl['PENDAPATAN']);
        $('#rekening_pendapatan').val(hsl['KODEREKENING']+'|'+hsl['URAIREKENING']); 
        $('#kode_pendapatan').val(hsl['KODEREKENING']); 
        // $('input[name="pendapatan"]').val(hsl['PERUBAHAN']);

        loadTabelAfektasi_SP2B('sp2b');

        $("#bank_asal").val(hsl['BANKASAL']); 
        $('#norek_bankasal option:contains("'+hsl['NOREKBANKASAL']+'")').prop('selected', true);

        if(hsl['LOCKED'] == 'Y'){ 
            $.alertable.alert(hsl['PESAN']); 
            $('#kunci_sp2b').addClass('disetujui');
            $('#src_kegiatan').css('pointer-events','none');
        } else {
            $('#kunci_sp2b').removeClass('disetujui');
            $('#src_kegiatan').css('pointer-events','');
        }

        set_IsLocked(hsl['LOCKED']);

        // if (hsl['SUMBERDANA'].split('|').length > 1) {
        //   $('#frm_sumberdana').val(hsl['SUMBERDANA'].split('|')[1]);
        //   $('#frm_sumberdana_x').val(hsl['SUMBERDANA'].split('|')[0]);
        // }else{
        //   $('#frm_sumberdana').val(hsl['SUMBERDANA']);
        //   $('#frm_sumberdana_x').val('');
        // }
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
        $('input[name="tgl_sp3b"]').val(msg['tanggal']); 
        $('#status_keperluan').val(msg['info']); 
        $('input[name="norek_bendahara"]').val(msg['norek']);
        $('input[name="bank_bendahara"]').val(msg['bank']);
        $('input[name="npwp_bendahara"]').val(msg['npwp']);
        $('input[name="bendahara"]').val(msg['berhak']); 
        $('input[name="inpt_triwulan"]').val(msg['triwul']);
        $('#triwulan').val(msg['triwul']);

        loadTabelAfektasi_SP2B('spm');
        $("#no_sp2b").focus();
      }
  });
}

function SaveSP2D_BARJAS(){
    var frm      = $("#myForm");
    var aksi     = $("#aksi").val();
    var skpd     = $("#organisasi").val();
    var nosp2b   = $("#no_sp2b").val();
    var nosp2bX  = $("#no_sp2b_x").val();
    var kegiatan = $("#kegiatan").val();
    var nospm    = $("#no_spm").val();
    var ktrngn   = $("#status_keperluan").val()
    var bendahr  = $("#bendahara").val();
    var norek    = $("#norek_bendahara").val();
    var tanggal  = cekTanggal($("#tgl_sp3b").val(), $("#tgl_sp2b").val());
    var CKsp2b   = cekNoSp2d(nosp2b);
    var ceked    = [];
    var arrMsg   = [];
    var batas, jumlah;

    function cekValid(){
      console.log('cuk');
      // cek afektasi 
      $(".afektasichk:checked").each(function(){
          var pelyu = $(this).attr("alt"); 
          ceked.push(pelyu);

          var row   = $('#dataTable_sp2b td').closest("tr"); 
          otorisasi = toAngka(row.children('td.otorisasi'+pelyu).text());
          anggaran  = toAngka(row.children('td.anggaran'+pelyu).text());
          batas     = toAngka(row.children('td.batas'+pelyu).text());
          jumlah    = toAngka(row.children('td.lalu'+pelyu).text()) + toAngka($('#input_tbl'+pelyu).val());
          rekening  = row.children('td.kode'+pelyu).text()+" "+row.children('td.urai'+pelyu).text();

          cekValidasi(rekening,otorisasi,jumlah,batas,anggaran);

      });
    }

    if(aksi == "true"){
        if(CKsp2b){ $.alertable.alert("Nomor SP2B Sudah digunakan!"); return false; }
    } else {
        if(nosp2b != nosp2bX){
          if(CKsp2b){ $.alertable.alert("Nomor SP2B Sudah digunakan!"); return false; }
        }
    }

    if(kegiatan == ""){
        $.alertable.alert("Kegiatan harus diisi terlebih dahulu!"); return false;
    } else if(nosp2b == ""){
        $.alertable.alert("Nomor SP2B harus diisi terlebih dahulu!"); return false;
    } else if(nospm == ""){
        $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
    } else if(ktrngn == ""){
        $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
    } else if(bendahr == ""){
        $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
    } else if(norek == ""){
        $.alertable.alert("Nomor Rekening Bendahara Pengeluaran / Pihak Ketiga belum diisi!"); return false;
    } else if(!tanggal){
        $.alertable.alert("Tanggal SP2B tidak boleh kurang dari tanggal SP3B !"); return false;
    // } else if($('#frm_sumberdana_x').val()==''){
    //   if(parseInt($('#jml_sumdan__').text()) == 0){
    //     message_ok('error', 'Sumberdana Belum Ada, Silahkan Diperbaiki Dahulu !');
    //   }else if(parseInt($('#jml_sumdan__').text()) > 1){
    //     message_ok('error', 'Sumberdana Lebih Dari Satu, Silahkan Diperbaiki Terlebih Dahulu !');
    //   }
    //   $('#frm_sumberdana').focus();
    //   return false;
   
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
                    $("#no_sp2b_x").val(nosp2b);
                    isSimpan = false;
                    $('input[name="aksi"]').val(isSimpan);
                    loadPertama('btn_hapus','1');
                    loadDataSP2D_BARJAS();
                    if(!isCetak){ cetak_lap_sp2b_barjas();}
                  }
                  $.alertable.alert(x['pesan']);
                }
            });
          }, function() {
              message_ok('error', 'Simpan data '+nosp2b+' dibatalkan!');
          });
        }
    }
}

function Del_sp2b_BARJAS(){
  var skpd    = $("#organisasi").val();
  var nosp2b  = $("#no_sp2b_x").val();

  if(nosp2b == ""){
      $.alertable.alert("Data SP2B belum dipilih !"); return false;
  } else {
      $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data SP2B Dengan Nomor '+nosp2b+' ?').then(function(){
          $.ajax({
              headers: { "X-CSRFToken": csrf_token },
              type: 'POST',
              url: frm_aksi,
              data: {skpd:skpd, nosp2b:nosp2b},
              dataType:"json",
              success: function(z){
                if(z['issimpan'] == 0){ clearForm_SP2B(); }
                $.alertable.alert(z['pesan']);
              }
          });
      }, function() {
          message_ok('error', 'Hapus data '+nosp2b+' dibatalkan!');
      });
  }
}

function lap_sp2b_barjas(){
  var posisi = $("#btn_simpan").is("[disabled]");

  //if(posisi){
      //if(cekSukses){
         // isCetak = false;
         // SaveSP2D_BARJAS();
      //} else {
          isCetak = posisi;
          cetak_lap_sp2b_barjas();
      //}
  //} else {
    //  isCetak = false;
     // SaveSP2D_BARJAS();
 // }
}

function cetak_lap_sp2b_barjas(){
  var skpd   = $("#organisasi").val();
  var nosp2b = $("#no_sp2b").val();
  var nospm  = $("#no_spm").val();

  if(nosp2b == ""){ 
    $.alertable.alert("Data SP2B belum dipilih !"); return false; 
  } else if(nospm == ""){ 
    $.alertable.alert("Nomor SP3B belum dipilih !"); return false; 
  } else { 
    showModalLaporan('lap_sp2b'); 
  }
}
function LoadRekeningPendapatan(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModalRekening(e,'rekening_pendapatan',skpd);
  }
}

function showModalRekening(e,modal,skpd){ 
  var url_load  = "";
  var loadModal = "";

  var linkLoad  = $(e).attr('alt');

  switch(modal) { 
    case 'rekening_pendapatan':

      loadModal = "Lihat Sumber Dana TA. "+Thn_log;         
      url_load  = linkLoad+"?organisasi="+skpd;
      break;

  } 
  // document.getElementById("myModalLabel").innerHTML = loadModal;
  // $("#showModal").modal();
  // $(".modal-body-showmodal").load(url_load);
  // $(".modal-dialog").css('width', widthnya);
  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', widthnya);

};
function OnFokus_numbs(e){
  $(e).val(toAngkaDec($(e).val()));
}

function OnBlur_numbs(e){
$(e).val(toRp_WithDecimal($(e).val()));
getTotalCols();
}