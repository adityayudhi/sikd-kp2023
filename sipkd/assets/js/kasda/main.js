var isSimpan  = true;
var hslcek_x;

// limit word
function limitWords(textToLimit, wordLimit){
  var finalText = "";
  var text2 = textToLimit.replace(/\s+/g, ' ');
  var text3 = text2.split(' ');
  var numberOfWords = text3.length;
  var i=0;

  if(numberOfWords > wordLimit) {
    for(i=0; i< wordLimit; i++)
      finalText = finalText+" "+ text3[i]+" ";
    return finalText+"…";

  } else {return textToLimit;}
}

function autoNoBkuKas(){
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: url_kasda_autonokas, ////dari base/main.html
        data :{},
        dataType: 'json',
        success: function(msg){
          $("#no_bukukas").val(msg['hasilnya']);
        }
    });
}

function isTanggalValid(tglawal, tglakhir){
    var cintaku = cekTanggal(tglawal, tglakhir); //// dari main-modul.js
    if(!cintaku){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); 
        return false;
    }
}

function cekNoBukti(cekdata){
    if(cekdata){
        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            type: "POST",
            url: url_kasda_nobukti, ////dari base/main.html
            data: {kode:cekdata},
            dataType: 'json',
            success: function(msg){ hslcek_x = msg['hasilnya']; }
        });
    }
    return hslcek_x;
}

function clearForm_KASDA(asal){
    isSimpan = true;
    if(isSimpan){ 
        $("#no_bukukas").val('');
        autoNoBkuKas(); 
    }
    $('input[name="aksi"]').val(isSimpan);

    function klir_text(){
        $("#no_bukukas_xx").val('')
        $("#no_bukti").val('');
        $("#no_bukti_xx").val('');
        $("#tgl_bukti").val(DateNowInd());
        $("#tgl_transaksi").val(DateNowInd());
        $("#sumber_dana").val(0);
        $("#deskripsi").val('');
    }

    switch(asal.toLowerCase()) { 
        case "sts":
        case "contrakemarin":
        case "awal":
            klir_text();
            break;

        case "nota":
            klir_text();
            break;
            
        case "contra":
            if($('#org_tampilkan').val() != ""){
                $('#jenissp2d').val('UP');
                $('#sp2d-up').addClass("btn-success");
            } else {
                $('#jenissp2d').val('');
                $('#sp2d-up').removeClass("btn-success");
            }
            
            $('#sp2d-gu').removeClass("btn-success");
            $('#sp2d-tu').removeClass("btn-success");
            $('#sp2d-ls').removeClass("btn-success");
            $("#btn_next").hide();
            $("#btn_back").hide();
            $("#div_next").hide();
            $("#div_back").hide();
            klir_text();
            break;

        case "pindahbuku":
            klir_text();
            $("#sumber_dana_from").val(0);
            $("#sumber_dana_to").val(0); 
            $("#jml_transaksi").val('0,00');
            break;
    }

    if(asal.toLowerCase() != "pindahbuku"){ Afektasi_kasda_tabel(asal); }
}

function modal_KASDA(e,modal){
    var url_load  = "";
    var loadModal = "";
    var linkLoad  = $(e).attr('alt');
    var kd_skpd   = $('#organisasi').val();

    switch(modal) {
        case 'kasda_mdl_afektasi':  
            if(kd_skpd==''){$.alertable.alert("Pilih Organisasi Terlebih Dahulu !!!"); return false;}
            var rowid = $(e).attr('rowid');
            loadModal = "Cari Kode Rekening TA. "+Thn_log;         
            url_load  = linkLoad+"?i="+rowid+"&d="+kd_skpd;         
            break;

        case 'list_kasda':  
            loadModal = "Cari Transaksi TA. "+Thn_log;    
            url_load  = linkLoad;         
            break;
    }

    document.getElementById("ReportModalLabel").innerHTML = loadModal;
    $("#ReportModal").modal();
    $(".modal-body-report").load(url_load);
    $(".modal-search").css('width', '800px');
}

