from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
from support.support_report import *
from datetime import datetime
import decimal

def akuntansi(request,jenis_akuntansi):
    tahun   = tahun_log(request)
    path = ''
    skpd = set_organisasi(request)
    sipkd_perubahan = perubahan(request)
    pejabat_pengguna_anggaran = ''
    array_jenis_laporan = ''
    array_jenis_laporan2 = ''
    array_bulanan = ''
    judul = ''
    kode_urusan             = request.POST.get('kdurusan','')
    kode_suburusan          = request.POST.get('kdsuburusan','')
    kode_organisasi         = request.POST.get('kdorganisasi','')
    array_bulan    = [
    {'kode':'0','bulan':'-- Pilih Bulan --'},{'kode':'1','bulan':'JANUARI'},{'kode':'2','bulan':'FEBUARI'},{'kode':'3','bulan':'MARET'},
    {'kode':'4','bulan':'APRIL'},{'kode':'5','bulan':'MEI'},{'kode':'6','bulan':'JUNI'},{'kode':'7','bulan':'JULI'},{'kode':'8','bulan':'AGUSTUS'}, 
    {'kode':'9','bulan':'SEPTEMBER'},{'kode':'10','bulan':'OKTOBER'},{'kode':'11','bulan':'NOVEMBER'},{'kode':'12','bulan':'DESEMBER'},
    ]
    array_perubahan = [
    {'kode':'0','nama':'-- Pilih Perubahan --'},{'kode':'1','nama':'Sebelum Perubahan'},{'kode':'2','nama':'Sesudah Perubahan'},
    ]
    array_periode    = [
    {'kode':'0','nama':'-- Pilih Triwulan --'},{'kode':'1','nama':'Triwulan I'},{'kode':'2','nama':'Triwulan II'},
    {'kode':'3','nama':'Triwulan III'},{'kode':'4','nama':'Triwulan IV'}
    ]
    array_spj = [
    {'kode':'0','nama':'-- Pilih Jenis SPJ --'},{'kode':'1','nama':'Semua (UP-GU / TU)'},{'kode':'2','nama':'UP-GU'},{'kode':'3','nama':'TU'}
    ]

    if skpd["kode"] == '': 
        kode = 0
    else: 
        kode = skpd["kode"]

    if kode_urusan != '' and kode_suburusan != '' and kode_organisasi !='':             
        with connection.cursor() as pejabat_ppk:
            pejabat_ppk.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpkd where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and upper(jabatan) like %s and jenissistem=%s ",
                [tahun_log(request),kode_urusan,kode_suburusan,kode_organisasi,'%BENDAHARA UMUM%',2])
            pejabat_pengguna_anggaran = dictfetchall(cursor)

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT kodesumberdana, urai from penatausahaan.sumberdanarekening ORDER BY kodesumberdana")
        master_dana = dictfetchall(cursor)

    if jenis_akuntansi=='datalrappkd':
        path = 'data_lra.html'
    elif jenis_akuntansi=='dataloppkd':
        path = 'data_lo.html'
    elif jenis_akuntansi=='datalpeppkd':
        path = 'data_lpe.html'
    elif jenis_akuntansi=='dataaruskas':
        path = 'data_arus_kas.html'
    elif jenis_akuntansi=='daftarisianlampiran':
        path = 'lampiran_perda.html'
    elif jenis_akuntansi=='laporanverifikasi':
        array_jenis_laporan = [{'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'Kartu Pengawas - Uang Persediaan'},  
        {'kode':'2','nama':'Kartu Pengawas - Tambahan Uang Persediaan'},{'kode':'3','nama':'Kartu Pengawas - Realisasi Anggaran'}, 
        {'kode':'4','nama':'Register SP2D'},{'kode':'5','nama':'Register SP2D Rincian'},{'kode':'6','nama':'Register SPJ'},{'kode':'7','nama':'Rekap Sisa SP2D TU Yang Belum di LPJ-kan'}, 
        {'kode':'8','nama':'Rekap SP2D TU Yang di LPJ-kan'},{'kode':'9','nama':'LPJ Fungsional Versi Akuntansi'},{'kode':'10','nama':'Laporan SP2D'}, 
        {'kode':'11','nama':'Kertas Kerja'},{'kode':'12','nama':'Laporan Realisasi Per SKPD Persumberdana'},{'kode':'13','nama':'Rekap Realisasi Persumberdana'}]
        judul = 'Laporan Verifikasi '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporanakuntansi':
        array_jenis_laporan = [{'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'Laporan Realisasi Anggaran Pemda Semester Pertama'},  
        {'kode':'2','nama':'Laporan Realisasi Anggaran SKPD Semester Pertama'},{'kode':'3','nama':'Laporan LRA Pemda'},{'kode':'4','nama':'Laporan LRA Per SKPD'} ]
        judul = 'Laporan Akutansi '
        path = 'laporan.html'
    elif jenis_akuntansi=='lrabulanan':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'KEMENTRIAN'},{'kode':'2','nama':'KPPN'}, 
        ]
        array_bulanan    = [
        {'kode':'0','bulan':'-- Pilih Bulan --'},{'kode':'1','bulan':'JANUARI'},{'kode':'2','bulan':'FEBUARI'},{'kode':'3','bulan':'MARET'},
        {'kode':'4','bulan':'APRIL'},{'kode':'5','bulan':'MEI'},{'kode':'6','bulan':'JUNI'},{'kode':'7','bulan':'JULI'},{'kode':'8','bulan':'AGUSTUS'}, 
        {'kode':'9','bulan':'SEPTEMBER'},{'kode':'10','bulan':'OKTOBER'},{'kode':'11','bulan':'NOVEMBER'},{'kode':'12','bulan':'DESEMBER'},{'kode':'13','bulan':'Semester I'},{'kode':'14','bulan':'Semester II'},
        ]
        judul = 'Laporan Realisasi Anggaran Bulanan '
        path = 'laporan.html'
    elif jenis_akuntansi=='lrapertriwulan':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'Laporan LRA PEMDA'},{'kode':'2','nama':'Laporan LRA Per SKPD'}, 
        ]
        judul = 'Laporan Realisasi Per Triwulan  '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporanperdaperbup':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'Perda LRA (Ringkasan LRA)'},{'kode':'2','nama':'Lampiran 1 (Menurut Urusan Pemerintah Daerah dan Organisasi)'},{'kode':'3','nama':'Lampiran 2 (Rincian Menurut Urusan Pemerintah Daerah dan Organisasi)'}, 
        {'kode':'4','nama':'Lampiran 3 (Rekapitulasi Realisasi Menurut Urusan Pemerintah dan Organisasi)'},{'kode':'5','nama':'Lampiran 4 (Rekapitulasi Realisasi Untuk Keselarasan dan Keterpaduan)'}, 
        {'kode':'6','nama':'Lampiran 5 (Daftar Piutang)'},{'kode':'7','nama':'Lampiran 6 (Daftar Inventasi)'},{'kode':'8','nama':'Lampiran 7 Perda (Daftar Penambahan dan Pengurangan Aset Daerah)'}, 
        {'kode':'9','nama':'Lampiran 8 Perda (Daftar Penambahan dan Pengurangan Aset Lainnya)'},{'kode':'10','nama':'Lampiran 9 Perda(Daftar Kegiatan yang Belum Diselesaikan Sampai Akhir Tahun)'}, 
        {'kode':'11','nama':'Lampiran 10 Perda (Daftar Dana Cadangan)'},{'kode':'12','nama':'Lampiran 11 Perda (Daftar Pinjaman)'},{'kode':'13','nama':'Lampiran Tambahan (Ringkasan Belanja Per Fungsi, Urusan, Organisasi dan Jenis)'} 
        ]
        array_jenis_laporan2 = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},
        {'kode':'2','nama':'Lampiran I ( Ringkasan LRA )'},
        {'kode':'3','nama':'Lampiran II ( Penjabaran LRA)'}
        ]

        judul = 'Laporan Perda / Perdub '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporanbukubesarnonbelanja':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},{'kode':'1','nama':'SP2D ( PFK / PERHITUNGAN FIHAK KETIGA )'},{'kode':'2','nama':'NOTA'}, 
        {'kode':'3','nama':'STS ( PENDAPATAN )'},{'kode':'4','nama':'Pengembalian Tahun Lalu'},{'kode':'5','nama':'Pengembalian UP/GU/TU Tahun Berjalan'},{'kode':'6','nama':'Pengembalian LS Tahun Berjalan'}, 
        {'kode':'7','nama':'Rekap STS Pendapatan'}, 
        ]
        judul = 'Laporan Buku Besar Non Belanja '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporanbukubesarbelanja': 
        judul = 'Laporan Buku Besar Belanja '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporantambahan':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},
        {'kode':'1','nama':'Laporan Realisasi Per Rekening ( PENDAPATAN )'},
        {'kode':'2','nama':'Laporan Realisasi Per Rekening ( BELANJA TIDAK LANGSUNG )'},
        {'kode':'3','nama':'Laporan Realisasi Per Rekening ( BELANJA TIDAK LANGSUNG -> PEGAWAI )'},
        {'kode':'4','nama':'Laporan Realisasi Per Rekening ( BELANJA TIDAK LANGSUNG -> NON PEGAWAI )'},
        {'kode':'5','nama':'Laporan Realisasi Per Rekening ( BELANJA LANGSUNG - PEGAWAI )'},
        {'kode':'6','nama':'Laporan Realisasi Per Rekening ( BELANJA LANGSUNG - BARANG DAN JASA )'},
        {'kode':'7','nama':'Laporan Realisasi Per Rekening ( BELANJA LANGSUNG - MODAL )'},
        {'kode':'8','nama':'Laporan Realisasi Per Rekening ( BELANJA LANGSUNG )'}
        ]
        judul = 'Laporan Tambahan '
        path = 'laporan.html'
    elif jenis_akuntansi=='laporanringkasank2':
        array_jenis_laporan = [
        {'kode':'0','nama':'-- Pilih Jenis Laporan --'},
        {'kode':'1','nama':'Laporan Realisasi Per Rekening ( PENDAPATAN )'},
        {'kode':'2','nama':'Laporan Realisasi Per Rekening ( BELANJA )'}
        ]
        judul = 'Laporan Ringkasan K-2 '
        path = 'laporan.html'

    data = {'organisasi_ppkd':get_PPKD(request)[0]['kode']+' - '+get_PPKD(request)[0]['urai'],
            'kd_org_ppkd':get_PPKD(request)[0]['kode'], 
            'ur_org_ppkd':get_PPKD(request)[0]['urai'],
            'organisasi':skpd["skpd"],
            'kd_org':kode, 
            'ur_org':skpd["urai"],
            'perubahan':str(sipkd_perubahan),
            'arrPerubahan':array_perubahan,
            'arrPeriode':array_periode,
            'pengguna_anggaran':pejabat_pengguna_anggaran,
            'arrBulan':array_bulan,
            'arrBulanan':array_bulanan,
            'arrSpj':array_spj,
            'jenis_laporan':array_jenis_laporan,
            'jenis_laporan2':array_jenis_laporan2,
            'master_dana':master_dana,
            'judul_laporan':judul,
            'jenis_akuntansi':jenis_akuntansi
            }
    return render(request, 'akuntansi/'+path+'',data)

