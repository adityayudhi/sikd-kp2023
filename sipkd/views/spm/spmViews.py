from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import datetime, decimal
import pprint

def spm(request,jenis_spm):
    tahun   = tahun_log(request)
    skpd = set_organisasi(request)
    path = ''
    sipkd_perubahan = perubahan(request)
    arrBln  = []
    pejabat_pengguna_spm = ''
    pejabat_ppk_spm = ''
    kode_urusan       = request.POST.get('kdurusan','')
    kode_suburusan    = request.POST.get('kdsuburusan','')
    kode_organisasi   = request.POST.get('kdorganisasi','')
    kode_unit         = request.POST.get('kdunit','')
    is_khusus = False


    array_jenis_laporan = [{'kode':'1','nama':'Register SPM'},  
        {'kode':'2','nama':'Kartu Kendali SPM'}, 
        {'kode':'3','nama':'Register SP2D'},]
    arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]
    arrPeriod    = [{'kode':'0','nama':'-- Pilih Triwulan --'}, 
        {'kode':'1','nama':'Triwulan I'}, {'kode':'2','nama':'Triwulan II'},
        {'kode':'3','nama':'Triwulan III'}, {'kode':'4','nama':'Triwulan IV'}]

    aidi_bln = 1
    for i in monthList: # monthList -> array from config.py
        arrBln.append({'id':aidi_bln, 'kode':i, 'nama':monthList[i], 'tahun':tahun})
        aidi_bln += 1

    if skpd["kode"] == '': kode = 0
    else: kode = skpd["kode"]

    if jenis_spm=='ls_ppkd':
        path = 'ls_ppkd.html'
    elif jenis_spm=='ls_btl_ppkd_hutang':
        path = 'ls_btl_ppkd_hutang.html'
    elif jenis_spm=='up':
        path = 'up.html'
    elif jenis_spm=='gu':
        path = 'gu.html'
    elif jenis_spm=='tu':
        path = 'tu.html'
    elif jenis_spm=='gj':
        path = 'gj.html'
    elif jenis_spm=='ls':
        path = 'ls_barjas.html'
    elif jenis_spm=='gu_nihil':
        path = 'gu_nihil.html'
    elif jenis_spm=='non_angg':
        path = 'non_anggaran.html'
    elif jenis_spm=='tu_nihil':
        path = 'tu_nihil.html'
    elif jenis_spm=='persetujuan_skpd':
        path = 'persetujuan_skpd.html'
    elif jenis_spm=='persetujuan_ppkd':
        path = 'persetujuan_ppkd.html'
    elif jenis_spm=='laporanspm':
        path = 'laporan.html'

        if skpd:
            is_khusus = True
        else:
            is_khusus = False

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select * from master.PEJABAT_SKPKD where tahun= %s and jenissistem=2 ORDER BY id ASC", [tahun])
            pejabat_ppk_spm = dictfetchall(cursor)

        if kode_urusan != '' and kode_suburusan != '' and kode_organisasi !='':             
            with connection.cursor() as pejabat_ppk:
                pejabat_ppk.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
                    " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and jenissistem=%s ",
                    [tahun_log(request),kode_urusan,kode_suburusan,kode_organisasi,kode_unit,2])
                pejabat_pengguna_spm = dictfetchall(cursor)


    data = {'organisasi':skpd["skpd"],
            'kd_org':kode, 
            'ur_org':skpd["urai"],
            #'ppkd':get_PPKD(request)[0],
            'perubahan':str(sipkd_perubahan),
            'arrPerubahan':arrPerubahan,
            'arrPeriode':arrPeriod,
            'pengguna_anggaran_spm':pejabat_pengguna_spm,
            # 'ppk_spm':pejabat_ppk_spm,
            'jenis_laporan_spm':array_jenis_laporan,
            'jenis_spm':jenis_spm,
            'is_khusus':is_khusus,
        }
    return render(request, 'spm/'+path+'',data)

