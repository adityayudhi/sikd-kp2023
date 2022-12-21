/*
JavaScript untuk modul Config
created by Joel Hermawan @GI 2016 
SIPKD Application

===============================================================================================================================
*/


// SETING APLIKASI ============================================================================================================
function cekUpate(){

  var msg_atas  = "Anda yakin akan mengganti setelan aplikasi?";
  var msg_bawah = "Penggantian setelan aplikasi dibatalkan.";

  konfirm_simpan('', '', msg_atas, msg_bawah, 'error', '', 'myForm');
}

// JENIS JABATAN ==============================================================================================================
function gantiJenisJBTN(val){
    //alert(val);
    sessionStorage.setItem('trig', val);
    var url = $("#url_tabel").val();
    $.ajax({
        // type: "POST",
        url: '/sipkd/konfig/get_listJabatan/',
        data: {'idnya':val},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function() {
          $(".cover").show();
        },
        success: function(response){
          //alert('responnya='+response);
          $('#tabel-jenis-jabatan').html(response);
          $(".cover").hide();
        }
    });
}

function saveMSJabatan(){
    var msg_atas  = "Anda yakin akan meyimpan data Jabatan?";
    var msg_bawah = "Data Jabatan batal disimpan!";
    sessionStorage.setItem("trig", $("#jns_pejabat").val());
    konfirm_simpan('', '', msg_atas, msg_bawah, 'error', '', 'myForm')
}

// PEJABAT SKPD ===============================================================================================================
function gantiOrganisasi(val){
  var urls     = $("#url_tabel").val();
  var Cookie   = getCookie("pejabatSKPD");

  $.ajax({
      type: "GET",
      url: urls,
      data: {id:val},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){
        $('#tabel-pejabat-skpd').html(response);
        $(".cover").hide();
      }
  });

  if(Cookie != ''){
    removeCookie("pejabatSKPD");
  }
}

// JS PEJABAT SKPKD ===========================================================================================================
function gantiOrganisasiSKPKD(val){
  var url     = $("#url_tabel").val();
  var Cookie  = getCookie("pejabatSKPKD");

  $.ajax({
      type: "POST",
      url: url,
      data: {id:val},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){
        $('#tabel-pejabat-skpkd').html(response);
        $(".cover").hide();
      }
  });

  if(Cookie != ''){
    removeCookie("pejabatSKPKD");
  }
}

function savePejabatSKPKD(){
  var SKPKD = $("#organisasi").val();

  if(SKPKD != 0){

      $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
          setCookie("pejabatSKPKD", SKPKD, 1);
          document.getElementById('myForm').submit();
      }, function() {
          message_ok('error', 'Simpan data dibatalkan!');
          removeCookie("pejabatSKPKD");
      });

  } else {
    $.alertable.alert('Organisasi belum dipilih!');
  }
}

// JS PEJABAT SKPKD ===========================================================================================================

function savePejabatSKPKD(){
  $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
      document.getElementById('myForm').submit();
  }, function() {
      message_ok('error', 'Simpan data dibatalkan!');
  });
}

// JS DASAR HUKUM =============================================================================================================

// function dasarHkmByOrg(e){
//   var dsr = $("#dasarHkm").val();
//   getDasarHukum(dsr, e);
// }

// function getDasarHukum(jns, org){
//   var url = $("#url_tabel").val();

//   $.ajax({
//       type: "POST",
//       url: url,
//       data: {id:jns, skpd:org},
//       async: false,
//       dataType: "html",
//       timeout: 10000,
//       success: function(response){
//         $('#Tabel-DasarHukum').html(response);
//       }
//   });

// }

function saveDasarHukum(act){
  var SKPD  = $("#organisasi").val();
  var dasar = $("#dasarHkm").val();

  if(dasar == 0){
    saveDSRHKM(SKPD, dasar, act);
  } else {
    if(SKPD != 0){
        saveDSRHKM(SKPD, dasar, act);
      } else {
        $.alertable.alert('Organisasi belum dipilih!');
      }
  }
}

