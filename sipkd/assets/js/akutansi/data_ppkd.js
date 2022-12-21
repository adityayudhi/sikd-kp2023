var array_rekening = [];
$('#btn_simpan').click(function(){
  var skpd = $("#organisasi").val();
    if(skpd != 0){
      save_data_ppkd() 
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }

});

function org_ppkd_change(val){        
  var urls     = $("#url_tabel_data_ppkd").val();
  $.ajax({
      type: "GET",
      url: urls,
      data: {id:val,jenis_data:$('#jenis_data_ppkd').val()},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){      
        $('#tabel-data-ppkd').html(response);
        $(".cover").hide();
      }
  });
}

function save_data_ppkd(){         

  if($( '#organisasi').val() == 0){
    $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else{ 
    $.alertable.confirm("Anda yakin akan menyimpan data LRA ?").then(function() {       
      $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        url: link_simpan_data_spjskpd,
        data: 
          {
            'jenis_data':$('#jenis_data_spjskpd').val(),
            'kdurusan':$('#organisasi').val().split('.')[0],
            'kdsuburusan':$('#organisasi').val().split('.')[1],
            'kdorganisasi':$('#organisasi').val().split('.')[2],
            'data_rekening':$('#data_rekening').val(),
            'jumlah_data':$('#jumlah_data_spjskpd').val(),
          },
          success: function(data){
            message_ok("success",data);
            }                      
        });
    }, function() {
      message_ok('error', 'Anda telah membatalkan penghapusan data.');          
    });
  }      
}