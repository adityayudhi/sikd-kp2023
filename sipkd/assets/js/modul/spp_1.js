/*
JavaScript untuk modul SPP
created by Kurnianto Tri Nugoroho @GI 2019 
SIPKD Application

===============================================================================================================================
*/

var NoSPP     = "";
var isSimpan  = true;
var isTambah  = true;
var SumNoSPP  = "";
var cekSukses = false;

function CekNoSPP(URL,skpd,nospp){ 
  if(nospp){
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: URL,
        dataType: "json",
        data: {skpd:skpd, spp:nospp},
        async: false,
        success: function(msg){
          SumNoSPP = msg['nospp'];
        }
    });
  }
  return SumNoSPP;
}

function clearFormSPP_UP(skpd){
    NoSPP = "";
    isSimpan = true;
    isTanggal= false;
    
    $('#org_tampilkan').val('');
    $('#organisasi').val('');
    $('#no_spp').val('');
    $('#kunci_spd').html('(DRAFT)');
    $('#tanggal_spp').val(DateNowInd());
    $('#bendahara').val('');
    $('#norek_bendahara').val('');
    $('#npwp_bendahara').val('');
    $('#nama_bank').val('');
    $('#nomor_skup').val('');
    $('#tanggal_skup').val(DateNowInd());
    $('#jumlah_skup').val('');
    $('#dasar_spd').val('');
    $('#nama_rekening_bank').val('');
    $('#tanggal_spd').val(DateNowInd());
    $('#jumlah_spd').val('');
    $('#sisa_spd').val('');
    $('#status_keperluan').val('');
    $('#TotalSPP').html('0,00');
    $('#terbilang').html('Nol Rupiah');
    $("#no_spp").attr('readonly', false);

    // getTriwulan('#tanggal_spp','#triwulan');
    // $('#inpt_triwulan').val($('#triwulan').val());

    loadPertama('btn_simpan','1');
    loadPertama('btn_hapus','0');

}

function clearFormSPP_PPKD(skpd){
    var jenis = $('#jenis').val();
    var table = $('#dataspd').DataTable();    
    NoSPP = "";
    isSimpan = true;
    isTanggal= false;

    // console.log(jenis);    

    if((jenis=='gu') || (jenis=='gu_nihil')){
      $('#organisasi').val('');
      $('#org_tampilkan').val('');
      $('#no_lpj').val(''); 
      table.clear().draw();
      $('#no_lpj').attr('readonly',false);
      $("#btn_no_lpj").css('pointer-events','');               
    }else if(jenis=='ls'){
      $('#organisasi').val('');
      $('#org_tampilkan').val('');
      $('#kode_bidang').val('');
      $('#kode_program').val('');
      $('#kode_kegiatan').val('');
      $('#urai_kegiatan').val('');
      $('#jenis_dpa').val(0);
      $('#tanggal_dpa').val('');
      $('#nomor_dpa').val('');
      $('#pelaksanaan').val('');
      $('#nama_perusahaan').val('');
      $('#alamat_perusahaan').val('');
      $('#pimp_perusahaan').val('');
      $('#bank_perusahaan').val('');
      $('#nomor_kontrak').val('');
      $('#npwp_perusahaan').val('');
      $('#norek_perusahaan').val('');
      $('#bentuk_perusahaan').val(0);
    }else if(jenis=='gj'){
      $('#organisasi').val('');
      $('#org_tampilkan').val('');      
    }else if(jenis=='tu'){
      $('#organisasi').val('');
      $('#org_tampilkan').val('');      
    }    
    $('#no_spp').val('');
    $('#kunci_spd').html('(DRAFT)');
    $('#tanggal_spp').val(DateNowInd());
    $('#bendahara').val('');
    $('#norek_bendahara').val('');
    $('#npwp_bendahara').val('');
    $('#nama_bank').val('');    
    $('#status_keperluan').val('');
    $('#nama_rekening_bank').val('');
    $('#TotalSPP').html('0,00');
    $('#terbilang').html('Nol Rupiah');
    $('input[name="aksi"]').val(isSimpan);
    $('#no_spp').attr('readonly',false);
    // $('#tanggal_spp').attr('disabled',false);

    getTriwulan('#tanggal_spp','#triwulan');
    ambilAfektasi();
    // $('#inpt_triwulan').val($('#triwulan').val());

    loadPertama('btn_simpan','1');
    loadPertama('btn_hapus','0');

}

function org_skpd_change_up(val){        
    var urls     = $("#url_tabel").val();
    var Cookie   = getCookie("sppUPSKPD");       
  
    if(val != 0){
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
          success: function(data){              
            datanya = JSON.parse(data)['list_up'];
            $('#no_spp').focus();         
            if(datanya!=''){                
              rp = datanya[0].jumlahspp;                
              uraian_terbilang = rp.replace('.00','');                
              if(datanya[0].nospp!=''){
                $.alertable.alert('SPP UP sudah pernah dibuat !');
              }
              NoSPP = datanya[0].nospp;               
              $('input[name="no_spp_lama"]').val(datanya[0].nospp);
              $('#no_spp').val(datanya[0].nospp);               
              $('#tanggal_spp').val(datanya[0].tglspp);
              $('#bendahara').val(datanya[0].bendaharapengeluaran);
              $('#norek_bendahara').val(datanya[0].norekeningbendahara);
              $('#npwp_bendahara').val(datanya[0].npwp);
              $('#nama_bank').val(datanya[0].namabank);
              $('#nomor_skup').val(datanya[0].sk_up);
              $('#tanggal_skup').val(datanya[0].tgl_sk_up);
              $('#jumlah_skup').val(toRp_WithDecimal(datanya[0].jml_sk_up));
              $('#dasar_spd').val(datanya[0].nospd);
              $('#tanggal_spd').val(datanya[0].tglspd);
              $('#jumlah_spd').val(toRp_WithDecimal(datanya[0].jmlspd));
              $('#sisa_spd').val(toRp_WithDecimal(datanya[0].sisadanaspd));
              $('#status_keperluan').val(datanya[0].deskripsipekerjaan);
              $('#nama_rekening_bank').val(datanya[0].namarekeningbank);

              $('#TotalSPP').html(toRp_WithDecimal(datanya[0].jumlahspp));
              $('#terbilang').html(terbilang(rp));                

              if(datanya[0].locked == 'Y'){
                $('#kunci_spd').val('(DISETUJUI)');
                $("#kunci_spd").addClass('disetujui');
                $("#no_spp").attr('readonly', true);
                // $('#tanggal_spp').attr('disabled',true);
                loadPertama('btn_simpan','0');
                loadPertama('btn_hapus','0');
                if(jenis=='gu'||jenis=='gu_nihil'){
                  $("#no_lpj").attr('readonly', true);
                  $("#btn_no_lpj").css('pointer-events','none');
                }
              }else{
                $('#kunci_spd').val('(DRAFT)');
                $("#kunci_spd").removeClass('disetujui');
                $("#no_spp").attr('readonly', false);
                // $('#tanggal_spp').attr('disabled',false);
                loadPertama('btn_simpan','1');
                loadPertama('btn_hapus','1');
                if(jenis=='gu'||jenis=='gu_nihil'){
                  $("#no_lpj").attr('readonly', false);
                  $("#btn_no_lpj").css('pointer-events','');
                }
              }

              isSimpan = false;
              $('input[name="aksi"]').val(isSimpan);                
            } else {                
              $('#no_spp').val('');
              $('#kunci_spd').html('(DRAFT)');              
              $('#bendahara').val('');
              $('#norek_bendahara').val('');
              $('#npwp_bendahara').val('');
              $('#nama_bank').val('');        
              $('#nomor_skup').val('');
              $('#jumlah_skup').val('');
              $('#nama_rekening_bank').val('');
              $('#tanggal_spp').val(DateNowInd()); 
              $('#tanggal_skup').val(DateNowInd());              
              $('#tanggal_spd').val(DateNowInd());
              $('#jumlah_spd').val('');
              $('#sisa_spd').val('');
              $('#status_keperluan').val('');
              $('#TotalSPP').html('0,00');
              $('#terbilang').html('Nol Rupiah');

              ambilSKUP(val);
              loadPertama('btn_hapus','0');
          }
         
          $(".cover").hide();
       }
      });
    }else {
      clearFormSPP_UP(val);
    }
    
    if(Cookie != ''){
      removeCookie("sppUPSKPD");
    }
}

function ambilSKUP(val){
    var cek_skup = $("#cek_skup").val();
    $.ajax({
        type: "GET",
        url: cek_skup,
        data: {id:val},
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function() {
          $(".cover").show();
        },
        success: function(data){              
          datanya = JSON.parse(data)['list_up'];   
          $('#no_spp').focus();         
          if(datanya!=''){                
            rp = datanya[0].jumlahspp;                
            uraian_terbilang = rp.replace('.00','');                
            
            $('#no_spp').val('');               
            $('#tanggal_spp').val(datanya[0].tglspp);              
            $('#nomor_skup').val(datanya[0].sk_up);
            $('#tanggal_skup').val(datanya[0].tgl_sk_up);
            $('#jumlah_skup').val(toRp_WithDecimal(datanya[0].jml_sk_up));
            $('#dasar_spd').val(datanya[0].nospd);
            $('#tanggal_spd').val(datanya[0].tglspd);
            $('#jumlah_spd').val(toRp_WithDecimal(datanya[0].jmlspd));
            $('#sisa_spd').val(toRp_WithDecimal(datanya[0].sisadanaspd));              
            $('#TotalSPP').html(toRp_WithDecimal(datanya[0].jumlahspp));
            $('#terbilang').html(terbilang(rp));

            isSimpan = true;
            $('input[name="aksi"]').val(isSimpan); 
          } else {  
            $.alertable.alert('SK UP Belum dibuat. Mohon Hubungi Bidang Anggaran !');
          }
        }
    });  
}