function saveDSRHKM(SKPD, dasar, act){
  var frm = $("#myForm");

  function SubMItForm(){
    $.ajax({
      type: frm.attr('method'),
      url: frm.attr('action'),
      data: frm.serialize(),
      success: function (data) {
        dasarHukum(dasar);
      }
    });
  }

  if(act == "del"){
      SubMItForm();
      $.alertable.alert('Data Dasar Hukum berhasil dihapus');

  } else if(act == "yes"){
      $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
          SubMItForm();
          $.alertable.alert('Data Dasar Hukum berhasil disimpan');
      }, function() {
          message_ok('error', 'Simpan data dibatalkan!');
      });
  }
}

// JS SUMBER DANA =============================================================================================================

function cekSaveRekSumberDana(aksi){
  var sumberdana  = $("#sumberdana").val();
  var old_sumDana = $("#old_sumberdana").val();
  var rekening    = $("#rekening").val();
  var old_rek     = $("#old_rekening").val();
  var bankasal    = $("#bankasal").val();
  var namabank    = $("#namabank").val();

  var urlCek      = $("#urlCekData").val();
  var data        = $("#selekValRow").val();
  var value       = Base64.encode(sumberdana+"|"+rekening+"|"+bankasal+"|"+namabank);
  var pesan       = "Sumber Dana : "+sumberdana+" dan Rekening Pencairan : "+rekening+", sudah ada.";

  if(rekening == ""){
      $.alertable.alert("Nomor Rekening Pencairan masih kosong.");
  } else if(bankasal == ""){
      $.alertable.alert("Nomor Bank Asal Pencairan masih kosong.");
  } else if(namabank == ""){
      $.alertable.alert("Nomor Nama Bank Pencairan masih kosong.");
  } else {
      // CEK DATA SUDAH ADA APA BELUM
      AjaxCeker(urlCek, value, '');

      if(aksi == "add"){

        if(hasilCek == 1){
            $.alertable.alert(pesan);
        } else {
            saveRekSumDana();
        }

      } else if(aksi == "edit"){

          if(sumberdana != old_sumDana || rekening != old_rek){

              if(hasilCek == 1){
                  $.alertable.alert(pesan);
              } else {
                  saveRekSumDana();
              }

          } else {
              saveRekSumDana();
          }
      }
  }

};

function saveRekSumDana(){

  $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
      document.getElementById('myForm').submit();
  }, function() {
      message_ok('error', 'Simpan data dibatalkan!');
  });
};

function EditSumberDana(e,jika){

  if(jika == 'no'){
      $.alertable.alert('Pilih dulu data yang akan diedit.');
  } else {
      showModal(e,'dana');
  }
}

function DeleteSumberDana(e,jika){
  var link  = $(e).attr('alt');
  var url   = $("#urlCekRekDana").val();
  var data  = $("#selekValRow").val();
  var balik = Base64.decode(data).split("|");

  var pesan = "Apakah anda yakin ingin menghapus Sumber Dana : "+balik[0]+" Dengan Rekening : "+balik[1]+"?";

  // CEK DATA SUDAH DIPAKAI APA BELUM
  AjaxCeker(link, data, '');

  if(jika == 'no'){
      $.alertable.alert('Pilih dulu data yang akan dihapus.');
  } else if (hasilCek == 1){
      $.alertable.alert('Sumber Dana : '+balik[0]+' Dengan Rekening : '+balik[1]+', telah digunakan di SP2D');
  } else {
      $.alertable.confirm(pesan).then(function() {
          self.location.href = url+"&kode="+data;
      }, function() {
          message_ok('error', 'Simpan data dibatalkan!');
      });
  }
}

// JS TANGGAL PENAGIHAN =======================================================================================================

function SaveTglTagihan(){
  var nonFisik  = $("#tgl_nonfisik").val();
  var Fisik     = $("#tgl_fisik").val();
  var linkSave  = $("#myForm").attr('action');
  var modal     = $("#menu-stup_tagihan");


  $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
      // SIMPAN DATA
      $.ajax({
          type: "POST",
          url: linkSave,
          data: {tgl_nonfisik:nonFisik, tgl_fisik:Fisik},
          async: false,
          success: function(){
            $.alertable.alert('Data Telah Tersimpan');
          }
      });

  }, function() {
      message_ok('error', 'Simpan data dibatalkan!');
  });
}

// JS BENDAHARA PEMBANTUUUUUU =================================================================================================

