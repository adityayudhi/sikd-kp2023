var isSimpan = true;
var array_spm_sekakarang = [];
var array_rekening = [];
$(document).ready(function () {
   $('#datapfk').DataTable( {
            scrollY: 60,
            paging: false,
            scrollX: true,
            fixedHeader: true,
            "bLengthChange": false,
            "bInfo": false,
            "searching": false,
    });
   $('#dataspd').DataTable( {
        scrollY: 90,
        paging: false,
        scrollX: true,
        fixedHeader: true,
        "bLengthChange": false,
        "bInfo": false
    });
   $('#dataspm').DataTable( {
        scrollY: 45,
        paging: false,
        scrollX: true,
        fixedHeader: true,
        "bLengthChange": false,
        "bInfo": false,
        "searching": false,
    });
   $('#table_spm').DataTable( {
        scrollY: 120,
        paging: false,
        scrollX: true,
        fixedHeader: true,
        "bLengthChange": false,
        "bInfo": false,
        "searching": false,
    });
   $('#table_dasar_spd').DataTable( {
        scrollY: 90,
        paging: false,
        scrollX: true,
        fixedHeader: true,
        "bLengthChange": false,
        "bInfo": false,
        "searching": false,
    });
    $('#tgl_spm').daterangepicker({
            singleDatePicker: true,
            calender_style: "picker_4",
        }, function (start, end, label) {

        })
    $('#tgl_spp').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    }, function (start, end, label) {

    });
});
/*----------------------------------------------------------------------------------------------------*/
$('#btn_lihat_spm').click(function(){
  var organisasi = $("#kd_org2").val();
    if(organisasi != 0){
      render_modal('Load SPM','SPM',[$('#kd_org2').val(), $('#jen').val()]);
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }

});

$('#btn_lihat_spm_ls').click(function(){
  var organisasi = $("#kd_org2").val();
    if(organisasi != 0){
      render_modal('Lihat LS','SPM_LS',[$('#kd_org2').val(), $('#jen').val()]);
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }

});

$('#btn_spp_spm').click(function(){
  var organisasi = $("#kd_org2").val();
  var spm_jenis = $("#jen").val();
    if(organisasi != 0){
      if(spm_jenis == 'LS'){
       render_modal('Load SPP LS','SPP_LS',[$('#kd_org2').val(), $('#jen').val()]); 
     }else{
        render_modal('Load SPP','SPP',[$('#kd_org2').val(), $('#jen').val()]); 
     }
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }
});

$('#btn_bendahara').click(function(){
  var organisasi = $("#kd_org2").val();
    if(organisasi != 0){
      render_modal('List Bendahara','bendahara',[$('#kd_org2').val(),]);
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }
});

$('#btn_rekening').click(function(){
  var organisasi = $("#kd_org2").val();
    if(organisasi != 0){
      render_modal('List Rekening','rekening',[$('#kd_org2').val(),]);
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }
});

$('#btn_tambah_spm').click(function(){
	location.reload(true);
});

$('#btn_simpan').click(function(){
	simpan_spm();
});

function cekLaporanSPM(){
  var skpd = $("#kd_org2").val();
  var nospm_report = $("#no_spm").val();
  if(skpd == 0){
      $.alertable.alert("Organisasi belum dipilih")
  } else {
      if(nospm_report==''){
        $.alertable.alert('Nomor SPM belum diisi'); 
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
        showModalLaporanSPM('laporan_spm');
      }      
  }
}

$('#btn_hapus').click(function(){
	hapus_spm();
});

function showModalLaporanSPM(modal){ 
  var url_load  = "";
  var loadModal = "";
  var linkLoad  = link_laporan_spm;
  var act       = getUrlVars(linkLoad)["act"];

  switch(modal) {
    case 'laporan_spm':
        var skpd  = $('#kd_org2').val();
        var jenis = $('#jen').val();
        if (jenis == 'NON_ANGG'){
          loadModal = "Cetak Surat Permintaan Pembayaran Non Anggaran TA. "+Thn_log;
        } else {
          loadModal = "Cetak Surat Permintaan Pembayaran "+jenis+" TA. "+Thn_log;
        }       
        url_load  = linkLoad+"?skpd="+skpd;;
        break;
  } 

  document.getElementById("myModalLabel").innerHTML = loadModal;
  $("#showModal").modal();
  $(".modal-body-showmodal").load(url_load);
  $(".modal-dialog").css('width', '800px');
}