def pejabat_pengguna(request):

    data = []

    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpkd where tahun=%s and jenissistem=2 and upper(jabatan) like %s",
                    [tahun_log(request),'%BENDAHARA%'])
                data = dictfetchall(cursor)


    return HttpResponse(json.dumps(data), content_type="application/json")

def get_data_ppkd(request,jenis_akuntansi):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)   
        data = request.GET.get('jenis_data', None)   
        # list_data = ''

        if ((gets != '0') or (gets != '') or (gets != '0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0'
            aidi = skpd.split('.')

        if data=='datalrappkd':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0') as koderekening, uraian, real_kemarin as jumlah FROM penatausahaan.fc_report_akrual_lra_ppkd(%s,%s,%s,%s,%s,%s,%s)"
                    "  where ( (kodejenis is not null and kodejenis<>0 and isbold=0) or (kodeobjek is not null and kodeobjek<>0 and isbold=0) or (kodeobjek<>0 and kodeobjek is not null and isbold=0)  ) ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun']), 1])
                list_data = dictfetchall(cursor)

        elif data=='dataloppkd':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0')  as koderekening, uraian, real_kemarin as jumlah FROM penatausahaan.fc_report_akrual_lo_ppkd(%s,%s,%s,%s,%s,%s)"
                    "  where ( (kodejenis is not null and kodejenis<>0 and isbold=0) or (kodeobjek is not null and kodeobjek<>0 and isbold=0) or (kodeobjek<>0 and kodeobjek is not null and isbold=0)  ) ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun'])])
                list_data = dictfetchall(cursor)

        elif data=='datalpeppkd':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select NOMOR as koderekening ,uraian,REAL_KEMARIN as jumlah FROM penatausahaan.fc_report_akrual_lpe_ppkd(%s,%s,%s,%s,%s,%s,%s)",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun']), 1])
                list_data = dictfetchall(cursor)

        elif data=='dataaruskas':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select NOMOR as koderekening ,uraian,REAL_KEMARIN as jumlah FROM penatausahaan.fc_report_akrual_kas(%s,%s,%s) where isbold=0",
                    [tahun_log(request), tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun'])])
                list_data = dictfetchall(cursor)

        data = {'data_spjppkd': list_data}

        return render(request, 'akuntansi/tabel/list_data_ppkd.html', data)
    else:
        return redirect('sipkd:index')


def simpan_data_ppkd(request,jenis_akuntansi):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            data                 = request.POST.get('jenis_data','')
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            data                 = request.POST.get('jenis_data', '')   
            rekening             = json.loads(request.POST.get('data_rekening', None))
            jumlah               = json.loads(request.POST.get('jumlah_data', None))
            urai                 = json.loads(request.POST.get('uraian', None))
            total                = request.POST.get('total_jumlah', '')
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''

            if data=='datalrappkd':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lra_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 1])

                for x in range(len(rekening)):
                    pisah_rekening      = rekening[x].split('.')
                    kdakun              = pisah_rekening[0]
                    kdkelompok          = pisah_rekening[1]
                    kdjenis             = pisah_rekening[2]
                    kdobjek             = pisah_rekening[3]
                    new_jumlah = jumlah[x]
                    print(kdakun+'..'+kdkelompok+'..'+kdjenis+'..'+kdobjek)
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lra_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,JUMLAH,ISSKPD)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdakun,kdkelompok,kdjenis,kdobjek,new_jumlah,1])
                        hasil = "Data LRA berhasil disimpan!"

            elif data=='dataloppkd':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lo_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 1])

                for x in range(len(rekening)):
                    pisah_rekening      = rekening[x].split('.')
                    kdakun              = pisah_rekening[0]
                    kdkelompok          = pisah_rekening[1]
                    kdjenis             = pisah_rekening[2]
                    kdobjek             = pisah_rekening[3]
                    new_jumlah = jumlah[x]

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lo_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,JUMLAH,ISSKPD,JUMLAHN)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdakun,kdkelompok,kdjenis,kdobjek,new_jumlah,1,total])
                        hasil = "Data LO berhasil disimpan!"

            elif data=='datalpeppkd':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lpe_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 1])

                for x in range(len(rekening)):
                    new_jumlah = jumlah[x]

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lpe_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODE,JUMLAH,ISSKPD,JUMLAHN)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,rekening[x],new_jumlah,1,total])
                        hasil = "Data LPE berhasil disimpan!"

            elif data=='dataaruskas':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.sal_kemarin where TAHUN=%s ",
                        [tahun_log(request)])

                for x in range(len(rekening)):
                    new_jumlah = jumlah[x]
                    new_urai = urai[x]
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.sal_kemarin (TAHUN,KODE,URAIAN,JUMLAH)"
                            " VALUES (%s,%s,%s,%s)",
                            [tahun_log(request),rekening[x],new_urai,new_jumlah])
                        hasil = "Data LPE berhasil disimpan!"

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def getlampiranperda(request,jenis_akuntansi):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)
        jenis_lampiran = request.GET.get('jenisLampiranPerda', None)
        list_lampiran = []
        if jenis_lampiran == '1':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(" SELECT * FROM APBD.DAFTAR_PIUTANG WHERE tahun = %s ORDER BY urut ASC", [tahun_log(request)])
                list_lampiran = dictfetchall(cursor)
        
        if jenis_lampiran == '2':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(" SELECT * FROM APBD.DAFTAR_PENYERTAAN_MODAL WHERE tahun = %s ORDER BY urut ASC", [tahun_log(request)])
                list_lampiran = dictfetchall(cursor)

        if jenis_lampiran == '3':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(" SELECT * FROM APBD.DAFTAR_DANA_CADANGAN WHERE tahun = %s ORDER BY urut ASC", [tahun_log(request)])
                list_lampiran = dictfetchall(cursor)

        if jenis_lampiran == '4':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(" SELECT *,to_char(tanggalpinjaman, 'YYYY-mm-dd') as tanggal1 FROM APBD.DAFTAR_PINJAMAN_DAERAH WHERE tahun = %s ORDER BY urut ASC", [tahun_log(request)])
                list_lampiran = dictfetchall(cursor)

                for i in range(len(list_lampiran)):
                    list_lampiran[i]['tgl_indonya'] = tgl_indo(datetime.strptime(list_lampiran[i]['tanggal1'], '%Y-%m-%d'))

        data = {'list_lampiran_perda': list_lampiran, 'jenis_lampiran': jenis_lampiran}

        return render(request, 'akuntansi/tabel/list_lampiran_perda.html', data)

    else:
        return redirect('sipkd:index')