function cekSimpanData(url){    
  var skpd  = $('#organisasi').val();
  var noSPP = $('#no_spp').val();
  var jenis = $('#jenis').val();  

  CekNoSPP(url,skpd,noSPP);
  if(isSimpan==true){    
    if(NoSPP != noSPP){      
      if(SumNoSPP > 0){
          $.alertable.alert("Nomor SPP : "+noSPP+", sudah digunakan.");
          return false;
      }
    }
  }   
  
  if($('#organisasi').val() == 0){
      $.alertable.alert('Organisasi Belum dipilih');
  } else if($('#no_spp').val() == ""){
      $.alertable.alert('Nomor SPP belum diisi');
  } else if($('#tanggal_spp').val() == ""){
      $.alertable.alert('Tanggal SPP belum diisi');
  } else if($('#bendahara').val() == ""){
      $.alertable.alert('Nama Bendahara belum diisi');
  } else if($('#norek_bendahara').val() == ""){
      $.alertable.alert('Nomor Rekening Bank belum diisi');
  } else if($('#nama_rekening_bank').val() == ""){
      $.alertable.alert('Nama Pemilik Rekening belum diisi');
  } else if($('#nama_bank').val() == ""){
      $.alertable.alert('Nama Bank belum diisi');
  } else if($('#npwp_bendahara').val() == ""){
      $.alertable.alert('NPWP belum diisi');
  } else if($('#status_keperluan').val() == ""){
      $.alertable.alert('Status Keperluan Belum diisi');
  }else {      
      if(jenis=='up'){
        simpanData();
      }else if(jenis=='ls ppkd'){        
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
            cekBatas_SPP();                     
          });
        }else{
          cekBatas_SPP();
        }     
      }else if(jenis=='ls'){
        if($('#urai_kegiatan').val() == ""){
          $.alertable.alert('Kegiatan Belum dipilih');
        } else if($('#pelaksanaan').val() == ""){
          $.alertable.alert('Waktu Pelaksanaan belum diisi');
        }else if($('#nama_perusahaan').val() == ""){
          $.alertable.alert('Nama Perusahaan belum diisi');
        }else if($('#bentuk_perusahaan').val() == 0){
          $.alertable.alert('Bentuk Perusahaan belum dipilih');
        }else if($('#alamat_perusahaan').val() == ""){
          $.alertable.alert('Alamat Perusahaan belum diisi');
        }else if($('#pimp_perusahaan').val() == ""){
          $.alertable.alert('Nama Pimpinan belum diisi');
        }else if($('#npwp_perusahaan').val() == ""){
          $.alertable.alert('NPWP belum diisi');
        }else if($('#bank_perusahaan').val() == ""){
          $.alertable.alert('Nama Bank Perusahaan belum diisi');
        }else if($('#norek_perusahaan').val() == ""){
          $.alertable.alert('No. Rekening Perusahaan belum diisi');
        }else if($('#nomor_kontrak').val() == ""){
          $.alertable.alert('No. Kontrak Perusahaan belum diisi');
        }else if($('#jenis_dpa').val() == 0){
          $.alertable.alert('Jenis DPA belum dipilih');
        }else{
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
                cekBatas_SPP();                     
              });
            }else{
              var chekOto = $(".afektasichk").is(":checked");
              if(chekOto==false){
                  $.alertable.confirm("Rekening Belum ada yang dipilih");
              }else{
                  cekBatas_SPP();
              }              
            }    
        }
      }else if(jenis=='gu' || jenis=='gu_nihil' || jenis=='tu_nihil'){                
        if($('#no_lpj').val()==""){
          $.alertable.alert('Nomor LPJ belum diisi');
        }else{
          simpanDataSPP();
        }  
      }else{
        simpanDataSPP();
      }
  }
}

function cekBatas_SPP(){  
  var val = []; var sekarang = [];  
  var lalu = []; var batas = [];
  var koderekening = []; var urai = [];
  var batas_rekening = '';    
  $(':checkbox:checked').each(function(i){
      val[i] = $(this).val().split('|'); 
      console.log(val[i]);
      koderekening[i] = val[i][0];
      sekarang[i] = val[i][1];
      urai[i] = val[i][3];     
      lalu[i] = val[i][4]; 
      batas[i] = val[i][5];            
      
      if((eval(toAngkaDec(sekarang[i]))+eval(toAngkaDec(lalu[i])))>eval(toAngkaDec(batas[i]))){
        batas_rekening = batas_rekening +', '+ koderekening[i]+' '+urai[i];                
      }     
  });
  batas_rekening = batas_rekening.substr(1,batas_rekening.length); 

  if(batas_rekening != ''){
    $.alertable.alert("Rekening "+batas_rekening+" melebihi batas. Harap Ubah Anggaran Kas dan Perbaiki SPD di Bidang Anggaran!"); return false;
  }else{
    simpanDataSPP();
  } 

}

function jenisDPAOnChange(val){

  var jns   = $("#jenis_dpa option:selected").text();
  var skpd  = $("#organisasi").val();
  var url   = $("#jenis_dpa").attr("alt");

  $.ajax({
      type: 'POST',
      url: url,
      headers: { "X-CSRFToken": csrf_token },
      dataType: "json",
      data: {skpd:skpd, jns:jns},
      success: function (data) {  
        if(data['tanggal']==null){
          var enable = '-1';
        }else{
          var enable = '1';
        }     
        $("#tanggal_dpa").val(data['tanggal']);
        loadPertama('btn_simpan',enable);
        if(enable == "-1"){
            $.alertable.alert("Tanggal penetapan "+jns+" belum disetting ! Silakan setting melalui Konfig -> Setting Dasar Hukum");
        }
      }
  });
}

function simpanData(){
  var organisasi = $("#organisasi").val();
  var no_spp = $("#no_spp").val();
  var no_spp_lama = $("#no_spp_lama").val();
  var tanggal_spp = $("#tanggal_spp").val();
  var bendahara = $("#bendahara").val();
  var norek_bendahara = $("#norek_bendahara").val();
  var nama_bank = $("#nama_bank").val();
  var npwp_bendahara = $("#npwp_bendahara").val();
  var status_keperluan = $("#status_keperluan").val();
  var nomor_skup = $("#nomor_skup").val();
  var tanggal_skup = $('#tanggal_skup').val();
  var jumlah_skup = toAngkaDec($('#jumlah_skup').val());
  var dasar_spd = $('#dasar_spd').val();
  var tanggal_spd = $('#tanggal_spd').val();
  var jumlah_spd = toAngkaDec($('#jumlah_spd').val());
  var sisa_spd = toAngkaDec($('#sisa_spd').val());
  var aksi = $("#aksi").val();
  var simpanUP = $("#simpanUP").val();    
  var nama_rekening_bank = $("#nama_rekening_bank").val();    

  $.alertable.confirm("Anda yakin akan menyimpan data data?").then(function() {            
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: simpanUP,
        data: {         
          'organisasi':organisasi,
          'no_spp':no_spp,
          'no_spp_lama' : no_spp_lama,
          'tanggal_spp':tanggal_spp,
          'bendahara' : bendahara,
          'norek_bendahara' : norek_bendahara,
          'nama_bank' : nama_bank,
          'npwp_bendahara' : npwp_bendahara,
          'status_keperluan' : status_keperluan,
          'nomor_skup' : nomor_skup,
          'jumlah_skup' : jumlah_skup,
          'dasar_spd' : dasar_spd,
          'tanggal_spd' : tanggal_spd,
          'jumlah_spd' : jumlah_spd,
          'sisa_spd' : sisa_spd,
          'tanggal_skup' : tanggal_skup,
          'aksi' : aksi,
          'nama_rekening_bank' : nama_rekening_bank,
          
        },
        dataType: 'html',
        success: function (data) {                   
            message_ok("success",data);
            loadPertama('btn_hapus','1');
        }
    }); 
    }, function() {
        message_ok('error', 'SPP UP batal disimpan.');          
  });   
}

function simpanDataSPP(){
  var jenis = $('#jenis').val();  
  var frm = $('#frmSPP');
  var url = frm.attr('action');  
  var x = document.getElementById("perubahan").value;

  if (jenis!='non angg'){
    var y = document.getElementById("triwulan").value;
    $('#st_triwulan').val(y);
  }  
    
  $('#st_perubahan').val(x);
  
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
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
      }
  }); 
  
}

function deleteSPP_UP(){
    var skpd  = $('#organisasi').val();
    var nospp = $('#no_spp').val();
    var url = $('#deletesppup').val();
    var jenis = $('#jenis').val().toUpperCase();

    if(skpd == 0){
      $.alertable.alert('Organisasi Belum dipilih');
    }else{
      $.alertable.confirm("Anda yakin akan menghapus data SPP-"+jenis+" dengan Nomor : "+nospp+" ?").then(function() {            
          $.ajax({
                  type: "POST",
                  headers: { "X-CSRFToken": csrf_token },
                  url: url,
                  data: {         
                    'nospp':nospp,
                    'org':skpd                      
                  },
                  dataType: 'html',
                  success: function (data) {                   
                      message_ok("success",data);
                      if(jenis=='UP'){
                        clearFormSPP_UP(skpd);
                      }else{
                        clearFormSPP_PPKD(skpd);
                      }                                                                  
                  }
              }); 
          }, function() {
              message_ok('error', 'Anda telah membatalkan menghapus data SPP-'+jenis+'');          
      });
    }
}