function fungsi_modal(ini, asal){
	$('#showModal').modal('hide');
	var var_nospm, var_nospp, var_skpd, var_tgl_spm, var_tgl_spp, var_status_keperluan, var_nama_bendahara, var_rekening, var_nama_bank, var_no_npwp, var_up, var_kdbid, var_kdprog, var_kdkeg;
    var row     = $(ini).closest('tr'); 

    
    if (asal == 'SPM'){
      $nospm  = row.find('td:nth-child(1)');
      $tgl_spm  = row.find('td:nth-child(2)');
      $skpd = row.find('td:nth-child(3)');
      $status_keperluan = row.find('td:nth-child(4)');
      $nospp = row.find('td:nth-child(5)');
      $up = row.find('td:nth-child(6)');

      $.each($nospm, function(){ var_nospm    = $(this).text();}); 
      $.each($tgl_spm, function(){ var_tgl_spm    = $(this).text();}); 
      $.each($skpd, function(){ var_skpd  = $(this).text();}); 
      $.each($nospp, function(){ var_nospp  = $(this).text();});
      $.each($status_keperluan, function(){ var_status_keperluan  = $(this).text();});
      $.each($up, function(){ var_up  = $(this).text();});

      generate_rinci_spm(var_nospm);
      generate_rekening(var_nospm);
    }else if (asal == 'SPM_LS'){   
      $nospm  = row.find('td:nth-child(1)');
      $tgl_spm  = row.find('td:nth-child(2)');
      $skpd = row.find('td:nth-child(3)');
      $status_keperluan = row.find('td:nth-child(4)');
      $nospp = row.find('td:nth-child(5)');
      $up = row.find('td:nth-child(6)');
      $kdbid = row.find('td:nth-child(7)');
      $kdprog = row.find('td:nth-child(8)');
      $kdkeg = row.find('td:nth-child(9)');

      $.each($nospm, function(){ var_nospm    = $(this).text();}); 
      $.each($tgl_spm, function(){ var_tgl_spm    = $(this).text();}); 
      $.each($skpd, function(){ var_skpd  = $(this).text();}); 
      $.each($nospp, function(){ var_nospp  = $(this).text();});
      $.each($status_keperluan, function(){ var_status_keperluan  = $(this).text();});
      $.each($up, function(){ var_up  = $(this).text();});
      $.each($kdbid, function(){ var_kdbid  = $(this).text();});
      $.each($kdprog, function(){ var_kdprog  = $(this).text();});
      $.each($kdkeg, function(){ var_kdkeg  = $(this).text();});

      generate_rinci_spm(var_nospm);
      generate_rekening(var_nospm);
    }else if (asal == 'SPP'){   
      $nospp  = row.find('td:nth-child(1)');
      $tgl_spp  = row.find('td:nth-child(2)');
      $skpd = row.find('td:nth-child(3)');
      $status_keperluan = row.find('td:nth-child(4)');
      $up = row.find('td:nth-child(5)');
      
      $.each($nospp, function(){ var_nospp    = $(this).text();}); 
      $.each($tgl_spp, function(){ var_tgl_spp    = $(this).text();}); 
      $.each($skpd, function(){ var_skpd  = $(this).text();}); 
      $.each($status_keperluan, function(){ var_status_keperluan  = $(this).text();});
      $.each($up, function(){ var_up  = $(this).text();});

      generate_rinci_spp(var_nospp);
    }else if (asal == 'SPP_LS'){   
      $nospp  = row.find('td:nth-child(1)');
      $tgl_spp  = row.find('td:nth-child(2)');
      $skpd = row.find('td:nth-child(3)');
      $status_keperluan = row.find('td:nth-child(4)');
      $up = row.find('td:nth-child(5)');
      $kdbid = row.find('td:nth-child(6)');
      $kdprog = row.find('td:nth-child(7)');
      $kdkeg = row.find('td:nth-child(8)');

      $.each($nospp, function(){ var_nospp    = $(this).text();}); 
      $.each($tgl_spp, function(){ var_tgl_spp    = $(this).text();}); 
      $.each($skpd, function(){ var_skpd  = $(this).text();}); 
      $.each($status_keperluan, function(){ var_status_keperluan  = $(this).text();});
      $.each($up, function(){ var_up  = $(this).text();});
      $.each($kdbid, function(){ var_kdbid  = $(this).text();});
      $.each($kdprog, function(){ var_kdprog  = $(this).text();});
      $.each($kdkeg, function(){ var_kdkeg  = $(this).text();});

      generate_rinci_spp(var_nospp);    
    }else if (asal == 'bendahara'){      
      $nama_bendahara  = row.find('td:nth-child(4)');
      $rekening  = row.find('td:nth-child(3)');
      $nama_bank = row.find('td:nth-child(2)');
      $no_npwp = row.find('td:nth-child(1)'); 
      
      $.each($nama_bendahara, function(){ var_nama_bendahara = $(this).text();}); 
      $.each($rekening, function(){ var_rekening    = $(this).text();}); 
      $.each($nama_bank, function(){ var_nama_bank  = $(this).text();}); 
      $.each($no_npwp, function(){ var_no_npwp  = $(this).text();});
      // $.each($skpd, function(){ var_skpd  = $(this).text();}); 
      var_skpd = $('#kd_org2').val();
    }

    
    var_skpd2 = var_skpd.split('.');
    var_take_spp = $('#kd_org2').val().split('.');

    $.get(is_skpkd_js(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2])).done(
	    function(){ 
  	    	
        if (asal == 'SPM'){
          $('#kd_org2').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2].split('-')[0]);
          $('#kd_org2_urai').val(var_skpd2[2].split('-')[1]);
          $('#kd_org').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]);

      		$('#no_spm').val(var_nospm);
          $('#tgl_spm').val(var_tgl_spm); 
          $('#no_spp').val(var_nospp);
          $('#tgl_spp').val(var_tgl_spm); 
          $('#status_keperluan').val(var_status_keperluan);   
          $('#jml_spm').val(var_up);   
          $('#jumlah_spm_up').val(var_up);
          $('#jml_spp_lama').val(var_up);
          // $('#terbilang').text(' '+terbilang(toAngka(var_up).toString()))
          $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(var_up).toString())))
          
          generate_dataTable_spm();
          generate_dataTable_spd_dasar(var_nospm, var_tgl_spm);
        } else if (asal == 'SPM_LS') {
          $('#kd_org2').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2].split('-')[0]);
          $('#kd_org2_urai').val(var_skpd2[2].split('-')[1]);
          $('#kd_org').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]);

          $('#no_spm').val(var_nospm);
          $('#tgl_spm').val(var_tgl_spm); 
          $('#no_spp').val(var_nospp);
          $('#tgl_spp').val(var_tgl_spm); 
          $('#status_keperluan').val(var_status_keperluan);   
          $('#jml_spm').val(var_up);   
          $('#jumlah_spm_up').val(var_up);
          $('#jml_spp_lama').val(var_up);
          $('#kdbid').val(var_kdbid);
          $('#kdprog').val(var_kdprog);
          $('#kdkeg').val(var_kdkeg);
          // $('#terbilang').text(' '+terbilang(toAngka(var_up).toString()))
          $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(var_up).toString())))
          
          generate_dataTable_spm();
          generate_dataTable_spd_dasar(var_nospm, var_tgl_spm);
        } else if (asal == 'SPP') {
          $('#no_spp').val(var_nospp);
          $('#tgl_spp').val(var_tgl_spp);
          $('#tgl_spm').val(var_tgl_spp);
          $('#deskripsi_spp').val(var_status_keperluan);
          $('#jml_spp').val(var_up); 
          $('#jml_spp_lama').val(var_up); 
          // $('#terbilang').text(' '+terbilang(toAngka(var_up).toString()))
          $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(var_up).toString())))
          
          generate_dataTable_afektasi_spm();
          generate_dataTable_spd_dasar_to_spp(var_nospp, var_tgl_spp);
        } else if (asal == 'SPP_LS') {
          $('#no_spp').val(var_nospp);
          $('#tgl_spp').val(var_tgl_spp);
          $('#tgl_spm').val(var_tgl_spp);
          $('#deskripsi_spp').val(var_status_keperluan);
          $('#jml_spp').val(var_up); 
          $('#jml_spp_lama').val(var_up);
          $('#kdbid').val(var_kdbid);
          $('#kdprog').val(var_kdprog);
          $('#kdkeg').val(var_kdkeg); 
          // $('#terbilang').text(' '+terbilang(toAngka(var_up).toString()))
          $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(var_up).toString())))
          
          generate_dataTable_afektasi_spm();
          generate_dataTable_spd_dasar_to_spp(var_nospp, var_tgl_spp);          
        } else if (asal == 'bendahara') {
          $('#bendahara').val(var_nama_bendahara); 
          $('#npwp_bendahara').val(var_rekening);
          $('#nama_bank').val(var_nama_bank); 
          $('#norek_bendahara').val(var_no_npwp);
        };
	    }
	);  
}

