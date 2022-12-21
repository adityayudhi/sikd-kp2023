

var array_keg = [];
var array_rinci = [];
var var_page = '';
var pjg_keg = 0;
var pjg_rinci = 0;
$(document).ready(function () {
    var table = $('#daftar_otorisasi').DataTable( {
        scrollY: 259,
        paging: false,
        "ordering": false
    });
    $('#btn_simpan').attr('disabled','disabled');
    $('#btn_prev').attr('disabled','disabled');
});

$('#kd_org2').change(function(){
	$.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambil_skpkd,
        data :{
            'kode':$('#kd_org2').val(),
            'jenis_load':'keg',
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
        	$('#jnsdpa').html('');
        	$('#jnsdpa').append('<option value="">-- PILIH JENIS DPA --</option>');
            for (var i = 0; i < JSON.parse(data)['array'].length; i++) {
            	$('#jnsdpa').append('<option value="'+JSON.parse(data)['array'][i]+'">'+JSON.parse(data)['array'][i]+'</option>');
            }
            $(".cover").hide();
        },
        error: function(){
            message_ok('error', 'Proses Gagal !');
            $(".cover").hide();
        }
    });
});

function ambil_skpkd(){
	array_keg = [];
	$.ajax({
        type : "POST",
        headers : { "X-CSRFToken": csrf_token },
        url : link_ambil_skpkd,
        data :{
            'kode':$('#kd_org2').val(),
            'jenis':$('#jnsdpa').val(),
            'jenis_load':'keg',
        },
        dataType: 'html',
        beforeSend: function() {
            $(".cover").show();
        },
        success: function(data){
        	pjg_keg = JSON.parse(data)['kegiatan'].length;
        	$('#daftar_otorisasi').DataTable( {
                destroy:true,
                "bLengthChange":false, 
                scrollY:259,
                scrollX:true,
                fixedHeader:true,
                paging:false,
                "ordering": false,
                data: JSON.parse(data)['kegiatan'],
                'createdRow':  function (row, data, index) {
                    $('td', row).css({ 'cursor': 'pointer'});
                    for (var i = 3; i <= 5; i++) {
                    	$('td', row).eq(i).css({ 'text-align': 'right'});
                    	$('td', row).eq(i).text(toRp_WithDecimal(data[i]));
                    }

                    if (data[0]=='0') {
                    	$('td', row).eq(0).html('<input type="checkbox" class="chk_oto_keg" onclick="checkclick_lock_keg(this, \''+index+'\', \'keg\')" id="check_'+index+'">\
                    							<input type="hidden" name="cek_keg" id="cek_keg_'+index+'" value="'+data[0]+'"/>\
		        								<input type="hidden" name="val_keg" id="val_keg_'+index+'" value="'+data[9]+'&'+data[10]+'&'+data[11]+'_'+data[1]+'"/>');
                    }else if(data[0]=='1'){
                    	$('td', row).eq(0).html('<input type="checkbox" onclick="checkclick_lock_keg(this, \''+index+'\', \'keg\')" checked = "checked" id="check_'+index+'">');
                    }
                    $('td', row).eq(0).css({ 'text-align': 'center'});

                   	if (data[7] == '0') {
                   		$('td', row).css({ 'background-color': '#8af460'});
                   	}else{
                   		$('td', row).css({ 'background-color': '#f9f697'});
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
                    for (var i = 3; i <= 5; i++) {
                    	total = api
	                        .column( i )
	                        .data()
	                        .reduce( function (a, b) {
	                            return intVal(a) + intVal(b);
	                        }, 0 );
	                    $( api.column( i ).footer() ).html(toRp_WithDesimal(total.toString()));
                    }
                }
            });
            $(".cover").hide();
            $('#btn_next').removeAttr('disabled');
			$('#btn_simpan').attr('disabled','disabled');
		    $('#btn_prev').attr('disabled','disabled');
		    var_page = 'keg';
        },
        error: function(){
            message_ok('error', 'Proses Gagal !');
            $(".cover").hide();
        }
    });
}

function ambil_rincian_lock(){
	$.ajax({
	    type : "POST",
	    headers : { "X-CSRFToken": csrf_token },
	    url : link_ambil_skpkd,
	    data :{
	    	'kode':$('#kd_org2').val(),
	        'kode_keg':JSON.stringify(array_keg),
	        'jenis':$('#jnsdpa').val(),
	        'jenis_load':'rinci',
	    },
	    dataType: 'html',
	    beforeSend: function() {
	        $(".cover").show();
	    },
	    success: function(data){
	    	pjg_rinci = JSON.parse(data)['kegiatan'].length;
	    	$('#btn_simpan').removeAttr('disabled');
			$('#btn_prev').removeAttr('disabled');

	    	$('#daftar_otorisasi').DataTable( {
	            destroy:true,
	            "bLengthChange":false, 
	            scrollY:259,
	            scrollX:true,
	            fixedHeader:true,
	            paging:false,
                "ordering": false,
	            "order": [[ 1, "asc" ]],
	            data: JSON.parse(data)['kegiatan'],
	            "columnDefs": [
		            {
		                "targets": [ 6 ],
		                "visible": false
		            }
		        ],
	            'createdRow':  function (row, data, index) {
	                $('td', row).css({ 'cursor': 'pointer'});
	                for (var i = 3; i <= 5; i++) {
	                	$('td', row).eq(i).css({ 'text-align': 'right'});
	                	$('td', row).eq(i).text(toRp_WithDecimal(data[i]));
	                }

	                if (!data[1].includes('-')) {
	                	$('td', row).eq(3).text(toRp_WithDecimal(data[9]));
	                	$('td', row).eq(4).text(toRp_WithDecimal(data[10]));
	                	$('td', row).eq(5).text(toRp_WithDecimal(data[11]));
	                }

	                

	                if (data[0]=='0') {
	                	if (data[1].includes('-')) {
	                		$('td', row).eq(0).html('<input type="checkbox" class="chk_oto_rinci" onclick="checkclick_lock_keg(this, \''+index+'\', \'rinci\')" id="check_'+index+'">\
	                							<input type="hidden" name="cek_rinci" id="cek_rinci_'+index+'" value="'+data[0]+'"/>\
		        								<input type="hidden" name="val_rinci" id="val_rinci_'+index+'" value="'+data[12]+'&'+data[13]+'&'+data[14]+'_'+data[1]+'"/>');
	                	}else{
	                		$('td', row).eq(0).text('');
	                	}
	                }else if(data[0]=='1'){
	                	if (data[1].includes('-')) {
	                		array_rinci.push(data[12]+'&'+data[13]+'&'+data[14]+'_'+data[1]);
	                    	$('td', row).eq(0).html('<input type="checkbox" class="chk_oto_rinci" onclick="checkclick_lock_keg(this, \''+index+'\', \'rinci\')" checked = "checked" id="check_'+index+'">\
	                    							<input type="hidden" name="cek_rinci" id="cek_rinci_'+index+'" value="'+data[0]+'"/>\
			        								<input type="hidden" name="val_rinci" id="val_rinci_'+index+'" value="'+data[12]+'&'+data[13]+'&'+data[14]+'_'+data[1]+'"/>');
	                	}else{
	                		$('td', row).eq(0).text('');
	                	}
	                }

	                $('td', row).eq(0).css({ 'text-align': 'center'});
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
	                for (var i = 3; i <= 5; i++) {
	                	if (!data[1].includes('-')) {
	                		total2 = api
		                        .column( i )
		                        .data()
		                        .reduce( function (a, b) {
		                        	return intVal(a) + intVal(b);
		                        }, 0 );
		                    $( api.column( i ).footer() ).html(toRp_WithDesimal(total2.toString()));
	                	}	                    	
	                }
	            }
	        });
	        $('#btn_next').attr('disabled','disabled');
	        $(".cover").hide();
	        var_page='rinci';
	    },
	    error: function(){
	        message_ok('error', 'Proses Gagal !');
	        $(".cover").hide();
	    }
	});
}

$('#jnsdpa').change(function(){
	ambil_skpkd();
});

function cek_uncek_all(e, chkclass, page){
    $('.'+chkclass+'_'+page).each(function(){ 
        this.checked = e.checked; 
    });

    if (page=='keg') {
    	jml = pjg_keg;
    }else{
    	jml = pjg_rinci;
    }

    if(e.checked){
        $('#frm_spd_lock_anggaran input[name=cek_'+page+']').val('1');
        if (page=='keg') {
        	array_keg=[];
        }else if(page=='rinci'){
        	array_rinci = [];
        }

        for (var i = 0; i < jml; i++) {
        	if (page=='keg') {
        		if ($("#val_"+page+"_"+i+"").val()!=undefined) {
        			array_keg.push($("#val_"+page+"_"+i+"").val()); 	
        		}
	        }else if (page=='rinci'){
	        	if ($("#val_"+page+"_"+i+"").val()!=undefined) {
	        		array_rinci.push($("#val_"+page+"_"+i+"").val()); 
	        	}
	        }
        }
        
    } else {
        $('#frm_spd_lock_anggaran input[name=cek_'+page+']').val('0');
        for (var i = 0; i < jml; i++) {
        	if (page=='keg') {
	        	array_keg.splice(array_keg.indexOf($("#val_"+page+"_"+i+"").val()), 1); 
	        }else if (page=='rinci'){
	        	array_rinci.splice(array_rinci.indexOf($("#val_"+page+"_"+i+"").val()), 1);
	        }
        }
    }
};

function checkclick_lock_keg(e, urutan, tabel){
	value = $("#val_"+tabel+"_"+urutan+"").val();

    if(e.checked){
        $("#cek_"+tabel+"_"+urutan+"").val('1');
        if (tabel=='keg') {
        	array_keg.push(value); 
        }else if (tabel=='rinci'){
        	if (value.includes('-')) {
        		array_rinci.push(value); 
        	}
        }
    } else {
        $("#cek_"+tabel+"_"+urutan+"").val('0');
        if (tabel=='keg') {
        	array_keg.splice(array_keg.indexOf(value), 1); 
        }else if (tabel=='rinci'){
        	array_rinci.splice(array_rinci.indexOf(value), 1);
        }
    }
}

$('#btn_next').click(function(){
	if ($('#kd_org2').val() != '' && $('#jnsdpa').val() != '') {
		if (array_keg.length < 1) {
			$.alertable.alert('Kegiatan belum dipilih !');
		}else{
			ambil_rincian_lock();	
		}
	}
});

$('#btn_prev').click(function(){
	array_rinci = [];
	ambil_skpkd();
});

$('#btn_simpan').click(function(){
	$.ajax({
	    type : "POST",
	    headers : { "X-CSRFToken": csrf_token },
	    url : link_insert_lock,
	    data :{
	    	'kode_org':$('#kd_org2').val(),
	        'kode_rinci':JSON.stringify(array_rinci),
	        'kode_keg':JSON.stringify(array_keg),
	    },
	    dataType: 'html',
	    beforeSend: function() {
	        $(".cover").show();
	    },
	    success: function(data){
	    	message_ok('success','Proses Berhasil');
	    	array_rinci = [];
	        $(".cover").hide();
	        ambil_rincian_lock();
	    },
	    error: function(){
	        message_ok('error', 'Proses Gagal !');
	        $(".cover").hide();
	    }
	});
});