function loadSPP_UP(e){
  var skpd = $("#organisasi").val();  

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'spp');
  }
  
}

function LoadBedaharaSPP_UP(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'bendahara');
  }
}

function LoadKegiatanSPP(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'kegiatan');
  }
}

function cekLaporanSPP(e){
  var skpd = $("#organisasi").val();
  var nospp = $("#no_spp").val(); 
  var kunci   = $("#kunci_spd").html();

  console.log(kunci); 

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      if(nospp==''){
        $.alertable.alert('Nomor SPP belum diisi'); 
      }else if($('#bendahara').val()==""){
        $.alertable.alert('Nama Bendahara belum diisi');
      }else if($('#norek_bendahara').val() == ""){
        $.alertable.alert('Nomor Rekening Bank belum diisi');
      } else if($('#nama_bank').val() == ""){
        $.alertable.alert('Nama Bank belum diisi');
      } else if($('#npwp_bendahara').val() == ""){
        $.alertable.alert('NPWP belum diisi');
      } else if($('#status_keperluan').val() == ""){
        $.alertable.alert('Status Keperluan Belum diisi');       
      }else{                
        showModalLaporan('laporan_spp');
      }      
  }
}

function LoadDataSPP(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("persetujuanSPP");
  var ppkd = 0; 

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spp').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("persetujuanSPP");
  } 
}

function LoadDataSPPPPKD(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("persetujuanSPPPPKD"); 
  var ppkd = 1;

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spp_ppkd').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("persetujuanSPPPPKD");
  } 
}

function LoadLPJSPP(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih");
  } else {
      showModal(e,'lpj');
  }
}

function LoadPerusahaan_LSBARJAS(e){
  var skpd = $("#organisasi").val();

  if(skpd == 0){
       $.alertable.alert("Organisasi belum dipilih")
  } else {
      showModal(e,'perusahaan');
  }
}

function simpanDraftSPP(e){  
  var frm = $('#draftSPP');
  var url = frm.attr('action');
  var skpd = $("#organisasi").val();
  var chekDraftSPP = $(".checkbox_draftspp").is(":checked");  

   
  if(chekDraftSPP == false){
    $.alertable.alert("Nomor SPP Belum ada yang dipilih");
        return false;
  }else{
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
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
      }
    }); 
  }
}

function simpanSPP(e){  
  var frm = $('#setujuSPP');
  var url = frm.attr('action');
  var skpd = $("#organisasi").val();
  var chekSPP = $(".checkbox_spp").is(":checked");  

  if(chekSPP == false){
    $.alertable.alert("Nomor SPP Belum ada yang dipilih");
        return false;
  }else{
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
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
      }
    }); 
  }
}

function org_skpd_change(val){ 
  
    if ($('#jenis').val()!='ls')
    {
      ambilAfektasi();  
    }
  
}

function org_skpd_change_spp(val){  
    var jenis = $('#jenis').val();
    var aksi = $('input[name="aksi"]').val();

    
    if(jenis=='tu'){
      if(aksi=='true'){
        ambilSPP();
        getKegiatanSPP_TU();
      }else{
        ambilSPP();
        getKegiatanSPP_TU();
        getBelanjaSPP_TU();  
      }      
    }else{
      ambilSPP();
      ambilAfektasi();  
    }    
}

function ambilKegiatan(){
  var skpd = $("#organisasi").val();
  var kodebidang = $("#kode_bidang").val();
  var kodeprogram = $("#kode_program").val();
  var kodekegiatan = $("#kode_kegiatan").val();
  var kodesubkegiatan = $("#kode_subkegiatan").val();
  var url  = $("#url_kegiatan").val();
  var organisasi = skpd.split('.');
 
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:skpd,
        kodebidang:kodebidang,
        kodeprogram:kodeprogram,
        kodekegiatan:kodekegiatan,
        kodesubkegiatan:kodesubkegiatan
      },
      async: false,
      dataType: "html",
      timeout: 10000,
      dataType: "json",
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){        
        $("#urai_kegiatan").val(data['urai']); 
        $("#nomor_dpa").val(kodebidang+'.'+organisasi[2]+'.'+kodebidang+'.'+kodeprogram+'.'+kodekegiatan+'.'+kodesubkegiatan+'.5');         
      }
    });

}

function ambilAfektasi(){    
  var skpd = $("#organisasi").val();  
  var nospp = $("#no_spp").val();
  var tanggal = $("#tanggal_spp").val();
  var isppkd = $('#isppkd').val();
  var url  = $("#url_afektasi").val();
  var jenis = $("#jenis").val(); 
  var kd_bidang = $("#kode_bidang").val(); 
  var kd_program = $("#kode_program").val();
  var kd_kegiatan = $("#kode_kegiatan").val();
  var kd_subkegiatan = $("#kode_subkegiatan").val();
  

  if(jenis=='ls'){    
    if(skpd!='' && kd_bidang!='' && kd_program!='' && kd_kegiatan!=''&& kd_subkegiatan!=''){
      kd_bidang = $("#kode_bidang").val();
      kd_program = $("#kode_program").val();
      kd_kegiatan = $("#kode_kegiatan").val();  
      kd_subkegiatan = $("#kode_subkegiatan").val();  
    }else{
      kd_bidang = '';
      kd_program = 0;
      kd_kegiatan = 0;
      kd_subkegiatan = 0;
    }      
  } 

  if(skpd==0){
    skpd = '0.0.0.0';
  }else if(skpd==''){
    skpd = '0.0.0.0';
  }  

    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:skpd,
        spp:nospp,
        tgl:tanggal,
        isppkd:isppkd,
        bidang:kd_bidang,
        program:kd_program,
        kegiatan:kd_kegiatan,
        subkegiatan:kd_subkegiatan
      },
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#tabel_spp_afektasi').html(response); 
                
        if(jenis!='non angg'){
          ambilSPD(); 
        }             
        $(".cover").hide();
      }
    });
}

function ambilRincianLPJ(){    
  var skpd = $("#organisasi").val();  
  var nolpj = $("#no_lpj").val();
  var tanggal = $("#tanggal_spp").val();  
  var url  = $("#url_lpjgu").val();
  var jenis = $("#jenis").val();

    if(skpd==0){
      skpd = '0.0.0.0';
    }else if(skpd==''){
      skpd = '0.0.0.0';
    }  

    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:skpd,
        nolpj:nolpj,
        tgl:tanggal
      },
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#tabel_spp_afektasi').html(response); 
        
        ambilSPD();            
        $(".cover").hide();
      }
  });

  getTriwulan('#tanggal_spp','#triwulan');
}

function ambilSPP(){  
  var skpd = $("#organisasi").val();
  var nospp = $("#no_spp").val();
  var url  = $("#url_ambilspp").val(); 
  var jenis  = $("#jenis").val();
  var perubahan = $("#perubahan").val();
  var triwulan = $("#triwulan").val();  

    if(skpd==0){
      skpd = '0.0.0.0';
    }

    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:skpd,
        nospp:nospp        
      },
      async: false,
      dataType: "json",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){         
      
        if(jenis=='gu'||jenis=='gu_nihil'){
          $("#no_lpj").val(data['nospj']);           
        }else if(jenis=='ls'){
          $("#nama_perusahaan").val(data['namaperusahaan']);
          $("#alamat_perusahaan").val(data['alamatperusahaan']);
          $("#pimp_perusahaan").val(data['namapimpinanperusahaan']);
          $("#bank_perusahaan").val(data['namabank']);
          $("#nomor_kontrak").val(data['nokontrak']);
          $("#npwp_perusahaan").val(data['npwp']);
          $("#norek_perusahaan").val(data['norekperusahaan']);
          $("#pelaksanaan").val(data['waktupelaksanaan']);
          $("#tanggal_dpa").val(data['tgldpa']);
          
          if (data['bentuk_perusahaan']==null){
            $("#bentuk_perusahaan").val(0);
          }else{
            $("#bentuk_perusahaan").val(data['bentuk_perusahaan']);
          }

          if (data['jenisdpa']=='DPA-SKPD'){
            $('#jenis_dpa').val('DPA-SKPD');
          }else{
            $('#jenis_dpa').val('DPPA-SKPD');
          }
          if(data['kegiatanlanjutan']=='T'){
            $('#keg_lanjutan1').prop("checked", false);
            $('#keg_lanjutan2').prop("checked", true);
          }else{
            $('#keg_lanjutan1').prop("checked", true);
            $('#keg_lanjutan2').prop("checked", false);
          }
        }                
        // datanya = JSON.parse(data)['list_spp'];                   
        $("#bendahara").val(data['bendaharapengeluaran']);  
        $("#norek_bendahara").val(data['norekeningbendahara']);
        $("#nama_rekening_bank").val(data['nama_rekening_bank']);
        $("#npwp_bendahara").val(data['npwp']);
        $("#nama_bank").val(data['namabank']); 

      
        
        if(data['perubahan']==undefined){
          $("#perubahan").val(perubahan);
        }else{
          $("#perubahan").val(data['perubahan']);   
        }       
        if(data['triwulan']==undefined){
          $("#triwulan").val(triwulan);  
        }else{
          $("#triwulan").val(data['triwulan']);  
        }              
        $("#locked").val(data['locked']);
        $("#no_spp_lama").val(data['nospp']);

        var lock = data['locked'];        
        if(lock == 'Y'){
          $("#kunci_spd").html('(DISETUJUI)');
          $("#kunci_spd").addClass('disetujui');
          $("#no_spp").attr('readonly', true);
          // $('#tanggal_spp').attr('disabled',true);
          $.alertable.alert(data['pesan']);
          loadPertama('btn_simpan','0');
          loadPertama('btn_hapus','0');

          if(jenis=='gu'||jenis=='gu_nihil'){
            $("#no_lpj").attr('readonly',true);
            $("#btn_no_lpj").css('pointer-events','none');
          }
        }else{
          $("#kunci_spd").html('(DRAFT)');
          $("#kunci_spd").removeClass('disetujui');
          $("#no_spp").attr('readonly', false);
          // $('#tanggal_spp').attr('disabled',false);
          loadPertama('btn_simpan','1');
          loadPertama('btn_hapus','1');
          if(jenis=='gu'||jenis=='gu_nihil'){
            $("#no_lpj").attr('readonly',false);
            $("#btn_no_lpj").css('pointer-events','');
          }
        }

        if(nospp==''){
          isSimpan = true;
        }else{
          isSimpan = false;  
        }
        
        $('input[name="aksi"]').val(isSimpan);
        $(".cover").hide();
      }
  });
}