function generate_dataTable_spm(){
  var untuk_TU = $("#jen").val();
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_tabel_rinci_spm,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
      		 'kdsuburusan':$('#kd_org2').val().split('.')[1],
      		 'kdorganisasi':$('#kd_org2').val().split('.')[2],
         'nospm':$('#no_spm').val(),  
         'tgl_spm':$('#tgl_spm').val(), 
         'kdbid':$('#kdbid').val(), 
         'kdprog':$('#kdprog').val(), 
         'kdkeg':$('#kdkeg').val(), 
  			 'jenis_spm':$('#jen').val(),	
  			},
      dataType: 'html',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        var array_spm_sekakarang = [];
        // var array_rekening = [];
        // perbaikan
        array_rekening = [];
      	$('#dataTable_spm').DataTable( {
      		destroy:true,
          scrollY: 100,
          paging: false,
          scrollX: true,
          fixedHeader: true,
          "bLengthChange": false,
          "bInfo": false,
          "searching": false,
	        data: JSON.parse(data)['data_tbl_spm'],
	        'createdRow':  function (row, data, index) {
            if (data[5] != '0.00'){
              array_spm_sekakarang.push(data[5]);
              array_rekening.push(data[0]+'|'+data[5]);
            }
	        	$('td', row).css({ 'cursor': 'pointer'});
	        	for (var i = 2; i <= 7; i++) {
	        		$('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
	        	}
	        },
	        "footerCallback": function ( row, data, start, end, display ) {
	            var api = this.api(), data;
	 
	            // Remove the formatting to get integer data for summation
	            var intVal = function ( i ) {
	                return typeof i === 'string' ?
	                    i.replace(/[\$,]/g, '')*1 :
	                    typeof i === 'number' ?
	                        i : 0;
	            };
	 
	            // Total over all pages
	            total4 = api
	                .column( 5 )
	                .data()
	                .reduce( function (a, b) {
	                    return intVal(a) + intVal(b);
	                }, 0 );
	 			for (var i = 2; i <= 7; i++) {
	 				total = api
	                .column( i )
	                .data()
	                .reduce( function (a, b) {
	                    return intVal(a) + intVal(b);
	                }, 0 );
	 				$( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
	 			}
        // $('#tot_sekarang').text(' '+toAngkaDec(toRp_WithDecimal(total4)));
	 			$('#tot_sekarang').text(' '+toRp_WithDecimal(total4.toString()));  
        if (untuk_TU == 'TU_NIHIL'){
          $('#tot_terbilang').text('Nihil');
        } else{
  	 			$('#tot_terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDecimal(total4))));
        }
	 			$('#jum_tot_spm').val(total4.toString());
	       }
	    });$(".cover").hide();
      }
  });
}

