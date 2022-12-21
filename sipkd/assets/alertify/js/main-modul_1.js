/*
JavaScript untuk modul Main
created by Joel Hermawan @GI 2016 
SIPKD Application

===============================================================================================================================
*/

var hasilCek  = "";
var getUrl    = window.location;
var pageUrl   = window.location.href.substring(window.location.protocol.length);
var baseUrl   = "//"+ getUrl.host+"/"+getUrl.pathname.split('/')[1]+"/";
var Thn_log   = $('.tahun-load').val();
var route     = $('#route_id').val();
var isModal   = "false";
var js_arg = [];
var asal_modal = '';

// HARUS ANGKA
function isNumberKey(e){
  // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 188]) !== -1 ||
      // Allow: Ctrl+A,Ctrl+C,Ctrl+V, Command+A
      ((e.keyCode == 65 || e.keyCode == 86 || e.keyCode == 67 || e.keyCode == 88 || e.keyCode == 90 || e.keyCode == 89) && (e.ctrlKey === true || e.metaKey === true)) ||
      // Allow: home, end, left, right, down, up
      (e.keyCode >= 35 && e.keyCode <= 40)) {
      // let it happen, don't do anything
      return;
    }
    
    
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
    }
};

function replace_titik(e){
  e.value.replace(/\./g,'').replace(/,/g,'.');
}

// Jika Copy Paste Dari Excel dengan Format  Rp 27.834.609.000,21 30,2rpsdsd  Rp. 27,834,609,000.21

$('.paste').on("paste",function(e){
    e.stopPropagation();
    e.preventDefault();
            
    var cd = e.originalEvent.clipboardData;
    var $this = $(this);
    var hilangkan_huruf = cd.getData("text/plain").trim().replace(/[^0-9.,]/g,'');
    var desimal = hilangkan_huruf.substr(hilangkan_huruf.length - 3);
    
    if (desimal.indexOf(',') != -1||desimal.indexOf('.') != -1) {
      var hilangkan_huruf2 = hilangkan_huruf.replace(/[^0-9]/g,'');

      if (desimal.indexOf(',')!=0 && desimal.indexOf(',')!=-1) {
        if(desimal.indexOf(',')==2){
          hilangkan_huruf2 = hilangkan_huruf2+'00';
        }else{
          hilangkan_huruf2 = hilangkan_huruf2+'0';  
        }
      }
      if(desimal.indexOf('.')!=0 && desimal.indexOf('.')!=-1){
        if(desimal.indexOf('.')==2){
          hilangkan_huruf2 = hilangkan_huruf2+'00';
        }else{
          hilangkan_huruf2 = hilangkan_huruf2+'0';  
        }
      }
      
      var sisipkan_koma = hilangkan_huruf2.substring(hilangkan_huruf2.length-2, 0)+','+hilangkan_huruf2.substring(hilangkan_huruf2.length-2);
      $this.val(sisipkan_koma);
    }else{
      if (hilangkan_huruf.indexOf(',') != -1||hilangkan_huruf.indexOf('.') != -1) {
        var hilangkan_huruf2 = hilangkan_huruf.replace(/[^0-9]/g,'');
        $this.val(hilangkan_huruf2);
      }else{
        $this.val(hilangkan_huruf);
      }
    }

    setTimeout(function(){
      return isNumberKey(e);  
    },0);
});

// FORMAT ANGKA TO RUPIAH
function toRp(angka){
    var rev     = parseInt(angka, 10).toString().split('').reverse().join('');
    var rev2    = '';
    for(var i = 0; i < rev.length; i++){
        rev2  += rev[i];
        if((i + 1) % 3 === 0 && i !== (rev.length - 1)){
            rev2 += '.';
        }
    }
    if(rev2 == 'NaN'){
      return '0,00';
    }else{
      return rev2.split('').reverse().join('') + ',00';
    }
}

/* FORMAT RUPIAH BY AAN*/
function formatRupiah(angka, prefix){
    var number_string = angka.replace(/[^,\d]/g, '').toString(),
        split    = number_string.split(','),
        sisa     = split[0].length % 3,
        rupiah     = split[0].substr(0, sisa),
        ribuan     = split[0].substr(sisa).match(/\d{3}/gi);
        
    if (ribuan) {
        separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }
    
    rupiah = split[1] != undefined ? rupiah + ',' + split[1] : rupiah;
    return prefix == undefined ? rupiah : (rupiah ? '' + rupiah : '');
}

// FORMAT ANGKA TO RUPIAH DENGAN DESIMAL DIBELAKANG KOMA (,) BY AAN
function toRp_WithDesimal(angka, decimalSeparator, thousandsSeparator, nDecimalDigits){
    // var num = parseFloat( angka ); //convert to float 
    if(angka==''){
      angka = '0';
    }
    
    var rep_titik = angka.replace(/\./g,'');
    var rep_titik_to_koma = rep_titik.replace(/,/g,'.');
    var num = parseFloat( rep_titik_to_koma );

    //default values  
    decimalSeparator = decimalSeparator || ',';  
    thousandsSeparator = thousandsSeparator || '.';  
    nDecimalDigits = nDecimalDigits == null? 2 : nDecimalDigits;  
  
    var fixed = num.toFixed(nDecimalDigits); //limit or add decimal digits  
    //separate begin [$1], middle [$2] and decimal digits [$4]  
    var parts = new RegExp('^(-?\\d{1,3})((?:\\d{3})+)(\\.(\\d{' + nDecimalDigits + '}))?$').exec(fixed);  

    
    if(num == 0){
        return fixed.replace('.', decimalSeparator); 
    }    
    // return fixed.replace('NaN', '0,00'); 
    
    if(parts){ //num >= 1000 || num < = -1000  
        return parts[1] + parts[2].replace(/\d{3}/g, thousandsSeparator + '$&') + (parts[4] ? decimalSeparator + parts[4] : '');  
    }else{  
        return fixed.replace('.', decimalSeparator);  
    }  

}

// TO ANGKA DECIMAL BY AAN
function toAngkaDesimal(rp){
  // console.log(rp);

  var x = rp == '' ? '0,00'.split(",") : rp.split(",");
  var y = parseInt(x[0].replace(/\./g, ''));

  if(x[1] == undefined ){
    x_1 = '00';
  } else {
    x_1 = x[1];
  }
  
  var z = y+","+x_1;
  
  return z;
}

function to_rp_Dec(angka){
  var   bilangan = angka;
  
  var number_string = bilangan.toString(),
    split = number_string.split(','),
    sisa  = split[0].length % 3,
    rupiah  = split[0].substr(0, sisa),
    ribuan  = split[0].substr(sisa).match(/\d{1,3}/gi);     
  if (ribuan) {
    separator = sisa ? '.' : '';
    rupiah += separator + ribuan.join('.');
  }
  rupiah = split[1] != undefined ? rupiah + ',' + split[1] : rupiah;

  // Cetak hasil  
  return rupiah;
}