function ambilSPD(){
  var skpd = $("#organisasi").val();  
  var tanggal = $("#tanggal_spp").val();
  var isppkd = $('#isppkd').val();
  var url  = $("#url_ambilspd").val();

  if(skpd==0){
    skpd = '0.0.0.0';
  }else if(skpd==''){
    skpd = '0.0.0.0';
  }  

    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:skpd,        
        tgl:tanggal,
        isppkd:isppkd
      },
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){              
        $('#tabel_spd').html(response);       
        $(".cover").hide();
      }
  });
}

function EditOnFokus(e, target, nomer){ 
  if(document.getElementById('afektasispp_'+nomer).checked == true){ 
      $('#'+target).prop('readonly', false);      
  }else{
      $('#'+target).prop('readonly', true);
  }
  
  document.getElementById(target).value = toAngkaDec(e);
}

function EditOnBlur(e, target, nomer){    
  var rupiah;
  var anggaran_sisa;
  var spp_total;
  var spp_sekarang;
  var jenis = $("#jenis").val();

  if(jenis=='non angg'){
    var anggaran      = toAngkaDec('0,00');
  }else{
    var anggaran      = toAngkaDec($("#anggaran_"+nomer).val());
  }
  
  var spp_lalu      = toAngkaDec($(".lalu"+nomer).html());

  var valCB       = $("#afektasispp_"+nomer).val().split("|");
  var gabung      = valCB[0];
  var gabung2      = valCB[2]+'|'+valCB[3]+'|'+valCB[4]+'|'+valCB[5];  
  
  // jika spp sekarang KOSONG bukan NOL
  if(e == ''){
      spp_sekarang  = parseInt(0);
  } else {
      spp_sekarang  = e;
  } 

  console.log(spp_sekarang);   

  $("#afektasispp_"+nomer).val(gabung+'|'+toRp_WithDecimal(spp_sekarang)+'|'+gabung2);

  // jika spp sekarang tidak sama dengan NOL
  if(spp_sekarang != 0){ 
      rupiah        = toRp_WithDecimal(spp_sekarang); // spp sekarang     
      
      console.log(eval(spp_sekarang));
      spp_total     = eval(spp_lalu) + eval(spp_sekarang); // total spp = spp lalu + spp sekarang
      if(jenis=='non angg'){
        anggaran_sisa = eval(spp_total);
      }else{
        anggaran_sisa = eval(anggaran) - eval(spp_total); // sisa anggaran = anggaran - total spp
      }
      
  } else {
      rupiah        = toRp_WithDecimal(0); 
      spp_total     = spp_lalu;
      if(jenis=='non angg'){
        anggaran_sisa = eval(spp_total);
      }else{
        anggaran_sisa = eval(anggaran) - eval(spp_total);
      }      
  }    

  // spp sekarang
  document.getElementById(target).value = rupiah;
  // total spp
  document.getElementById('span_jml'+nomer).innerHTML = toRp_WithDecimal(spp_total);
  // sisa anggaran
  if(jenis!='non angg'){
    document.getElementById('sisa_'+nomer).innerHTML = toRp_WithDecimal(anggaran_sisa);
  }  
  // total spp sekarang
  getTotalspp_sekarang();
  getJumlah();
}

function getTotalspp_sekarang(){
    var jenis = $("#jenis").val();
    var total = 0;
    var arrDT = document.getElementsByClassName('input_sekarang[]'); // ambil data array berdasarkan class
    var CTRL  = [];   

    if(arrDT.length != 0){
        for (var i = 0; i < arrDT.length; i++) { // UPDATE JUMLAH TOTAL FOOTER KOLOM BULAN
            CTRL.push(toAngkaDec(arrDT[i].value)); }; 
        total  = eval(CTRL.join("+"));
    } else { total = '0.00'; }

    if(jenis=='non angg'){
      idxCol= 7;
    }    


    var format = toAngkaDec(toRp_WithDecimal(total));        
    var column = table.column(idxCol); // idxCol dari index colomn, menyiapkan kolom yg akan diupdate
    $(column.footer()).html(toRp_WithDecimal(total)); // UPDATE jumlah di footer tabel kolom triwulan
    $("#total span").html('Rp. '+ toRp_WithDecimal(total));    
    if(jenis=='tu'){
      $('#totalspp').val(format); 
    }else{
      $('#total_spp').val(format); 
    }     
    $("#total_terbilang span").html(terbilang(format));
   
}

function getJumlah(){ // UPDATE JUMLAH TOTAL FOOTER KOLOM JUMLAH ALOKASI DAN SISA ALOKASI
    var ALTot = 0;  var ALSis = 0;
    var CTOT  = []; var CSIS  = [];
    var arRTO = $('td.row_jml').map(function(){return $(this).text().split('\n')[0];});
    var arSIS = $('td.row_sis').map(function(){return $(this).text().split('\n')[0];});
    
    if(arRTO.length != 0){ // UPDATE JUMLAH TOTAL FOOTER KOLOM JUMLAH ALOKASI
        for (var i = 0; i < arRTO.length; i++) { 
            CTOT.push(toAngkaDec(arRTO[i])); }; ALTot = eval(CTOT.join("+"));
    } else { ALTot = '0.00'; }

    if(arSIS.length != 0){ // UPDATE JUMLAH TOTAL FOOTER KOLOM SISA ALOKASI
        for (var i = 0; i < arSIS.length; i++) { 
            CSIS.push(toAngkaDec(arSIS[i])); }; ALSis = eval(CSIS.join("+"));
    } else { ALSis = '0.00'; }

    $(table.column(8).footer()).html(toRp_WithDecimal(ALTot));
    $(table.column(9).footer()).html(toRp_WithDecimal(ALSis));
}

// function OnBlurSpp_TU(e, target, nomer){
//   var rupiah;
//   var spp_sekarang;
//   var spp_jumlah;
//   var sisa_anggaran;

//   var anggaran    = toAngkaDec($(".anggaran"+nomer).html());
//   var spp_batas   = toAngkaDec($(".batas"+nomer).html());
//   var spp_lalu    = toAngkaDec($(".lalu"+nomer).html());
//   var Rekening    = $(".kode"+nomer).html()+"-"+$(".urai"+nomer).html();  

//   var url     = $("#url_afektasi").val();
//   var totAng  = toAngkaDec($('#datasppbelanja tfoot th:eq(2)').text());  
//   var totLal  = toAngkaDec($('#datasppbelanja tfoot th:eq(4)').text());
//   var totJml  = toAngkaDec($('#datasppbelanja tfoot th:eq(6)').text());
//   var totSis  = toAngkaDec($('#datasppbelanja tfoot th:eq(7)').text());

//   var valCB   = $("#afektasispp_"+nomer).val().split("|");
//   var gabung  = valCB[0]+'|'+valCB[1]+'|'+valCB[2];  

//   // jika spp sekarang KOSONG bukan NOL
//   if(e == ''){ spp_sekarang  = toAngkaDec(0); } else { spp_sekarang  = toAngkaDec(e); }

//   $.ajax({
//     type: "POST",
//     dataType:"json",
//     headers: { "X-CSRFToken": csrf_token },
//     url: url,
//     data: {sekarang:spp_sekarang, batas:spp_batas, lalu:spp_lalu, anggaran:anggaran,
//       totangg:totAng, totlal:totLal, totjml:totJml, totsis:totSis, rekening:Rekening},
//     async: false,
//     success: function(msg){       
//       $("#"+target).val(toRp_WithDecimal(msg['sppsekarang'])); // spp sekarang
//       $("#jmlSpp_"+nomer).html(toRp_WithDecimal(msg['sppjumlah'])); // spp jumlah 
//       $("#in_jml"+nomer).val(msg['sppjumlah']);
//       $("#sisSpp_"+nomer).html(toRp_WithDecimal(msg['sisaanggaran'])); // sisa anggaran 
//       $("#in_sis"+nomer).val(msg['sisaanggaran']);
//       $("#afektasispp_"+nomer).val(gabung+'|'+msg['sppsekarang']);

//       updateJML_SPP_TU();

//       if(msg['pesan'] != ""){ alertify.alert(msg['pesan']); }
//     }
//   });

//   function updateJML_SPP_TU(){
//     var ArrJml  = [];
//     var ArrSis  = [];
//     var url     = $("#url_hitungsisa").val();