function generate_dataTable_afektasi_spm(){
  var untuk_TU_dari_SPP = $("#jen").val();
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_tabel_afektasi_spm,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
           'kdsuburusan':$('#kd_org2').val().split('.')[1],
           'kdorganisasi':$('#kd_org2').val().split('.')[2],
         'nospp':$('#no_spp').val(),  
         'tgl_spp':$('#tgl_spp').val(),         
         'kdbid':$('#kdbid').val(), 
         'kdprog':$('#kdprog').val(), 
         'kdkeg':$('#kdkeg').val(), 
         'jenis_spm':$('#jen').val(), 
        },
      dataType: 'html',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        $(".cover").hide();
        $('#dataTable_spm').DataTable( {
          destroy:true,
          scrollY: 100,
          paging: false,
          scrollX: true,
          fixedHeader: true,
          "bLengthChange": false,
          "bInfo": false,
          "searching": false,
          data: JSON.parse(data)['data_afektasi_spm'],
          'createdRow':  function (row, data, index) {
            if (data[5] != '0.00'){
              array_spm_sekakarang.push(data[5]);
              array_rekening.push(data[0]+'|'+data[5]);
            }
            $('td', row).css({ 'cursor': 'pointer'});
            for (var i = 2; i <= 7; i++) {
              $('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
            }
          },
          "footerCallback": function ( row, data, start, end, display ) {
              var api = this.api(), data;
   
              // Remove the formatting to get integer data for summation
              var intVal = function ( i ) {
                  return typeof i === 'string' ?
                      i.replace(/[\$,]/g, '')*1 :
                      typeof i === 'number' ?
                          i : 0;
              };
   
              // Total over all pages
              total4 = api
                  .column( 5 )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
        for (var i = 2; i <= 7; i++) {
          total = api
                  .column( i )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
          $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
        }
        $('#tot_sekarang').text(' '+toRp_WithDecimal(total4.toString()));
        // $('#tot_sekarang').text(' '+toAngkaDec(toRp_WithDecimal(total4)));
        // $('#tot_terbilang').text(' '+terbilang(total4.toString()));
        if (untuk_TU_dari_SPP == 'TU_NIHIL'){
          $('#tot_terbilang').text('Nihil');
        } else{
          $('#tot_terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDecimal(total4))));
        }
        // $('#tot_terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDecimal(total4))));
        $('#jum_tot_spm').val(total4.toString());
         }
      });$(".cover").hide();
      }
  });

}