function loadBendPembantu(){
  var url   = $("#organisasi").attr("alt");
  var hsl   = $("#organisasi").val();

  $.ajax({
      type: "POST",
      url: url,
      data: {skpd:hsl},
      async: false,
      dataType: "html",
      timeout: 10000,
      success: function(response){
        $('#dtBendPembantu').html(response);
      }
  });

  loadKegiatan('');
  clearFormKegiatan();
}

function clearFormKegiatan(){
    $("#username_old").val('');
    $("#username").val('');
    $("#password").val('');
    $("#namapembantu").val('');
    $("#selekValRow").val('');
}

function loadKegiatan(e){

  $("#aksiForm").val(e);

  if(e == 'add'){
    clearFormKegiatan();
    document.getElementById("username").focus();
  }

  var url   = $("#url_kegiatan").val();
  var org   = $("#organisasi").val();
  var data  = $("#selekValRow").val();

  if(e != '' && org <= 0){
      $.alertable.alert('Organisasi belum dipilih');
  } else {

      $.ajax({
          type: "POST",
          url: url,
          data: {act:e, skpd:org, data:data},
          async: false,
          dataType: "html",
          timeout: 10000,
          success: function(response){
            $('#dtKegiatanBend').html(response);
            $("#selectORG").val(org);
          }
      });
  }
}

function loadPassword(data, url){
  $.ajax({
      type: "POST",
      url: url,
      data: {data:data},
      async: false,
      success: function(response){
        $("#password").val(response);
      }
  });
}

function cekUsername(e, val){
  var url       = $(e).attr("alt");
  var org       = $("#organisasi").val();
  var unameold  = $("#username_old").val();

  if(org != 0){
    if(unameold != val.toUpperCase()){
      AjaxCeker(url, val, org);

      if(hasilCek >= 1){
          loadPertama('btn_savePembantu','-1');
          $.alertable.alert('Username Sudah Digunakan..');
      } else if(val.toUpperCase() == "ADMIN"){
          loadPertama('btn_savePembantu','-1');
          $.alertable.alert('Pengguna dengan nama ADMIN tidak diperbolehkan');
      } else {
          loadPertama('btn_savePembantu','1');
      }
    } else {
        loadPertama('btn_savePembantu','1');
    }
  }
}

function SaveBendPembantu(){
  var unameold  = $("#username_old").val();
  var skpd      = $("#organisasi").val();
  var user      = $("#username").val();
  var pswd      = $("#password").val();
  var nama      = $("#namapembantu").val();
  var chkb      = $(".pilih_chk").is(":checked");
  var url       = $("#username").attr("alt");


  AjaxCeker(url, user, skpd);

  if(skpd <= 0){
      $.alertable.alert('Organisasi belum dipilih');
  } else if(user == ""){
      $.alertable.alert('User Name masih kosong');
  } else if(pswd == ""){
      $.alertable.alert('Password masih kosong');
  } else if(nama == ""){
      $.alertable.alert('Nama Bendahara Pembantu masih kosong');
  } else if(chkb == false){
      $.alertable.alert('Kegiatan belum ada yang dipilih');
  } else if(unameold != user.toUpperCase()){
      if(hasilCek >= 1){
          $.alertable.alert('Username Sudah Digunakan');
      } else {
          SimpanPembantuIsYes();
      }

  } else {
      SimpanPembantuIsYes();
  }

}

function SimpanPembantuIsYes(){
  var frm = $('#myForm');

  $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
      $.ajax({
          type: frm.attr('method'),
          url: frm.attr('action'),
          data: frm.serialize(),
          success: function (data) {
            loadBendPembantu();
            $.alertable.alert('Data Bendahara Pembantu berhasil disimpan');
          }
      });
  }, function() {
      message_ok('error', 'Simpan data dibatalkan!');
  });

}

function confimDelPembantu(f){
  var skpd  = $("#organisasi").val();
  var data  = $("#selekValRow").val();
  var url   = $(f).attr('alt');

  if(skpd == 0){
      $.alertable.alert('Organisasi belum dipilih');
  } else if(data == ""){
      $.alertable.alert('Nama Bendahara Pembantu belum dipilih');
  } else {
      $.alertable.confirm('Anda yakin akan menghapus data?').then(function() {
          $.ajax({
              type: 'POST',
              url: url,
              data: {token:skpd, y:data},
              success: function (data) {
                loadBendPembantu();
                $.alertable.alert('Data Bendahara Pembantu berhasil dihapus');
              }
          });
      }, function() {
          message_ok('error', 'Simpan data dibatalkan!');
      });
  }
}