//     $("input[name='input_jumrek[]']").each(function() { ArrJml.push($(this).val().replace(',','.')); });
//     $("input[name='input_sisrek[]']").each(function() { ArrSis.push($(this).val().replace(',','.')); });

//     var count    = document.getElementsByName('input_reksek[]');
//     var CTRL     = [];
//     var CEHK     = [];

//     $(".tubelanja:checked").each(function() {
//       CEHK.push($(this).attr("alt"));

//       for (var i = 0; i < CEHK.length; i++) {

//         var id = CEHK[i]-1;

//         if(CTRL.length < 1){          
//           CTRL.push(toAngkaDec(count[id].value));
//         } else {
//           CTRL.push(toAngkaDec(count[id].value));
//         }
//       };

//       if(CTRL.length > 1){ 
//         CTRL.splice(0, CEHK.length); 
//       }

//       CTRL.push(CTRL);
//     });

//     var Arr     = CTRL.pop();

//     $.ajax({
//       type: "POST",
//       dataType:"json",
//       headers: { "X-CSRFToken": csrf_token },
//       url: url,
//       data: {arrjml:ArrJml.toString(), arrsis:ArrSis.toString(), arrsek:Arr.toString()},
//       async: false,
//       success: function(msg){ 
//         $(".tot_jumlah").html(msg['totjumlah']);
//         $(".tot_sisa").html(msg['totsisa']);
//         $(".tot_sppSekarang").html(msg['totsekarang']);
//         $("#tot_sppskrng").val(msg['totsekarang']);
//         $(".terbilang").html(msg['terbilang']);
//       }
//     });
//   }
// }

// js lpj up/gu
function PageLoadLPJ_UPGU(skpd){
  loadDataLPJ_UPGU(skpd);

  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

}

function loadDataLPJ_UPGU(skpd){ 
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#tabel_data_lpj").attr("alt"),    
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(response){  
        $('#tabel_data_lpj').html(response);
        $(".cover").hide();
    }
  });
}

// js lpj tu
function awalLoadPageLPJ_TU(skpd){
  loadDataLPJ_TU(skpd);

  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);
  // tabDis_Enb_TU('1', '0');
}

function loadDataLPJ_TU(skpd){

  $('input[name="skpd"]').val(skpd);

  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#tabel_data_lpjtu").attr("alt"),
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(response){
        $('#tabel_data_lpjtu').html(response);
        $(".cover").hide();
    }
  });
}

// js lpj pengembalian 
function awalFormPengambilan_STS(skpd){

  loadDataSKPD_STS(skpd);
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);
  pilihBankSTS();

  dis_ena_bled("cariLPJ_btn",0);
}

function carilpj_sts(e){

  var skpd = $("#organisasi").val();
  var url  = $(e).attr("alt");

  if(skpd == 0){
       $.alertable.alert("Organisasi belum dipilih")
  } else {
      $('#modalLPJSTS_TU').modal();      
      document.getElementById("ModalLabel_LPJSTS_TU").innerHTML = "Cari Sisa SP2D TU";
      $("#modalLPJSTS_TU .modal-body").load(url+"?skpd="+skpd);
  }
}

function loadDataSKPD_STS(skpd){

  $('input[name="skpd"]').val(skpd);

  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#tabel_sts").attr("alt"),
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {$(".cover").show();},
    success: function(response){
        $('#tabel_sts').html(response);
        $(".cover").hide();
    }
  });
}

// cek PPK pada Laporan SPP ===============================
function pilihSKPDLaporan(e){
  
  // isSKPD_Laporan(e);
  getPenggunaAnggaran(e);
  getBendaharaPengeluaran(e);
  getCekedPPKD();
}

function LoadLaporanSPP(){
  var skpd  = $("#organisasi").val();

  getPenggunaAnggaran(skpd);
  getBendaharaPengeluaran(skpd); 
  getCekedPPKD(); 
}

function getCekedPPKD(){
  var ceked = $("#is_skpkd").is(":checked");

  if(ceked){
      $('input[name="is_skpkd"]').val('1');
  } else {
      $('input[name="is_skpkd"]').val('0');
  }
}

function getPenggunaAnggaran(skpd){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $('#drop_pengguna_anggaran').attr('alt'),
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){ 
      $('#drop_pengguna').html(JSON.parse(response)['isi_pengguna']); 
      getDetailPejabatLaporan('pengguna');     
    }
  });
}

function getBendaharaPengeluaran(skpd){
  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $('#url_drop_bendahara').attr('alt'),
    data: {skpd:skpd}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){ 
      $('#drop_bendahara').html(JSON.parse(response)['isi_bendahara']);     
      getDetailPejabatLaporan('bendahara'); 
    }
  });
}

function getDetailPejabatLaporan(set){  
  var data = $("#drop_"+set).val().split("|");  

  if(data[0] != 'x'){
      $('input[name="'+set+'"]').val(data[0]);
      $("#nama_"+set).val(data[1]);
      $("#nip_"+set).val(data[2]);
      $("#pangkat_"+set).val(data[3]);
  } else {
      $('input[name="'+set+'"]').val('0');
      $("#nama_"+set).val('');
      $("#nip_"+set).val('');
      $("#pangkat_"+set).val('');
  }
}

function cetakLaporanSPP(){

  var frm       = $('#registerSPP');
  var skpd      = $("#organisasi").val();
  var pengguna  = $("#pengguna").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else if(pengguna == 0){
      $.alertable.alert("Pengguna Anggaran belum dipilih.\nSeting Pejabat terlebih dahulu.");
      return false;
  } else {
    $.ajax({
      type: frm.attr('method'),
      url: frm.attr('action'),
      data: frm.serialize(),
      async: false,
      timeout: 10000,
      success: function(res){
          ShowIframeReport(res, "Laporan Register SPP - TA. "+Thn_log);
      }
    });
  }
}

// ============  LPJ UP UP/GU/TU ==================================//
function ModalInputShow(){
  isSimpan = true;
  isTambah = true;
  $('input[name="aksi"]').val(isSimpan);
  $('input[name="isTambah"]').val(isTambah);

  pertamaLoadFormInputLPJ_UPGU();

  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else {
      $('#modalInputLPJUPGU').modal('show');
      $(".modal-dialog").css('width', '90%');
  }
}

function pertamaLoadFormInputLPJ_UPGU(){  
  if(isSimpan){ 
      clearFormLPJ_UPGU();
      dis_ena_bled('save_kegiatan',0);
  } else {
      dis_ena_bled('save_kegiatan',1);
  }

  LoadInputLPJ_UPGU();
}

function kembali_kegiatan(){
  $('.kegiatan').css('display','');
  $('.add_kegiatan').css('display','none');

  LoadInputLPJ_UPGU();
  addkegiatanLPJ_UPGU();
}

function LoadInputLPJ_UPGU(){  
  if(isSimpan){    
    getNewNo_inLPJ_UPGU();
  }else{
    ambilNoSPD();  
  }   
  
  var skpd  = $("#organisasi").val();
  $('input[name="skpd"]').val(skpd);
  
  $.ajax({
    type: "POST",
    url: $("#tabel_kegiatan").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, nospj:$("#no_lpj").val(), aksi:isSimpan}, // var route from main-mod.js
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){      
        enable_disable_btn('1', '0', '0');          
        $('#tabel_kegiatan').html(response);        
    }
  });

  $("#uraian").focus();
}

function getNewNo_inLPJ_UPGU(){ 
  var skpd  = $("#organisasi").val();
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: $('#url_getnewnospj').attr('alt'),
      data: {skpd:skpd},
      async: false,
      success: function(msg){             
        $("#no_lpj").val(msg['nospj']);
      }
  });
}

function clearFormLPJ_UPGU(){
  $("#no_lpj").val('');
  $("#uraian").val('');
  $('#tgl_lpj').val(DateNowInd());

  enable_disable_btn('1', '0', '0');
}

function enable_disable_btn(keg, rek, lpj){

  loadPertama('btn_kegiatan',keg);
  loadPertama('btn_rekening',rek);
  loadPertama('btn_lpjupgu',lpj);

  if(keg == '1'){
      $("#kegiatan").removeClass('hidden');
      $("#rekening").addClass('hidden');
      $("#lpjupgu").addClass('hidden');
  }

  if(rek == '1'){
      $("#kegiatan").addClass('hidden');
      $("#rekening").removeClass('hidden');
      $("#lpjupgu").addClass('hidden');
  }

  if(lpj == '1'){
      $("#kegiatan").addClass('hidden');
      $("#rekening").addClass('hidden');
      $("#lpjupgu").removeClass('hidden');
  }
}

function kegiatanLPJ_UPGU(){
  $('.kegiatan').css('display','none');
  $('.add_kegiatan').css('display','');

  addkegiatanLPJ_UPGU();
}

function addkegiatanLPJ_UPGU(){

  var skpd  = $("#organisasi").val();  

  $.ajax({
    type: "POST",
    url: $("#tabel_add_kegiatan").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, nospj:$("#no_lpj").val(), kondisi:$("#kondisi").val()},
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){
        $('#tabel_add_kegiatan').html(response);
    }
  });
}

function nextRekening_LPJUPGU(){

    var skpd = $("#organisasi").val();
    var nolpj= $("#no_lpj").val();
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
          data: {skpd:skpd, nolpj:nolpj, arr:CEHK[0]},
          async: false,
          dataType: "html",
          timeout: 10000,
          success: function(response){
              enable_disable_btn('0', '1', '0');
              $('#tabel_rekening').html(response);
          }
        });
    }
}