function generate_dataTable_spd_dasar(no_spm, tgl_spm){
var jenis_spm = $("#jen").val();
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_tabel_rinci_dasar_spd,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
           'kdsuburusan':$('#kd_org2').val().split('.')[1],
           'kdorganisasi':$('#kd_org2').val().split('.')[2],
         'nospm':no_spm,  
         'tgl_spp':tgl_spm,
         'jenis_spm':jenis_spm
        },
      dataType: 'html',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        $('#table_dasar_spd').DataTable( {
          destroy:true,
          scrollY: 90,
          paging: false,
          scrollX: true,
          fixedHeader: true,
          "bLengthChange": false,
          "bInfo": false,
          "searching": false,
          data: JSON.parse(data)['data_tbl_dasar_spd'],
          'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            for (var i = 2; i <= 2; i++) {
              $('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
            }
          },
          "footerCallback": function ( row, data, start, end, display ) {
              var api = this.api(), data;
   
              // Remove the formatting to get integer data for summation
              var intVal = function ( i ) {
                  return typeof i === 'string' ?
                      i.replace(/[\$,]/g, '')*1 :
                      typeof i === 'number' ?
                          i : 0;
              };
   
              // Total over all pages
              total4 = api
                  .column( 2 )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
        for (var i = 2; i <= 2; i++) {
          total = api
                  .column( i )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
          $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
        }
        }
      });$(".cover").hide();
      }
  });
}

function generate_dataTable_spd_dasar_to_spp(no_spp, tgl_spp){
var jenis_spm_to_spp = $("#jen").val();
console.log(jenis_spm_to_spp);
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_tabel_rinci_dasar_spd_to_spp,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
           'kdsuburusan':$('#kd_org2').val().split('.')[1],
           'kdorganisasi':$('#kd_org2').val().split('.')[2],
         'nospp':no_spp,  
         'tgl_spp':tgl_spp,
         'jenis_spm_to_spp':jenis_spm_to_spp,
        },
      dataType: 'html',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        $('#table_dasar_spd').DataTable( {
          destroy:true,
          scrollY: 90,
          paging: false,
          scrollX: true,
          fixedHeader: true,
          "bLengthChange": false,
          "bInfo": false,
          "searching": false,
          data: JSON.parse(data)['data_tbl_dasar_spd_to_spp'],
          'createdRow':  function (row, data, index) {
            $('td', row).css({ 'cursor': 'pointer'});
            for (var i = 2; i <= 3; i++) {
              $('td', row).eq(i).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[i]));
            }
          },
          "footerCallback": function ( row, data, start, end, display ) {
              var api = this.api(), data;
   
              // Remove the formatting to get integer data for summation
              var intVal = function ( i ) {
                  return typeof i === 'string' ?
                      i.replace(/[\$,]/g, '')*1 :
                      typeof i === 'number' ?
                          i : 0;
              };
   
              // Total over all pages
              total4 = api
                  .column( 2 )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
        for (var i = 2; i <= 2; i++) {
          total = api
                  .column( i )
                  .data()
                  .reduce( function (a, b) {
                      return intVal(a) + intVal(b);
                  }, 0 );
          $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
        }
        }
      });$(".cover").hide();
      }
  });
}

function generate_rinci_spm(no_spm){
  $("#btn_simpan").removeAttr('disabled')
  $("#btn_cetak").removeAttr('disabled')
  $("#btn_hapus").removeAttr('disabled')
  $("#no_spm").removeAttr('disabled')
  $("#no_spp").removeAttr('disabled')
  $("#tgl_spm").removeAttr('disabled')
  $("#tgl_spp").removeAttr('disabled')
  $("#btn_spp_spm").removeClass('avoid-clicks')
  $("#btn_bendahara").removeClass('avoid-clicks')

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_generate_rinci_spm,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
           'kdsuburusan':$('#kd_org2').val().split('.')[1],
           'kdorganisasi':$('#kd_org2').val().split('.')[2],
         'no_spm':no_spm,  
        },
      dataType: 'json',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        var bendahara = data['data_rincian'][0]
        $('#bendahara').val(bendahara[16]);
          $('#no_spm_lama').val(bendahara[4]);
          $('#norek_bendahara').val(bendahara[8]);
          $('#nama_bank').val(bendahara[9]); 
          $('#npwp_bendahara').val(bendahara[10]);
          $('#jml_spp').val(bendahara[13]);
          $('#triwulan').val(bendahara[20]).trigger('change');
          $('#perubahan').val(bendahara[28]).trigger('change');
          $('#btn_simpan').html('<i class="fa fa-floppy-o"></i>&nbsp;&nbsp;Ubah');
          $('#kunci_spm').html('( DRAFT )');
          $('#kunci_spm').removeClass('disetujui');
          isSimpan = false;
          $('input[name="aksi"]').val(isSimpan);
          if(bendahara[24]=="Y"){
            $('#kunci_spm').html('(DISETUJUI)');
            $('#kunci_spm').addClass('disetujui');
            $("#btn_simpan").attr('disabled','disabled')
            $("#btn_hapus").attr('disabled','disabled')
            $("#no_spm").attr('disabled','disabled')
            $("#no_spp").attr('disabled','disabled')
            $("#tgl_spm").attr('disabled','disabled')
            $("#tgl_spp").attr('disabled','disabled')
            // $("#btn_spp_spm").attr('disabled','disabled')

            // add class
            $("#btn_spp_spm").addClass('avoid-clicks')
            $("#btn_bendahara").addClass('avoid-clicks')
            // endd add

            $("#perubahan").attr('disabled','disabled')
            $("#triwulan").attr('disabled','disabled')
            $("#status_keperluan").attr('disabled','disabled')
            $("#bendahara").attr('disabled','disabled')
            $("#norek_bendahara").attr('disabled','disabled')
            $("#nama_bank").attr('disabled','disabled')
            $("#btn_bendahara").attr('disabled','disabled')
            // $("#btn_bendahara").attr('readonly', true)
            $("#npwp_bendahara").attr('disabled','disabled')
            // ini untuk halaman UP
            $("#jml_spm").attr('disabled','disabled')
            $.alertable.alert("SPM Nomor: "+no_spm+" telah di ACC oleh pimpinan. Anda tidak diperkenankan mengubah dan menghapus SPM tersebut!")
            $(".cover").hide();
          } 
      },
      error:function(err){
        console.log(err)
      }
  });
}