def render_pengguna_anggaran(request,jenis_spm):

    data = []

    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','') 
            kdunit               = request.POST.get('kdunit','')

            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT id,nama,nip,pangkat, jabatan from master.pejabat_skpd \
                    where tahun=%s and kodeurusan=%s and kodesuburusan=%s \
                    and kodeorganisasi=%s and kodeunit=%s",
                    [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
                data = dictfetchall(cursor)


    return HttpResponse(json.dumps(data), content_type="application/json")

def tbl_afektasi_spm(request,jenis_spm):
    return render(request,'spm/tabel/data_spm.html')

def generate_tbl_dasar_spd(request,jenis_spm):
    data_tbl_dasar_spd = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    jenis_spm = request.POST.get('jenis_spm', '')
    tanggal = tgl_short(request.POST.get('tgl_spp','')).split('-')
    bulan = int(arrMonth[monthList[tanggal[1]]])

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != ''  and kdunit != '':
        if jenis_spm=='LS_PPKD' or jenis_spm== 'NON ANGG':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT distinct(nospd),to_char(tglspd,'dd/mm/yyyy') as tglspd,\
                    jumlahspd,tglspd as urut FROM penatausahaan.fc_view_spd(%s,%s,%s,%s,%s,%s)\
                    where kodeprogram='0' and kodekegiatan ='0' and isskpd='1' and jumlahspd<>0 ",
                [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
                data_tbl_dasar_spd = dictfetchall(cursor)
        else:
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT distinct(nospd),to_char(tglspd,'dd/mm/yyyy') as tglspd,\
                    jumlahspd,tglspd as urut FROM penatausahaan.fc_view_spd(%s,%s,%s,%s,%s,%s)\
                    where kodeprogram='0' and kodekegiatan ='0' and isskpd='0'  order by tglspd ",
                [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
                data_tbl_dasar_spd = dictfetchall(cursor)                            
    data = {
        'data_tbl_dasar_spd':convert_tuple(data_tbl_dasar_spd),
    }
    
    return JsonResponse(data)

def generate_tbl_dasar_spd_to_spp(request,jenis_spm):
    data_tbl_dasar_spd_to_spp = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    jenis_spm_to_spp = request.POST.get('jenis_spm_to_spp', '')
    tanggal = tgl_short(request.POST.get('tgl_spp','')).split('-')
    bulan = int(arrMonth[monthList[tanggal[1]]])

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        if jenis_spm_to_spp=='LS_PPKD' or jenis_spm_to_spp=='NON ANGG':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT distinct(nospd),to_char(tglspd,'dd/mm/yyyy') as tglspd,\
                    jumlahspd,tglspd as urut FROM penatausahaan.fc_view_spd(%s,%s,%s,%s,%s,%s)\
                    where kodeprogram='0' and kodekegiatan ='0' and isskpd='1' and jumlahspd<>0 ",
                [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
                data_tbl_dasar_spd_to_spp = dictfetchall(cursor)
        else:
            with connections[tahun_log(request)].cursor() as cursor:                            
                cursor.execute("SELECT distinct(nospd),to_char(tglspd,'dd/mm/yyyy') as tglspd,\
                    jumlahspd,tglspd as urut FROM penatausahaan.fc_view_spd(%s,%s,%s,%s,%s,%s)\
                    where kodeprogram='0' and kodekegiatan ='0' and isskpd='0' order by tglspd ",
                [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
                data_tbl_dasar_spd_to_spp = dictfetchall(cursor)
    data = {
        'data_tbl_dasar_spd_to_spp':convert_tuple(data_tbl_dasar_spd_to_spp),
    }
    
    return JsonResponse(data)

def generate_rinci_spm(request,jenis_spm):
    data_rincian = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    org = request.POST.get('skpd', '').split('.')
    
    nospm = str(request.POST.get('no_spm',''))

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM penatausahaan.spm"
            " where tahun=%s and kodeurusan=%s and kodesuburusan =%s and kodeorganisasi=%s and kodeunit=%s and nospm=%s ",
            [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospm])
            data_rincian = dictfetchall(cursor)                            
    data = {
        'data_rincian':convert_tuple(data_rincian),
    }
    
    return JsonResponse(data)

def generate_rinci_spp(request,jenis_spm):
    data_rincian_spp = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    org = request.POST.get('skpd', '').split('.')
    
    nospp = str(request.POST.get('no_spp',''))
    jenis_spm = request.POST.get('jenisspm')                      

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM penatausahaan.spp"
            " where tahun=%s and kodeurusan=%s and kodesuburusan =%s and kodeorganisasi=%s and kodeunit=%s and nospp=%s ",
            [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospp])
            data_rincian_spp = dictfetchall(cursor) 

    # for x in data_rincian_spp:
    #     x['triwulan'] = 'triwulan cuy'
    data = {
        'data_rincian_spp':convert_tuple(data_rincian_spp),
    }
    
    return JsonResponse(data)
   

def generate_tbl_spm(request,jenis_spm):
    data_tbl_spm = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    org = request.POST.get('skpd', '').split('.')
    
    nospm = request.POST.get('nospm','')
    tanggal = request.POST.get('tgl_spm','')    
    kdbid = request.POST.get('kdbid','')    
    kdprog = request.POST.get('kdprog',0)    
    kdkeg = request.POST.get('kdkeg','')    
    jenis_spm = request.POST.get('jenis_spm','')  

    if kdprog == '':
        kdprog = 0

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        if jenis_spm=='LS_PPKD' or jenis_spm=='NON ANGG' or jenis_spm=='GJ' or jenis_spm=='GU' or jenis_spm=='UP' or jenis_spm=='TU' or jenis_spm=='GU_NIHIL' or jenis_spm=='TU_NIHIL':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute('SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa \
                    FROM penatausahaan.fc_view_spm_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospm,'',0,'0',0,tgl_to_db(tanggal),jenis_spm.upper()])
                data_tbl_spm = dictfetchall(cursor)                           
        else:
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute('SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa \
                    FROM penatausahaan.fc_view_spm_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospm,kdbid,kdprog,kdkeg,0,tgl_to_db(tanggal),jenis_spm.upper()])
                data_tbl_spm = dictfetchall(cursor)
    data = {
        'data_tbl_spm':convert_tuple(data_tbl_spm),
    }
    return JsonResponse(data)

def generate_afektasi_spm(request,jenis_spm):
    data_afektasi_spm = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    org = request.POST.get('skpd', '').split('.')

    nospp = request.POST.get('nospp','')
    tanggal = request.POST.get('tgl_spp','')
    kdbid = request.POST.get('kdbid','')    
    kdprog = request.POST.get('kdprog','')    
    kdkeg = request.POST.get('kdkeg','')    
    jenis_spm = request.POST.get('jenis_spm','')
    
    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        if jenis_spm=='LS_PPKD' or jenis_spm=='NON ANGG' or jenis_spm=='GJ' or jenis_spm=='GU' or jenis_spm=='UP' or jenis_spm=='TU' or jenis_spm=='GU_NIHIL' or jenis_spm=='TU_NIHIL':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute('SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa \
                    FROM penatausahaan.fc_view_spp_rincian_to_spm_rincian(%s,%s,%s,%s,%s,%s,%s,%s)',
                    [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospp,tgl_to_db(tanggal),jenis_spm.upper()])
                data_afektasi_spm = dictfetchall(cursor)                               
        else:
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute('SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa \
                    FROM penatausahaan.fc_view_spp_rincian_to_spm_rincian(%s,%s,%s,%s,%s,%s,%s,%s)',
                    [tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospp,tgl_to_db(tanggal),jenis_spm.upper()])
                data_afektasi_spm = dictfetchall(cursor)
    
    data = {
        'data_afektasi_spm':convert_tuple(data_afektasi_spm),
    }
    return JsonResponse(data)

def generate_rekening(request,jenis_spm):
    data_rincian = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')

    nospm = request.POST.get('no_spm','')
    arrJns  = [{'kode':'0','nama':'PPn'},{'kode':'1','nama':'PPh-21'},{'kode':'2','nama':'PPh-22'},
        {'kode':'3','nama':'PPh-23'},{'kode':'4','nama':'PPh-25'},{'kode':'5','nama':'PB-1'},{'kode':'6','nama':'IWP-1%'},
        {'kode':'7','nama':'IWP-8%'},{'kode':'8','nama':'Potongan'}]

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.rekeningpotongan, s.idbiling, s.ntpn, s.jenispotongan as kdpajak, " 
            " (select kdrek from master.mpajak mp where mp.koderekening=s.rekeningpotongan) as kdrek, "
                "(select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun and"
                " r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||lpad(r.kodeobjek::text,2,'0')||'.'||lpad(r.koderincianobjek::text,2,'0')||'.'||lpad(r.kodesubrincianobjek::text,3,'0')=s.rekeningpotongan), s.jenispotongan, s.jumlah as jumlahpotongan"
                " FROM penatausahaan.spmpotongan"
                " s where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan =%s and s.kodeorganisasi=%s and s.kodeunit=%s and s.nospm=%s",
                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospm])
            data_rincian = dictfetchall(cursor)                               
    
    ArrDT = {'potongan':data_rincian, 'jnsPot':arrJns}
    
    return render(request,'spm/tabel/data_spm_potongan.html',ArrDT)

def cek_spm(request,jenis_spm):
    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            org                  = request.POST.get('skpd', '').split('.')
            no_spm               = request.POST.get('no_spm')

            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT COUNT(nospm) FROM PENATAUSAHAAN.SPM \
                    where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') \
                    and kodeunit=%s and nospm=%s",
                    [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm])
                hasil = cursor.fetchone()
            return HttpResponse(hasil[0])

def cek_pejabat(request,jenis_spm):
    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')

            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT count(jabatan) from master.pejabat_skpd \
                    where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s \
                    and kodeunit=%s and jenissistem=2",
                    [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
                hasil = cursor.fetchone()
            return HttpResponse(hasil[0])

def spm_save(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'LS_PPKD',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"
                
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, no_spm])       

                for x in range(len(rekening1)):
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[0]+'.'+split_bidang[1]
                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,"
                        "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                        "KODERINCIANOBJEK,JUMLAH,TANGGAL)"
                        " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,\
                        kdbidang,0,0,kdakun,kdkelompok,kdjenis,kdobjek,\
                        kdrincian,jumlah_spm,tgl_draft])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_delete(request,jenis_spm):
    hasil = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    org = request.POST.get('skpd', '').split('.') 
    nospm = request.POST.get('nospm','')

    
    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
        try:
            with connections[tahun_log(request)].cursor() as spm:
                spm.execute("DELETE FROM penatausahaan.spm where TAHUN=%s and KODEURUSAN = %s \
                    and KODESUBURUSAN = %s and KODEORGANISASI = %s and KODEUNIT = %s and NOSPM = %s",
                    [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospm])
                # spm.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and kodeunit = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospm])
                # spm.execute("DELETE FROM penatausahaan.spmpotongan where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and kodeunit = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospm])
                hasil = "Data SPM dengan nomor "+nospm+" berhasil dihapus!"
        except Exception as e:
            hasil = "SPM sudah disetujui, tidak diperkenankan mengubah atau menghapus data"

    return HttpResponse(hasil)


def load_modal_spm(request,jenis_spm):
    gets = request.GET.get('skpd', None)
    hidden_pelaksana = ''

    if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
        aidi = gets.split('.')
    else:
        skpd = '0.0.0.0'
        aidi = skpd.split('.')    

    # ambil bendahara
    if jenis_spm=='ls_ppkd' or jenis_spm=='non_angg':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select * from master.pejabat_skpd where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0')  and kodeunit=%s and upper(jabatan) like %s and jenissistem=%s ",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%%PPKD%%',2])
            bendahara = dictfetchall(cursor)
    else:
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and jenissistem=%s ",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],2])
            bendahara = dictfetchall(cursor)
    

    if jenis_spm=='ls_ppkd' or jenis_spm=='non_angg':
        hidden_pelaksana = 'hidden'
    elif jenis_spm=='up' or jenis_spm=='gu' or jenis_spm=='tu' or jenis_spm=='gu_nihil' or jenis_spm=='tu_nihil':
        hidden_pelaksana = '' 

    data = {
        'bendahara' : bendahara,
        'jenis_spm' : jenis_spm,
        'hidden_pelaksana' : hidden_pelaksana
    }
    return render(request,'spm/modal/modal_laporan.html',data)