// FORMAT ANGKA TO RUPIAH DENGAN DESIMAL DIBELAKANG KOMA (,)
function toRp_WithDecimal(angka, decimalSeparator, thousandsSeparator, nDecimalDigits){
    var num = parseFloat( angka ); //convert to float  
    //default values  
    decimalSeparator = decimalSeparator || ',';  
    thousandsSeparator = thousandsSeparator || '.';  
    nDecimalDigits = nDecimalDigits == null? 2 : nDecimalDigits;  
  
    var fixed = num.toFixed(nDecimalDigits); //limit or add decimal digits  
    //separate begin [$1], middle [$2] and decimal digits [$4]  
    var parts = new RegExp('^(-?\\d{1,3})((?:\\d{3})+)(\\.(\\d{' + nDecimalDigits + '}))?$').exec(fixed);   

    if(num == 0){
      return fixed.replace('.', decimalSeparator); 
    }
  
    if(parts){ //num >= 1000 || num < = -1000  
        return parts[1] + parts[2].replace(/\d{3}/g, thousandsSeparator + '$&') + (parts[4] ? decimalSeparator + parts[4] : '');  
    }else{  
        return fixed.replace('.', decimalSeparator);  
    }  
}

// FORMAT ANGKA TO RUPIAH DENGAN DESIMAL DIBELAKANG KOMA (,)
// UNTUK SUM/TOTAL COLOM TABEL [FOOTER]
function toRp_Dec_SUM(angka){
    var rev     = parseInt(angka, 10).toString().split('').reverse().join('');
    var rev2    = '';
    var des     = rev.substring(0,2).split('').reverse().join('');
    var ang     = rev.substring(2,rev.length);

    for(var i = 0; i < ang.length; i++){
        rev2  += ang[i];
        if((i + 1) % 3 === 0 && i !== (ang.length - 1)){
            rev2 += '.';
        }
    }

    if(rev != 0){
        return rev2.split('').reverse().join('') + ','+des;
    } else {
        return "0,00";
    }
}

// FORMAT RUPIAH TO ANGKA
function toAngka(rp){
  x = rp.replace(',00','');
  return parseInt(x.replace(/\./g, ''));
}

function toAngkaDec2(rp){
  var x = rp.split(".");
  var y = parseInt(x[0].replace(/\./g, ''));
  var z = x.join('');
  return z;
}

// FORMAT RUPIAH TO ANGKA DENGAN DESIMAL DIBELAKANG KOMA (,)
function toAngkaDec(rp){
  var x = rp.split(",");
  var y = parseInt(x[0].replace(/\./g, ''));
  var z = y+"."+x[1];
  
  return z;
}

// FORMAT RUPIAH TO ANGKA DENGAN DESIMAL DIBELAKANG KOMA (.)
function toAngkaDecimal(rp){
  var x = rp.split(".");  
  var y = parseInt(x[0].replace(/\./g, ''));
  var z = y+"."+x[1];
  // console.log(x)
  return z;
}

// function formatRupiah(angka, prefix){
//   var number_string = angka.replace(/[^,\d]/g, '').toString(),
//   split    = number_string.split(','),
//   sisa     = split[0].length % 3,
//   rupiah   = split[0].substr(0, sisa),
//   ribuan   = split[0].substr(sisa).match(/\d{3}/gi);
 
//   // tambahkan titik jika yang di input sudah menjadi angka ribuan
//   if(ribuan){
//     separator = sisa ? '.' : '';
//     rupiah += separator + ribuan.join('.');
//   }
 
//   rupiah = split[1] != undefined ? rupiah + ',' + split[1] : rupiah;
//   return prefix == undefined ? rupiah : (rupiah ? 'Rp. ' + rupiah : '');
// }

function terbilang(rp){
  var hasil = "";

  $.ajax({
      headers: { "X-CSRFToken": csrf_token },
      type: "POST",
      url: link_terbilang,
      data: {rp:rp},
      async: false,
      timeout: 10000,
      success: function(response){
        hasil = response;
      }
  });

  return hasil;}


// SET, GET & REMOVE COOKIES IN JAVASCRIPT
// SET COOKIES
function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// GET COOKIES
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// REMOVE COOKIE
function removeCookie(cname){
  document.cookie = cname+"=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

// VALIDASI LOGIN
function kliklogin(){

  if ($("#username").val() == ""){
      $.alertable.alert("User Name masih kosong, silahkan diisi terlebih dahulu."); 
      return false;
  } else if ($("#password").val() == ""){
      $.alertable.alert("Password Anda masih kosong, silahkan diisi."); 
      return false;
  } else if ($("#listtahun").val() == '0'){
      $.alertable.alert("Anda belum memilih tahun, silahkan pilih tahun terlebih dahulu."); 
      return false;
  } else {
    document.myForm.submit();
  }
};

// PREVIEW IMAGE UPLOAD
function PreviewImage(upImg,upPrev,nmFile,btnRemv) {
  var oFReader = new FileReader();
  var fileFoto = document.getElementById(upImg).files[0];

  var fileType = (fileFoto.type).toLowerCase();
  if(fileFoto){
    if(fileType !='image/png'){
      $.alertable.alert('Type file bukan PNG, type file anda [*.'+fileFoto.type+']');
    } else if(fileFoto.size > 200000){ //maks file 2 KB
      $.alertable.alert('File foto terlalu besar, maksimal 2KB');
    } else {
      oFReader.readAsDataURL(fileFoto);
      oFReader.onload = function (oFREvent) {
      document.getElementById(upPrev).src   = oFREvent.target.result;
      document.getElementById(nmFile).value = fileFoto.name;
      };
    }
  }
};

// pesan kotak bawah pojok
function message_ok(warna,pesan){
  if(pesan){ //log, success, error
    if(warna == "log") {alertify.log(pesan);}
      else if(warna == "success") {alertify.success(pesan);}
      else if(warna == "error") {alertify.error(pesan);}
  }
};

// pesan konfirmasi yes / no
function konfirm_batal(action, link, msg_atas, msg_bawah, warna, submit){
  $.alertable.confirm(msg_atas).then(function() {
      if(action == "href"){
        self.location.href=link;
      } else {
        // document.myForm.submit();
        document.getElementById("myForm").submit();
      }
  }, function() {
      message_ok(warna, msg_bawah);
  });
};

// AKTIV UNAKTIV BUTTON
function loadPertama(button, act){
  var baten   = document.getElementById(button);
  var attDis  = document.createAttribute("disabled");

  if(act < '1'){
    baten.setAttributeNode(attDis);
  } else {
      baten.removeAttribute("disabled");
  }
}

// pesan konfirmasi yes / no Form Twin
function konfirm_simpan(action, link, msg_atas, msg_bawah, warna, submit, form){

  $.alertable.confirm(msg_atas).then(function() {
      if(action == "href"){
        self.location.href=link;
      } else {
        // document.myForm.submit();
        document.getElementById(form).submit();
      }
  }, function() {
      message_ok(warna, msg_bawah);
  });
};

function link_self(url){
  self.location.href = url;
}

function alert_botom(color,message){

  if(message){
    switch(color) { //ANDA BISA MEMILIH WARNA PESAN
      case "log": // HITAM
          alertify.log(message);
          break;
      case "success": // HIJAU
          alertify.success(message);
          break;
      case "error": // MERAH
          alertify.error(message);
          break;
      }
  }
}

// SIGN OUT VALIDASI
function logout_confirm(user,link){
  if (user !="") {
      $.alertable.confirm(user+", anda yakin akan melakukan logout..?").then(function() {
          link_self(link);
      }, function() {
          alert_botom("error","anda telah membatalkan Logout");
      });
  }  
};

// TANGGAL SEKARANG / DATE NOW FORMAT INDONESIA
function DateNowInd(yes){
  var DateNow   = new Date();
  var hari      = DateNow.getDay();
  var tgl       = DateNow.getDate();
  var bulan     = DateNow.getMonth();
  // var tahun     = DateNow.getFullYear();
  var tahun     = $(".tahun-load").val();
  var tanggal;

  var NmHari    = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jum&#39at', 'Sabtu']
  var NmBulan   = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus',
        'September', 'Oktober', 'November', 'Desember'];

  if(tgl <= 9){
      tanggal = "0"+tgl;
  } else {
      tanggal = tgl;
  }

  if(yes != ""){
      return tanggal+" "+NmBulan[bulan]+" "+tahun;
  } else {
      return NmHari[hari]+", "+tanggal+" "+NmBulan[bulan]+" "+tahun;
  }
}

