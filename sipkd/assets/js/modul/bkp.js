var isSimpan  = true;

function BKP_UPGU_PageLoad(skpd){
  BKP_UPGU_load_data(skpd);

  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

}

function bkp_enable_disable_btn(keg, rek, lpj){

  loadPertama('btn_kegiatan',keg);
  loadPertama('btn_rekening',rek);
  loadPertama('btn_lpjupgu',lpj);

  if(keg == '1'){
      $("#kegiatan_bkp").removeClass('hidden');
      $("#rekening").addClass('hidden');
      $("#lpjupgu").addClass('hidden');
  }

  if(rek == '1'){
      $("#kegiatan_bkp").addClass('hidden');
      $("#rekening").removeClass('hidden');
      $("#lpjupgu").addClass('hidden');
  }

  if(lpj == '1'){
      $("#kegiatan_bkp").addClass('hidden');
      $("#rekening").addClass('hidden');
      $("#lpjupgu").removeClass('hidden');
  }
}

function BKP_UPGU_load_data(skpd){ 
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#tabel_data_bkp").attr("alt"),    
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(response){  
        $('#tabel_data_bkp').html(response);
        $(".cover").hide();
    }
  });
}

function BKP_kembali_kegiatan(){
  $('.kegiatan_bkp').css('display','');
  $('.add_kegiatan_bkp').css('display','none');

  BKP_UPGU_LoadInput();
  BKP_UPGU_AddKegiatan();
}

function BKP_UPGU_LoadInput(){  
  if(isSimpan){    
    BKP_UPGU_getNewNo_in();
  }else{
    BKP_UPGU_ambilNoSPD();  
  }   
  
  var skpd  = $("#organisasi").val();
  $('input[name="skpd"]').val(skpd);
  
  $.ajax({
    type: "POST",
    url: $("#tabel_kegiatan_bkp").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, nopspj:$("#no_pspj").val(), aksi:isSimpan}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){      
        bkp_enable_disable_btn('1', '0', '0');          
        $('#tabel_kegiatan_bkp').html(response);        
    }
  });

  $("#uraian").focus();
}

function BKP_UPGU_ambilNoSPD(){  
  var skpd  = $("#organisasi").val();
  if(isTambah){
    var nopspj = $("#no_pspj").val();
  }else{
    var nopspj = $(".chk_setuju:checked").val();
  }
      
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#url_cek_nospd").attr("alt"),
    data: {skpd:skpd, nopspj:nopspj}, // var route from main-mod.js
    async: false,
    dataType:"json",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(data){        
        $("#no_pspj").val(data['nopspj']);
        $("#no_pspj_old").val(data['nopspj']);
        $("#uraian").val(data['keperluan']); 
        $("#tgl_pspj").val(data['tglpspj']);
        $("#edNoSP2D").val(data['nosp2d']);

        dis_ena_bled('save_kegiatan',1);
        $(".cover").hide();
    }
  });
}

function BKP_UPGU_kegiatan(){
  $('.kegiatan_bkp').css('display','none');
  $('.add_kegiatan_bkp').css('display','');

  BKP_UPGU_AddKegiatan();
}

function BKP_UPGU_AddKegiatan(){
  var skpd  = $("#organisasi").val();  

  $.ajax({
    type: "POST",
    url: $("#tabel_add_kegiatan_bkp").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, nopspj:$("#no_pspj").val(), kondisi:$("#kondisi").val()},
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(response){
        $('#tabel_add_kegiatan_bkp').html(response);
        $(".cover").hide();
    }
  });
}

function BKP_UPGU_Edit(){

  isSimpan = false;
  $('input[name="aksi"]').val(isSimpan);
  isTambah = false;
  $('input[name="isTambah"]').val(isTambah);

  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else if($(".chk_setuju").is(":checked") == false){
      $.alertable.alert("Silahkan pilih data yang akan diedit !");
      return false;
  } else {
    if ($(".chk_setuju:checked").attr("locked") == 'Y') {
      $.alertable.alert("BKP Sudah DiVerfikasi Tidak Diperkenankan Mengedit, Hubungi Bidang Akuntansi !");
      return false;
    }else{
      $('#modalInputBKPUPGU').modal('show');
      BKP_UPGU_LoadInput();
    }
  }
}