def cetaklaporanspm(request,jenis_spm):
    post    = request.POST
    lapParm = {}
    where0  = ""
    where1  = ""
    # jenis_spm = jenis_spm.upper()
    
    organisasi  = post.get('org').split('.')
    tanggal_spm = tgl_to_db(post.get('tanggal_spm')).split('/')
    # bulan = tanggal_spm[1]

    bulan = 1

    if jenis_spm=='ls_ppkd' or jenis_spm=='non_angg':
        lapParm['file']         = 'penatausahaan/spm/spmppkd.fr3'  
    elif jenis_spm=='up':  
        lapParm['file']         = 'penatausahaan/spm/spm.fr3'  
    else:
        lapParm['file']         = 'penatausahaan/spm/spm.fr3'

    lapParm['tahun']            = "'"+tahun_log(request)+"'"  
    lapParm['nomer']            = "'"+post.get('nomer_spm')+"'"  
    lapParm['report_type']      = 'pdf'
    lapParm['kodeurusan']       = organisasi[0]
    lapParm['kodesuburusan']    = organisasi[1]
    lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
    lapParm['kodeunit']   = "'"+organisasi[3]+"'"   

    lapParm['bulanSPP']         = int(bulan)    
    lapParm['bulanKegiatan']    = ''
    if jenis_spm=='ls_ppkd' or jenis_spm=='non_angg':
        lapParm['isppkd']       = 1        
    else:
        lapParm['isppkd']       = 0        
    lapParm['idpa']             = "'"+post.get('id_mengajukan')+"'"
    lapParm['idpa2']             = "'"+post.get('id_pelaksana')+"'"
    if jenis_spm=='up':
        lapParm['idpa1']        = "'"+post.get('id_pelaksana')+"'"



    return HttpResponse(laplink(request, lapParm))