// CEK TANGGAL TANGGAL AKHIR TIDAK BOLEH LEBIH KECIL DARI TANGGAL AWAL
function cekTanggal(tglawal, tglakhir){
  var tgl_1 = Date.parse(getTglAngka(tglawal));
  var tgl_2 = Date.parse(getTglAngka(tglakhir));
  var hasil = tgl_2-tgl_1;
  var valid = true;

  if(hasil < 0){ valid = false;}
  return valid;
}

// tanggal ke angka
function getTglAngka(tgl){ //yyyy-mm-dd

  var bulan = {Januari:'01', Februari:'02', Maret:'03', April:'04', Mei:'05', Juni:'06',
        Juli:'07', Agustus:'08', September:'09', Oktober:'10', November:'11', Desember:'12'};

  var split = tgl.split(" ");
  return split[2]+"-"+bulan[split[1]]+"-"+split[0];
}

// BULAN TO ANGKA
function getBlnToNum(tgl){
  var bulan   = {Januari:'1', Februari:'2', Maret:'3', April:'4', Mei:'5', Juni:'6',
        Juli:'7', Agustus:'8', September:'9', Oktober:'10', November:'11', Desember:'12'};

  var split = tgl.split(" ");

  return bulan[split[1]];
}

function getDDMMYYYY(tgl){ //dd/mm/yyyy
  var bulan = {Januari:'01', Februari:'02', Maret:'03', April:'04', Mei:'05', Juni:'06',
        Juli:'07', Agustus:'08', September:'09', Oktober:'10', November:'11', Desember:'12'};

  var split = tgl.split(" ");

  return split[0]+"/"+bulan[split[1]]+"/"+split[2];
}

function getTglINDO(tgl){
  var NmBulan   = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus',
        'September', 'Oktober', 'November', 'Desember'];

  var split = tgl.split("/");
  // console.log(split)
  return split[0]+" "+NmBulan[split[1]]+" "+split[2];
}

//pemisah - (2018-01-10)
function getTglINDO2(tgl){
  var NmBulan   = ['','Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus',
        'September', 'Oktober', 'November', 'Desember'];

  var split = tgl.split("-");
  
  return split[2]+" "+NmBulan[split[1]<10 ? split[1].replace('0',''):split[1]]+" "+split[0];
}

function pad (str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}

function getTglINDO3(tgl){
  var NmBulan   = ['','Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus',
        'September', 'Oktober', 'November', 'Desember'];

  var split = tgl.split("-");
  
  return pad(split[2].split('T')[0],2)+" "+NmBulan[split[1]<10 ? split[1].replace('0',''):split[1]]+" "+split[0];
}

function convert_ke_bulan(tgl){
  var NmBulan   = ['','Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus',
        'September', 'Oktober', 'November', 'Desember'];

  var split = tgl.split("-");
  
  return NmBulan[split[0]<10 ? split[0].replace('0',''):split[0]]+" - "+NmBulan[split[1]<10 ? split[1].replace('0',''):split[1]];
}

// ambil nilai GET dari sebuah url
function getUrlVars(url) {
  var vars = {};
  var parts = url.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
    vars[key] = value;
  });
  return vars;
}

// JIKA LOGIN / LOGOUT BERHASIL
function slidePesan(pesan){
    message_ok("success", pesan);
};

// CEK ALL CHECKBOX
function do_this(e, chkclass, button){
  var baten   = document.getElementById(button);
  var attDis  = document.createAttribute("disabled");

  $('.'+chkclass).each(function() {
      this.checked = e.checked;                      
  });

  if(chkclass == "lck_spd"){
    var jml = $(":checkbox:checked").length;

    if(jml > 2){
      if(e.checked){ baten.setAttributeNode(attDis);
      } else {  baten.removeAttribute("disabled"); }
    } else {  baten.removeAttribute("disabled"); }
  }

};

// ENABLE DISABLE ELEMEN DOM HTML
function dis_ena_bled(target, aksi){
  var elemen    = document.getElementById(target);
  var attElm    = document.createAttribute("disabled");

  if(aksi == '0'){
    elemen.setAttributeNode(attElm);
  } else {
      elemen.removeAttribute("disabled");
  }
}

function max_check_only(e, button, jml){

  var jumlah  = $(":checkbox:checked").length;
  var baten   = document.getElementById(button);
  var attDis  = document.createAttribute("disabled");

  if(jumlah > jml){
    baten.setAttributeNode(attDis);
  } else {
      baten.removeAttribute("disabled");
  }
}

// CEK VIA AJAX
function AjaxCeker(URL, cekdata, tahun){
  if(cekdata){
    $.ajax({
        type: "POST",
        url: URL,
        data: {kode:cekdata, thn:tahun},
        async: false,
        success: function(msg){ 
          hasilCek = msg;
        }
    });
  }
  return hasilCek;
}

// GET TRI WULAN
function getTriwulan(sumber, target){

  var bulan   = {Januari:'1', Februari:'2', Maret:'3', April:'4', Mei:'5', Juni:'6',
        Juli:'7', Agustus:'8', September:'9', Oktober:'10', November:'11', Desember:'12'};

  var strTgl  = $(sumber).val();
  var arrTgl  = strTgl.split(" ");
  var bulan   = bulan[arrTgl[1]];
  var value;

    if(bulan <= 3){ value = '1'; }
    else if(bulan <= 6){ value = '2'; }
    else if(bulan <= 9){ value = '3'; }
    else{ value = '4'; }

  $(target).val(value);
  $(target).trigger('change');
}