function generate_rinci_spp(no_spp){
  var coba_1 = no_spp.split('/')[2];
  if(coba_1 == "SPP-LS PPKD"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-LS PPKD','SPM-LS PPKD')
    // var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-UP"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-UP','SPM-UP')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-GU"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-GU','SPM-GU')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-TU"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-TU','SPM-TU')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-GJ"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-GJ','SPM-GJ')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-GU-NIHIL"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-GU-NIHIL','SPM-GU-NIHIL')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
  } else if(coba_1 == "SPP-NON ANGGARAN"){
    var b = no_spp.split('/');
    var a = b[2].replace('SPP-NON ANGGARAN','SPM-NON ANGGARAN')
    var ambil = b[0]+'/'+b[1]+'/'+a+'/'+b[3]
}
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_generate_rinci_spp,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
           'kdsuburusan':$('#kd_org2').val().split('.')[1],
           'kdorganisasi':$('#kd_org2').val().split('.')[2],
           'kdunit':$('#kd_org2').val().split('.')[3],
           
           'skpd':$('#kd_org2').val(),
           'no_spp':no_spp,
        },
      dataType: 'json',
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(data){
        var form_rinci_spp = data['data_rincian_spp'][0]
          // $('#no_spm').val(ambil);
          $('#deskripsi_spp').val(form_rinci_spp[10]);
          $('#status_keperluan').val(form_rinci_spp[10]);
          $('#jml_spm').val(form_rinci_spp[14]);
          $('#jumlah_spm_up').val(toRp_WithDecimal(form_rinci_spp[14])); 
          $('#norek_bendahara').val(form_rinci_spp[16]);
          $('#nama_bank').val(form_rinci_spp[30]); 
          $('#triwulan').val(form_rinci_spp[38]).trigger('change');
          $('#bendahara').val(form_rinci_spp[46]);
          $('#npwp_bendahara').val(form_rinci_spp[43]);
          $('#perubahan').val(form_rinci_spp[40]).trigger('change'); 
          $(".cover").hide();
      },
      error:function(err){
        console.log(err)
      }
  });
}

function generate_rekening(no_spm){
  
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_generate_rekening,
      data: {
          'kdurusan':$('#kd_org2').val().split('.')[0],
          'kdsuburusan':$('#kd_org2').val().split('.')[1],
          'kdorganisasi':$('#kd_org2').val().split('.')[2],
          'no_spm':no_spm,  
        },
      dataType: 'html',
      timeout: 10000,
      success: function(response){
        $('#tabel_potongan_spm').html(response);
        }
  });
}

function OnFokus_potongan(e){
  $(e).val(toAngkaDec($(e).val()));
}

function OnBlur_potongan(e){
  $(e).val(toRp_WithDecimal($(e).val()));
}

function cekNoSPM(){
  var digunakan = false;

  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_cek_spm,
      data: {
        'kdurusan':$('#kd_org2').val().split('.')[0],
        'kdsuburusan':$('#kd_org2').val().split('.')[1],
        'kdorganisasi':$('#kd_org2').val().split('.')[2],
        'no_spm':$('#no_spm').val(),
      },
      async: false,
      success: function(msg){
        if(msg <= 0){ digunakan = false; } else { digunakan = true; }
      }
  });

  return digunakan;
}