def cetakspm(request):
    post    = request.POST
    lapSPM = {}
    
    jenis_laporan  = post.get('jenis_laporan')
    
    if jenis_laporan=='1':
        lapSPM['file']             = 'penatausahaan/spm/RegisterSPM.fr3'  
        lapSPM['idppk']            = post.get('id_ppk')

    elif jenis_laporan=='2':  
        kd_keg = post.get('kegiatan').split(".")
        kdbidang = kd_keg[0]+"."+kd_keg[1]
        kdprogram = kd_keg[2]
        kdkegiatan = kd_keg[3]+"."+kd_keg[4]
        kdsubkegiatan = kd_keg[5]

        lapSPM['file']             = 'penatausahaan/spm/kartukendalispm.fr3'  
        lapSPM['kodebidang']       = "'"+kdbidang+"'"
        lapSPM['kodeprogram']      = kdprogram
        lapSPM['kodekegiatan']     = "'"+kdkegiatan+"'"
        lapSPM['kodesubkegiatan']  = kdsubkegiatan
        lapSPM['kodekegiatan2']    = post.get('kegiatan')
        lapSPM['kegiatan']         = post.get('urai_keg')
        lapSPM['periode']          = post.get('bulan_ke')+' s/d '+post.get('bulan_sampai')
        
    elif jenis_laporan=='3':
        lapSPM['file']             = 'penatausahaan/spm/register_per_jenis.fr3'
        lapSPM['idppk']            = post.get('id_ppk')
        lapSPM['jenis']            = "'"+post.get('jenis_belanja')+"'"
        lapSPM['periode']          = post.get('bulan_ke')+' s/d '+post.get('bulan_sampai')

    lapSPM['tahun']            = "'"+tahun_log(request)+"'"  
    lapSPM['kodeurusan']       = post.get('kdurusan')
    lapSPM['kodesuburusan']    = post.get('kdsuburusan')
    lapSPM['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
    lapSPM['kodeunit']         = "'"+post.get('organisasi').split(".")[3]+"'" 
    lapSPM['kodeorganisasi2']  = post.get('organisasi')
    lapSPM['organisasi']       = post.get('urai_org')
    lapSPM['tglfrom']          = "'"+tgl_short(post.get('bulan_ke'))+"'"
    lapSPM['tglto']            = "'"+tgl_short(post.get('bulan_sampai'))+"'"
    lapSPM['idpa']             = post.get(str('id_pengguna'))
    lapSPM['tglcetak']         = tgl_short(post.get('tgl_cetak'))
    lapSPM['isppkd']           = post.get('ppkd_ceked')
    lapSPM['tglawal']          = "'"+tgl_short(post.get('bulan_ke'))+"'"
    lapSPM['tglakhir']         = "'"+tgl_short(post.get('bulan_sampai'))+"'"
    lapSPM['report_type']      = 'pdf'

    return HttpResponse(laplink(request, lapSPM))

def listpersetujuan_spm(request):

    arrBulan_SPM    = [{'kode':'1','bulan':'JANUARI'}, 
    {'kode':'2','bulan':'FEBRUARI'}, {'kode':'3','bulan':'MARET'},
    {'kode':'4','bulan':'APRIL'}, {'kode':'5','bulan':'MEI'},
    {'kode':'6','bulan':'JUNI'}, {'kode':'7','bulan':'JULI'},
    {'kode':'8','bulan':'AGUSTUS'}, {'kode':'9','bulan':'SEPTEMBER'},
    {'kode':'10','bulan':'OKTOBER'}, {'kode':'11','bulan':'NOVEMBER'}, {'kode':'12','bulan':'DESEMBER'}]

    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None) 
        isppkd = request.POST.get('isppkd', None)  
        get_bulan = request.POST.get('get_bulan', None)

        if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')        

        total_spm = 0
        total_setuju = 0

        if(isppkd=='1'):
            jenis = " and s.jenisspm in ('LS_PPKD','NON ANGG')"            
        else:
            jenis = " and s.jenisspm not in ('LS_PPKD','NON ANGG')"

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select s.nospm,s.tanggal,s.tanggal as tglspm, kodeunit, "
                "s.statuskeperluan as keperluan, (select  case when  sum (jumlah) is null then 0 else  sum (jumlah) end as jumlah from penatausahaan.spmrincian "
                "sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and "
                "sr.kodeorganisasi=s.kodeorganisasi and sr.nospm=s.nospm ) as jumlah, s.kodeurusan,s.kodesuburusan, "
                "s.kodeorganisasi,s.jenisspm,s.locked,0 as cek from penatausahaan.spm s "
                "where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s "
                "and s.kodeorganisasi=%s and s.kodeunit=%s "+jenis+" and locked='T' "
                "order by s.tanggal,s.nospm",[tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3]])
            list_draft_spm = dictfetchall(cursor)  

            cursor.execute("select s.nospm,s.tanggal as tglspm, s.statuskeperluan as keperluan, kodeunit, "
                "(select  case when  sum (jumlah) is null then 0 else  sum (jumlah) end as jumlah from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospm=s.nospm ) as jumlah, "
                "s.jenisspm,s.locked,0 as cek, COALESCE((select nosp2d from penatausahaan.sp2d sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospm=s.nospm),'-') as nosp2d, "
                "COALESCE((select to_char(sr.tanggal, 'DD/MM/YYYY') from penatausahaan.sp2d sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospm=s.nospm),'-') as tglsp2d from penatausahaan.spm s "
                "where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s and s.kodeorganisasi=%s and s.kodeunit=%s "
                ""+jenis+" and locked='Y' and  extract (month from s.tanggal)=%s "
                "order by s.tanggal,s.nospm",[tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3], get_bulan])
            list_setuju_spm = dictfetchall(cursor)   

        objek = []
        for x in list_setuju_spm:
            total_setuju += x['jumlah']
            objek.append({'nospm':x['nospm'],'tglspp':x['tglspm'], 'kodeunit':x['kodeunit'], 'nosp2d':x['nosp2d'],
                'tglsp2d':x['tglsp2d'], 'keperluan':x['keperluan'], 'jenisspm':x['jenisspm'],})
        
        for total in list_draft_spm:
            total_spm += total['jumlah']

        for total in list_setuju_spm:
            total_setuju += total['jumlah']

        if total_spm == 0:
            total_spm = '0,00'
        if total_setuju == 0:
            total_setuju = '0,00'

        data = {'get_bulan':get_bulan,'list_draft_spm' : ArrayFormater(list_draft_spm), 'isppkd' : isppkd,
            'list_setuju_spm' : ArrayFormater(list_setuju_spm), 'arrBulan_SPM' : arrBulan_SPM, 
            'total_spm' : total_spm, 'total_setuju' : total_setuju}

        return render(request, 'spm/tabel/list_persetujuanspm.html', data)

    else:
        return redirect('sipkd:index')