def addlampiranperda(request, jenis_akuntansi):
    action = request.GET.get('act')
    nourut = request.GET.get('id')
    jenis_lampiran = request.GET.get('jenis_lampiran')
    realbunga = sisapokokpinjaman = sisabunga = ''
    dasarhukum = jmlrencana = transferdarikasda = transferkekasda = tujuan = hasilasa = ''
    uraianpiutang = tahunpengakuan = saldoawal = penambahanpiutang = penguranganpiutang = ''
    tahunpenyertaan = pihakketiga = bentukpenyertaan = jmlawal = jmln = hasil = jmlterima = ''
    sumberpinjaman = tanggalpinjaman = jumlahpinjaman = jangkawaktu = persenbunga = tujuanpinjaman = realpokokpinjaman = ''
    max_kdtpad = []
    hasil = []
    print(jenis_lampiran)
    if jenis_lampiran == '1':
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT coalesce(max(urut)+ 1, 1) as nourut FROM APBD.DAFTAR_PIUTANG WHERE TAHUN=%s", [tahun_log(request)])
                max_kdtpad = dictfetchall(cursor)
                for result in max_kdtpad:
                    nourut = result['nourut']

        if action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM APBD.DAFTAR_PIUTANG WHERE TAHUN=%s AND URUT=%s ", [tahun_log(request), nourut])
                hasil = dictfetchall(cursor)
                for result in hasil:
                    nourut = result['urut']
                    tahunpengakuan = result['tahunpengakuan']
                    saldoawal = result['saldoawal']
                    penambahanpiutang = result['penambahanpiutang']
                    penguranganpiutang = result['penguranganpiutang']
                    uraianpiutang = result['uraianpiutang']

    elif jenis_lampiran == '2':
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT coalesce(max(urut)+ 1, 1) as nourut FROM APBD.DAFTAR_PENYERTAAN_MODAL WHERE TAHUN=%s", [tahun_log(request)])
                max_kdtpad = dictfetchall(cursor)
                for result in max_kdtpad:
                    nourut = result['nourut']

        if action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM APBD.DAFTAR_PENYERTAAN_MODAL WHERE TAHUN=%s AND URUT=%s ", [tahun_log(request), nourut])
                x = dictfetchall(cursor)
                for result in x:
                    nourut = result['urut']
                    tahunpenyertaan = result['tahunpenyertaan']
                    pihakketiga = result['pihakketiga']
                    dasarhukum = result['dasarhukum']
                    bentukpenyertaan = result['bentukpenyertaan']
                    jmlawal = result['jmlawal']
                    jmln = result['jmln']
                    hasilasa = result['hasil']
                    jmlterima = result['jmlterima']

    elif jenis_lampiran == '3':
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT coalesce(max(urut)+ 1, 1) as nourut FROM APBD.DAFTAR_DANA_CADANGAN WHERE TAHUN=%s", [tahun_log(request)])
                max_kdtpad = dictfetchall(cursor)
                for result in max_kdtpad:
                    nourut = result['nourut']

        if action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM APBD.DAFTAR_DANA_CADANGAN WHERE TAHUN=%s AND URUT=%s ", [tahun_log(request), nourut])
                hasil = dictfetchall(cursor)
                for result in hasil:
                    nourut = result['urut']
                    tujuan = result['tujuan']
                    dasarhukum = result['dasarhukum']
                    jmlrencana = result['jmlrencana']
                    saldoawal = result['saldoawal']
                    transferdarikasda = result['transferdarikasda']
                    transferkekasda = result['transferkekasda']

    elif jenis_lampiran == '4':
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT coalesce(max(urut)+ 1, 1) as nourut FROM APBD.DAFTAR_PINJAMAN_DAERAH WHERE TAHUN=%s", [tahun_log(request)])
                max_kdtpad = dictfetchall(cursor)
                for result in max_kdtpad:
                    nourut = result['nourut']

        if action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM APBD.DAFTAR_PINJAMAN_DAERAH WHERE TAHUN=%s AND URUT=%s ", [tahun_log(request), nourut])
                hasil = dictfetchall(cursor)
                for result in hasil:
                    nourut = result['urut']
                    sumberpinjaman = result['sumberpinjaman']
                    tanggalpinjaman = tgl_indo(result['tanggalpinjaman'])
                    jumlahpinjaman = result['jumlahpinjaman']
                    jangkawaktu = result['jangkawaktu']
                    persenbunga = result['persenbunga']
                    tujuanpinjaman = result['tujuanpinjaman']
                    realpokokpinjaman = result['realpokokpinjaman']
                    realbunga = result['realbunga']
                    sisapokokpinjaman = result['sisapokokpinjaman']
                    sisabunga = result['sisabunga']

    data = {'jenis_lampiran': jenis_lampiran,
            'nourut': nourut, 
            'action': action, 
            'dasarhukum': dasarhukum, 
            'tahunpengakuan': tahunpengakuan,
            'penambahanpiutang': penambahanpiutang,
            'penguranganpiutang': penguranganpiutang,
            'uraianpiutang': uraianpiutang,
            'tahunpenyertaan': tahunpenyertaan,
            'pihakketiga': pihakketiga,
            'bentukpenyertaan': bentukpenyertaan,
            'jmlawal': jmlawal,
            'jmln': jmln,
            'hasil': hasilasa,
            'jmlterima': jmlterima,
            'tujuan': tujuan,
            'jmlrencana': jmlrencana,
            'saldoawal': saldoawal,
            'transferdarikasda': transferdarikasda,
            'transferkekasda': transferkekasda,
            'sumberpinjaman': sumberpinjaman,
            'tanggalpinjaman': tanggalpinjaman,
            'jumlahpinjaman': jumlahpinjaman,
            'jangkawaktu': jangkawaktu,
            'persenbunga': persenbunga,
            'tujuanpinjaman': tujuanpinjaman,
            'realpokokpinjaman': realpokokpinjaman,
            'realbunga': realbunga,
            'sisapokokpinjaman': sisapokokpinjaman,
            'sisabunga': sisabunga}
    return render(request, 'akuntansi/modal/lampiran_perda.html', data)

