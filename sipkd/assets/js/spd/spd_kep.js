var isSimpan = true;
var perubahan_no_spd = false;
var skpd
var no_spd;
var berubah = true;

$(document).ready(function () {

  $('#tanggal_spd').daterangepicker({
      singleDatePicker: true,
      calender_style: "picker_4",
    }, function (start, end, label){
  });

  $('#btn_cetak').attr('alt', link_render_cetak_spd);

  // tambahan autonospd
  // autonospd_kep();

  get_clearformSPDKep();
});

function get_clearformSPDKep(){
  isSimpan = true;
  berubah = true;
  perubahan_no_spd = false;

  $('#no_spd').val(''); 
  $('#pk_nospd').val('');
  $('#no_spdold').val('');
  $('#isSimpan').val(isSimpan);
  $('#kunci_spd').text('(DRAFT)');
  $('#tanggal_spd').val($('#tanggal_spd').attr('alt'));
  $('#kd_org').val('');
  $('#kd_org2').val('');
  $('#kd_org2_urai').val('');
  $('#skpd_spd').val('');
  $('#bendahara_kep').val(0);
  $('#nip_bendahara').val('');
  $('#jnsdpa').val(0);
  $('#ketentuan').text('');
  $('#bulan').val(1);
  $('#jumlah_spd').text('Rp. 0,00');
  $('#terbilang').text('Nol Rupiah');
  $('#jum_tot_spd').val('0,00');

  generate_table_rinci_x();

}

/*----------------------------------------------------------------------------------------------------*/
$('#btn_lihat_spd').click(function(){
  render_modal('Load SPD','spd',['']);
  berubah = false;
});

$('#btn_tambah_spd').click(function(){
  location.reload(true);
});

$('#btn_simpan').click(function(){
  simpan_spd(function() {});
});

$('#btn_cetak').click(function(){
  skpd = $('#kd_org2').val();
  no_spd = $('#no_spd').val();
  var ini = $('#btn_cetak')['0'];
  if (perubahan_no_spd == true) {
    $.alertable.confirm('Apakah anda ingin menyimpan data terlebih dahulu ?').then(function() {
      //simpan_spd(function() {showModal(ini, 'cetak_spd');});
      showModal(ini, 'cetak_spd');
    }, function() {
        message_ok('error', 'Cetak Dibatalkan');
    });
  }else{
    //simpan_spd(function() {showModal(ini, 'cetak_spd');});     
    showModal(ini, 'cetak_spd');   
  }
});

$('#no_spd').change(function(){
  $(this).val($(this).val().replace(/\s/g, ''))
  perubahan_no_spd = true;
});

$('#btn_hapus').click(function(){
  hapus_spd();
});

$('#kd_org2').change(function(){
  isSimpan = true;
  if (var_skpkd=='0') {
    $('#jnsdpa').html('');
    $('#jnsdpa').append('<option value="DPA-SKPD">DPA-SKPD</option>');
    $('#jnsdpa').append('<option value="DPPA-SKPD">DPPA-SKPD</option>');
  }else{
    $('#jnsdpa').html('');
    $('#jnsdpa').append('<option value="DPA-SKPD">DPA-SKPD</option>');
    $('#jnsdpa').append('<option value="DPPA-SKPD">DPPA-SKPD</option>');
    $('#jnsdpa').append('<option value="DPA-PPKD">DPA-PPKD</option>');
    $('#jnsdpa').append('<option value="DPPA-PPKD">DPPA-PPKD</option>');
  }
  if ($('#jnsdpa').val()!='') {
    ambil_bendahara(); 
  } 

  // if (berubah==false){ get_clearformSPDKep(); }
  // else { generate_table_rinci_x(); }

});

$('#bulan').change(function(){
  // generate_table_rinci();
});

$('#jnsdpa').change(function(){
  // generate_table_rinci();
});

