// JS untuk form laporan kasda
// JOEL 06 Mei 2021 GI
// ====================================================================

$('input[type=radio][name=pil_tanggal]').change(function() {
    if (this.value == 'pertgl') {
        $("div.input-group input#periode_pertgl").prop("disabled",false);
        $(".input-group-addon.periode_pertgl").bind('click');
        $("div.input-group input#periode_pertgl").css('background-color','#fff');

        $("div.input-group input#periode_tglawal").prop("disabled",true);
        $(".input-group-addon.periode_tglawal").unbind('click');
        $("div.input-group input#periode_tglawal").css('background-color','#eee');
        $("div.input-group input#periode_tglakhir").prop("disabled",true);
        $(".input-group-addon.periode_tglakhir").unbind('click');
        $("div.input-group input#periode_tglakhir").css('background-color','#eee');
    }
    else if (this.value == 'daritgl') {
        $("div.input-group input#periode_pertgl").prop("disabled",true);
        $(".input-group-addon.periode_pertgl").unbind('click');
        $("div.input-group input#periode_pertgl").css('background-color','#eee');

        $("div.input-group input#periode_tglawal").prop("disabled",false);
        $(".input-group-addon.periode_tglawal").bind('click');
        $("div.input-group input#periode_tglawal").css('background-color','#fff');
        $("div.input-group input#periode_tglakhir").prop("disabled",false);
        $(".input-group-addon.periode_tglakhir").bind('click');
        $("div.input-group input#periode_tglakhir").css('background-color','#fff');
    }
});

$('input[type=radio][name=is_skpd]').change(function() {
    if (this.value == 'allskpd') {
        $("#col_organisasi").css('display','None');
        $("#org_tampilkan").val('');
        $("#organisasi").val('');
        $("#organisasi").attr('alt','');
        
    } else if (this.value == 'oneskpd') {
        $("#col_organisasi").css('display','');
    }
});

function pil_jns_lapor(){
    var jenis = $(frm_lap).find("#jns_laporan").val();

    if ((jenis == 3) || (jenis == 5)){
        $("#col_sumberdana").css('display','');
        $("#col_periode").css('display','None');
    } else {
        $("#col_sumberdana").css('display','None');
        $("#col_periode").css('display','None');
        $('#sumdana option:eq(0)').prop('selected', 'selected');
        $('#periode option:eq(0)').prop('selected', 'selected');
    }

    if (jenis == 6) $("#col_periode").css('display','');
}

function eChangePejabat_lap(e){
    var pelyu = e.split("|");
    $(frm_lap).find("#id_pejabat").val(pelyu[0]);
    $(frm_lap).find("#nama_pejabat").val(pelyu[1]);
    $(frm_lap).find("#nip_pejabat").val(pelyu[2]); 
    $(frm_lap).find("#pangkat_pejabat").val(pelyu[3]);
}

function cetakLapBooksp2d(){
    var cekSKPD = $('input[name="is_skpd"]:checked').val();
    var skpd = $("#organisasi").val();

    if(frm_lap.attr('id') == "frm_lapBigBooksp2d") { espe2de = "SP2D"; } 
    else { espe2de = "Non Belanja"; }

    if(cekSKPD == "oneskpd" && skpd == ""){
        $.alertable.alert("Organisasi harus dipilih terlebih dahulu!"); return false;
    } else {
        $.ajax({
            type: frm_lap.attr('method'),
            url: frm_lap.attr('action'),
            data: frm_lap.serialize(),
            async: false,
            timeout: 10000,
            success: function(res){
                ShowIframeReport(res, "Laporan Buku Besar "+espe2de+" TA. "+Thn_log);
            }
        });
    }
}

function cetakLaporanBUD(){
    var jenis = $(frm_lap).find("#jns_laporan").val(); 
    var sumdana = $("#sumdana").val();

    if ((jenis == 3) || (jenis == 5)){
        if(sumdana == "0"){ $.alertable.alert("Sumber Dana harus dipilih terlebih dahulu!"); return false; }
        else { cetaks(); }
    } else { cetaks(); }

    function cetaks(){
        $.ajax({
            type: frm_lap.attr('method'),
            url: frm_lap.attr('action'),
            data: frm_lap.serialize(),
            async: false,
            timeout: 10000,
            success: function(res){
                ShowIframeReport(res, "Laporan Bendahara Umum Daerah (BUD) TA. "+Thn_log);
            }
        });
    }

}