function BKP_ModalInput(){
  isSimpan = true;
  isTambah = true;
  $('input[name="aksi"]').val(isSimpan);
  $('input[name="isTambah"]').val(isTambah);

  BKP_UPGU_LoadFormInput();

  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else {
      $('#modalInputBKPUPGU').modal('show');
      $(".modal-dialog").css('width', '90%');
  }
}

function BKP_UPGU_LoadFormInput(){  
  if(isSimpan){ 
      BKP_UPGU_clearForm();
      dis_ena_bled('save_kegiatan',0);
  } else {
      dis_ena_bled('save_kegiatan',1);
  }

  BKP_UPGU_LoadInput();
}

function BKP_UPGU_clearForm(){
  $("#no_pspj").val('');
  $("#uraian").val('');
  $('#tgl_pspj').val(DateNowInd());

  bkp_enable_disable_btn('1', '0', '0');
}

function BKP_UPGU_getNewNo_in(){ 
  var skpd  = $("#organisasi").val();
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: $('#url_getnewnopspj').attr('alt'),
      data: {skpd:skpd},
      async: false,
      success: function(msg){             
        $("#no_pspj").val(msg['nopspj']);
      }
  });
}

function BKP_UPGU_nextDaftarKegiatan(){
  var cekbox  = $(".daftarkegiatan").is(":checked");
  var skpd    = $("#organisasi").val();
  var safetoinsert = false;

  if($("#uraian").val() == ""){
       $.alertable.alert("Uraian PSPJ Belum diisi !");
      return false;
  } else if(!cekbox){
       $.alertable.alert("Belum ada Kegiatan yang dipilih !");
      return false;
  } else {
      var frm  = $('#formModal');
      safetoinsert = true
      
      if (safetoinsert) {
        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            beforeSend: function() {$(".cover").show();},
            success: function (data) {            
              isSimpan = false;
              $('input[name="aksi"]').val(isSimpan);
              BKP_kembali_kegiatan();
              $(".cover").hide();
              BKP_UPGU_load_data(skpd);
            }
        });
      }
  }
}

function BKP_UPGU_nextRekening(){

    var skpd = $("#organisasi").val();
    var nopspj= $("#no_pspj").val();
    var CEHK = [];

    $(".kegiatan:checked").each(function(){ CEHK.push($(this).attr("value")); });

    if(CEHK.length < 1) {
        $.alertable.alert("Anda belum memilih kegiatan yang diLPJ kan!");
        return false;
    } else if(CEHK.length > 1) {
        $.alertable.alert("Untuk membuat LPJ harus per kegiatan!!");
        return false;
    } else {     

        $.ajax({
          type: "POST",
          url: $("#tabel_rekening").attr("alt"),
          headers: { "X-CSRFToken": csrf_token },
          data: {skpd:skpd, nopspj:nopspj, arr:CEHK[0]},
          async: false,
          dataType: "html",
          timeout: 10000,
          beforeSend: function() {$(".cover").show();},
          success: function(response){
              bkp_enable_disable_btn('0', '1', '0');
              $('#tabel_rekening').html(response);
              $(".cover").hide();
          }
        });
    }
}

function BKP_UPGU_nextRinci(){

  var skpd = $("#organisasi").val();
  var nopspj= $("#no_pspj").val();
  var keg  = $("#urai_kegiatan").html();
  var CEHK = [];

  $(".rekening:checked").each(function(){ CEHK.push($(this).attr("value")); });

  if(CEHK.length < 1) {
      $.alertable.alert("Anda belum memilih rekening yang diLPJ kan!");
      return false;
  } else if(CEHK.length > 1) {
      $.alertable.alert("Untuk membuat LPJ harus per rekening!!");
      return false;
  } else {

      $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: $("#tabel_lpjupgu_rinci").attr("alt"),        
        data: {skpd:skpd, nopspj:nopspj, kegiatan:keg, arr:CEHK[0]},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function() {$(".cover").show();},
        success: function(response){
            bkp_enable_disable_btn('0', '0', '1');
            $('#tabel_lpjupgu_rinci').html(response);
            $(".cover").hide();
        }
      });
  }
}