$('#bendahara_kep').change(function(){
  if ($(this).val()!=null) {
    $('#nip_bendahara').val($('#'+$(this).val().replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-')+'').attr('nip'));
  }
});

function ambil_bendahara(){
  kode = $('#kd_org2').val();
  isi_optn = '';
  id_selek = '';

  if (kode!='') {
    $.ajax({
        type: "POST",
          headers: { "X-CSRFToken": csrf_token },
          url: link_ambil_bendahara,
          data: {kode_organisasi:kode},
          async: false,
          success: function(data){ 
            for (var i = 0; i < JSON.parse(data).length; i++) {
              id_selek = 0;
              isi_optn += '<option urut="'+i+'" nip = "'+JSON.parse(data)[i]['nip']+'" id = "'+JSON.parse(data)[i]['nama'].replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-')+'" value="'+JSON.parse(data)[i]['nama']+'">'+JSON.parse(data)[i]['nama']+'</option>';
            }

            $('#bendahara_kep').html('');
            $('#bendahara_kep').append(isi_optn);
          },
          complete: function(xhr,status){
            $('#bendahara_kep').change();
          }
    });
  }
}

function fungsi_modal(ini, asal_modal){ 
    var var_nospd, var_skpd;
    var row     = $(ini).closest('tr'); 
    var tglnya  = '';

    var $nospd  = row.find('td:nth-child(1)');
    var $tgl = row.find('td:nth-child(2)');
    var $skpd = row.find('td:nth-child(3)');

    $.each($nospd, function(){ var_nospd  = $(this).text();}); 
    $.each($tgl, function(){ tglnya  = $(this).text();}); 
    $.each($skpd, function(){ var_skpd  = $(this).text();}); 

    var var_skpd2 = var_skpd.split(' - ')[0].split('.');
    var var_urai2 = var_skpd.split(' - ')[1];
    
    $.get(is_skpkd_js(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]+'.'+var_skpd2[3])).done(
      function(){ 
        $('#kd_org2').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]+'.'+var_skpd2[3]);
        $('#kd_org2_urai').val(var_urai2);
        $('#kd_org').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]+'.'+var_skpd2[3]+' - '+var_urai2);
        $('#kd_org2').trigger('change');
        $('#no_spd').val(var_nospd); 
        $('#no_spdold').val(var_nospd); 
        $('#tanggal_spd').val(tglnya);

        rinci_spd(var_skpd2[0],var_skpd2[1],var_skpd2[2],var_skpd2[3],var_nospd);
      }
    );  
}

function rinci_spd(kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd){
  isSimpan = false;
  berubah = true;
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_rinci_spd,
      data: {'kdurusan':kdurusan,
          'kdsuburusan':kdsuburusan,
          'kdorganisasi':kdorganisasi,
          'kdunit':kdunit,
          'nospd':nospd,  
        },
      dataType: 'html',
      beforeSend: function(){ $(".cover").show(); },
      success: function(data){
        var rinci = JSON.parse(data)['hasil'][0];
        $('#jnsdpa').val(rinci.jenisdpa);
        $('#bulan').val(rinci.bulan_awal);

        $('#bendahara_kep').val(rinci.bendaharapengeluaran);
        $('#bendahara_kep').change();
      
        // TambahFitur: Input Ketentuan Lain Lain
        if(rinci.uraian == null || rinci.uraian == '0,00'){
          $('#ketentuan').val('');
        }else{
          $('#ketentuan').val(rinci.uraian);
        }
        // TambahFitur: Input Ketentuan Lain Lain

        if (rinci.locked=='Y') {
          $('#btn_hapus').attr('disabled','disabled');
        }else{
          $('#btn_hapus').removeAttr('disabled');
        }

        $('#jumlah_spd').text('Rp. '+rinci.jumlahspd.toString());
        $('#jum_tot_spd').val(rinci.jumlahspd.toString());
        terbilangya = terbilang(toAngkaDec(rinci.jumlahspd.toString()));
        $('#terbilang').text(' '+terbilang(toAngkaDec(rinci.jumlahspd.toString())));
        
        $(".cover").hide();
        generate_table_rinci_x();
      },error:function(){
        message_ok("error","Ambil rincian SPD Gagal! ");
      }
  });
}

function generate_table_rinci_x(){
  $.ajax({
    headers: { "X-CSRFToken": csrf_token },
    type: "POST",
    url: link_tabel_rinci_spd,
    data: {'kdurusan':$('#kd_org2').val().split('.')[0],
      'kdsuburusan':$('#kd_org2').val().split('.')[1],
      'kdorganisasi':$('#kd_org2').val().split('.')[2],
      'kdunit':$('#kd_org2').val().split('.')[3],
      'nospd':$('#no_spd').val(),
    },
    async: false,
    dataType: "html",
    timeout: 10000,
    beforeSend: function(){ $(".cover").show(); },
    success: function(response){
      $('#view_tabel_spd_rincian').html(response);
      $(".cover").hide();
    }
  });
}

function generate_table_rinci(){
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_tabel_rinci_spd,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
          'kdsuburusan':$('#kd_org2').val().split('.')[1],
          'kdorganisasi':$('#kd_org2').val().split('.')[2],
          'kdunit':$('#kd_org2').val().split('.')[3],
          'nospd':$('#no_spd').val(), 
          'bulan':$('#bulan').val(),
          'jenisdpa':$('#jnsdpa').val(),
        },
      dataType: 'html',
      success: function(data){
        $('#table_spd').DataTable( {
          destroy:true,
          "bLengthChange": false, 
          scrollY:        "190px",
          scrollX:        true,
          //scrollCollapse: true,
          fixedHeader: true,
          paging:         false,
          "bInfo": false,
          data: JSON.parse(data)['data_rincian'],
          'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            for (var i = 2; i <= 6; i++) {
              $('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
            }
          },
          "footerCallback": function ( row, data, start, end, display ) {
              var api = this.api(), data;
   
              // Remove the formatting to get integer data for summation
              var intVal = function ( i ) {
                  return isNaN(typeof i === 'string' ?
                  i.replace(/[\$,]/g, '')*1 :
                  typeof i === 'number' ?
                      i : 0)==true?0:typeof i === 'string' ?
                      i.replace(/[\$,]/g, '')*1 :
                      typeof i === 'number' ?
                          i : 0;
              };
   
              // Total over all pages
              total4 = api
                  .column( 4 )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
        for (var i = 2; i <= 6; i++) {
          total = api
                  .column( i )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
          $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
         }

         $('#jumlah_spd').text('Rp. '+toRp_WithDesimal(total4.toString()));
         $('#jum_tot_spd').val(total4.toString());
         terbilangya = terbilang(toAngkaDec(toRp_WithDesimal(total4.toString())));
         $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(total4.toString()))));

         }
      });
        
      }
  });
}