function nextDaftarKegiatan(){

  var cekbox  = $(".daftarkegiatan").is(":checked");
  var skpd    = $("#organisasi").val();

  if($("#uraian").val() == ""){
       $.alertable.alert("Uraian LPJ Belum diisi !");
      return false;
  } else if(!cekbox){
       $.alertable.alert("Belum ada Kegiatan yang dipilih !");
      return false;
  } else {
      var frm  = $('#formModal');
      $.ajax({
          type: frm.attr('method'),
          url: frm.attr('action'),
          headers: { "X-CSRFToken": csrf_token },
          data: frm.serialize(),
          success: function (data) {            
            isSimpan = false;
            $('input[name="aksi"]').val(isSimpan);
            kembali_kegiatan();
            // loadDataLPJ_UPGU(skpd);
          }
      });
  }
}

function ambilNoSPD(){  

  var skpd  = $("#organisasi").val();
  if(isTambah){
    var nolpj = $("#no_lpj").val();
  }else{
    var nolpj = $(".chk_setuju:checked").val();
  }
      

  $.ajax({
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    url: $("#url_cek_nospd").attr("alt"),
    data: {skpd:skpd, nospj:nolpj}, // var route from main-mod.js
    async: false,
    dataType:"json",
    timeout: 10000,
    success: function(data){        
        $("#no_lpj").val(data['nospj']);
        $("#x_nolpj").val(data['nospj']);
        $("#uraian").val(data['keperluan']); 
        $("#tgl_lpj").val(data['tglspj']);
        $("#edNoSP2D").val(data['nosp2d']);

        dis_ena_bled('save_kegiatan',1);
    }
  });
}

function update_kegiatan_lpjupgu(){
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
        kembali_kegiatan();
        // loadDataLPJ_UPGU(skpd);
      }
  });
}

function deleteLPJ_UPGU(url){ 
  var jenis = $("#jenis").val();
  if(jenis=='TU'){
    var frm = $('#lpjTU');
    var pesan = 'LPJ TU';
  }else if(jenis=='GU'){
    var frm = $('#lpjUPGU');
    var pesan = 'LPJ UP/GU';
  }else{
    var frm = $('#pengembalian');
    var pesan = 'STS';
  }  
  var skpd = $("#organisasi").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else if($(".chk_setuju").is(":checked") == false){
      $.alertable.alert("Silahkan pilih data yang akan dihapus !");
      return false;
  } else {
      var CEHK  = [];

      $(".chk_setuju:checked").each(function() {
          CEHK.push($(this).attr("value"));
      });

      $.alertable.confirm('Anda Yakin ingin menghapus data '+pesan+' : '+CEHK).then(function () {          
          $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            url: url,            
            data: frm.serialize(),
            dataType:"html",            
            success: function(msg){  
              if(jenis=='PENGEMBALIAN'){
                loadDataSKPD_STS(skpd);
              }else if(jenis=='TU'){
                loadDataLPJ_TU(skpd);                
              }else{
                loadDataLPJ_UPGU(skpd);
              }  
              message_ok('success', msg);   
            }
          });

      },function() { 
        message_ok('error', 'Hapus data '+pesan+' dibatalkan!');
      });
  }
}

function nextLPJUPGU(){

  var skpd = $("#organisasi").val();
  var nolpj= $("#no_lpj").val();
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
        data: {skpd:skpd, nolpj:nolpj, kegiatan:keg, arr:CEHK[0]},
        async: false,
        dataType: "html",
        timeout: 10000,
        success: function(response){
            enable_disable_btn('0', '0', '1');
            $('#tabel_lpjupgu_rinci').html(response);
        }
      });
  }
}

function backToRekeningLPJ_UPGU(){
  enable_disable_btn('0', '1', '0');
  nextRekening_LPJUPGU();
}

function EditLPJ_UPGU(){

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

      $('#modalInputLPJUPGU').modal('show');
      LoadInputLPJ_UPGU();
  }
}

function simpanLPJ_UPGU_rinci(){
  var url   = $("#save_lpjupgu").attr('alt');
  var frm   = $('#formModal');
  var sisa  = toAngka($('input[name="sisa_anggaran"]').val());
  var skpd  = $("#organisasi").val();
  
  isSimpan = false;
  $('input[name="aksi"]').val(isSimpan);

  if(sisa < 0){
      $.alertable.alert("Data Total LPJ Melebihi Sisa Anggaran");
      return false;
  } else {
      $.alertable.confirm('Anda Yakin ingin menyimpan data rincian LPJ UP/GU ?').then(function () {        
            $.ajax({
              type: frm.attr('method'),
              url: url,
              headers: { "X-CSRFToken": csrf_token },
              data: frm.serialize(),
              success: function (data) {
                message_ok('success',data);
                
                document.getElementById('sisa_anggaran').value = $('input[name="sisa_anggaran"]').val();
                loadDataLPJ_UPGU(skpd);
                nextLPJUPGU();
                isSimpan = false;
                $('input[name="aksi"]').val(isSimpan);
              }
            });
        },function() { 
            message_ok('error', 'Data rincian LPJ UP/GU batal disimpan !');
        });
  }
}

function del_kegiatan_lpjupgu(){

  var url   = $("#del_kegiatan").attr('alt'); 
  var skpd  = $("#organisasi").val();
  var nolpj = $("#no_lpj").val();
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
              kembali_kegiatan(); 
              // loadDataLPJ_UPGU(skpd);             
            }
          });
        },function(){ 
          message_ok('error', 'Hapus data Kegiatan dibatalkan!');        
      });

  }
}

//========= SPP TU ==========================//
function getKegiatanSPP_TU(){
  var url     = $("#url_kegiatan").val();
  var skpd    = $("#organisasi").val();
  var tglSpp  = $("#tanggal_spp").val();
  var noSpp   = $("#no_spp").val();
  var aksi = $('input[name="aksi"]').val();

  $("#tbl_sppkegiatan").removeClass('hidden');
  $("#tbl_sppbelanja").addClass('hidden');

  if(aksi=='true'){
    loadPertama('btn_simpan','1');
    loadPertama('btn_cetak','-1');
    loadPertama('btn_hapus','1');
  }else{
    loadPertama('btn_simpan','-1');
    loadPertama('btn_cetak','-1');
    loadPertama('btn_hapus','-1');
  }
  

  $.ajax({
    type: "POST",
    url: url,
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, tglspp:tglSpp, nospp:noSpp},
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function() {
      $(".cover").show();
    },
    success: function(response){

      $('#tbl_sppkegiatan').html(response);
      loadPertama('btn_kegiatan','-1');
      loadPertama('btn_belanja','1');
      $(".cover").hide();
    }
  });
}

function LOAD_Belanja_TGL(){
  var aksi = $('input[name="aksi"]').val();

  if(aksi == "true"){
      getKegiatanSPP_TU();
  } else {
      getKegiatanSPP_TU();
      getBelanjaSPP_TU();
  }
}

function getBelanjaSPP_TU(){

  var url     = $("#url_belanja").val();
  var chekOto = $(".chk_kdrek").is(":checked");
  var skpd    = $("#organisasi").val();
  var noSpp   = $("#no_spp").val();
  var tglSpp  = $("#tanggal_spp").val();
  var kunci   = $("#kunci_spd").html();
  var kode;

  // panggil validasi data form
  cekDataSPP_TU();

  if(cekSukses){

    var oto = [];
    $(".chk_kdrek:checked").each(function() {
        oto.push($(this).attr("value"));
    });

    var frm = $('#frmSPP');

    if(chekOto == false){
        $.alertable.alert("Belum ada Rekening Kegiatan yang dipilih !!!");
        return false;
    } else {
        $.ajax({
          type: "POST",
          url: url,
          headers: { "X-CSRFToken": csrf_token },
          data: frm.serialize(),
          async: false,
          dataType: "html",
          timeout: 10000,
          beforeSend: function() {
            $(".cover").show();
          },
          success: function(response){

            $("#tbl_sppkegiatan").addClass('hidden');
            $("#tbl_sppbelanja").removeClass('hidden');

            $('#tbl_sppbelanja').html(response);
            
            if(kunci != "(DRAFT)"){
                loadPertama('btn_simpan','-1');
                loadPertama('btn_cetak','1');
                loadPertama('btn_hapus','-1');
            } else {
                loadPertama('btn_simpan','1');
                loadPertama('btn_cetak','1');
                loadPertama('btn_hapus','1');
            }

            loadPertama('btn_kegiatan','1');
            loadPertama('btn_belanja','-1');

            // AMBIL DATA SPD
            // getSPD_SPP_TU();
            $(".cover").hide();
          }
        });
    }
  }
}

function cekDataSPP_TU(){
  // VALIDASI DATA FORM SPP-TU
  var skpd        = $("#organisasi").val();
  var noSpp       = $("#no_spp").val();
  var tglSpp      = $("#tanggal_spp").val();
  var bendahara   = $("#bendahara").val();
  var norek       = $("#norek_bendahara").val();
  var namabank    = $("#nama_bank").val();
  var npwp        = $("#npwp_bendahara").val();
  var keperluan   = $("#status_keperluan").val();

  if(skpd == 0){
      $.alertable.alert("Organisasi Belum dipilih");
      return false;
  } else if(noSpp == ""){
      $.alertable.alert("Nomor SPP belum diisi");
      return false;
  } else if(tglSpp == ""){
      $.alertable.alert("Tanggal SPP belum diisi");
      return false;
  } else if(bendahara == ""){
      $.alertable.alert("Nama Bendahara Belum diisi");
      return false;
  } else if(norek == ""){
      $.alertable.alert("Nomor Rekening Bank Belum diisi");
      return false;
  } else if(namabank == ""){
      $.alertable.alert("Nama Bank Belum diisi");
      return false;
  } else if(npwp == ""){
      $.alertable.alert("NPWP Belum diisi");
      return false;
  } else if(keperluan == ""){
      $.alertable.alert("Status Keperluan Belum diisi");
      return false;
  } else {
      return cekSukses = true;
  }
}