function BKP_UPGU_backToRekening(){
  bkp_enable_disable_btn('0', '1', '0');
  BKP_UPGU_nextRekening();
}

function simpanBKP_UPGU_rinci(){
  var url   = $("#save_lpjupgu").attr('alt');
  var frm   = $('#formModal');
  var sisa  = toAngka($('input[name="sisa_anggaran"]').val());
  var skpd  = $("#organisasi").val();
  
  isSimpan = false;
  $('input[name="aksi"]').val(isSimpan);

  if(sisa < 0){
      $.alertable.alert("Data Total Permohonan LPJ Melebihi Sisa Anggaran");
      return false;
  } else {
      $.alertable.confirm('Anda Yakin ingin menyimpan data rincian Permohonan LPJ UP/GU ?').then(function () {        
        $.ajax({
          type: frm.attr('method'),
          url: url,
          headers: { "X-CSRFToken": csrf_token },
          data: frm.serialize(),
          beforeSend: function() {$(".cover").show();},
          success: function (data) {
            message_ok('success',data);
            
            document.getElementById('sisa_anggaran').value = $('input[name="sisa_anggaran"]').val();
            // BKP_UPGU_load_data(skpd);
            BKP_UPGU_nextRinci();
            isSimpan = false;
            $('input[name="aksi"]').val(isSimpan);
            // BKP_UPGU_PageLoad($('#organisasi').val());
            // isMdl_Potongan = 'true';
            // $('#modalInputBKPUPGU').modal('hide');
            $(".cover").hide();
          }
        });
      },function() { 
        message_ok('error', 'Data rincian Permohonan LPJ UP/GU batal disimpan !');
      });
  }
}

function deleteBKP_UPGU(url){ 
  var jenis = $("#jenis").val();
  var frm = $('#lpjUPGU');
  var pesan = 'LPJ UP/GU';
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else if($(".chk_setuju").is(":checked") == false){
      $.alertable.alert("Silahkan pilih data yang akan dihapus !");
      return false;
  } else {

      var CEHK  = [];
      var CEHK_verif = [];

      $(".chk_setuju:checked").each(function() {
          CEHK.push($(this).attr("value"));
          CEHK_verif.push($(this).attr("locked"));
      });

      for (var i = 0; i < CEHK_verif.length; i++) {
        if (CEHK_verif[i] == 'Y') {
          $.alertable.alert("Terdapat LPJ Yang Sudah DiVerfikasi, Tidak Diperkenankan Menghapus, Silahkan Hubungi Bidang Akuntansi !");
          return false;
        }
      }

      $.alertable.confirm('Anda Yakin ingin menghapus data '+pesan+' : '+CEHK).then(function () {          
          $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            url: url,            
            data: frm.serialize(),
            dataType:"html",            
            success: function(msg){  
              BKP_UPGU_load_data(skpd);
              message_ok('success', msg);   
            }
          });

      },function() { 
        message_ok('error', 'Hapus data '+pesan+' dibatalkan!');
      });
  }
}