// FUNGSI SIMPAN KASDA
$("#btn_simpan").click(function(){

  switch(form_kasda){
    case "frmkasda_sts":
      SaveKASDA_sts();
      break;

    case "frmkasda_contrakemarin":
      SaveKASDA_contrakemarin();
      break;

    case "frmkasda_pindahbuku":
      SaveKASDA_pindahbuku();
      break;

    case "frmkasda_saldo":
      SaveKASDA_saldo();
      break;

    case "frmkasda_nota":
      SaveKASDA_nota();
      break;
    
    case "frmkasda_contra":
      SaveKASDA_contra();
      break;

	case "sp2d":
      SaveSP2D();
      break;  }
  
});

// FUNGSI DELETE KASDA
$("#btn_hapus").click(function(){
  switch(form_kasda){
    case "frmkasda_sts":
      deleteKASDA_sts();
      break;

    case "frmkasda_contrakemarin":
      deleteKASDA_contrakemarin();
      break;

    case "frmkasda_pindahbuku":
      deleteKASDA_pindahbuku();
      break;

    case "frmkasda_saldo":
      deleteKASDA_saldo();
      break;
    
    case "frmkasda_nota":
        deleteKASDA_nota();
        break;
      
    case "frmkasda_contra":
        deleteKASDA_contra();
        break;
  }
  
});

function Afektasi_kasda_tabel(asal){
    var skpd = $("#organisasi").val();
    var nobkas  = $("#no_bukukas").val();
    var no_bukti  = $("#no_bukti").val();

    if (asal.toLowerCase() == 'contra') {
        var jenissp2d  = $("#jenissp2d").val();
        var aksi = $('input[name="aksi"]').val();
        ambilRekeningLS='';
    }else{
        var jenissp2d  = '';
        var aksi = '';
        ambilRekeningLS='';
    }

    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_tabelAfektasi_kasda,
        data: {asal:asal, skpd:skpd, nobkas:nobkas, no_bukti:no_bukti, jenissp2d:jenissp2d, aksi:aksi, ambilRekeningLS:ambilRekeningLS},
        dataType: "html",
        beforeSend: function(){ $(".cover").show(); },
        success: function(response){
            $('#dataTable_afektasi_html').html(response);
            $(".cover").hide();
        }
    });
}

function loadData_KASDA(asal){
    var skpd = $("#organisasi").val();
    var nobkas  = $("#no_bukukas").val();
    var no_bukti  = $("#no_bukti_xx").val();

    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        type: "POST",
        url: link_load_data_kasda,
        data: {skpd:skpd, nobkas:nobkas, no_bukti:no_bukti},
        async: false,
        dataType: "json",
        success: function (hsl) {  
            isSimpan = false;
            $('input[name="aksi"]').val(isSimpan);
            $("#no_bukukas_xx").val(hsl['NOBUKAS_X']);
            $("#tgl_bukti").val(hsl['TGLBUKTI']);
            $("#tgl_transaksi").val(hsl['TGLTRANS']);
            $("#sumber_dana").val(hsl['KDSUMDAN']);
            $("#deskripsi").val(hsl['DESKRIPSI']);

            if(asal.toLowerCase()=='contra'){
                $("#jenissp2d").val(hsl['JENISSP2D']);
                $('#sp2d-up').removeClass("btn-success");
                $('#sp2d-gu').removeClass("btn-success");
                $('#sp2d-tu').removeClass("btn-success");
                $('#sp2d-ls').removeClass("btn-success");
                if(hsl['JENISSP2D'] == 'UP'){
                    $('#sp2d-up').addClass("btn-success");
                }else if(hsl['JENISSP2D'] == 'GU'){
                    $('#sp2d-gu').addClass("btn-success");
                }else if(hsl['JENISSP2D'] == 'TU'){
                    $('#sp2d-tu').addClass("btn-success");
                }else if(hsl['JENISSP2D'] == 'LS'){
                    $('#sp2d-ls').addClass("btn-success");
                    $('#btn_simpan').attr("disabled", true);
                    $('#btn_next').show();
                    $('#div_next').show();
                    $('#btn_back').hide();
                    $('#div_back').hide();
                }
            }

            if(asal.toLowerCase() == "pindahbuku"){
                $("#sumber_dana_from").val(hsl['KDSUMDAN_FR']);
                $("#sumber_dana_to").val(hsl['KDSUMDAN_TO']);
                $("#jml_transaksi").val(toRp_WithDecimal(hsl['JML_TRANSAKSI']));
            } else {
                Afektasi_kasda_tabel(asal);
            }

            if(hsl['LOCKED'] == 'Y'){ 
                $.alertable.alert(hsl['PESAN']); 
                loadPertama('btn_simpan','-1');
                loadPertama('btn_hapus','-1');
            } else {
                loadPertama('btn_simpan','1');
                loadPertama('btn_hapus','1');
            }
        }
    });
}