def savelampiranperda(request,jenis_akuntansi):
    done = status = ''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            jenis_lampiran = request.POST.get('jenis_lampiran')
            nourut = request.POST.get('nourut')
            action = request.POST.get('action')
            dasarhukum = request.POST.get('dasarhukum')
            tahunpengakuan = request.POST.get('tahunpengakuan')
            saldoawal  = request.POST.get('saldoawal')
            penambahanpiutang  = request.POST.get('penambahanpiutang')
            penguranganpiutang = request.POST.get('penguranganpiutang')
            uraianpiutang  = request.POST.get('uraianpiutang')
            tahunpenyertaan = request.POST.get('tahunpenyertaan')
            pihakketiga = request.POST.get('pihakketiga')
            bentukpenyertaan   = request.POST.get('bentukpenyertaan')
            jmlawal = request.POST.get('jmlawal')
            jmln   = request.POST.get('jmln')
            hasil  = request.POST.get('hasil')
            jmlterima  = request.POST.get('jmlterima')
            tujuan = request.POST.get('tujuan')
            jmlrencana = request.POST.get('jmlrencana')
            transferdarikasda  = request.POST.get('transferdarikasda')
            transferkekasda = request.POST.get('transferkekasda')
            sumberpinjaman = request.POST.get('sumberpinjaman')
            tanggalpinjaman = request.POST.get('tanggalpinjaman')
            jumlahpinjaman = request.POST.get('jumlahpinjaman')
            jangkawaktu = request.POST.get('jangkawaktu')
            persenbunga = request.POST.get('persenbunga')
            tujuanpinjaman = request.POST.get('tujuanpinjaman')
            realpokokpinjaman  = request.POST.get('realpokokpinjaman')
            realbunga  = request.POST.get('realbunga')
            sisapokokpinjaman  = request.POST.get('sisapokokpinjaman')
            sisabunga  = request.POST.get('sisabunga')
            if jenis_lampiran == '1':
                status = 'Daftar Piutang'
                if action == 'add':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO APBD.DAFTAR_PIUTANG(tahun,urut,tahunpengakuan,saldoawal, "
                                       "penambahanpiutang,penguranganpiutang,uraianpiutang) "
                                       "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                       [tahun_log(request), nourut, tahunpengakuan, saldoawal, penambahanpiutang, penguranganpiutang, uraianpiutang])
                        done = "Data "+status+" berhasil disimpan!"
                if action == 'edit':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE APBD.DAFTAR_PIUTANG set tahunpengakuan=%s, saldoawal=%s,"
                                       "penambahanpiutang=%s, penguranganpiutang=%s where tahun=%s and urut=%s",
                                       [tahunpengakuan, saldoawal, penambahanpiutang, penguranganpiutang, tahun_log(request), nourut])
                    done = "Data"+status+" berhasil diubah!"

            elif jenis_lampiran == '2':
                status = 'Daftar Penyertaan Modal'
                if action == 'add':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO APBD.DAFTAR_PENYERTAAN_MODAL(tahun,urut,tahunpenyertaan,pihakketiga, "
                                   "dasarhukum,bentukpenyertaan,jmlawal,jmln,hasil,jmlterima) "
                                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                   [tahun_log(request), nourut, tahunpenyertaan, pihakketiga, dasarhukum, bentukpenyertaan, jmlawal, jmln, hasil, jmlterima])
                    done = "Data "+status+" berhasil disimpan!"
                if action == 'edit':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE APBD.DAFTAR_PENYERTAAN_MODAL set tahunpenyertaan=%s, pihakketiga=%s,"
                            "dasarhukum=%s, bentukpenyertaan=%s, jmlawal=%s, jmln=%s, hasil=%s, jmlterima=%s where tahun=%s and urut=%s",
                            [tahunpenyertaan, pihakketiga, dasarhukum, bentukpenyertaan, jmlawal, jmln, hasil, jmlterima, tahun_log(request), nourut])
                        done = "Data"+status+" berhasil diubah!"

            elif jenis_lampiran == '3':
                status = 'Daftar Dana Cadangan'
                if action == 'add':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO APBD.DAFTAR_DANA_CADANGAN(tahun,urut,tujuan, "
                                   "dasarhukum,jmlrencana,saldoawal,transferdarikasda,transferkekasda) "
                                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                   [tahun_log(request), nourut, tujuan, dasarhukum, jmlrencana, saldoawal, transferdarikasda, transferkekasda])
                    done = "Data "+status+" berhasil disimpan!"
                if action == 'edit':
                    
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE APBD.DAFTAR_DANA_CADANGAN set tujuan=%s, dasarhukum=%s,"
                            "jmlrencana=%s, saldoawal=%s, transferdarikasda=%s, transferkekasda=%s where tahun=%s and urut=%s",
                            [tujuan, dasarhukum, jmlrencana, saldoawal, transferdarikasda, transferkekasda, tahun_log(request), nourut])
                        done = "Data"+status+" berhasil diubah!"

            elif jenis_lampiran == '4':
                status = 'Daftar Pinjaman Daerah'
                if action == 'add':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO APBD.DAFTAR_PINJAMAN_DAERAH (tahun,urut,sumberpinjaman,tanggalpinjaman, "
                                   "jumlahpinjaman,jangkawaktu,persenbunga,tujuanpinjaman,realpokokpinjaman,realbunga,sisapokokpinjaman,sisabunga) "
                                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                   [tahun_log(request), nourut, sumberpinjaman, tgl_to_db(tanggalpinjaman), jumlahpinjaman, jangkawaktu, persenbunga, tujuanpinjaman, realpokokpinjaman, realbunga, sisapokokpinjaman, sisabunga])
                    done = "Data "+status+" berhasil disimpan!"
                if action == 'edit':
                    
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE APBD.DAFTAR_PINJAMAN_DAERAH set sumberpinjaman=%s, tanggalpinjaman=%s,"
                            "jumlahpinjaman=%s, jangkawaktu=%s, persenbunga=%s, tujuanpinjaman=%s, realpokokpinjaman=%s, realbunga=%s, sisapokokpinjaman=%s, sisabunga=%s where tahun=%s and urut=%s",
                            [sumberpinjaman, tgl_to_db(tanggalpinjaman), jumlahpinjaman, jangkawaktu, persenbunga, tujuanpinjaman, realpokokpinjaman, realbunga, sisapokokpinjaman, sisabunga, tahun_log(request), nourut])
                        done = "Data"+status+" berhasil diubah!"

        return HttpResponse(done)
    else:
        return redirect('sipkd:index')


