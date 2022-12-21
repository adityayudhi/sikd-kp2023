var array_rekening = [];
$('#btn_simpan').click(function(){
  var skpd = $("#organisasi").val();
    if(skpd != 0){
      save_data_spjskpd() 
    }else{
      $.alertable.alert("Organisasi Belum Dipilih..!!");
    }

});

function org_spjskpd_change(val){        
  var urls     = $("#url_tabel_data_spjskpd").val();
  var Cookie   = getCookie("Data_SPJSKPD"); 
  $.ajax({
      type: "GET",
      url: urls,
      data: {id:val,jenis_data:$('#jenis_data_spjskpd').val()},
      async: false,
      dataType: "html",
      timeout: 10000,
      beforeSend: function() {
        $(".cover").show();
      },
      success: function(response){      
        $('#tabel-data-spjskpd').html(response);
        $(".cover").hide();
      }
  });

  if(Cookie != ''){
    removeCookie("Data_SPJSKPD");
  }
}

function save_data_spjskpd(){        

  var temp=[];
  var temp2=[];
  if($( '#organisasi').val() == 0){
    $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
  } else{ 
    $.alertable.confirm("Anda yakin akan menyimpan data LRA ?").then(function() { 

      $.each($('.nomor_rekening'),function(e,obj){
        temp.push($(this).attr('data-value'))
      })
      $.each($('.arrJml'),function(e,obj){
        temp2.push(toAngka($(this).val()))
      })


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
            'data_rekening':JSON.stringify(temp), 
            'jumlah_data':JSON.stringify(temp2), 
            'total_jumlah':toAngka($('#total_jumlah').text()),
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