// JS SHOW MODAL ============================================================================================================
function CekShowModal(e,modal){

    switch(modal){
      case "lap_sp2d":
	        link_frm_lap = $(e).attr('alt');
	        showModalLaporan(modal);
	      break;

      case "tree_btl":
        var kd_organisasi = $('#organisasi').val();
        var kd_tree = $('#kd_tree').val();
        if (kd_organisasi=='0.0.0.0') {
          $.alertable.alert("Pilih Organisasi Terlebih Dahulu !!!");
          return false;
        }
        else if (kd_tree==''){
          $.alertable.alert("Rekening Belum Dipilih !!!");
          return false;
        }else if (kd_tree!='5 - BELANJA'){
          $.alertable.alert("Rekening Belum Dipilih Dengan Benar !!!");
          return false;
        }else{
          showModal(e,modal);
        }
      break;

      case "tree_bl":
        var kd_organisasi = $('#organisasi').val();
        var kd_tree = $('#kd_tree_belanja').val();
        if (kd_organisasi=='0.0.0.0') {
          $.alertable.alert("Pilih Organisasi Terlebih Dahulu !!!");
          return false;
        }
        else if (kd_tree==''){
          $.alertable.alert("Rekening Belum Dipilih !!!");
          return false;
        }else if (kd_tree!='5 - BELANJA'){
          $.alertable.alert("Rekening Belum Dipilih Dengan Benar !!!");
          return false;
        }else{
          showModal(e,modal);
        }
      break;
      
      case "tree_prapendapatanppkd":
        var kd_organisasi = $('#organisasi').val();
        var kd_tree = $('#kd_tree_pendapatan').val();
        if (kd_organisasi=='0.0.0.0') {
            $.alertable.alert("Pilih Organisasi Terlebih Dahulu !!!");	
            return false;
        }else if (kd_tree==''){
            $.alertable.alert("Rekening Belum Dipilih !!!");
            return false;
        }else if (kd_tree!='4 - PENDAPATAN'){
            $.alertable.alert("Rekening Belum Dipilih Dengan Benar !!!");
            return false;
        }else{
            showModal(e,modal);
        }
      break;
      case "lpj_upgu":
  		  if($('#organisasi').val() == 0){
  		      $.alertable.alert('Organisasi belum dipilih');
            return false;
        } else if($(".chk_setuju").is(":checked") == false){
            $.alertable.alert("Silahkan pilih data yang akan dicetak !"); 
            return false;
        } else {
            showModalLaporan(modal);
        }
      break;         
    }
}

function showModal_ajax(data, modal){
  var url_load  = "";
  var loadModal = "";
  // var linkLoad  = e;

  switch(modal) {
    case 'edit_skup':  
        loadModal = "Edit SKUP";
        // url_load  = linkLoad;
        break;
  }

  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").html(data);
  $(".modal-dialog").css('width', '800px');
}