def setuju_draft_spm(request):
    hasil = ''
    lock = request.GET.get('act')

    # print(request.GET)
    # print(request.POST)
    
    if request.method == 'POST':
        tahun = tahun_log(request)
        gets = request.POST.get('skpd', '')      
        kdunit = request.POST.get('kdunit')

        if(lock == 'lock'):
            locked = 'Y'
            chkspm = request.POST.getlist('cek_draft')
            nomor = request.POST.getlist('nomer_draft')
        else:
            locked = 'T'  
            chkspm = request.POST.getlist('cek_spm')
            nomor = request.POST.getlist('nomer_spm')

        if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.') 
        
        for i in range(0,len(chkspm)):
            cek = chkspm[i]            
            nomer_spm = nomor[i]
            spm = cek+':'+nomer_spm  
            split_spm = spm.split(':')
           
            if(split_spm[0]=='1'):
                nospm = split_spm[1] 
        
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.spm set locked=%s where tahun=%s"
                        " and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and KODEUNIT=%s"
                        " and NOSPM in (%s)",[locked,tahun,aidi[0],aidi[1],aidi[2],aidi[3],nospm])
                    
                if(locked == "Y"):
                    # hasil = "NO SPM "+nospm+" Telah di Setujui"
                    hasil = "NO SPM Telah di Setujui"
                else:
                    # hasil = "NO SPM "+nospm+" Telah di Unlock"
                    hasil = "NO SPM Telah di Unlock"

    return HttpResponse(hasil)





