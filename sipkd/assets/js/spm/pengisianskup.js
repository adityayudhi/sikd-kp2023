var act = 'edit';
$(document).ready(function () {
	table = $('#tabel_pengisianskup').DataTable( {
        "bLengthChange": false, 
        scrollY:        "250px",
        scrollX:        true,
        //scrollCollapse: true,
        fixedHeader: true,
        paging:         false,
    });

    if (sessionStorage.getItem("last_org_skup")!=null) {
    	$('#kd_org2').val(sessionStorage.getItem("last_org_skup").split('-')[0].replace(/[_\s]/g, ''));
    	$('#kd_org').val(sessionStorage.getItem("last_org_skup"));
    	$('#kd_org2_urai').val(sessionStorage.getItem("last_org_skup").split('-')[1].trim());
    	get_skup();
    }

    $("#kd_org2").change(function(){
		get_skup();
	});

    $('#btn_tambah_data').attr('alt',link_modal_tambah_skup);

    $('#btn_tambah_data').click(function(){
    	if ($('#kd_org2').val()=='') {
    		$.alertable.alert('Pilih Organisasi Terlebih Dahulu !')
    	}else{
    		showModal(this,'tambah_skup');
    		act = 'add';
    	}
    });
});

function get_skup(){
	$.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrf_token },
      url: link_data_skup,
      data: {'kdurusan':$('#kd_org2').val().split('.')[0],
      		 'kdsuburusan':$('#kd_org2').val().split('.')[1],
      		 'kdorganisasi':$('#kd_org2').val().split('.')[2],
  			},
      dataType: 'html',
      success: function(data){
     	table = $('#tabel_pengisianskup').DataTable( {
      		destroy:true,
	        "bLengthChange": false, 
	        scrollY:        "250px",
	        scrollX:        true,
	        //scrollCollapse: true,
	        fixedHeader: true,
	        paging:         false,
	        "bInfo": false,
	        data: JSON.parse(data)['hasil'],
	        'createdRow':  function (row, data, index) {
	        	$('td', row).css({ 'cursor': 'pointer'});
	        	$('td', row).eq(3).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[3]));
	        	$('td', row).eq(1).css({ 'text-align': 'center'}).text(getTglINDO2(data[1].toString()));
	        	$('td', row).eq(2).css({ 'text-align': 'center'});
	        	$('td', row).eq(4).css({ 'text-align': 'center'});
	        	$('td', row).eq(4).html('<div onclick="edit(\''+data[0]+'\')" style="margin-right:5px;" class="btn btn-info btn-sm" title="Ubah Data">\
					                        <i class="fa fa-pencil-square-o"></i>\
					                    </div>\
					                    <div onclick="hapus(\''+data[0]+'\')" style="margin-right:5px;" class="btn btn-danger btn-sm" title="Hapus Data">\
					                        <i class="fa fa-trash"></i>\
					                    </div>');
	        },
	    });
      },
      error: function(){
      	message_ok("error","Proses Gagal! ");
      }
  });
}

function edit(no_skup){
	$.ajax({
		type : "POST",
		headers : { "X-CSRFToken": csrf_token },
		url	: link_modal_edit_skup,
		data :{
			'kdurusan':$('#kd_org2').val().split('.')[0],
			'kdsuburusan':$('#kd_org2').val().split('.')[1],
			'kdorganisasi':$('#kd_org2').val().split('.')[2],
			'no_skup':no_skup,
		},
		dataType: 'html',
		success: function(data){
			showModal_ajax(data, 'edit_skup');
		},
		error: function(){
			message_ok('error', 'Proses Gagal !');
		}
	});
}

function hapus(no_skup){
	$.alertable.confirm("Anda yakin ingin menghapus SKUP "+no_skup).then(function() {
		$.ajax({
			type : "POST",
			headers : { "X-CSRFToken": csrf_token },
			url	: link_modal_hapus_skup,
			data :{
				'kdurusan':$('#kd_org2').val().split('.')[0],
				'kdsuburusan':$('#kd_org2').val().split('.')[1],
				'kdorganisasi':$('#kd_org2').val().split('.')[2],
				'no_skup':no_skup,
				'act': 'del',
			},
			dataType: 'html',
			success: function(data){
				message_ok('success', 'Data berhasil dihapus');
				get_skup();
			},
			error: function(){
				message_ok('error', 'Proses Gagal !');
			}
		});
	}, function() {
		alert_botom("error","anda telah membatalkan Logout");
	});
}