function showModal_pspj_bkp(e,modal,number){ 
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');

  switch(modal) { 
    case 'sp2d_mdl_potongan':
      var rowid = $(e).attr('rowid');
      var nobuk = $(e).attr('nobuk').replace(/\//g,'^');
      var tglbuk= $(e).attr('tglbuk').replace(/\ /g,'_');
      var skpd  = $("#organisasi").val();
      var nopspj = $("#no_pspj").val().replace(/\//g,'^');

      loadModal = "Lihat Rekening Potongan TA. "+Thn_log;         
      url_load  = linkLoad+"?i="+rowid+"&b="+encodeURIComponent(nobuk)+"&t="+tglbuk+"&s="+skpd+"&n="+nopspj;
      break;

    case 'sumberdana_kontrak':
      var rowid = $(e).attr('rowid');
      var nobuk = $(e).attr('nobuk').replace(/\//g,'^');
      var tglbuk= $(e).attr('tglbuk').replace(/\ /g,'_');
      var skpd  = $("#organisasi").val();
      var nopspj = $("#no_pspj").val().replace(/\//g,'^');
   
      loadModal = "Lihat Sumber Dana TA. "+Thn_log;         
      url_load  = linkLoad+"?i="+rowid+"&b="+encodeURIComponent(nobuk)+"&t="+tglbuk+"&s="+skpd+"&n="+nopspj;
      break;

  } 

  $("#mdl_show_sumdan .modal-body").html('');
  $("#mdl_show_sumdan").attr("rowid",number);
  $("#mdl_show_sumdan .modal-title").html(loadModal);
  $("#mdl_show_sumdan").modal();  
  $("#mdl_show_sumdan .modal-body").load(url_load);
  $("#mdl_show_sumdan .modal-dialog").css('width', '800px');

};

function BKP_ModalLaporanShow(nomer){
  var url       = $('#modalReportLPJUPGU').attr("alt");
  var no_bukti  = $("#no_bukti_"+nomer).val();
  var tgl_bukti = $("#tgl_bukti_"+nomer).val();
  var urai_kw   = $("#urai_kw_"+nomer).val();
  var skpd      = $("#organisasi").val();
  var nolpj     = $("#no_pspj").val();

  var postig    = Base64.encode(no_bukti+"|"+tgl_bukti+"|"+urai_kw+"|"+skpd+"|"+nolpj);  

  $('#modalReportLPJUPGU').modal();
  $("#modalReportLPJUPGU .modal-body").load(url+"?base="+postig);
}

function BKP_UPGU_update_kegiatan(){
  var skpd = $("#organisasi").val();
  var frm  = $('#formModal');

  $.ajax({
      type: frm.attr('method'),
      headers: { "X-CSRFToken": csrf_token },
      url: $("#save_kegiatan").attr("alt"),
      data: frm.serialize(),
      success: function (data) {
        message_ok('success',data);
        
        isSimpan = false;
        $('input[name="aksi"]').val(isSimpan);
        BKP_kembali_kegiatan();
        BKP_UPGU_load_data(skpd);
        // $('#modalInputBKPUPGU').modal('hide');
      }
  });
}

function BKP_UPGU_delete_kegiatan(){

  var url   = $("#del_kegiatan").attr('alt'); 
  var skpd  = $("#organisasi").val();
  var frm   = $('#formModal');
  var CEHK  = [];  
  
  if($(".kegiatan").is(":checked") == false){
      $.alertable.alert("Silahkan pilih data yang akan dihapus !");
      return false;
  } else {
      $(".kegiatan:checked").each(function() {
        CEHK.push($(this).attr("value"));
      });

      $.alertable.confirm('Anda Yakin ingin menghapus data Kegiatan ?').then(function () {
          
          $.ajax({
            type: "POST",
            url: url,
            headers: { "X-CSRFToken": csrf_token },
            data: frm.serialize(),
            dataType:"html", 
            success: function(msg){ 
              message_ok('success',msg);          
              isSimpan = false;
              $('input[name="aksi"]').val(isSimpan);
              BKP_kembali_kegiatan(); 
              // BKP_UPGU_load_data(skpd);   
              // $('#modalInputBKPUPGU').modal('hide');          
            }
          });
        },function(){ 
          message_ok('error', 'Hapus data Kegiatan dibatalkan!');        
      });

  }
}

function BKP_UPGU_cekCetak(e){
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');

  if($('#organisasi').val() == 0){
      $.alertable.alert('Organisasi belum dipilih');
      return false;
  } else if($(".chk_setuju").is(":checked") == false){
      $.alertable.alert("Silahkan pilih data yang akan dicetak !"); 
      return false;
  } else {
      var judul   = $("#judul_form").html();
      var skpd    = "?skpd="+$("#organisasi").val();
      var nopspj  = [];
      var jnsCtk  = 0; 

      $(".chk_setuju:checked").each(function() {
          nopspj.push($(this).attr("value").replace(' ','+'));
      });
      
      loadModal = "Cetak "+judul;
      url_load  = linkLoad+skpd+"&nopspj="+nopspj+"&jnsct="+jnsCtk;

      document.getElementById("myModalLabel").innerHTML = loadModal;
      $("#showModal").modal();
      $(".modal-body-showmodal").load(url_load);
      $(".modal-dialog").css('width', '800px');
  }
};
