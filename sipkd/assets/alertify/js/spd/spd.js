var isSimpan = true;
var perubahan_no_spd = false;
var skpd
var no_spd;
var berubah = true;
$(document).ready(function () {
	$('#table_spd').DataTable( {
        "bLengthChange": false, 
        scrollY:        "190px",
        scrollX:        true,
        //scrollCollapse: true,
        fixedHeader: true,
        paging:         false,
        "bInfo": false,
    });

    $('#tanggal_spd').daterangepicker({
        singleDatePicker: true,
        calender_style: "picker_4",
    }, function (start, end, label) {
    });

    $('#btn_cetak').attr('alt', link_render_cetak_spd);
});

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
      simpan_spd(function() {showModal(ini, 'cetak_spd');});
    }, function() {
        message_ok('error', 'Cetak Dibatalkan');
    });
  }else{
    simpan_spd(function() {showModal(ini, 'cetak_spd');});        
  }
});

$('#no_spd').change(function(){
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
		$('#bendahara').change();	
	}	

	
  if (berubah==true) {
    generate_table_rinci();
  }
});

$('#bulan').change(function(){
	generate_table_rinci();
});

$('#jnsdpa').change(function(){
	generate_table_rinci();
});

$('#bendahara').change(function(){
  if ($(this).val()!=null) {
    $('#nip_bendahara').val($('#'+$(this).val().replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-')+'').attr('nip'));
  }
});

function ambil_bendahara(){
	kode = $('#kd_org2').val();
	if (kode!='') {
		$.ajax({
	    	type: "POST",
	      	headers: { "X-CSRFToken": csrf_token },
	      	url: link_ambil_bendahara,
	      	data: {kode_organisasi:kode},
	      	async: false,
	      	success: function(data){ 
	      		$('#bendahara').html('');
	      		for (var i = 0; i < JSON.parse(data).length; i++) {
	      			$('#bendahara').append('<option nip = "'+JSON.parse(data)[i]['nip']+'" id = "'+JSON.parse(data)[i]['nama'].replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '-')+'" value="'+JSON.parse(data)[i]['nama']+'">'+JSON.parse(data)[i]['nama']+'</option>')
	      		}
	      	}
		});
	}
}

function fungsi_modal(ini, asal_modal){	var var_nospd, var_skpd;
    var row     = $(ini).closest('tr'); 
    var tglnya = '';

    var $nospd  = row.find('td:nth-child(1)');
    var $tgl = row.find('td:nth-child(2)');
    var $skpd = row.find('td:nth-child(3)');

    $.each($nospd, function(){ var_nospd    = $(this).text();}); 
    $.each($tgl, function(){ tglnya  = $(this).text();}); 
    $.each($skpd, function(){ var_skpd  = $(this).text();}); 

    var var_skpd2 = var_skpd.split('.');
    
    $.get(is_skpkd_js(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2])).done(
	    function(){ 
	    	$('#kd_org2').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]);
	    	$('#kd_org2_urai').val(var_skpd2[3]);
	    	$('#kd_org').val(var_skpd2[0]+'.'+var_skpd2[1]+'.'+var_skpd2[2]+' - '+var_skpd2[3]);
    		$('#kd_org2').trigger('change');
    		$('#no_spd').val(var_nospd); 
    		rinci_spd(var_skpd2[0],var_skpd2[1],var_skpd2[2],var_nospd);
        $('#tanggal_spd').val(tglnya);

	    }
	);  
}

function rinci_spd(kdurusan, kdsuburusan, kdorganisasi, nospd){
	isSimpan = false;
  berubah = true;
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_rinci_spd,
      data: {'kdurusan':kdurusan,
      		 'kdsuburusan':kdsuburusan,
      		 'kdorganisasi':kdorganisasi,
  			 'nospd':nospd,	
  			},
      dataType: 'html',
      success: function(data){
      	rinci = JSON.parse(data)['hasil'][0];
      	$('#jnsdpa').val(rinci.jenisdpa);
      	$('#bendahara').val(rinci.bendaharapengeluaran);
      	$('#bulan').val(rinci.bulan_awal);
      	if (rinci.locked=='Y') {
      		$('#btn_hapus').attr('disabled','disabled');
      	}else{
      		$('#btn_hapus').removeAttr('disabled');
				}
				generate_table_rinci();
      },error:function(){
				message_ok("error","Ambil rincian SPD Gagal! ");
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

				 $('#jumlah_spd').text(': Rp. '+toRp_WithDesimal(total4.toString()));
				 $('#jum_tot_spd').val(total4.toString());
				 terbilangya = terbilang(toAngkaDec(toRp_WithDesimal(total4.toString())));
				 $('#terbilang').text(' '+terbilang(toAngkaDec(toRp_WithDesimal(total4.toString()))));
	       }
			});
				
      }
  });
}

function simpan_spd(callback){
  if ($('#no_spd').val()=='') {
    $.alertable.alert('Nomor SPD masih kosong !');
  }else if($('#kd_org2').val()==''){
    $.alertable.alert('Kode organisasi masih kosong !');
  }else if($('#jnsdpa').val()==''){
    $.alertable.alert('Jenis DPA masih kosong !');
  }else if($('#bendahara').val()==''){
    $.alertable.alert('Bendahara masih kosong !');
  }else{
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_simpan_spd,
        data: {'kdurusan':$('#kd_org2').val().split('.')[0],
             'kdsuburusan':$('#kd_org2').val().split('.')[1],
             'kdorganisasi':$('#kd_org2').val().split('.')[2],
           'nospd':$('#no_spd').val(),  
           'bulan':$('#bulan').val(),
           'jenisdpa':$('#jnsdpa').val(),
           'jumlah_total':$('#jum_tot_spd').val(),
           'tanggal_draft':$('#tanggal_spd').val(),
           'bendahara':$('#bendahara').val(),
           'isSimpan':isSimpan,
          },
        dataType: 'html',
        success: function(data){
          message_ok("success",data);
          perubahan_no_spd = false;
          callback();
        },
        error: function(){
          message_ok("error","Proses Gagal! ");
        }
    });
  }
}

function hapus_spd(){
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_hapus_spd,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
      		 'kdsuburusan':$('#kd_org2').val().split('.')[1],
      		 'kdorganisasi':$('#kd_org2').val().split('.')[2],
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
}