function OnFokus_transaksi(e){
    $(e).val(toAngkaDec($(e).val()));
}

function OnBlur_transaksi(e){
    $(e).val(toRp_WithDecimal($(e).val()));
}

// KASDA STS ==================================================
// ============================================================
function SaveKASDA_sts(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana = $("#sumber_dana").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var kodereken = $('input[name="cut_kdrek"]').val();
    var ceknobukti = cekNoBukti(no_bukti);

    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor STS Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor STS Sudah digunakan!"); return false; }
        }
    }

    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor STS masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana == "0"){
        $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(kodereken == ""){
        $.alertable.alert("Data Rekening belum ada yang dipilih!"); return false;
    } else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else if(!cekPenerimaanPengeluaran()){
    $.alertable.alert("Data Penerimaan ataupun Pengeluaran belum diisi !"); return false;
    } else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('STS');
                    }
                    $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}

function deleteKASDA_sts(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data STS Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('sts'); } 
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }

}

// KASDA CONTRAKEMARIN ==============================================
// ==================================================================
function SaveKASDA_contrakemarin(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana = $("#sumber_dana").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var kodereken = $('input[name="cut_kdrek"]').val();
    var ceknobukti = cekNoBukti(no_bukti);

    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
        }
    }

    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor Bukti masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana == "0"){
        $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(kodereken == ""){
        $.alertable.alert("Data Rekening belum ada yang dipilih!"); return false;
    } else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else if(!cekPenerimaanPengeluaran()){
    $.alertable.alert("Data Penerimaan ataupun Pengeluaran belum diisi !"); return false;
    } else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('CONTRAKEMARIN');
                    }
                    $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}

function deleteKASDA_contrakemarin(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data Transaksi Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('contrakemarin'); } 
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }
}

// KASDA PINDAH BUKU =========================================================
// ===========================================================================
function SaveKASDA_pindahbuku(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana_from = $("#sumber_dana_from").val();
    var sumr_dana_to = $("#sumber_dana_to").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var jml_transaksi = $('#jml_transaksi').val();
    var ceknobukti = cekNoBukti(no_bukti);

    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
        }
    }
    
    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor Bukti masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana_from == "0"){
        $.alertable.alert("Sumber Dana Asal harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana_to == "0"){
        $.alertable.alert("Sumber Dana Tujuan harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(jml_transaksi == "0,00"){
        $.alertable.alert("Jumlah Transaksi masih kosong!"); return false;
    } else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else {  
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('PINDAHBUKU');
                    }
                    $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}

function deleteKASDA_pindahbuku(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data Transaksi Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('pindahbuku'); }
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }
}

//============= SALDO AWAL================
function SaveKASDA_saldo(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana = $("#sumber_dana").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var kodereken = $('input[name="cut_kdrek"]').val();
    var ceknobukti = cekNoBukti(no_bukti);

    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
        }
    }

    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor Bukti masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana == "0"){
        $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(kodereken == ""){
        $.alertable.alert("Data Rekening belum ada yang dipilih!"); return false;
    }else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else if(!cekPenerimaanPengeluaran()){
        $.alertable.alert("Data Penerimaan ataupun Pengeluaran belum diisi !"); return false;
    }
    else {
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('AWAL');
                    }
                    $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}
function deleteKASDA_saldo(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data Bukti Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('awal'); } 
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }

}