function simpan_spm(){
  var CKspm  = cekNoSPM($("#no_spm").val());
  var rek_potongan = $('input[name="cut_kdrek"]');
  var urai_potongan = $('span[name="uraipot"]');
  var jumlah_potongan = $('input[name="jml_pot"]');
  var jenis_potongan = $("[name='jns_cut']")

  function elementsToArray(param, type="val"){
    var arr = []
    $.each(param,function(e,obj){
      if(type == "val"){
        var val = $(obj).val()
      }else{
        var val = $(obj).html()
      }
      if(val.length >0){
        arr.push(val)
      }
    });
    return arr;
  }  

   var rek_potongan_arr=elementsToArray(rek_potongan) ,
    urai_potongan_arr = elementsToArray(urai_potongan, "html"),
    jumlah_potongan_arr = elementsToArray(jumlah_potongan),
    jenis_potongan_arr = elementsToArray(jenis_potongan);


    var bulan = {'Januari':'01', 'Februari':'02', 'Maret':'03', 'April':'04', 
  'Mei':'05', 'Juni':'06', 'Juli':'07', 'Agustus':'08',
    'September':'09', 'Oktober':'10', 'November':'11', 'Desember':'12'};

  var demo = $('#tgl_spp').val();
    var demos = demo.split(' ');

    var demounix = new Date(demos[2]+'-'+bulan[demos[1]]+'-'+demos[0]).getTime();
    var demo2 = $('#tgl_spm').val();
    var demos2 = demo2.split(' ');
    var demounix2 = new Date(demos2[2]+'-'+bulan[demos2[1]]+'-'+demos2[0]).getTime();


 if($( '#kd_org2').val() == 0){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else if($('#no_spm').val() == ""){
      $.alertable.alert("Nomor SPM harus diisi terlebih dahulu!"); return false;
  // } else if(CKspm == 1){
  //     $.alertable.alert("Nomor SPM : "+$('#no_spm').val()+" sudah digunakan!"); return false;
  } else if(demounix > demounix2){
      $.alertable.alert("Tanggal SPM harus sama/diatas tanggal SPP!"); return false;
  } else if($('#no_spp').val() == ""){
      $.alertable.alert("Nomor SPP harus dipilih terlebih dahulu!"); return false;
  } else if($('#status_keperluan').val() == ""){
      $.alertable.alert("Status Keperluan harus diisi terlebih dahulu!"); return false;
  } else if($('#bendahara').val() == ""){
      $.alertable.alert("Nama yang berhak memegang kas belum diisi!"); return false;
  } else if(!$('#tgl_spm').val()){
      $.alertable.alert("Tanggal SPM tidak boleh kurang dari tanggal SPP !"); return false;
  } else{ 
      $.alertable.confirm("Anda yakin akan menyimpan data SPM dengan Nomor : "+$('#no_spm').val()+" ?").then(function() {       
        $.ajax({
          type: "POST",
          headers: { "X-CSRFToken": csrf_token },
          url: link_simpan_spm,
          data: 
            {
              'kdurusan':$('#kd_org2').val().split('.')[0],
              'kdsuburusan':$('#kd_org2').val().split('.')[1],
              'kdorganisasi':$('#kd_org2').val().split('.')[2],
              'no_spm':$('#no_spm').val(), 
              'no_spm_lama':$('#no_spm_lama').val(), 
              'tgl_spm':$('#tgl_spm').val(), 
              'tgl_draft':$('#tgl_spm').val(), 
              'deskripsi_spp':$('#deskripsi_spp').val(),
              'no_spp':$('#no_spp').val(),
              'tgl_spp':$('#tgl_spp').val(),
              'tgl_spp':$('#tgl_spp').val(),
              'jml_spm':$('#jml_spm').val(),
              'jml_spp_x':$('#jml_spp').val(),
              'bendahara':$('#bendahara').val(),
              'nama_bendahara':$('#bendahara').val(),
              'norek_bendahara':$('#norek_bendahara').val(),
              'nama_bank':$('#nama_bank').val(),
              'jenis_spm':$('#jen').val(),
              'npwp':$('#npwp_bendahara').val(),
              'informasi':$('#deskripsi_spp').val(),
              'perubahan':$('#perubahan').val(),
              'triwulan':$('#triwulan').val(),
              'status_keperluan':$('#status_keperluan').val(),
              'spm_sekarang':array_spm_sekakarang[0],
              'spm_rekening1':JSON.stringify(array_rekening),
              'rekening_potongan':JSON.stringify(rek_potongan_arr),
              'uraian_potongan':JSON.stringify(urai_potongan_arr),
              'jumlah_potongan':JSON.stringify(jumlah_potongan_arr),
              'jenis_potongan':JSON.stringify(jenis_potongan_arr),
              'aksi':isSimpan,
            },
            success: function(data){
              message_ok("success",data);
              $("#btn_hapus").attr('disabled',false);
              $("#btn_cetak").attr('disabled',false);
              }                      
          });
    }, function() {
        message_ok('error', 'Anda telah membatalkan penghapusan data.');          
      });
  }
}

function hapus_spm(){
  if($('#no_spm').val() == ""){
      $.alertable.alert("Data SPM tidak terisi !!!");
  } else{ 
      $.alertable.confirm("Anda yakin akan menyimpan data SPM dengan Nomor : "+$('#no_spm').val()+" ?").then(function() {       
        $.ajax({
          type: "POST",
          headers: { "X-CSRFToken": csrf_token },
          url: link_hapus_spm,
          data: 
            {
              'kdurusan':$('#kd_org2').val().split('.')[0],
              'kdsuburusan':$('#kd_org2').val().split('.')[1],
              'kdorganisasi':$('#kd_org2').val().split('.')[2],
              'nospm':$('#no_spm').val(),
            },
            dataType: 'html',
            success: function(data){
              message_ok("success",data);
              setTimeout(location.reload(true), 2000);  
              }                      
          });
    }, function() {
        message_ok('error', 'Anda telah membatalkan penghapusan data.');          
      });
  }
}

function LoadData_Persetujuan_SPM(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("persetujuanSPM"); 
  var bulan = 1; 
  var ppkd = 0;
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd,
        get_bulan:bulan},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spm').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("persetujuanSPM");
  } 
}