// JS USER ====================================================================================================================

function pilihFilter(hsl){
  if(hsl == "UNAME"){
    $("#input_filter").css("display","");
    $("#pilih_filter").css("display","none");

  } else if(hsl == "HAKAKSES"){
    $("#input_filter").css("display","none");
    $("#pilih_filter").css("display","");
  }
}

function aksesUser(e, url, act){
  var uName = $("#user_name").val();
  var Hak   = $("#jns_jabatan").val();

  $.ajax({
      type: "POST",
      url: url,
      data: {input:uName, pilih:Hak, act:act},
      async: false,
      dataType: "html",
      timeout: 10000,
      success: function(response){
        $('#tabel-hak-akses').html(response);
      }
  });
}

function cekSimpanUser(url, act, thn){

  var HakAkses  = $("#jns_jabatan").val();
  var Uname     = $("#user_name").val().toUpperCase();
  var chekSKPD  = $(".checkbox_skpd").is(":checked");

  if(Uname != ''){
    AjaxCeker(url, Uname, thn);
  }


  if(Uname == ""){
      $.alertable.alert("User Name masih kosong..!!");
      return false;
  } else if(Uname == "ADMIN"){
      $.alertable.alert("User Name dengan nama ADMIN tidak diperbolehkan..!!");
      return false;
  } else if($("#password").val() == ""){
      $.alertable.alert("Password masih kosong..!!");
      return false;
  } else if(HakAkses == "--PILIH--"){
      $.alertable.alert("Hak Akses belum dipilih..!!");
      return false;
  } else if(chekSKPD == false){
      $.alertable.alert("SKPD belum dipilih..!!");
      return false;
  } else if(act == 'add'){
      if(hasilCek >= 1){
        $.alertable.alert("User Name Sudah Digunakan..!!");
        return false;
      } else {
          saveJikaSudahOke();
      }

  } else {
      saveJikaSudahOke();
  }
}

function cekSimpanJabatan(url, act){

  var kdjabatan = $("#kdjabatan").val();
  var nmjabatan = $("#nmjabatan").val();
  var jnsjabatan   = $("#jnsjabatan").val();

  if(kdjabatan == ""){
      $.alertable.alert("Kode Jabatan masih kosong..!!");
      return false;
  } else if(nmjabatan == ""){
      $.alertable.alert("Nama Jabatan masih kosong..!!");
      return false;
  } else if(jnsjabatan == "--pilihfungsi--"){
      $.alertable.alert("Jenis Jabatan belum dipilih..!!");
      return false;
  } else{
    saveJikaSudahOke_jabatan(act);
  }
}

function cekSimpanSubUrusan(url, act){

  var kdsuburusan = $("#kdsuburusan").val();
  var nmsuburusan = $("#nmsuburusan").val();
  var jnsfungsi   = $("#jnsfungsi").val();

  if(kdsuburusan == ""){
      $.alertable.alert("Kode Sub Urusan masih kosong..!!");
      return false;
  } else if(nmsuburusan == ""){
      $.alertable.alert("Nama masih kosong..!!");
      return false;
  } else if(jnsfungsi == "--pilihfungsi--"){
      $.alertable.alert("Hak Akses belum dipilih..!!");
      return false;
  } else{
    saveJikaSudahOke_sub(act);
  }
}

function cekSimpanOrganisasi(url, act){

  var kd_org = $("#kdorg").val();
  var nm_org = $("#nm_org").val();
  var alamat   = $("#alamat").val();
  var notelp   = $("#notelp").val();
  var nofax   = $("#nofax").val();
  var email   = $("#email").val();
  // var act = $("#act").val();

  if(kd_org == ""){
      $.alertable.alert("Kode Organisasi Masih Kosong!");
      return false;
  } else if(nm_org == ""){
      $.alertable.alert("Nama organisasi Masih Kosong!");
      return false;
  } else if(alamat == ""){
      $.alertable.alert("Alamat Masih Kosong!");
      return false;
  } else if(notelp == ""){
      $.alertable.alert("No Telp Masih Kosong!");
      return false;
  } else if(nofax == ""){
      $.alertable.alert("No Fax Masih Kosong!");
      return false;
  } else if(email == ""){
      $.alertable.alert("Email Masih Kosong!");
      return false;
  } else{
      saveJikaSudahOke_org(act);
  }

}

