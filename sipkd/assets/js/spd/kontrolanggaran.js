var array_keg = [];
var pjg_keg = 0;
$(document).ready(function () {
    var table = $('#kontrol_anggaran').DataTable( {
        scrollY: 257,
        paging: false,
    });
    $('#btn_next').attr('disabled','disabled');
    $('#btn_prev').attr('disabled','disabled');
});

$('#kd_org2').change(function(){
	if (var_skpkd == '1') {
		$('#cek_ppkd').html('<label><input type="checkbox" id="ppkd_checked" onClick="is_checked(this)">&nbsp;PPKD</label>');
	}else{
		$('#cek_ppkd').html('');
	}

	if ($('#ppkd_checked').is(':checked')) {
		var_skpkd = '1';
	}else{
		var_skpkd = '0';
	}
	
	load_kontrol_anggaran();
});

function load_kontrol_anggaran(){
	$.ajax({
	    type : "POST",
	    headers : { "X-CSRFToken": csrf_token },
	    url : link_load_kontrolanggaran,
	    data :{
	    	'kode':$('#kd_org2').val(),
	        'jenis_load':'keg',
	        'isskpd':var_skpkd,
	    },
	    dataType: 'html',
	    beforeSend: function() {
	        $(".cover").show();
	    },
	    success: function(data){
	    	pjg_keg = JSON.parse(data)['list_kontrol_anggaran'].length;
	    	$('#kontrol_anggaran').DataTable( {
	            destroy:true,
	            "bLengthChange":false, 
	            scrollY:259,
	            scrollX:true,
	            fixedHeader:true,
	            paging:false,
	            "columnDefs": [
				    { "title": "<input type=\"checkbox\" onClick=\"cek_uncek_all_kontrolangg(this, 'chk_kontrolangg', 'keg')\"/>", "targets": 0, "width": "2%"},
				    { "title": "Kode Kegiatan", "targets": 1, "width": "20px" },
				    { "title": "Uraian", "targets": 2, "width": "170px" },
				    { "title": "Anggaran", "targets": 3, "width": "10px" },
				    { "title": "SPD Terbit", "targets": 4, "width": "10px" },
				    { "title": "SP2D Terbit", "targets": 5, "width": "10px" },
				    { "title": "Sisa SPD", "targets": 6, "width": "10px" },
				    { "title": "Sisa Anggaran", "targets": 7, "width": "10px" },
				    {"targets": [ 7 ], "visible": true},
				  ],
	            "order": [[ 1, "asc" ]],
	            data: JSON.parse(data)['list_kontrol_anggaran'],
	            'createdRow':  function (row, data, index) {
	                $('td', row).css({ 'cursor': 'pointer'});

	                for (var i = 3; i <= 7; i++) {
	                	$('td', row).eq(i).css({ 'text-align': 'right'});
	                	$('td', row).eq(i).text(data[i]=='None' ? toRp_WithDecimal('0'):toRp_WithDecimal(data[i]));
	                }	                

	                if (data[0]=='0') {
	                	$('td', row).eq(0).html('<input type="checkbox" class="chk_kontrolangg_keg" onclick="checkclick_kontrolangg_keg(this, \''+index+'\', \'keg\')" id="check_'+index+'">\
	                							<input type="hidden" name="cek_keg" id="cek_keg_'+index+'" value="'+data[0]+'"/>\
		        								<input type="hidden" name="val_keg" id="val_keg_'+index+'" value="'+data[1]+'"/>');
	                }else if(data[0]=='1'){
	                	array_keg.push(data[1]);
	                	$('td', row).eq(0).html('<input type="checkbox" class="chk_kontrolangg_keg" onclick="checkclick_kontrolangg_keg(this, \''+index+'\', \'keg\')" checked = "checked" id="check_'+index+'">\
	                    						<input type="hidden" name="cek_keg" id="cek_keg_'+index+'" value="'+data[0]+'"/>\
			        							<input type="hidden" name="val_keg" id="val_keg_'+index+'" value="'+data[1]+'"/>');
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
	                for (var i = 3; i <= 7; i++) {
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
	        $('#btn_next').removeAttr('disabled');
	        $(".cover").hide();
	        // var_skpkd = '0';
	    },
	    error: function(){
	        message_ok('error', 'Proses Gagal !');
	        $(".cover").hide();
	    }
	});
}

function ambil_rincian_kontrolangg(){
	$.ajax({
	    type : "POST",
	    headers : { "X-CSRFToken": csrf_token },
	    url : link_load_kontrolanggaran,
	    data :{
	    	'kode':$('#kd_org2').val(),
	        'kode_keg':JSON.stringify(array_keg),
	        'jenis_load':'rinci',
	        'isskpd':var_skpkd,
	    },
	    dataType: 'html',
	    beforeSend: function() {
	        $(".cover").show();
	    },
	    success: function(data){
	    	$('#kontrol_anggaran').DataTable( {
	            destroy:true,
	            "bLengthChange":false, 
	            scrollY:259,
	            scrollX:true,
	            fixedHeader:true,
	            paging:false,
	            "columnDefs": [
				    { "title": "Kode Kegiatan", "targets": 0, "width": "150px"},
				    { "title": "Uraian", "targets": 1, "width": "460px" },
				    { "title": "Anggaran", "targets": 2, "width": "97px" },
				    { "title": "SPD Terbit", "targets": 3 },
				    { "title": "SP2D Terbit", "targets": 4 },
				    { "title": "Sisa SPD", "targets": 5 },
				    { "title": "Sisa Anggaran", "targets": 6 },
				    {"targets": [ 7 ], "visible": false},
				  ],
	            "order": [[ 0, "asc" ]],
	            data: JSON.parse(data)['list_kontrol_anggaran'],
	            'createdRow':  function (row, data, index) {
	                $('td', row).css({ 'cursor': 'pointer'});

	                for (var i = 2; i <= 6; i++) {
	                	$('td', row).eq(i).css({ 'text-align': 'right'});
	                	$('td', row).eq(i).text(toRp_WithDecimal(data[i] == 'None'?'0':data[i]));
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
	                for (var i = 2; i <= 6; i++) {
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
	        $('#btn_next').attr('disabled','disabled');
	        $('#btn_prev').removeAttr('disabled');
	        array_keg = [];
	        $(".cover").hide();
	    },
	    error: function(){
	        message_ok('error', 'Proses Gagal !');
	        $(".cover").hide();
	    }
	});
}

function cek_uncek_all_kontrolangg(e, chkclass, page){
    $('.'+chkclass+'_'+page).each(function(){ 
        this.checked = e.checked; 
    });

    if(e.checked){
        $('#frm_kontrolangg input[name=cek_'+page+']').val('1');
        for (var i = 0; i < pjg_keg; i++) {
        	if ($("#val_"+page+"_"+i+"").val()!=undefined) {
    			array_keg.push($("#val_"+page+"_"+i+"").val()); 	
    		}
        }
        
    } else {
        $('#frm_kontrolangg input[name=cek_'+page+']').val('0');
        for (var i = 0; i < pjg_keg; i++) {
        	array_keg.splice(array_keg.indexOf($("#val_"+page+"_"+i+"").val()), 1);
        }
    }
};

function checkclick_kontrolangg_keg(e, urutan, tabel){
    if(e.checked){
        $("#cek_"+tabel+"_"+urutan+"").val('1');
        if (tabel=='keg') {
        	array_keg.push($("#val_"+tabel+"_"+urutan+"").val()); 
        }else if (tabel=='rinci'){
        	array_rinci.push($("#val_"+tabel+"_"+urutan+"").val()); 
        }
    } else {
        $("#cek_"+tabel+"_"+urutan+"").val('0');
        if (tabel=='keg') {
        	array_keg.splice(array_keg.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1); 
        }else if (tabel=='rinci'){
        	array_rinci.splice(array_rinci.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1);
        }
    }
}

function is_checked(e){
	if(e.checked){
		var_skpkd = '1';
		load_kontrol_anggaran();
	}else{
		var_skpkd = '0';
		load_kontrol_anggaran();
	}
}

$('#btn_next').click(function(){
	if (array_keg.length<=0) {
		$.alertable.alert('Belum ada kegiatan yang dipilih !')
	}else{
		ambil_rincian_kontrolangg();	
	}
});

$('#btn_prev').click(function(){
	load_kontrol_anggaran();
	$(this).attr('disabled','disabled');
});