function simpan_spd(callback){
  var frm_spd = $("#form_spd");
  $('#isSimpan').val(isSimpan);
  $('#skpd_spd').val($('#kd_org2').val());
  $('#btn_simpan').attr('disabled', 'disabled');
  // tambahan validasi anggaran minus
  let melebihi = 0;
  $('#table_spd_rincian tr').each(function(i, obj) {
    if ($(this).find('td:eq(7) span').text() != '') {
      var anggaran_sisa = toAngka($(this).find('td:eq(7) span').text())
      if (anggaran_sisa < 0) {
        melebihi +=1;
      }
    }
  });
  // tambahan validasi anggaran minus

  if ($('#no_spd').val()=='') {
    $.alertable.alert('Nomor SPD masih kosong !');
    $('#btn_simpan').removeAttr('disabled');
  }else if($('#kd_org2').val()==''){
    $.alertable.alert('Kode organisasi masih kosong !');
    $('#btn_simpan').removeAttr('disabled');
  }else if($('#jnsdpa').val()==''){
    $.alertable.alert('Jenis DPA masih kosong !');
    $('#btn_simpan').removeAttr('disabled');
  }else if($('#bendahara_kep').val()=='' || $('#bendahara_kep').val()===null){
    $.alertable.alert('Bendahara masih kosong !');
    $('#btn_simpan').removeAttr('disabled');
  }else if(melebihi > 0){
    $.alertable.alert('Terdapat '+melebihi+' nilai SPD yang melebihi anggaran (SISA ANGGARAN MINUS) ! Perbaiki dan pastikan Tidak ada yang minus!');
    $('#btn_simpan').removeAttr('disabled');
  }else{
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_simpan_spd,
      data: frm_spd.serialize(),
      
      dataType: 'html',
      success: function(data){
        // tambahan autonospd
        if(data == 'Nomor SPD sudah ada !'){
          message_ok("error",data);
          $.alertable.alert('NOMOR SPD SUDAH DIGUNAKAN! KLIK OK UNTUK MEMPERBARUI NOMOR SPD dan ULANGI SIMPAN KEMBALI!').always(function() {
            // location.reload(true);
            // autonospd_kep();
            message_ok("success",'Nomor SPD Sudah Diperbarui, Silakan Di Simpan Kembali');
            perubahan_no_spd = false;
            callback();
            $('#btn_simpan').removeAttr('disabled');
          });
        }else{
          $.alertable.alert('SPD BERHASIL disimpan  untuk '+ $('#kd_org').val() +' dengan nomor '+ $('#no_spd').val() +'.').always(function() {
            message_ok("success",data);
            perubahan_no_spd = false;
            callback();
            location.reload(true);
          });
        }
        // end tambahan autonospd

        // original
        // message_ok("success",data);
        // perubahan_no_spd = false;
        // callback();
      },
      error: function(){
        message_ok("error","Proses Gagal! ");
      }
    });
  }
}

function hapus_spd(){

  if ($('#kd_org2').val()=='') {
      $.alertable.alert('Kode organisasi belum dipilih!');
  } else if($('#no_spd').val()==''){
      $.alertable.alert('Nomor SPD masih kosong!');
  } else if($('#table_spd_rincian').DataTable().rows().count() <= 1){
      $.alertable.alert('Data Rekening masih kosong');
  } else {
      $.alertable.confirm('Apakah anda yakin ingin menghapus data SPD '+$('#no_spd').val()+' ?').then(function() {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            url: link_hapus_spd,
            data: {'kdurusan':$('#kd_org2').val().split('.')[0],
                'kdsuburusan':$('#kd_org2').val().split('.')[1],
                'kdorganisasi':$('#kd_org2').val().split('.')[2],
                'kdunit':$('#kd_org2').val().split('.')[3],
                'nospd':$('#no_spd').val(),
              },
            dataType: 'html',
            success: function(data){
              message_ok("success",data);
              location.reload(true);
            },
            error: function(){
              message_ok("error","Proses Gagal! ");
            }
        });
      }, function() {
        message_ok('error', 'Hapus data dibatalkan.');
      });
  }

};

// tambahan autonospd
function autonospd_kep(){
  $.ajax({
    type: "GET",
    headers: { "X-CSRFToken": csrf_token },
    url: '/sipkd/spd/spd_kep/autonospd_kep',
    data: {},
    dataType: 'html',
    success: function(data){
      data = JSON.parse(data)
      $("#no_spd").val(data.nospd);
    },error:function(){
      console.log('isi sendiri ya nomor spdnya')
    }
  });
}