// KASDA NOTA ==============================================
// ==================================================================
function cekPenerimaanPengeluaran(){
    var status = true;
    $('#dataTable_afektasi > tbody  > tr').each(function(index, tr) { 
        var uraian = $(this).find('td:nth-child(3)').find('span').text();
        var penerimaan = $(this).find('td:nth-child(4)').find('input').val();
        var pengeluaran = $(this).find('td:nth-child(5)').find('input').val();
        if (uraian!='' && penerimaan=='0,00' && pengeluaran=='0,00') {
            if (penerimaan == '0,00'){
                $(this).find('td:nth-child(4)').find('input').focus();
            }else if(pengeluaran =='0,00'){
                $(this).find('td:nth-child(5)').find('input').focus();
            }
            status = false
        }
     });
     return status;
}
function SaveKASDA_nota(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana = $("#sumber_dana").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var kodereken = $('input[name="cut_kdrek"]').val();
    var ceknobukti = cekNoBukti(no_bukti);

    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
        }
    }

    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor Bukti masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana == "0"){
        $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(kodereken == ""){
        $.alertable.alert("Data Rekening belum ada yang dipilih!"); return false;
    } else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else if(!cekPenerimaanPengeluaran()){
        $.alertable.alert("Data Penerimaan ataupun Pengeluaran belum diisi !"); return false;
    }else{
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('NOTA');
                    }
                    $.alertable.alert(x['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}

function deleteKASDA_nota(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data Transaksi Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('nota'); } 
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }

}

// KASDA TAHUN BERJALAN==============================================
// ==================================================================

function selectJenisSP2D(jenis){
    var organisasi = $('#organisasi').val();
    if(organisasi == ""){
        $.alertable.alert("Organisasi Belum dipilih!"); return false;
    }else{
        $('#jenissp2d').val(jenis);
        $('#sp2d-up').removeClass("btn-success");
        $('#sp2d-gu').removeClass("btn-success");
        $('#sp2d-tu').removeClass("btn-success");
        $('#sp2d-ls').removeClass("btn-success");
        if (jenis=='UP' || jenis=='GU' || jenis=='TU') {
            if(jenis=='UP'){
                $('#sp2d-up').addClass("btn-success");
            }else if(jenis=='GU'){
                $('#sp2d-gu').addClass("btn-success");
            }else if(jenis=='TU'){
                $('#sp2d-tu').addClass("btn-success");
            }
            Afektasi_kasda_tabel('CONTRA');
            $("#btn_next").hide();
            $("#div_next").hide();
            $("#btn_back").hide();
            $("#div_back").hide();
            $("#btn_simpan").attr("disabled", false);
        }else if(jenis == 'LS'){
            Afektasi_kasda_tabel('CONTRA');
            $('#sp2d-ls').addClass("btn-success");
            $("#btn_next").show();
            $("#div_next").show();
            $("#btn_back").hide();
            $("#div_back").hide();
            $("#btn_simpan").attr("disabled", true);
        }
    }
}

function nextRekening_LS(){

    var skpd = $("#organisasi").val();
    var nobkas  = $("#no_bukukas").val();
    var no_bukti  = $("#no_bukti").val();
    var jenissp2d  = $("#jenissp2d").val();
    var aksi = $('input[name="aksi"]').val();
    var CEHK = [];
    var asal = "contra";
    var ambilRekeningLS = 'true';

    $(".kegiatan:checked").each(function(){ CEHK.push($(this).attr("value")); });
    // console.log(skpd);
    // console.log(CEHK);

    if(CEHK.length < 1) {
        $.alertable.alert("Anda belum memilih kegiatan!");
        return false;
    }else if(CEHK.length > 1){
        $.alertable.alert("Anda tidak bisa memilih lebih dari satu kegiatan!");
        return false;
    } else {     
        $.ajax({
            headers: { "X-CSRFToken": csrf_token },
            type: "POST",
            url: link_tabelAfektasi_kasda,
            data: {asal:asal, skpd:skpd, nobkas:nobkas, no_bukti:no_bukti, jenissp2d:jenissp2d, aksi:aksi, arr:CEHK[0], ambilRekeningLS:ambilRekeningLS, },
            dataType: "html",
            beforeSend: function(){ $(".cover").show(); },
            success: function(response){
                $('#dataTable_afektasi_html').html(response);
                $(".cover").hide();
                ambilRekeningLS='';
                $('#btn_next').hide();
                $('#div_next').hide();
                $('#btn_back').show();
                $('#div_back').show();
                $("#btn_simpan").attr("disabled", false);
            }
        });
    }
}

$("#btn_back").on("click", function(){
    selectJenisSP2D("LS");
});

function SaveKASDA_contra(){
    var frm     = $("#myForm");
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas").val();
    var skpd    = $("#organisasi").val();
    var no_bukti  = $("#no_bukti").val();
    var no_buktiXX  = $("#no_bukti_xx").val();
    var tgl_bukti = $("#tgl_bukti").val();
    var sumr_dana = $("#sumber_dana").val();
    var tgl_transaksi = $("#tgl_transaksi").val();
    var deskripsi = $("#deskripsi").val();
    var kodereken = $('input[name="cut_kdrek"]').val();
    var jenissp2d = $('#jenissp2d').val();
    var ceknobukti = cekNoBukti(no_bukti);
    var CEHK = [];
    if (jenissp2d == "LS"){
        $(".kegiatan:checked").each(function(){ CEHK.push($(this).attr("value")); });
    }
    
    if(aksi == "true"){
        if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
    } else {
        if(no_bukti != no_buktiXX){
          if(ceknobukti > 0){ $.alertable.alert("Nomor Bukti Sudah digunakan!"); return false; }
        }
    }

    if(nobkas == ""){
        $.alertable.alert("Nomor Buku Kas masih kosong!"); return false;
    } else if(no_bukti == ""){
        $.alertable.alert("Nomor Bukti masih kosong!"); return false;
    } else if(skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else if(sumr_dana == "0"){
        $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false;
    } else if(deskripsi == ""){
        $.alertable.alert("Deskripsi masih kosong!"); return false;
    } else if(!cekTanggal(tgl_bukti, tgl_transaksi)){
        $.alertable.alert("Tanggal Transaksi tidak boleh lebih kecil dari Tanggal Pindah Buku !"); return false;
    } else if(jenissp2d == ""){
        $.alertable.alert("Jenis SP2D belum dipilih !"); return false;
    } else if(jenissp2d == "LS" && CEHK.length < 1){
        $.alertable.alert("Kegiatan atau Rekening belum dipilih !"); return false;
    }else{
        $.alertable.confirm('Anda yakin akan menyimpan data?').then(function() {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                dataType:"json",
                success: function(x){
                    if(x['issimpan'] >= 1){
                        $("#no_bukti_xx").val(no_bukti);
                        isSimpan = false;
                        $('input[name="aksi"]').val(isSimpan);
                        loadData_KASDA('contra');
                        
                    }
                    $.alertable.alert(x['pesan']);
                    if ($('#jenissp2d').val()=='LS') {
                        $('#btn_simpan').attr("disabled", true);
                        $('#btn_next').show();
                        $('#div_next').show();
                        $('#btn_back').hide();
                        $('#div_back').hide();
                    } 
                }
            });
        }, function() {
            message_ok('error', 'Simpan data Buku Kas : '+nobkas+' dibatalkan!');
        });
    }
}

function deleteKASDA_contra(){
    var aksi    = $("#aksi").val();
    var nobkas  = $("#no_bukukas_xx").val();
    var no_bukti  = $("#no_bukti_xx").val();

    if(aksi == "true"){
        $.alertable.alert("Data Transaksi belum dipilih!"); return false;
    } else {
        $.alertable.confirm('Apakah anda Yakin Untuk Menghapus Data Transaksi Dengan Nomor Buku Kas '+nobkas+' ?').then(function(){
            $.ajax({
                headers: { "X-CSRFToken": csrf_token },
                type: 'POST',
                url: $("#myForm").attr('alt'),
                data: {aksi:aksi, nobkas:nobkas, nobuk:no_bukti},
                dataType:"json",
                success: function(z){
                    if(z['issimpan'] == 0){ clearForm_KASDA('contra'); } 
                    $.alertable.alert(z['pesan']);
                }
            });
        }, function() {
            message_ok('error', 'Hapus data '+nobkas+' dibatalkan!');
        });
    }

}