//========= LPJ TU ====================//
function AddInputLPJ_TU(){
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);

  ShowModalInputLPJ_TU();
}

function ShowModalInputLPJ_TU(){
  var judul = "";

  if(isSimpan){ 
    clearFormInputLPJ_TU(); 
    loadPertama("save_lpjtu",0);
    judul = "Input";
  } else { 
    loadPertama("save_lpjtu",1); 
    judul = "Edit";
  }

  if($("#organisasi").val() == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else {
      document.getElementById("judulmodal").innerHTML = judul+" LPJ SP2D TU (LPJ SP2D-TU)";
      $('#modalInputLPJ_TU').modal('show');
      $(".modal-dialog").css('width', '90%');
  }
}

function clearFormInputLPJ_TU(){
  $("#no_lpj").val(''); 
  $("#x_no_lpj").val('');
  $("#no_sp2d").val('');
  $("#x_no_sp2d").val('');
  $('#tgl_lpj').val(DateNowInd());
  $('#uraian').val('');
  $("#uraian").attr("readonly", false);
}

function ambilRincianSP2D_LPJTU(sp2d, kdrek){
  var skpd = $("#organisasi").val();
  var nolpj = $("#x_nolpj").val();  

  if(isSimpan){ getNoLPJ_TU(skpd); }

  $.ajax({
    type: "POST",
    url: $("#tabel_rekening").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, sp2d:sp2d, nolpj:nolpj}, 
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){
        tabDis_Enb_TU('1', '0');
        $('#tabel_rekening').html(response);
    }
  });
}

function getNoLPJ_TU(skpd){
  $.ajax({
    type: "POST",
    url: $('#get_nolpj').attr('alt'),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd},
    success: function(hasil){
        $("#no_lpj").val(hasil['nospj']);
        $("#x_nolpj").val($("#no_lpj").val());
    }
  });
}

function tabDis_Enb_TU(rek, tu){

  loadPertama("btn_rekening",rek);
  loadPertama("btn_spjtu",tu);

  if(rek == '1'){
      $("#rekening_tu").removeClass('hidden');
      $("#rincian_spjtu").addClass('hidden');
  }

  if(tu == '1'){
      $("#rekening_tu").addClass('hidden');
      $("#rincian_spjtu").removeClass('hidden');
  }
}

function EditInputLPJ_TU(e){
  isSimpan = false;
  $('input[name="aksi"]').val(isSimpan);

  var skpd  = $("#organisasi").val();
  var CEHK  = [];

  $(".chk_setuju:checked").each(function(){ CEHK.push($(this).attr("value")); });

  if(CEHK.length < 1) {
      $.alertable.alert("Anda belum memilih nomor LPJ TU yang akan diedit!");
      return false;
  } else if(CEHK.length > 1) {
      $.alertable.alert("Untuk mengedit data LPJ TU harus per nomor LPJ!!");
      return false;
  } else {      
      ShowModalInputLPJ_TU();

      $.ajax({
        type: "POST",
        dataType:"json",
        url: $(e).attr("alt"),
        headers: { "X-CSRFToken": csrf_token },
        data: {skpd:skpd, nospj:CEHK[0]},
        success: function (data) {

            $("#no_lpj").val(data["nospj"]);
            $("#x_nolpj").val(data["nospj"]); 
            $("#tgl_lpj").val(data["tglspj"]); 
            $("#no_sp2d").val(data["nosp2d"]); 
            $("#uraian").val(data["keperluan"]); 

          ambilRincianSP2D_LPJTU(data["nosp2d"],'');
        }
      });
  }
}

function nextRekeningToRinci_TU(){

  var skpd  = $("#organisasi").val();
  var nolpj = $('#no_lpj').val();
  var sp2d  = $('#no_sp2d').val();
  var urai  = $('#uraian').val();
  var keg   = $("#urai_kegiatan").val();

  if(nolpj == ""){
      $.alertable.alert("Nomor LPJ masih kosong !"); return false;
  } else if(sp2d == ""){
      $.alertable.alert("Nomor SP2D masih kosong !"); return false;
  } else if(urai == ""){
      $.alertable.alert("Uraian LPJ masih kosong !"); return false;
  } else {

      var CEHK = [];
      $(".cek_rekening:checked").each(function(){ CEHK.push($(this).attr("value")); });

      if(CEHK.length < 1) {
          $.alertable.alert("Anda belum memilih rekening yang diLPJ kan!");
          return false;
      } else if(CEHK.length > 1) {
          $.alertable.alert("Untuk membuat LPJ harus per rekening!!");
          return false;
      } else {

          $.ajax({
            type: "POST",
            url: $("#tabel_rincilpj_tu").attr("alt"),
            headers: { "X-CSRFToken": csrf_token },
            data: {skpd:skpd, nolpj:nolpj, kegiatan:keg, arr:CEHK[0]},
            async: false,
            dataType: "html",
            timeout: 10000,
            success: function(response){
                tabDis_Enb_TU('0', '1');
                $('#tabel_rincilpj_tu').html(response);
                $('#uraian').attr("readonly", "readonly");
            }
          });
      }
  }
}

function after_save_del_lpjtu(){
  var sp2d  = $('#no_sp2d').val();
  var kdrek = $('#urai_rekening').val();
  var koderekening = kdrek.split('-');
  var rekening = koderekening[0]+'-'+koderekening[1];
  
  ambilRincianSP2D_LPJTU(sp2d, rekening);
}

function Update_LPJ_TU(ini){

  var frm   = $("#formModal");
  var nolpj = $('#no_lpj').val();
  var sp2d  = $('#no_sp2d').val();
  var urai  = $('#uraian').val();
  var skpd  = $("#organisasi").val();

  if(nolpj == ""){
      $.alertable.alert("Nomor LPJ masih kosong !"); return false;
  } else if(sp2d == ""){
      $.alertable.alert("Nomor SP2D masih kosong !"); return false;
  } else if(urai == ""){
      $.alertable.alert("Uraian LPJ masih kosong !"); return false;
  } else {    
      $.alertable.confirm('Anda Yakin ingin menyimpan data rincian LPJ TU ?').then(function () {        
            $.ajax({
              type: frm.attr('method'),
              url: $(ini).attr("alt"),
              headers: { "X-CSRFToken": csrf_token },
              data: frm.serialize(),
              success: function (data) {
                // alert(data);
                message_ok('success', data);   
                // $.alertable.alert("Data telah berhasil disimpan");                
                loadDataLPJ_TU(skpd);
                isSimpan = false;
                $('input[name="aksi"]').val(isSimpan);
              }
            });
        },function() { 
          message_ok('error', 'Data rincian LPJ TU batal disimpan !');         
      });
  }
}

//==================== Pengembalian STS ==============================//
function AddLPJ_STS(){
  isSimpan = true;
  $('input[name="aksi"]').val(isSimpan);
  
  ShowModalInput_STS();
  getTabelRinci_STS('');
}

function getTabel_STS(CEHK){ 

  var skpd = $("#organisasi").val();
  var jnis = $('input[name="myRadios"]:checked').val();
  var nosts= $("#no_sts").val();
  var sp2d = $("#no_sp2d").val();
  var kdrek= $("#kode_rekening").val();
  var act  = $('input[name="aksi"]').val(); 

  if(jnis != null){ jnis = jnis; } else { jnis = "xx";}
  
  $.ajax({
    type: "POST",
    url: $("#tabel_rincian_sts").attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, jenis:jnis, nosts:nosts, sp2d:sp2d, kdrek:kdrek, arr:CEHK.toString(), action:act},
    async: false,
    dataType: "html",
    timeout: 10000,
    success: function(response){
        $('#tabel_rincian_sts').html(response);
    }
  });
}

function getTabelSTS_LS(){
    var skpd = $("#organisasi").val();
    var nosts= $("#no_sts").val();

    $.ajax({
      type: "POST",
      url: $("#tabel_rincian_sts_ls").attr("alt"),
      headers: { "X-CSRFToken": csrf_token },
      data: {skpd:skpd,nosts:nosts},
      async: false,
      dataType: "html",
      timeout: 10000,
      success: function(response){
          $('#tabel_rincian_sts_ls').html(response);
      }
    });
}

function back_sts_ls(){
  $("#tabel_rincian_sts").addClass("hidden"); 
  $("#tabel_rincian_sts_ls").removeClass("hidden");
  dis_ena_bled("back_sts",0); 
  dis_ena_bled("next_sts",1);
}

function pilihBankSTS(){
  var kode  = $("#rek_bank").val();  
  var nama  = kode.split('|')[4];
  var rekn  = kode.split('|')[3];

  $('input[name="nama_bank"]').val(nama);
  $('input[name="no_rekening"]').val(rekn);
}

function getTabelRinci_STS(rinci){
  var jnis = $('input[name="myRadios"]:checked').val();

  if(jnis != null){ jnis = jnis; } else { jnis = "xx";}

  if(jnis == 'LS'){
      $("#tabel_rincian_sts").addClass("hidden"); 
      $("#tabel_rincian_sts_ls").removeClass("hidden");
      dis_ena_bled("back_sts",0); 
      dis_ena_bled("next_sts",1);

      getTabel_STS('');
      getTabelSTS_LS();

  } else {
      $("#tabel_rincian_sts").removeClass("hidden"); 
      $("#tabel_rincian_sts_ls").addClass("hidden");

      getTabel_STS('');
  }
}