function showModal(e,modal){
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');
  var act       = getUrlVars(linkLoad)["act"];

  switch(modal) {
    case "user":
        if(act == "add"){
          loadModal = "Tambah Pengguna TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Edit Pengguna TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

     case "bendahara_pembantu":
        if(act == "add"){
          loadModal = "Tambah Bendahara Pembantu TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Edit Bendahara Pembantu TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "set_fungsi":
        if(act == "add"){
          loadModal = "Tambah Fungsi TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Fungsi TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "set_bidang":
        if(act == "add"){
          loadModal = "Tambah Bidang TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Bidang TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "list_org":
        loadModal = "List Organisasi TA."+Thn_log;
        url_load  = linkLoad;
        break;

    case "list_keg":
        loadModal = "List Kegiatan TA."+Thn_log;
        url_load  = linkLoad;
        break;
    
    case "laporan_spm":
        var skpd = $('#kd_org2').val();
        var jenis = $('#jenis').val();
        loadModal = "Cetak Surat Permintaan Membayar "+jenis.toUpperCase()+" TA. "+Thn_log;
        url_load  = linkLoad;
        break;

    case "list_shb":
        loadModal = "List SSH TA."+Thn_log;
        url_load  = linkLoad;
        break;
        
    case "upload":
        loadModal = "Sistem Informasi Pengelolaan Keuangan Daerah";
        url_load  = linkLoad;
        break;

    case "uploadpraskpd":
        loadModal = "UPLOAD DATA PRA SKPD -> RKA SKPD TA."+Thn_log;
        url_load  = linkLoad;
        break;

    case "uploadprappkd":
        loadModal = "UPLOAD DATA PRA PPKD -> RKA PPKD TA."+Thn_log;
        url_load  = linkLoad;
        break;    
    case "datalanjutan":
        if(act == "add"){
          loadModal = "Data Kegiatan Lanjutan TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Data Lanjutan TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "lanjutanbl":
        loadModal = "Data Kegiatan Lanjutan TA."+Thn_log;
        url_load  = linkLoad;
        break;

    case "suburusan":
        if(act == "add"){
          loadModal = "Tambah Sub Urusan TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Sub Urusan TA."+Thn_log;
        }
        url_load  = linkLoad;
        break; 

    case "organisasi":
        if(act == "add"){
          loadModal = "Tambah Organisasi TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Organisasi TA."+Thn_log;
        } else if(act == "list"){
          loadModal = "List Organisasi TA."+Thn_log;
        }
        url_load  = linkLoad;
        break; 

    case 'ubahpwd':         
        loadModal = "Ubah Password TA."+Thn_log;      
        url_load = linkLoad;         
        break;

    case 'tree_btl':
        loadModal = "Pilih Rekening BTL TA."+Thn_log;
        url_load = linkLoad;
        break;

    case 'tree_bl':
        loadModal = "Pilih Rekening Belanja Langsung TA."+Thn_log;
        url_load = linkLoad;
        break;

    case 'rekening':         
        loadModal = "Tambah Rekening TA."+Thn_log;        
        url_load = linkLoad;                 
    break;    

    case 'setupmenu':  // joel ================       
        loadModal = "Ubah Data Menu TA."+Thn_log;        
        url_load = linkLoad;        
        break;

    case 'addpejabatskpkd':  
        if(act == "add"){
          loadModal = "Tambah Pejabat SKPKD TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Pejabat SKPKD TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;  

    case 'wilayah':         
        loadModal = "Setting Wilayah TA." +Thn_log;         
        url_load = linkLoad;                 
        break;   

    case "spp":
        var skpd    = $("#organisasi").val().split("-");

        if(skpd == 0){
            alertify.alert('Organisasi belum dipilih');
            return false;
        } else {
            loadModal = "Lihat Data SPP";
            url_load  = linkLoad+"?id="+skpd[0];
        }
        break;

    case "bendahara":
        var skpd    = $("#organisasi").val().split("-");

        loadModal = "Cari Bendahara";
        url_load  = linkLoad+"?id="+skpd[0];
        break; 

    case "kegiatan":
        var skpd    = $("#organisasi").val().split("-");

        loadModal = "Cari Kegiatan";
        url_load  = linkLoad+"?id="+skpd[0];
        break; 

    case "lpj":
        var skpd    = $("#organisasi").val().split("-");

        loadModal = "Cari LPJ UP/GU";
        url_load  = linkLoad+"?id="+skpd[0];
        break; 

    case "perusahaan":
        var skpd    = $("#organisasi").val().split("-");

        loadModal = "Cari Pihak Ketiga";
        url_load  = linkLoad+"?id="+skpd[0];
        break; 

    case 'addtpad':  
        if(act == "add"){
          loadModal = "Tambah TPAD TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah TPAD TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case 'adddasarhukum':  
        if(act == "add"){
          loadModal = "Tambah Dasar Hukum TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Dasar Hukum TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case 'addpejabatskpd':  
        if(act == "add"){
          loadModal = "Tambah Pejabat SKPD TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Pejabat SKPD TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case 'tree_prapembiayaan':
        loadModal = "Pilih Rekening Pembiayaan TA."+Thn_log;
        url_load = linkLoad;
        break; 

    case 'rka_bl':
        aksi = $(e).attr('act');
        if(aksi == "add"){
          loadModal = "Tambah Program TA."+Thn_log;
        } else if(aksi == "edit"){
          loadModal = "Ubah Program TA."+Thn_log;
        }
        url_load = linkLoad;
        break; 

    case "jabatan":
        if(act == "add"){
          loadModal = "Tambah Master Jabatan TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Master Jabatan TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "sumberdana":
        if(act == "add"){
          loadModal = "Tambah Sumberdana TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Sumberdana TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "urusan":
        if(act == "add"){
          loadModal = "Tambah Urusan TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Urusan TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "program":
        if(act == "add"){
          loadModal = "Tambah Program TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Program TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case "kegiatan":
        if(act == "add"){
          loadModal = "Tambah Kegiatan TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Kegiatan TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;

    case 'addsumberdanaskpd':  
        if(act == "add"){
          loadModal = "Tambah Sumberdana SKPD TA."+Thn_log;
        } else if(act == "edit"){
          loadModal = "Ubah Sumberdana SKPD TA."+Thn_log;
        }
        url_load  = linkLoad;
        break;    

    case 'tambah_skup':  
        loadModal = "Tambah SK UP";
        url_load  = linkLoad;
        break;

    case 'cetak_spd':
        loadModal = "Cetak SPD";
        url_load  = linkLoad;
        break;
    case 'cetak_sp2d_up_gu_tu_gunihil':
        loadModal = "Cetak SP2D Surat Perintah Pencairan Dana";        
        url_load  = linkLoad;
        break;
    case 'cetak_kontrol_spd':
        loadModal = "Cetak Kontrol SPD";
        url_load  = linkLoad;
        break;
  }
  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', '800px');
};

// JOEL 20 Feb 2019 ==============================================
// MODAL UNTUK INPUT LPJ =========================================
function Modal_in_LPJ(from,act){
  var data_x    = $("#check_spj").text().replace(/\//g,'_').replace(/\ /g,'+');
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = link_mdl_sp2dlpj+"?f="+from+"&a="+parseInt(act)+"&dt="+data_x;

  switch(from) {
    case 'GU':
        loadModal = "Input SPJ SP2D GU (SPJ SP2D-GU) TA. "+Thn_log;        
        url_load  = linkLoad;
        break;

    case 'TU':
        loadModal = "Input SPJ SP2D TU (SPJ SP2D-TU) TA. "+Thn_log;
        url_load  = linkLoad;
        break;
    case 'cetak_sp2d_up_gu_tu_gunihil':
        loadModal = "Cetak SP2D Surat Perintah Pencairan Dana";        
        url_load  = linkLoad;
        break;
    case 'cetak_kontrol_spd':
        loadModal = "Cetak Kontrol SPD";
        url_load  = linkLoad;
        break;
  }

  document.getElementById("myModalLabel").innerHTML = loadModal;  
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', '90%');
};

function showModalLaporan(modal){ // joel, 24 jan 2019 =======================================
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = link_frm_lap;
  var act       = getUrlVars(linkLoad)["act"];
  switch(modal) {
    case 'lap_sp2d_ppkdbtl':
        loadModal = "Cetak Laporan Surat Perintah Pencairan Dana - LS PPKD TA. "+Thn_log;
        url_load  = linkLoad;
        break;
    case 'lap_sp2d':
        loadModal = "Cetak Laporan SP2D TA. "+Thn_log;
        url_load  = linkLoad;
        break;
    case 'lap_sp2d_gaji':
        loadModal = "Cetak Laporan Surat Perintah Pencairan Dana - LS GJ TA. "+Thn_log;
        url_load  = linkLoad;
        break;
    case "lap_sp2d_barjas": 
        loadModal = "Cetak Laporan Surat Perintah Pencairan Dana - LS BARJAS TA. "+Thn_log;
        url_load  = linkLoad;
        break;
    case "lap_sp2d_nona": 
        loadModal = "Cetak Laporan Surat Perintah Pencairan Dana NON ANGGARAN TA. "+Thn_log;
        url_load  = linkLoad;
        break;
  case "lap_sp2d_tolak": 
        loadModal = "Cetak Laporan Penolakan SP2D TA. "+Thn_log;
        url_load  = linkLoad;
        break;

  }
}

function showModalLaporan(modal){ // joel =======================================
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = link_frm_lap;
  var act       = getUrlVars(linkLoad)["act"];

  switch(modal) {
    case 'laporan_spp':
        var skpd = $('#organisasi').val();
        var jenis = $('#jenis').val();        
        loadModal = "Cetak Surat Permintaan Pembayaran "+jenis.toUpperCase()+" TA. "+Thn_log;
        url_load  = linkLoad+"?skpd="+skpd;
        break;    
    
    case "lpj_upgu":
        var judul   = $("#judul_form").html();
        var skpd    = "?skpd="+$("#organisasi").val();
        var form    = $('#jenis').val();
        var nolpj   = [];
        var jenis   = "";
        var jnsCtk  = 0; 
        if(form != "PENGEMBALIAN"){ jnsCtk = 0; } else { jnsCtk = 1; }
    		$(".chk_setuju:checked").each(function() {
            nolpj.push($(this).attr("value").replace(' ','+'));
            jenis = $("#jenis_lpj").attr("alt");
        });
            
        var title = "&judul="+judul.toUpperCase().replace(/\//g,'_').replace(' ','+');
        loadModal = "Cetak "+judul;
        url_load  = linkLoad+skpd+"&nolpj="+nolpj+"&jnsct="+jnsCtk+"&jenis="+jenis+title;
             
        break;  
  } 

  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', '800px');
}

function modal_searching(e,modal){ // joel =============================
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');

  switch(modal) {
    case 'perda':         
      loadModal = "Cari Dasar Hukum TA. "+Thn_log;         
      url_load  = linkLoad;         
      break;

    case 'list_kegiatan':
      switch(form_sp2d){
        case 'sp2d_laporan':
          var urai = $("#lapForm_sp2d #org_tampilkan").val();
          var skpd = $("#lapForm_sp2d #organisasi").val();
        break;

        case 'sp2d_barjas':
          var urai = $("#org_tampilkan").val();
          var skpd = $("#organisasi").val();
        break;
      }

      if(skpd != ""){
          loadModal = "Cari Data Kegiatan "+urai+" TA. "+Thn_log;         
          url_load  = linkLoad+"?id="+skpd+"&frm="+form_sp2d;  
      } else {
          $.alertable.alert("Organisasi belum dipilih !"); return false;
      }   
      break;

    case 'edit_advis':
      var dtAdvis = $("#inp_advis").val().split("|");
      var tanggal = $("#per_tgl_advis").val();

      loadModal = "Edit Advis SP2D TA. "+Thn_log;         
      url_load  = linkLoad+"?ad="+dtAdvis[0]+"&tg="+tanggal;         
      break;

    case 'sp2d_mdl_cut':
      var rowid = $(e).attr('rowid');
      loadModal = "Cari Data Rekening Potongan TA. "+Thn_log;         
      url_load  = linkLoad+"?i="+rowid;
      break;

    case 'list_org':
      loadModal = "Cari Data Organisasi TA. "+Thn_log;         
      url_load  = linkLoad;         
      break;

    case 'awesome':
      loadModal = "Cari Ikon Font Awesome";         
      url_load  = linkLoad;         
      break; 

    case 'sp2d_for_bku':
      var skpd = $("#organisasi").val();
      var asal = $("#aksi").attr('alt');
      if(skpd == ""){
          $.alertable.alert("Organisasi belum dipilih !"); return false;
      } else {
          loadModal = "Cari SP2D "+asal+" TA. "+Thn_log;         
          url_load  = linkLoad+"?id="+skpd+"&as="+asal;  
      }       
      break;

    case 'sp2d_lpj_tu_gu':
      var skpd = $("#organisasi").val();
      var asal = $("#aksi").attr('alt');
      if(skpd == ""){
          $.alertable.alert("Organisasi belum dipilih !"); return false;
      } else {
          loadModal = "Cari LPJ "+asal+" TA. "+Thn_log;         
          url_load  = linkLoad+"?id="+skpd+"&as="+asal;  
      }       
      break;

    case 'sp2d_lihat_spj':
      var skpd = $("#organisasi").val();
      var asal = $("#aksi").attr('alt');
      if(skpd == ""){
          $.alertable.alert("Organisasi belum dipilih !"); return false;
      } else {
          loadModal = "Cari SPJ "+asal+" TA. "+Thn_log;         
          url_load  = linkLoad+"?id="+skpd+"&as="+asal;  
      }       
      break;
  } 

  document.getElementById("ReportModalLabel").innerHTML = loadModal;
  $("#ReportModal").modal();
  $(".modal-body-report").load(url_load);
  $(".modal-search").css('width', '800px');
}

function showModalSmall(e,modal){
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = $(e).attr('alt');
  // var act       = getUrlVars(linkLoad)["act"];

  switch(modal) {
    case 'perubahan':         
        loadModal = "Setting Perubahan TA. "+Thn_log         
        url_load = linkLoad;         
        break;

    case 'rekening':
        loadModal = "Pilih Rekening Pendapatan TA. "+Thn_log         
        url_load = linkLoad;         
        break;

  } 

  document.getElementById("myModalLabel").innerHTML = loadModal;  
  $("#showModal").modal();  
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', '500px');

};

// SHOW REPOT WITH IFRAME IN MODAL
function ShowIframeReport(res, title){
  var ifrm = document.createElement("iframe");
  ifrm.setAttribute("src", res+"#zoom=90");  ifrm.setAttribute("frameborder", 0);
  ifrm.style.width  = "100%";
  ifrm.style.height = "500px";
  // ifrm.style.background = "#F6F6F6";
  ifrm.style.background = "url(/statics/images/loading.gif) no-repeat center top";

  document.getElementById("ReportModalLabel").innerHTML = title;
  $("#ReportModal").modal();
  $(".modal-body-report").html(ifrm);
  $(".modal-search").css('width', '');
}

function adjust_datatable(){ // joel    
  $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
}

// IF DOKUMEN SIYAP
$(document).ready(function() {

  // LOAD INPUT MASK NIP & NPWP
  $(":input").inputmask();

  // LOAD LOADING MODAL
  var images  = '<div width="100%" style="text-align:center;"><img src="/statics/images/30.gif"></div>';

  $("#showModal").on("show.bs.modal", function() {
    $(".modal-body-showmodal").html(images);

    $('.modal .modal-body').css('overflow-y', 'auto');  // joel
    $('.modal .modal-body').css('min-height', $(window).height() * 0.1); // joel
  });

  $("#ReportModal").on("show.bs.modal", function() {
    $(".modal-body-report").html(images);
  });

  $('#ReportModal').on('shown.bs.modal', function(e){ // joel
      adjust_datatable();
  });

  $('#showModal').on('shown.bs.modal', function(e){ // joel
     adjust_datatable();
     isModal = "true";
  });  

  $('#showModal').on('hide.bs.modal', function(e){ // joel
     isModal = "false";
     $(".modal-body-showmodal").html('');
     adjust_datatable();
  }); 

  $('#ReportModal').on('hide.bs.modal', function(e){ // joel
     $(".modal-body-report").html('');
     adjust_datatable();
  });

  // BUTTON NEXT AND BACK Input LPJ SP2D UP/GU (LPJ SP2D-UP/GU)
  $('.continue').click(function(){
    $('.nav-tabs > .active').next('li').find('a').trigger('click');
  });
  $('.back').click(function(){
    $('.nav-tabs > .active').prev('li').find('a').trigger('click');
  });

  $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){ // joel
     $($.fn.dataTable.tables(true)).DataTable()
        .columns.adjust()
        .fixedColumns().relayout();
  });



});

function generate_tabel(id_tabel,id_kode_tree,selectableNodes,searchingnodes,nm_klik_kanan,arg){
    var jml_child, jumlah_child = 0;
    var volume, volume_p = 0;
    arr = []
    if (selectableNodes!=undefined) {
        jml_child = selectableNodes.length;
        for (var i = 0; i < jml_child; i++) {
            no=i+1;
            if(selectableNodes[i].volume == ''){
                volume = 0;
            }else{
                volume = selectableNodes[i].volume;
            }
            if(selectableNodes[i].volume_p == ''){
                volume_p = 0;
            }else{
                volume_p = selectableNodes[i].volume_p;
            }

            if (selectableNodes[i].jumlah-selectableNodes[i].jumlah_p<0) {
                hasil = '('+toRp_WithDecimal((selectableNodes[i].jumlah-selectableNodes[i].jumlah_p)*-1)+')'
            }else{
                hasil = toRp_WithDecimal(selectableNodes[i].jumlah-selectableNodes[i].jumlah_p)
            }
            jumlah_child = selectableNodes[i].child.split('.').length;
            if(jumlah_child>5){
              arr.push([selectableNodes[i].child.split('.')[selectableNodes[i].child.split('.').length-1],selectableNodes[i].urai,volume,selectableNodes[i].satuan,toRp_WithDecimal(selectableNodes[i].harga),toRp_WithDecimal(selectableNodes[i].jumlah),volume_p,selectableNodes[i].satuan_p,toRp_WithDecimal(selectableNodes[i].harga_p),toRp_WithDecimal(selectableNodes[i].jumlah_p),hasil]);  
            }else{
              arr.push([selectableNodes[i].child,selectableNodes[i].urai,volume,selectableNodes[i].satuan,toRp_WithDecimal(selectableNodes[i].harga),toRp_WithDecimal(selectableNodes[i].jumlah),volume_p,selectableNodes[i].satuan_p,toRp_WithDecimal(selectableNodes[i].harga_p),toRp_WithDecimal(selectableNodes[i].jumlah_p),hasil]);  
            }
        }
    }else if(selectableNodes==undefined){
        no=1;
        if(searchingnodes.volume == ''){
            volume = 0;
        }else{
            volume = searchingnodes.volume;
        }
        if(searchingnodes.volume_p == ''){
            volume_p = 0;
        }else{
            volume_p = searchingnodes.volume_p;
        }
        if (searchingnodes.jumlah-searchingnodes.jumlah_p<0) {
                hasil = '('+toRp_WithDecimal((searchingnodes.jumlah-searchingnodes.jumlah_p)*-1)+')'
            }else{
                hasil = toRp_WithDecimal(searchingnodes.jumlah-searchingnodes.jumlah_p)
            }  
            // console.log('test');      
        // arr.push([searchingnodes.child.split('.')[searchingnodes.child.split('.').length-1],searchingnodes.urai,volume,searchingnodes.satuan,toRp_WithDecimal(searchingnodes.harga),toRp_WithDecimal(searchingnodes.jumlah),volume_p,searchingnodes.satuan_p,toRp_WithDecimal(searchingnodes.harga_p),toRp_WithDecimal(searchingnodes.jumlah_p),hasil]);
    }
    
    $('#'+id_tabel+'').DataTable( {
        destroy:true,
        "scrollY": 150,   
        "scrollX": true,          
        "paging": false,
        "searching": false,
        "info":false,
        data: arr,
        'createdRow':  function (row, data, index) {
           $('td', row).eq(2).attr('class', 'volume');
           $('td', row).eq(4).attr('class', 'field_angka');
           $('td', row).eq(5).attr('class', 'field_angka');
           $('td', row).eq(6).attr('class', 'volume');
           $('td', row).eq(8).attr('class', 'field_angka');
           $('td', row).eq(9).attr('class', 'field_angka');
           $('td', row).eq(10).attr('class', 'field_angka');
        }
    });

    $('tbody > tr').css({ 'cursor': 'pointer'});
    $("#"+id_tabel+"  tr").click(function(){
        $('.selected').removeClass('selected');
        $(this).addClass('selected');
        var tr          = $(this).closest("tr");
            RowIndek    = tr.index();

        var Kls         = tr.attr('class');
        var arKl        = Kls.split(" ");
            clsSelek    = arKl[1];
    });

    $( "#"+id_tabel+"  tr" ).contextmenu(function(event) {
        var node_remove = $("#"+id_kode_tree+"").val().replace(/\s/g, "").split("-");
        var kode = node_remove[0].split(".");
        var pjg_kode = kode.length;

        event.preventDefault();
        if ($("#"+id_kode_tree+"").val()=='') {
            $.alertable.alert('Rekening Belum Dipilih!!!');
        } else{
            if (pjg_kode==1) {
                $('#menu-kustom').html("<a onclick='"+nm_klik_kanan+"(\"add\",\""+arg+"\")'><li>Tambah "+arg.toUpperCase()+"</li></a>");
            } else if(pjg_kode==5){
                $('#menu-kustom').html("<a onclick='"+nm_klik_kanan+"(\"add\",\"sub1\")'><li>Tambah SUB1</li></a><a onclick='"+nm_klik_kanan+"(\"del\",\"parent\")'><li>Hapus "+$('#'+id_kode_tree+'').val()+"</li></a>");
            }else if(pjg_kode==6){
                $('#menu-kustom').html("<a onclick='"+nm_klik_kanan+"(\"add\",\"sub2\")'><li>Tambah SUB2</li></a><a onclick='"+nm_klik_kanan+"(\"del\",\"sub1\")'><li>Hapus "+$('#'+id_kode_tree+'').val()+"</li></a>");
            }else if(pjg_kode==7){
                $('#menu-kustom').html("<a onclick='"+nm_klik_kanan+"(\"add\",\"sub3\")'><li>Tambah SUB3</li></a><a onclick='"+nm_klik_kanan+"(\"del\",\"sub2\")'><li>Hapus "+$('#'+id_kode_tree+'').val()+"</li></a>");
            }else if(pjg_kode==8){
                $('#menu-kustom').html("<a onclick='"+nm_klik_kanan+"(\"del\",\"sub3\")'><li>Hapus "+$('#'+id_kode_tree+'').val()+"</li></a>");
            }
            $(".menu-kustom").finish().toggle(255)
             .css({
                  "top": event.pageY + "px",
                  "left": event.pageX + "px"
             });           
        }
        
    }); 

    $('tbody > tr> td.field_angka').css({ 'text-align': 'right'});
    $('tbody > tr> td.volume').css({ 'text-align': 'center'});

    $('thead > tr> th.uraian-tbl').css({ 'min-width': '300px', 'max-width': '300px' });
    $('thead > tr> th.rekening').css({ 'min-width': '60px', 'max-width': '70px' });
    $('thead > tr> th.satuan').css({ 'min-width': '80px', 'max-width': '100px'});
    $('thead > tr> th.jumlah').css({ 'min-width': '80px', 'max-width': '100px'});
}

function get_url_js(){
  var pageURL = $(location).attr("href");
  pageURL = pageURL.split("/");
  pageURL = "/"+pageURL[3]+"/"+pageURL[4]+"/"+pageURL[5]+"/";
  return pageURL;
}

function render_modal(header,asal,js_arg){
  asal_modal = asal;
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_modal,
      data: {'asal':asal,'js_arg':JSON.stringify(js_arg),},
      dataType: 'html',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        $('#ReportModalLabel').html(header);
        $("#ReportModal").modal();
        $(".modal-body-report").html(data);
        $(".modal-dialog").css('width', '800px');
        $(".cover").hide();
      }
  });
}

function is_skpkd_js(g){
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_is_skpkd,
      data: {'g':g},
      dataType: 'html',
      success: function(data){
        var_skpkd = data;
      }
  });
}

// //mendefinisikan satuan 
// var units = [' ',  'ribu ', 'juta', 'milyar',  'triliun', 'biliun'];
// //Mendefinisikan bilangan
// var angka = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan"];
// //membuat function untuk memecah bilangan menjadi array beranggota 3 digit
// var terbilang = function(feed) {
  
//   //menginisiasi luaran
//   var output = '';
  
//   if (feed.length % 3 > 0) {
//     feed = '00'.substr(0, (3 - feed.length % 3)) + feed;
//     //1234 akan diubah menjadi 001234
//   }
//   //menyisipkan titik sebagai separator 
//   //001234 akan diubah menjadi 001.123
//   while (/(\d+)(\d{3})/.test(feed)) {
//     feed = feed.replace(/(\d+)(\d{3})/, '$1' + '.' + '$2');
//   }

//   var segment3 = feed.split('.'); 
//   //Membilang setiap segmen 3 digit
//   $.each(segment3, function(i, v){
//     //memecah 3 digit menjadi arrau 1 digit
//     var digit = v.split('');
//     //menentukan nilai ratusan
//     if(digit[0] == '1'){
//       output += 'seratus ';
//     }else if(digit[0] != '0'){
//       output += angka[digit[0]] + ' ratus ';    
//     }
//     //menentukan nilai puluhan
//     if(digit[1] == '1'){
//       if(digit[2] == '0'){
//         output += 'sepuluh ';
//       }else{
//         output += angka[digit[2]]+ 'belas '; 
//       }          
//     }else if(digit[1] != '0'){
//       output += angka[digit[1]] +' puluh ' + angka[digit[2]]+' ';
//     }else{
//       if(digit[0] == '0' && digit[1]=='0' && digit[2]=='1'){
//         output += 'se';
//       }else{
//         output += angka[digit[2]]+ ' ';
//       }
//     }
//     output += units[segment3.length-i-1]+' ';
//   })
//   return output+' rupiah';
// }

if (get_url_js()!="/sipkd/spd/pengisianskup/") {
  sessionStorage.removeItem("last_org_skup");
}

$('.select_tabel tbody').on( 'click', 'tr', function () {
    if ( $(this).hasClass('selected') ) {
        $(this).removeClass('selected');
    }
    else {
        $('.select_tabel').DataTable().$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }
} );

function render_laporan(header,data){
  $('#myModalLabel').html(header);
  $("#showModal").modal();
  $(".modal-body-showmodal").html(data+'.html');
  $(".modal-dialog").css('width', '800px');
}

function ambilBank(){
  $.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambilBank,
        data :{
            'koderekening':$('#norek_bankasal').val(),
        },
        dataType: 'html',
        success: function(data){
          hasilnya = JSON.parse(data)['rekening'][0];

          $('#bank_asal').val(hasilnya['bank_asal']);
          $('#bank_bendahara').val(hasilnya['bank']);
        },
        error: function(){
            message_ok('error', 'Proses ambil data bank gagal !');
        }
    });
}

function action_sp2dsekarang(e,index,pjg_row) {
  sekarang_verti = 0;
  jumlah_verti = 0;
  sisa_verti = 0;

  anggaran = parseFloat(toAngkaDec($('#anggaran_'+index+'').val()));
  batas = parseFloat(toAngkaDec($('#batas_'+index+'').val()));
  lalu = parseFloat(toAngkaDec($('#lalu_'+index+'').val()));
  sekarang = e.value == '' ? parseFloat(toAngkaDec('0,00')):parseFloat(toAngkaDec(e.value));
  jumlah = parseFloat(toAngkaDec($('#jumlah_'+index+'').val()));
  sisa = parseFloat(toAngkaDec($('#sisa_'+index+'').val()));

  jum_hori = lalu+sekarang;
  sisa_hori = anggaran - (lalu+sekarang);

  // Mengubah nilai
  if (jum_hori>anggaran) {
    $.alertable.alert('Jumlah SP2D melebihi anggaran');
    $('#jumlah_'+index+'').focus();
  }else{
    $('#jumlah_'+index+'').val(toRp_WithDecimal(jum_hori));
    $('#sisa_'+index+'').val(toRp_WithDecimal(sisa_hori));

    //jumlah vertikal (perkolom)

    array_jumlah_sekarang=[];

    for (var i = 0; i < pjg_row; i++) {
      sekarang_verti =sekarang_verti  + parseFloat(toAngkaDec($('#sekarang_'+i+'').val()==''?'0,00':$('#sekarang_'+i+'').val()));
      jumlah_verti = jumlah_verti + parseFloat(toAngkaDec($('#jumlah_'+i+'').val()));
      sisa_verti = sisa_verti + parseFloat(toAngkaDec($('#sisa_'+i+'').val()));
      
      value_sekarang = $('#sekarang_'+i+'').val() == '' ? toAngkaDec('0,00'):toAngkaDec($('#sekarang_'+i+'').val());

      if ($('#check_'+i).is(":checked")==true) {
        // console.log(parseFloat(toAngkaDec($('#sekarang_'+i+'').val())));
        array_jumlah_sekarang.push($('#val_rinci_'+i+'').val()+'^'+parseFloat(value_sekarang)+'^'+parseFloat(toAngkaDec($('#anggaran_'+i+'').val()))+'^'+$('#otorisasi_'+i+'').val());
      }
      
    }

    var table = $('#tabelnya').DataTable();

    $( table.column( 6 ).footer() ).html(toRp_WithDecimal(sekarang_verti)); //sekarang
    $( table.column( 7 ).footer() ).html(toRp_WithDecimal(jumlah_verti)); //jumlahsp2d
    $( table.column( 8 ).footer() ).html(toRp_WithDecimal(sisa_verti)); //sisa
    $(e).val(toRp_WithDecimal(e.value == '' ? parseFloat(toAngkaDec('0,00')):parseFloat(toAngkaDec(e.value))));
    $('#jml_sp2d').text(toRp_WithDecimal(sekarang_verti));
    $('#sp2d_terbilang').text(terbilang(toAngkaDec(toRp_WithDecimal(sekarang_verti))));
  }
}

function updateJumlah(hasil_rekening) {
    var jumlah_bawah = 0;
    for (var i = 0; i < hasil_rekening['rekening'].length; i++) {
      jumlah_bawah = jumlah_bawah + parseFloat(hasil_rekening['rekening'][i][6]);
    }
    $('#jml_sp2d').text(toRp_WithDecimal(jumlah_bawah));
    $('#sp2d_terbilang').text(terbilang(toAngkaDec(toRp_WithDecimal(jumlah_bawah))));
}