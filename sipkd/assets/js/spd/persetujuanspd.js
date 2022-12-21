var array_draft = []; 
var array_unlock = [];
var aksi = ''
$(document).ready(function () {
    var table = $('#tabel_draft').DataTable( {
        "bLengthChange": false, 
        scrollY:        "250px",
        scrollX:        true,
        fixedHeader: 	true,
        paging:         false,
        "bInfo":false,
    });

    var table = $('#tabel_unlock').DataTable( {
        "bLengthChange": false, 
        scrollY:        "250px",
        scrollX:        true,
        fixedHeader: 	true,
        paging:         false,
        "bInfo":false,
    });
    load_draft_spd();
});

function load_draft_spd(){
	$.ajax({
		type : "POST",
		headers : { "X-CSRFToken": csrf_token },
		url	: link_load_draft_persetujuan_spd,
		data :{
		},
		dataType: 'html',
		beforeSend: function() {
			$(".cover").show();
	    },
		success: function(data){
			// TABEL DRAFT
			$('#tabel_draft').DataTable( {
	      		destroy:true,
		        "bLengthChange":false, 
		        scrollY:"250px",
		        scrollX:true,
		        fixedHeader:true,
		        paging:false,
		        "bInfo":false,
		        data: JSON.parse(data)['draft'],
		        'createdRow':  function (row, data, index) {
		        	$('td', row).css({ 'cursor': 'pointer'});
		        	$('td', row).eq(5).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[5]));
		        	$('td', row).eq(1).css({ 'text-align': 'center'}).text(getTglINDO2(data[1].toString()));
		        	$('td', row).eq(3).css({ 'text-align': 'center'})
		        	$('td', row).eq(4).css({ 'text-align': 'center'}).text(convert_ke_bulan(data[4]));
		        	$('td', row).eq(7).css({ 'text-align': 'center'}).html('<input type="checkbox" class="chk_rek_draft" onClick="checkclick(this, '+index+',\'draft\')"/>\
		        															<input type="hidden" name="cek_draft" id="cek_draft_'+index+'" value="'+data[7]+'"/>\
		        															<input type="hidden" name="val_draft" id="val_draft_'+index+'" value="'+data[0]+'_'+data[2]+'"/>');
		        	
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
		            total = api
		                .column( 5 )
		                .data()
		                .reduce( function (a, b) {
		                    return intVal(a) + intVal(b);
		                }, 0 );
		 			$( api.column( 5 ).footer() ).html(toRp_WithDesimal(total.toString()));
		       	}
		    });

			// TABEL SETUJU
		    $('#tabel_unlock').DataTable( {
	      		destroy:true,
		        "bLengthChange":false, 
		        scrollY:"250px",
		        scrollX:true,
		        fixedHeader:true,
		        paging:false,
		        "bInfo":false,
		        data: JSON.parse(data)['setuju'],
		        'createdRow':  function (row, data, index) {
		        	$('td', row).css({ 'cursor': 'pointer'});
		        	$('td', row).eq(5).css({ 'text-align': 'right'}).text(toRp_WithDecimal(data[5]));
		        	$('td', row).eq(1).css({ 'text-align': 'center'}).text(getTglINDO2(data[1].toString()));
		        	$('td', row).eq(3).css({ 'text-align': 'center'})
		        	$('td', row).eq(4).css({ 'text-align': 'center'}).text(convert_ke_bulan(data[4]));
		        	$('td', row).eq(7).css({ 'text-align': 'center'}).html('<input type="checkbox" class="chk_rek_unlock" onClick="checkclick(this, '+index+',\'unlock\')"/>\
		        															<input type="hidden" name="cek_unlock" id="cek_unlock_'+index+'" value="'+data[7]+'"/>\
		        															<input type="hidden" name="val_unlock" id="val_unlock_'+index+'" value="'+data[0]+'_'+data[2]+'"/>');
		        	
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
		            total = api
		                .column( 5 )
		                .data()
		                .reduce( function (a, b) {
		                    return intVal(a) + intVal(b);
		                }, 0 );
		 			$( api.column( 5 ).footer() ).html(toRp_WithDesimal(total.toString()));
		       	}
		    });
			$(".cover").hide();
		},
		error: function(){
			message_ok('error', 'Proses Gagal !');
		}
	});
}

function cek_uncek_all(e, chkclass, page){
    $('.'+chkclass+'_'+page).each(function(){ 
        this.checked = e.checked; 
    });

    if(e.checked){
        $('#frm_'+page+' input[name=cek_'+page+']').val('1');
        
        for (var i = 0; i < $('#frm_'+page+' input[name=val_'+page+']').length; i++) {
        	if (page=='draft') {
	        	array_draft.push($("#val_"+page+"_"+i+"").val()); 
	        }else if (page=='unlock'){
	        	array_unlock.push($("#val_"+page+"_"+i+"").val()); 
	        }
        }
        
    } else {
        $('#frm_'+page+' input[name=cek_'+page+']').val('0');
        for (var i = 0; i < $('#frm_'+page+' input[name=val_'+page+']').length; i++) {
        	if (page=='draft') {
	        	array_draft.splice(array_draft.indexOf($("#val_"+page+"_"+i+"").val()), 1); 
	        }else if (page=='unlock'){
	        	array_unlock.splice(array_unlock.indexOf($("#val_"+page+"_"+i+"").val()), 1);
	        }
        }
    }
};

function checkclick(e, urutan, tabel){
    if(e.checked){
        $("#cek_"+tabel+"_"+urutan+"").val('1');
        if (tabel=='draft') {
        	array_draft.push($("#val_"+tabel+"_"+urutan+"").val()); 
        }else if (tabel=='unlock'){
        	array_unlock.push($("#val_"+tabel+"_"+urutan+"").val()); 
        }
    } else {
        $("#cek_"+tabel+"_"+urutan+"").val('0');
        if (tabel=='draft') {
        	array_draft.splice(array_draft.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1); 
        }else if (tabel=='unlock'){
        	array_unlock.splice(array_unlock.indexOf($("#val_"+tabel+"_"+urutan+"").val()), 1);
        }
    }
}

$('#btn_setuju').click(function(){
	aksi = 'draft';
	setujui_spd();
});

$('#btn_unlock').click(function(){
	aksi = 'unlock';
	setujui_spd();
});

function setujui_spd(){
	$.ajax({
		type : "POST",
		headers : { "X-CSRFToken": csrf_token },
		url	: link_setuju_draft,
		data :{
			'array_draft':JSON.stringify(array_draft),
			'array_unlock':JSON.stringify(array_unlock),
			'aksi':aksi,
		},
		dataType: 'html',
		success: function(data){
			load_draft_spd();
			message_ok('success', data);
		},
		error: function(){
			message_ok('error', 'Proses Gagal !');
			$(".cover").hide();
		}
	});
}