def deletelampiranperda(request, jenis_akuntansi):
    # get id
    nourut = request.POST.get('nourut')
    jenis_lampiran = request.POST.get('jenis_lampiran')
    done = status = ''

    if jenis_lampiran == '1':
        status = 'Daftar Piutang'
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("DELETE FROM APBD.DAFTAR_PIUTANG where TAHUN=%s and urut=%s", [tahun_log(request), nourut])
        done = "Data Lampiran "+status+" berhasil dihapus!"

    elif jenis_lampiran == '2':
        status = 'Daftar Penyertaan Modal'
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("DELETE FROM APBD.DAFTAR_PENYERTAAN_MODAL where TAHUN=%s and urut=%s", [tahun_log(request), nourut])
        done = "Data Lampiran "+status+" berhasil dihapus!"

    elif jenis_lampiran == '3':
        status = 'Daftar Dana Cadangan'
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("DELETE FROM APBD.DAFTAR_DANA_CADANGAN where TAHUN=%s and urut=%s", [tahun_log(request), nourut])
        done = "Data Lampiran "+status+" berhasil dihapus!"

    elif jenis_lampiran == '4':
        status = 'Daftar Pinjaman Daerah'
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("DELETE FROM APBD.DAFTAR_PINJAMAN_DAERAH where TAHUN=%s and urut=%s", [tahun_log(request), nourut])
        done = "Data Lampiran "+status+" berhasil dihapus!"

    return HttpResponse(done)