function LoadData_Persetujuan_SPM_PPKD(e){
  var url  = $("#url_tabel").val();  
  var Cookie   = getCookie("persetujuanSPMPPKD"); 
  var bulan = 1; 
  var ppkd = 1;
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:e,
        isppkd:ppkd,
        get_bulan:bulan},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spm_ppkd').html(response);       
        $(".cover").hide();
      }
  }); 

  if(Cookie != ''){
    removeCookie("persetujuanSPMPPKD");
  } 
}

function getPersetujuanPPKD_SPM(val){ 
  var organisasi   = $("#kd_org2").val(); 
  var url  = $("#url_tabel").val();  
  var ppkd = 1;
  if($( '#kd_org2').val() == 0){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else{
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:organisasi,
        isppkd:ppkd,
        get_bulan:val},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spm_ppkd').html(response);       
        $(".cover").hide();
      }
    }); 
  }
}

function getPersetujuan_SPM(val){ 
  var organisasi   = $("#kd_org2").val(); 
  var url  = $("#url_tabel").val();  
  var ppkd = 0;
  if($( '#kd_org2').val() == 0){
      $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else{
  $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: {
        skpd:organisasi,
        isppkd:ppkd,
        get_bulan:val},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){        
        $('#table_persetujuan_spm').html(response);       
        $(".cover").hide();
      },
      error:function(err){
        console.log(err)
      }
    }); 
  }
}

function SimpanDraftSPM(e){  
  var frm = $('#draftSPM');
  var url = frm.attr('action');
  var skpd = $("#kd_org2").val();
  var chekDraftSPM = $(".checkbox_draftspm").is(":checked");  

  // test
  var data = [];
  var message = [];

  $.each($(".checkbox_draftspm:checked"),function(e,obj){
    var nomor_draft = $(obj).attr('data-draft')
    var month = $(obj).attr('data-tgldraft');
    data.push('nomer_draft='+nomor_draft)
    data.push('cek_draft='+1)
  })
  data.push('skpd='+skpd)


  if(chekDraftSPM == false){
    $.alertable.alert("Nomor SPM Belum ada yang dipilih");
        return false;
  }else{
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: data.join("&"),
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){ 
        $( "#kd_org2" ).trigger('change');
        $("#bulan_spm").trigger('change')
        message_ok('success', response);       
        $(".cover").hide();
      }
    }); 
  }
}

function SimpanSetujuSPM(e){  
  var frm = $('#setujuSPM');
  var url = frm.attr('action');
  var skpd = $("#kd_org2").val();
  var chekSPM = $(".checkbox_spm").is(":checked");  
  var data = [];
  var message = [];

  $.each($(".checkbox_spm:checked"),function(e,obj){
    var nosp2d = $(obj).attr('data-nosp2d')
    var nospm = $(obj).attr('data-spm')
    
    if(nosp2d == "None"){
      data.push('nomer_spm='+nospm)
      data.push('cek_spm='+1)
    }else{
      message.push(nosp2d)
    }

  })
  data.push('skpd='+skpd)

  if(chekSPM == false){
    $.alertable.alert("Nomor SPM Belum ada yang dipilih");
        return false;
  }else if(data.length == 1){
      $.alertable.alert("No SPM "+message.join(",")+" sudah dibuatkan SP2D, anda tidak dapat mengubahnya.");
  }else{
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: url,
      data: data.join("&"),
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){ 
        // setTimeout(location.reload(true), 2000);
        $( "#kd_org2" ).trigger('change');
        $("#bulan_spm").trigger('change')
        message_ok('success', response);       
        $(".cover").hide();
      }
    }); 
  }
}

// JS SPM BTL - PPKD =========================================================================================================

function load_tabel_SPM(){
        $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabel,
        async: false,
        dataType: "html",
        timeout: 10000,
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
            $('#tabel_dataspm').html(response);
            $(".cover").hide();
        }
      });
}

