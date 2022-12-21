function buka_modal(){
	$.ajax({
            url: '{% url "apbd:get_organisasi" %}',
            data: {
              'username': 's'
            },
            dataType: 'json',
            success: function (data) {
                alert(data['hasil'])
                //$("#message").html(data['is_taken']);
              // if (data.is_taken) {
              //   alert("A user with this username already exists.");
              // }
            },
            error: function(data){
            	alert('GAGAL MANINGGGG');
            }
          });
}