function cekSimpanProgram(url, act){

  var kdprogram = $("#kdprogram").val();
  var nmprogram = $("#nmprogram").val();

  if(kdprogram == ""){
      $.alertable.alert("Kode Program masih kosong..!!");
      return false;
  } else if(nmprogram == ""){
      $.alertable.alert("Nama Program masih kosong..!!");
      return false;
  } else{
    saveJikaSudahOke_prog(act);
  }
}

function cekSimpanDana(url, act){

  var kdsumberdana = $("#kdsumberdana").val();
  var nmsumberdana = $("#nmsumberdana").val();

  if(kdsumberdana == ""){
      $.alertable.alert("Kode Dana masih kosong..!!");
      return false;
  } else if(nmsumberdana == ""){
      $.alertable.alert("Sumber Dana masih kosong..!!");
      return false;
  } else{
    saveJikaSudahOke(act);
  }
}

function cekSimpanUrusan(url, act){

  var kdurusan = $("#kdurusan").val();
  var nmurusan = $("#nmurusan").val();

  if(kdurusan == ""){
      $.alertable.alert("Kode Urusan masih kosong..!!");
      return false;
  } else if(nmurusan == ""){
      $.alertable.alert("Nama Urusan masih kosong..!!");
      return false;
  } else{
    saveJikaSudahOke_uru(act);
  }
}

function cekSimpanKegiatan(url, act){

  var kdkegiatan = $("#kdkegiatan").val();
  var nmkegiatan = $("#nmkegiatan").val();

  if(kdkegiatan == ""){
      $.alertable.alert("Kode Kegiatan masih kosong..!!");
      return false;
  } else if(nmkegiatan == ""){
      $.alertable.alert("Nama Kegiatan masih kosong..!!");
      return false;
  } else{
    saveJikaSudahOke_keg(act);
  }
}

function cekSimpanDataLanjutan(url, act){

  var kd_org = $("#kd_org").val();
  var nm_org = $("#nm_org").val();
  var alamat   = $("#alamat").val();
  var notelp   = $("#notelp").val();
  var nofax   = $("#nofax").val();
  var email   = $("#email").val();

  if(kd_org == ""){
      $.alertable.alert("Kode organisasi masih kosong..!!");
      return false;
  } else if(nm_org == ""){
      $.alertable.alert("Nama organisasi masih kosong..!!");
      return false;
  } else if(alamat == ""){
      $.alertable.alert("Alamat masih kosong..!!");
      return false;
  } else if(notelp == ""){
      $.alertable.alert("No Telp masih kosong..!!");
      return false;
  } else if(nofax == ""){
      $.alertable.alert("No Fax masih kosong..!!");
      return false;
  } else if(email == ""){
      $.alertable.alert("Email masih kosong..!!");
      return false;
  } else{
      saveJikaSudahOke_org('add');
  }
}

function saveJikaSudahOke(){

  $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
      document.getElementById('myForm').submit();
  }, function() {
      message_ok('error', 'Simpan data dibatalkan!');
  });
}

function setUserDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}

function setSumberDanaDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      if(total_sp2d != 0){
           $("#btnHapus").trigger( "click" );; 
        }
        else{
          msg_bawah = "Anda telah membatalkan penghapusan data.";
        }
      return false;
  }
}

function setDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}

function setMasterJabatanDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      localStorage.setItem("trig", $("#jns_pejabat").val());
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}

function setMasterDanaDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}

function setDelete(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan penghapusan data.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}

function setUserUbahPwd(pesan, link){
  if (pesan !="") {
      action    = "href";
      msg_atas  = pesan;
      msg_bawah = "Anda telah membatalkan perubahan password.";
      konfirm_batal(action, link, msg_atas, msg_bawah, 'error', '');
      return false;
  }
}
// //UNTUK MENGECEK NAMA TABLE ADA ATAU TIDAK
// SELECT COUNT(RDB$RELATION_NAME) AS JML FROM RDB$RELATIONS
// WHERE RDB$RELATION_NAME = 'PENGGUNA'