function changerbtn_jns(e){

  var jenis = $(e).val();
  var skpd  = $("#organisasi").val();

  if(jenis == "TU"){ 
    dis_ena_bled("cariLPJ_btn",1); 
  } else { 
    dis_ena_bled("cariLPJ_btn",0); 
    $("#no_lpj").val('');
  }

  OnOffBtnBackNext_STS(jenis);

  // HAPUS NOSP2D
  $("#no_sp2d").val('');
  // UBAH HIDDEN CLASS
  back_sts_ls();

  if(isSimpan){
    // UPDATE NOMOR STS TAMBAH JENIS LPJ GJ,LS,UP,TU
    getNoLPJ_STS(skpd);
  }
  // AMBIL TABEL RINCIAN STS
  getTabelRinci_STS('');
}

function clearFormInput_STS(){
  $("#no_sts").val('');
  $("#x_no_sts").val('');
  $('#tgl_sts').val(DateNowInd());
  $("#no_lpj").val('');
  $("#no_sp2d").val('');
  $('#uraian').val('');
  $("input[name='myRadios']").attr("checked", false);
  document.getElementById("rek_bank").selectedIndex = "0";
  dis_ena_bled("cariLPJ_btn",0);
  $("#back_sts").addClass("hidden");
  $("#next_sts").addClass("hidden");
  dis_ena_bled("back_sts",0);

  back_sts_ls();
  pilihBankSTS();
  getTabelRinci_STS('');
}

function updateKodeNoSTS(){
  var jenis = $('input[name="myRadios"]:checked').val();
  var nosts = $("#no_sts").val();
  var pecah = nosts.split("/");
  var kode  = pecah[1].split("-");

  if(jenis != null){ jenis = jenis; } else { jenis = "XX";}

  var hasil = pecah[0]+"/"+kode[0]+"-"+jenis+"/"+pecah[2]+"/"+pecah[3];
  $("#no_sts").val(hasil);
  $("#x_no_sts").val($("#no_sts").val());
}

function getNoLPJ_STS(skpd){

  var jnis = $('input[name="myRadios"]:checked').val();
  if(jnis != null){ jnis = jnis; } else { jnis = "XX";}

  $.ajax({
    type: "POST",
    url: $('#get_no').attr("alt"),
    headers: { "X-CSRFToken": csrf_token },
    data: {skpd:skpd, jenis:jnis},
    dataType:"json",
    success: function(hasil){        
        $("#no_sts").val(hasil['nospj']);
        $("#x_no_sts").val($("#no_sts").val());
        updateKodeNoSTS();
    }
  });
}

function next_sts_ls(){

  var CEHK  = [];

  $(".chk_pilih:checked").each(function(){ CEHK.push($(this).attr("value")); });

  if(CEHK.length < 1) {
      $.alertable.alert("Anda belum memilih kegiatan !");
      return false;
  } else {
    
      $("#tabel_rincian_sts").removeClass("hidden"); 
      $("#tabel_rincian_sts_ls").addClass("hidden");

      getTabel_STS(CEHK);

      dis_ena_bled("back_sts",1); 
      dis_ena_bled("next_sts",0);
  }
}

function Click_sts(cb){
  var CEHK  = [];
  $(".chk_pilih:checked").each(function(){ CEHK.push($(this).attr("value")); });
  getTabel_STS(CEHK);
}

function ShowModalInput_STS(){
  var judul = "";
  var skpd  = $("#organisasi").val();

  if(isSimpan){ 
    clearFormInput_STS(); 
    getNoLPJ_STS(skpd);

    judul = "Input";
  } else {  
    judul = "Edit";
  }

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else {
      document.getElementById("judulmodal").innerHTML = judul+" Pengembalian";
      $('#modalInput_STS').modal('show');
      $(".modal-dialog").css('width', '90%');
  }
}

function editLPJ_STS(ini){

  var skpd  = $("#organisasi").val();
  var CEHK  = [];
  isSimpan  = false;

  $('input[name="aksi"]').val(isSimpan);
  $(".chk_setuju:checked").each(function(){ CEHK.push($(this).attr("value")); });

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih !");
      return false;
  } else if(CEHK.length < 1) {
      $.alertable.alert("Anda belum memilih nomor STS yang akan diedit!");
      return false;
  } else if(CEHK.length > 1) {
      $.alertable.alert("Untuk mengedit data harus per nomor STS !");
      return false;
  } else {
      
      ShowModalInput_STS();

      $.ajax({
        type: "POST",
        dataType:"json",
        headers: { "X-CSRFToken": csrf_token },
        url: $(ini).attr("alt"),
        data: {skpd:skpd, nosts:CEHK[0]},
        success: function (data) {

            $("#no_sts").val(data["nosts"]);
            $("#x_no_sts").val(data["nosts"]);
            $('#tgl_sts').val(data["tglsts"]);
            $("#no_lpj").val(data["nolpj"]);
            $("#no_sp2d").val(data["nosp2d"]);
            $('#uraian').val(data["uraian"]);
            $("input[name='myRadios'][value='"+data["jenis"]+"']").prop("checked", true);
            $("#rek_bank option:contains("+data["rekening"]+")").attr('selected', 'selected');

            OnOffBtnBackNext_STS(data["jenis"]);
            getTabelRinci_STS('');

        }
      });
  }
}

function OnOffBtnBackNext_STS(jenis){
  if(jenis == "LS"){
      $("#back_sts").removeClass("hidden");
      $("#next_sts").removeClass("hidden");
  } else {
      $("#back_sts").addClass("hidden");
      $("#next_sts").addClass("hidden");
  }
}

function simpan_lpj_sts(ini){
  var frm   = $("#formModal");
  var nosts = $("#no_sts").val();
  var jenis = $('input[name="myRadios"]:checked').val();
  var nolpj = $("#no_lpj").val();
  var urai  = $('#uraian').val();
  var skpd  = $("#organisasi").val();

  if(nosts == ""){
      $.alertable.alert("No. STS Pengembalian belum diisi !");
      return false;
  } else if(jenis == null){
      $.alertable.alert("Jenis Pengembalian belum dipilih !");
      return false;
  } else if(jenis == "TU" && nolpj == ""){
      $.alertable.alert("No. LPJ Pengembalian belum diisi !");
      return false;
  } else if(urai == ""){
      $.alertable.alert("Uraian Pengembalian belum diisi !");
      return false;
  } else {
      $.alertable.confirm('Anda Yakin ingin menyimpan data rincian Pengembalian?').then(function() {
            $.ajax({
              type: frm.attr('method'),
              url: $(ini).attr("alt"),
              headers: { "X-CSRFToken": csrf_token },
              data: frm.serialize(),
              success: function (data) {
                // $.alertable.alert("Data telah berhasil disimpan");
                message_ok('success', data); 
                
                loadDataSKPD_STS(skpd);
                isSimpan = false;
                $('input[name="aksi"]').val(isSimpan);
              }
            });
        },function(){ 
            message_ok('error', 'Data rincian Pengembalian batal disimpan !');         
      });
  }
}

function handleClick(cb,target1){
  if(cb.checked == true){
      $(target1).prop('readonly', false);
      $(target1).focus();
  } else {
      $(target1).prop('readonly', true);
  }
}

function newAddInputLPJ_TU(){
  AddInputLPJ_TU();
  ambilRincianSP2D_LPJTU('', '');
}

function LoadNoSP2D(e){
  var skpd = $("#organisasi").val();
  var url  = $(e).attr("alt");

  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      $('#modalReportLPJTU').modal();
      document.getElementById("ReportModalLabel_TU").innerHTML = "Cari SP2D";
      $("#modalReportLPJTU .modal-body").load(url+"?skpd="+skpd);      
  }
}

function simpanLPJ_TU_rinci(){
  var url   = $("#save_kegiatan").attr("alt");
  var frm   = $("#formModal");
  var sisa  = toAngka($('input[name="sisa_anggaran"]').val());
  var skpd  = $("#organisasi").val();


  if(sisa < 0){
      $.alertable.alert("Data Total LPJ Melebihi Sisa Anggaran");
      return false;
  } else {      
      $.alertable.confirm('Anda Yakin ingin menyimpan data rincian LPJ TU ?').then(function () {
        $.ajax({
              type: frm.attr('method'),
              url: url,
              headers: { "X-CSRFToken": csrf_token },
              data: frm.serialize(),
              success: function (data) {
                // alert(data);
                message_ok('success',data);
                
                loadDataLPJ_TU(skpd);
                isSimpan = false;
                $('input[name="aksi"]').val(isSimpan);
              }
            });
        },function(){ 
            message_ok('error', 'Data rincian LPJ TU batal disimpan !');
        });
  }
}

function ModalLaporanLPJShow(nomer){
  var url       = $('#modalReportLPJUPGU').attr("alt");
  var no_bukti  = $("#no_bukti_"+nomer).val();
  var tgl_bukti = $("#tgl_bukti_"+nomer).val();
  var urai_kw   = $("#urai_kw_"+nomer).val();
  var skpd      = $("#organisasi").val();
  var nolpj     = $("#no_lpj").val();

  var postig    = Base64.encode(no_bukti+"|"+tgl_bukti+"|"+urai_kw+"|"+skpd+"|"+nolpj);  

  $('#modalReportLPJUPGU').modal();
  $("#modalReportLPJUPGU .modal-body").load(url+"?base="+postig);
}