def cetak_laporan(request):
    post        = request.POST
    reportParam = {}
    
    jenis_akuntansi     = post.get('laporan')
    jenis_laporan       = post.get('jenis_laporan')
    versi_laporan       = post.get('versi_laporan')
    versi_sesuai        = post.get('versi_sesuai')
    versi_skpd          = post.get('versi_skpd')
    jenis_realisasi     = post.get('jenis_realisasi')
    nama_pengguna       = post.get('nama_pengguna')
    nip_pengguna        = post.get('nip_pengguna')
    pangkat_pengguna    = post.get('pangkat_pengguna')
    jenis_spj           = post.get('jenis_spj')
    jenis_belanja       = post.get('jenis_belanja')
    jenis_peraturan     = post.get('jenis_peraturan')
    status_perubahan    = post.get('status_perubahan')
    if status_perubahan =='1':
        status = '0'
    else:
        status = '1'
    jenis_realisasi  = post.get('jenis_realisasi')
    if jenis_realisasi =='0':
        realisasi = 'SPJ'
    else:
        realisasi = 'SP2D'
    jenis_triwulan  = post.get('jenis_triwulan')
    if jenis_triwulan =='1': triwulan = 'Triwulan I'
    elif jenis_triwulan =='2': triwulan = 'Triwulan II'
    elif jenis_triwulan =='3': triwulan = 'Triwulan III'
    elif jenis_triwulan =='4': triwulan = 'Triwulan IV'
    jenis_bulan  = post.get('jenis_bulan')
    if jenis_bulan =='1': bulanx = 'JANUARI'
    elif jenis_bulan =='2': bulanx = 'FEBUARI'
    elif jenis_bulan =='3': bulanx = 'MARET'
    elif jenis_bulan =='4': bulanx = 'APRIL'
    elif jenis_bulan =='5': bulanx = 'MEI'
    elif jenis_bulan =='6': bulanx = 'JUNI'
    elif jenis_bulan =='7': bulanx = 'JULI'
    elif jenis_bulan =='8': bulanx = 'AGUSTUS'
    elif jenis_bulan =='9': bulanx = 'SEPTEMBER'
    elif jenis_bulan =='10': bulanx = 'OKTOBER'
    elif jenis_bulan =='11': bulanx = 'NOVEMBER'
    elif jenis_bulan =='12': bulanx = 'DESEMBER'
    elif jenis_bulan =='13': bulanx = 'SEMESTER I'
    elif jenis_bulan =='14': bulanx = 'SEMESTER II'
    cek_skpkd        = post.get('ppkd_ceked')

    if jenis_akuntansi=='laporanverifikasi':

        if jenis_laporan=='1':
            reportParam['file']                 = 'penatausahaan/akuntansi/KartuPengawasanUP.fr3'  
            reportParam['jenissp2d']            = "'"+'UP'+"'"
        elif jenis_laporan=='2':  
            reportParam['file']                 = 'penatausahaan/akuntansi/KartuPengawasanUP.fr3'  
            reportParam['jenissp2d']            = "'"+'TU'+"'"
        elif jenis_laporan=='3':
            reportParam['file']                 = 'penatausahaan/akuntansi/KartuPengawasanRealisasiAnggaran.fr3'
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['kodeorganisasi2']      = post.get('organisasi')
            reportParam['organisasi']           = post.get('urai_org')
        elif jenis_laporan=='4' :
            reportParam['file']                 = 'penatausahaan/akuntansi/RegisterSP2D.fr3'
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['kodeorganisasi2']      = post.get('organisasi')
            reportParam['organisasi']           = post.get('urai_org')
            reportParam['periode']              = tgl_short(post.get('bulan_ke'))+' - '+tgl_short(post.get('bulan_sampai'))
            reportParam['isskpd']               = post.get('ppkd_ceked')
        elif jenis_laporan=='5':
            reportParam['file']                 = 'penatausahaan/akuntansi/RegisterSP2DRincian.fr3'
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['kodeorganisasi2']      = "'"+post.get('organisasi')+"'"
            reportParam['organisasi']           = "'"+post.get('urai_org')+"'"
            reportParam['periode']              = tgl_short(post.get('bulan_ke'))+' - '+tgl_short(post.get('bulan_sampai'))
            reportParam['isskpd']               = post.get('ppkd_ceked')
        elif jenis_laporan=='6':
            reportParam['file']                 = 'penatausahaan/akuntansi/RegisterSPJ.fr3'
            if jenis_spj=='1' :
                reportParam['jenis1']           = "'"+'SEMUA'+"'"
                reportParam['jenis']            = 'UP-GU / TU'
            elif jenis_spj=='2' :
                reportParam['jenis1']           = "'"+'GU'+"'"
                reportParam['jenis']            = 'GU (Ganti Uang Persediaan)'
            elif jenis_spj=='3' :
                reportParam['jenis1']           = "'"+'TU'+"'"
                reportParam['jenis']            = 'TU (Tambahan Uang Persediaan)'
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['kodeorganisasi2']      = "'"+post.get('organisasi')+"'"
            reportParam['organisasi']           = "'"+post.get('urai_org')+"'"
            reportParam['periode']              = tgl_short(post.get('bulan_ke'))+' - '+tgl_short(post.get('bulan_sampai'))
            reportParam['isskpd']               = post.get('ppkd_ceked')
        elif jenis_laporan=='7' or jenis_laporan=='8':
            if jenis_laporan=='7':
                reportParam['file']             = 'penatausahaan/akuntansi/RekapSP2dTUNonSPJ.fr3'
                reportParam['organisasi']       = "'"+post.get('urai_org')+"'"
                reportParam['qry']              = "where kodeurusan='"+post.get('kdurusan')+"' and kodesuburusan='"+post.get('kdsuburusan')+"' and kodeorganisasi='"+post.get('kdorganisasi')+"' and jumlahspj=0 and tglkasda is not null"
            elif jenis_laporan=='8':
                reportParam['file']             = 'penatausahaan/akuntansi/RekapSP2dTUSPJ.fr3'            
                reportParam['qry']              = "where kodeurusan='"+post.get('kdurusan')+"' and kodesuburusan='"+post.get('kdsuburusan')+"' and kodeorganisasi='"+post.get('kdorganisasi')+"' and tglkasda is not null"
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['isskpd']               = post.get('ppkd_ceked')
        elif jenis_laporan=='9':
            if jenis_belanja=='0' :
                reportParam['file']             = 'penatausahaan/akuntansi/SuratPengesahanSPJ.fr3'
                if cek_skpkd =='1' :
                    reportParam['file']         = 'penatausahaan/akuntansi/SuratPengesahanSPJPPKD.fr3'
            elif jenis_belanja=='1' :
                reportParam['file']             = 'penatausahaan/akuntansi/SuratPengesahanSPJPenerimaanSKPD.fr3'
            reportParam['kodeurusan']           = post.get('kdurusan')
            reportParam['kodesuburusan']        = post.get('kdsuburusan')
            reportParam['kodeorganisasi']       = "'"+post.get('kdorganisasi')+"'"
            reportParam['kodeorganisasi2']      = "'"+post.get('organisasi')+"'"
            reportParam['organisasi']           = "'"+post.get('urai_org')+"'"
            reportParam['periode']              = tgl_short(post.get('bulan_ke'))+' s/d '+tgl_short(post.get('bulan_sampai'))
            reportParam['isskpd']               = post.get('ppkd_ceked')
            reportParam['bulan']                = post.get('jenis_bulan')
        elif jenis_laporan=='10':
            reportParam['file']                 = 'penatausahaan/akuntansi/lap_spj_sp2d.fr3'
            reportParam['periode']              = tgl_short(post.get('bulan_ke'))+' s/d '+tgl_short(post.get('bulan_sampai'))
            reportParam['jenis']                = post.get('jenis_spj')
        elif jenis_laporan=='11':
            reportParam['file']                 = 'penatausahaan/akuntansi/KertasKerjaVerifikasi.fr3'
        elif jenis_laporan=='12' or jenis_laporan=='13':
            if jenis_laporan=='12':
                reportParam['file']             = 'penatausahaan/akuntansi/RealisasiPerSKPDPerSumberDana.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            elif jenis_laporan=='13':
                reportParam['file']             = 'penatausahaan/akuntansi/RekapPerSKPDPerSumberDana.fr3'

            reportParam['kodesumberdana']       = post.get('kode_sumberdana')
            reportParam['sumberdana']           = post.get('sumberdana')
            reportParam['periodeawal']          = "'"+tgl_short(post.get('bulan_ke'))+"'"
            reportParam['periodeakhir']         = "'"+tgl_short(post.get('bulan_sampai'))+"'"

        reportParam['tglawal']                  = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']                 = "'"+tgl_short(post.get('bulan_sampai'))+"'"
        reportParam['tglfrom']                  = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglto']                    = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    elif jenis_akuntansi=='laporanakuntansi':

        if jenis_laporan=='1':
            if versi_laporan=='0':
                reportParam['file']         = 'penatausahaan/akuntansi/LRA_1_Akrual.fr3'

            elif versi_laporan=='1':
                reportParam['file']         = 'penatausahaan/akuntansi/LRA_1_permen.fr3'

            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['bulan']            = '6'

        elif jenis_laporan=='2':  
            if versi_laporan== '0':
                if cek_skpkd=='0':
                    reportParam['file']     = 'penatausahaan/akuntansi/LRA_1_SKPD.fr3'
                elif cek_skpkd=='1':
                    reportParam['file']     = 'penatausahaan/akuntansi/LRA_1_PPKD.fr3'
            elif versi_laporan=='1':
                reportParam['file']         = 'penatausahaan/akuntansi/lra_skpd_permen.fr3'  

            reportParam['kodeurusan']       = post.get('kdurusan')
            reportParam['kodesuburusan']    = post.get('kdsuburusan')
            reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['bulan']            = '6'

        elif jenis_laporan=='3':
            if versi_laporan=='0':
                reportParam['file']         = 'penatausahaan/akuntansipemda/Lra_Triwulan_SAP.fr3'
            elif versi_laporan=='1':
                reportParam['file']         = 'penatausahaan/akuntansipemda/Lra_Triwulan_permen59.fr3'  

            reportParam['triwulan']         = post.get('jenis_triwulan')
            reportParam['xtriwulan']        = triwulan
        elif jenis_laporan=='4':
            if versi_laporan=='0':
                reportParam['file']         = 'penatausahaan/akuntansipemda/Lra_Triwulan_SAP_SKPD.fr3'
            elif versi_laporan=='1':
                reportParam['file']         = 'penatausahaan/akuntansipemda/Lra_Triwulan_permen59_SKPD.fr3'
  
            reportParam['isskpd']           = post.get('ppkd_ceked')
            reportParam['kodeurusan']       = post.get('kdurusan')
            reportParam['kodesuburusan']    = post.get('kdsuburusan')
            reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['triwulan']         = post.get('jenis_triwulan')
            reportParam['xtriwulan']        = triwulan

        reportParam['isskpd']           = cek_skpkd
        reportParam['status']           = status
        reportParam['jenisReal']        = realisasi
        reportParam['line1']            = ''            
        if jenis_triwulan =='1':
            reportParam['tglawal']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']     = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']        = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
            reportParam['bulan']        = '3' 
        elif jenis_triwulan =='2':
            reportParam['tglawal']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']     = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']        = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['bulan']        = '6'
        elif jenis_triwulan =='3':
            reportParam['tglawal']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']     = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']        = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
            reportParam['bulan']        = '9' 
        elif jenis_triwulan =='4':
            reportParam['tglawal']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']     = "'"+'31-Dec-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']      = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']        = "'"+'31-Dec-'+''+tahun_log(request)+''"'"
            reportParam['bulan']        = '12'

    elif jenis_akuntansi=='lrabulanan':

        if jenis_laporan=='1':
            if versi_laporan=='0':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan_sap.fr3'
            elif versi_laporan=='1':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan.fr3'
            elif versi_laporan=='2':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan_pmk.fr3'

            reportParam['tglawal']      = "'"+tgl_short(post.get('bulan_ke'))+"'"
            reportParam['tglakhir']     = "'"+tgl_short(post.get('bulan_sampai'))+"'"
            reportParam['tglfrom']      = "'"+tgl_short(post.get('bulan_ke'))+"'"
            reportParam['tglto']        = "'"+tgl_short(post.get('bulan_sampai'))+"'"
            reportParam['bulan']        = post.get('jenis_bulan')

            if jenis_bulan =='1' or jenis_bulan=='2' or jenis_bulan=='3' or jenis_bulan=='4' or jenis_bulan=='5' or jenis_bulan=='6' or jenis_bulan=='7' or jenis_bulan=='8' or jenis_bulan=='9' or jenis_bulan=='10' or jenis_bulan=='11' or jenis_bulan=='12':
                reportParam['xbulan']   = bulanx
            elif jenis_bulan =='13':
                reportParam['bulan']    = '6'
                reportParam['xbulan']   = bulanx
            elif jenis_bulan =='14':
                reportParam['bulan']    = '12'
                reportParam['xbulan']   = bulanx 

        elif jenis_laporan=='2':  
            if versi_laporan== '0':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan_sap_2.fr3'
            elif versi_laporan=='1':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan_2.fr3'  
            elif versi_laporan=='2':
                reportParam['file']     = 'penatausahaan/akuntansipemda/Lra_bulanan_pmk_2.fr3'

            reportParam['triwulan']     = post.get('jenis_triwulan')
            reportParam['xtriwulan']    = triwulan
            if jenis_triwulan =='1':
                reportParam['tglawal']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglakhir'] = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
                reportParam['tglfrom']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglto']    = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
                reportParam['bulan']    = '3'
                reportParam['xbulan']   = 'SEMESTER I' 
            elif jenis_triwulan =='2':
                reportParam['tglawal']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglakhir'] = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
                reportParam['tglfrom']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglto']    = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
                reportParam['bulan']    = '6' 
                reportParam['xbulan']   = 'SEMESTER II'
            elif jenis_triwulan =='3':
                reportParam['tglawal']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglakhir'] = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
                reportParam['tglfrom']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglto']    = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
                reportParam['bulan']    = '9' 
                reportParam['xbulan']   = 'SEMESTER III'
            elif jenis_triwulan =='4':
                reportParam['tglawal']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglakhir'] = "'"+'31-Dec-'+''+tahun_log(request)+''"'"
                reportParam['tglfrom']  = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
                reportParam['tglto']    = "'"+'31-Dec-'+''+tahun_log(request)+''"'"
                reportParam['bulan']    = '12'  
                reportParam['xbulan']   = 'SEMESTER IV'

        reportParam['status']           = status
        reportParam['jenisReal']        = realisasi
        reportParam['line1']            = ''

    elif jenis_akuntansi=='lrapertriwulan':

        if jenis_laporan=='1' and versi_laporan=='0':
            reportParam['file']             = 'penatausahaan/akuntansipemda/Lra_Triwulan_SAP.fr3'
        elif jenis_laporan=='1' and versi_laporan=='1':
            reportParam['file']             = 'penatausahaan/akuntansipemda/Lra_Triwulan_permen59.fr3'
        elif jenis_laporan=='2' and versi_laporan== '0':  
            reportParam['file']             = 'penatausahaan/akuntansipemda/Lra_Triwulan_SAP_SKPD.fr3'
            reportParam['kodeurusan']       = post.get('kdurusan')
            reportParam['kodesuburusan']    = post.get('kdsuburusan')
            reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['isskpd']           = cek_skpkd
        elif jenis_laporan=='2' and versi_laporan=='1':
            reportParam['file']             = 'penatausahaan/akuntansipemda/Lra_Triwulan_permen59_SKPD.fr3'  
            reportParam['kodeurusan']       = post.get('kdurusan')
            reportParam['kodesuburusan']    = post.get('kdsuburusan')
            reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['isskpd']           = cek_skpkd

        reportParam['status']               = status
        reportParam['jenisReal']            = realisasi
        reportParam['line1']                = ''
        reportParam['triwulan']             = post.get('jenis_triwulan')
        reportParam['xtriwulan']            = triwulan

        if jenis_triwulan =='1':
            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'31-Mar-'+''+tahun_log(request)+''"'"
        elif jenis_triwulan =='2':
            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'30-Jun-'+''+tahun_log(request)+''"'"
        elif jenis_triwulan =='3':
            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'30-Sep-'+''+tahun_log(request)+''"'"
        elif jenis_triwulan =='4':
            reportParam['tglawal']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglakhir']         = "'"+'31-Dec-'+''+tahun_log(request)+''"'"
            reportParam['tglfrom']          = "'"+'01-Jan-'+''+tahun_log(request)+''"'"
            reportParam['tglto']            = "'"+'31-Dec-'+''+tahun_log(request)+''"'" 

    elif jenis_akuntansi=='laporanperdaperbup':

        if jenis_peraturan =='0':

            if jenis_laporan =='1' and versi_sesuai== '0':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI.fr3'
            elif jenis_laporan =='1' and versi_sesuai=='1':
                reportParam['file']             = 'penatausahaan/akuntansi/perda59.fr3'
            elif jenis_laporan =='2':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI1.fr3'
            elif jenis_laporan =='3':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            elif jenis_laporan =='4':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI3.fr3'
            elif jenis_laporan =='5':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI4.fr3'
            elif jenis_laporan =='6':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI5.fr3'
            elif jenis_laporan =='7':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI6.fr3'
            elif jenis_laporan =='8':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI7.fr3'
            elif jenis_laporan =='9':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI8.fr3'
            elif jenis_laporan =='10':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI9.fr3'
            elif jenis_laporan =='11':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI10.fr3'
            elif jenis_laporan =='12':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI11.fr3'
            elif jenis_laporan =='13':
                reportParam['file']             = 'penatausahaan/akuntansi/LampiranI12.fr3'

        elif jenis_peraturan == '1':

            if jenis_laporan =='2':
                reportParam['file']             = 'penatausahaan/akuntansipemda/PerbubI.fr3'
            elif jenis_laporan =='3':
                if cek_skpkd=='0':
                    reportParam['file']         = 'penatausahaan/akuntansipemda/PerbubII.fr3'
                elif cek_skpkd=='1':
                    reportParam['file']         = 'penatausahaan/akuntansipemda/PerbubII.1.fr3'

                reportParam['isskpd']           = cek_skpkd
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"

        reportParam['tglperda']                 = "'"+tgl_short(post.get('tgl_perda'))+"'"
        reportParam['noperda']                  = post.get('no_perda')
        reportParam['idrancangan']              = post.get('id_rancangan')
        reportParam['halaman']                  = post.get('halaman')
        reportParam['salinan']                  = post.get('salinan')
        reportParam['tglawal']                  = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']                 = "'"+tgl_short(post.get('bulan_sampai'))+"'"
        reportParam['tglfrom']                  = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglto']                    = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    elif jenis_akuntansi=='laporanbukubesarnonbelanja':
        if jenis_laporan =='1':
            reportParam['jb']                   = "'"+'SP2D'+"'"
            reportParam['bb']                   = 'Perhitungan Pihak Ketiga'
            reportParam['jsp2d']                = "'"+''+"'"
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"            
        elif jenis_laporan == '2':
            reportParam['jb']                   = "'"+'NOTA'+"'"
            reportParam['bb']                   = 'NOTA Pihak Ketiga'
            reportParam['jsp2d']                = "'"+''+"'"
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"            
        elif jenis_laporan == '3':
            reportParam['jb']                   = "'"+'STS'+"'"
            reportParam['bb']                   = 'Surat Tanda Setoran'
            reportParam['jsp2d']                = "'"+''+"'"            
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"            
        elif jenis_laporan == '4':
            reportParam['jb']                   = "'"+'CONTRAKEMARIN'+"'"
            reportParam['bb']                   = 'Setoran Sisa Kas Bendahara Tahun Kemarin'
            reportParam['jsp2d']                = "'"+''+"'"
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"            
        elif jenis_laporan == '5':
            reportParam['jb']                   = "'"+'CONTRA'+"'"
            reportParam['bb']                   = 'Pengembalian UP/GU/TU Tahun Berjalan'
            reportParam['jsp2d']                = "'"+'UP'+"'"
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"
        elif jenis_laporan == '6':
            reportParam['jb']                   = "'"+'CONTRA'+"'"
            reportParam['bb']                   = 'Pengembalian LS Tahun Berjalan'
            reportParam['jsp2d']                = "'"+'LS'+"'"
            if versi_skpd =='0':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja1.fr3'
                reportParam['skpd']             = "'"+''+"'"
            elif versi_skpd == '1':
                reportParam['file']             = 'penatausahaan/akuntansipemda/laporanNonBelanja2.fr3'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
                reportParam['skpd']             = "'"+post.get('organisasi')+"'"            
        elif jenis_laporan == '7':
            reportParam['file']                 = 'penatausahaan/akuntansipemda/RekapSTS.fr3'
            if versi_skpd=='0':
                reportParam['skpd']             = '1'
            else:
                reportParam['skpd']             = '0'
                reportParam['kodeurusan']       = post.get('kdurusan')
                reportParam['kodesuburusan']    = post.get('kdsuburusan')
                reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['jb']                   = "'"+'STS'+"'"
            reportParam['bb']                   = 'Surat Tanda Setoran'
            reportParam['jsp2d']                = "'"+''+"'"

        reportParam['periodeawal']              = tgl_short(post.get('bulan_ke'))
        reportParam['periodeakhir']             = tgl_short(post.get('bulan_sampai'))
        reportParam['tglawal']                  = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']                 = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    elif jenis_akuntansi=='laporanbukubesarbelanja':

        if versi_skpd =='0':
            reportParam['file']             = 'penatausahaan/akuntansipemda/laporanBelanja1.fr3'
            reportParam['skpd']             = "'"+''+"'"
        elif versi_skpd == '1':
            reportParam['file']             = 'penatausahaan/akuntansipemda/laporanBelanja2.fr3'
            reportParam['kodeurusan']       = post.get('kdurusan')
            reportParam['kodesuburusan']    = post.get('kdsuburusan')
            reportParam['kodeorganisasi']   = "'"+post.get('kdorganisasi')+"'"
            reportParam['skpd']             = "'"+post.get('organisasi')+"'"

        reportParam['bb']                   = 'BUKU BESAR SP2D'
        reportParam['jb']                   = "'"+'SP2D'+"'"
        reportParam['periodeawal']          = tgl_short(post.get('bulan_ke'))
        reportParam['periodeakhir']         = tgl_short(post.get('bulan_sampai'))
        reportParam['tglawal']              = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']             = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    elif jenis_akuntansi=='laporantambahan':
        if jenis_laporan =='1' or jenis_laporan == '2' or jenis_laporan == '3' or jenis_laporan == '4' or jenis_laporan == '5' or jenis_laporan == '6' or jenis_laporan == '7' or jenis_laporan == '8':
            reportParam['jenis']            = "'"+jenis_laporan+"'"

        reportParam['perubahan']            = "'"+status+"'"
        reportParam['file']                 = 'penatausahaan/akuntansipemda/LaporanRincianAnggaran.fr3'
        reportParam['tglawal']              = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']             = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    elif jenis_akuntansi=='laporanringkasank2':
        if jenis_laporan =='1':
            reportParam['file']             = 'penatausahaan/akuntansipemda/Laporank2.fr3'
        elif jenis_laporan == '2':
            reportParam['file']             = 'penatausahaan/akuntansipemda/Laporank2Belanja.fr3'

        reportParam['jenis']                = jenis_laporan
        reportParam['perubahan']            = status
        reportParam['tglawal']              = "'"+tgl_short(post.get('bulan_ke'))+"'"
        reportParam['tglakhir']             = "'"+tgl_short(post.get('bulan_sampai'))+"'"

    reportParam['id']                       = post.get(str('id_pengguna'))
    reportParam['idpa']                     = post.get(str('id_pengguna'))
    reportParam['nama']                     = post.get(str('nama_pengguna'))
    if nip_pengguna =='':
        reportParam['nip']                  = ''
    else:
        reportParam['nip']                  = 'Nip : '+nip_pengguna
    reportParam['pangkat']                  = post.get(str('pangkat_pengguna'))
    reportParam['jabatan']                  = post.get(str('jabatan_pengguna'))
    reportParam['tahun']                    = "'"+tahun_log(request)+"'"  
    reportParam['tglcetak']                 = tgl_short(post.get('tgl_cetak'))
    reportParam['report_type']              = 'pdf'

    return HttpResponse(laplink(request, reportParam))