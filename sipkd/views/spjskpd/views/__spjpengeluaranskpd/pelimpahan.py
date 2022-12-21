from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from .. import main
from ...anov import *
from django.db import connection,connections
from sipkd.config import username

# CUSTOM #
jenisjenis = {
    'KELUAR': 'Pemberian Pelimpahan',
    'TERIMA': 'Pertanggung jawaban Pelimpahan',
}

isskpd = 0
sekarang_penerimaan_re = 'TERIMA'

def load(rq):
    data = {'entry': {}, 'rincian': [], 'potongan': [],}
    try:
        jenis_bku = rq.GET['jenis_bku']
        cond = (
            rq.GET['tahun'],
            rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
            isskpd,
            rq.GET['no_bku'],
        )
    except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

    with querybuilder() as qb:
        qb.execute("""
            SELECT a.* FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
            AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
            AND a.isskpd = %s
            AND a.no_bku = %s
            AND a.jenis_bku = 'PELIMPAHAN'
        """, cond)
        qb.result_one(data['entry'])

    if jenis_bku == 'TERIMA':
        jumlah = data['entry']['penerimaan']
        data['entry']['penerimaan'] = data['entry']['pengeluaran']
        data['entry']['pengeluaran'] = jumlah

        del data['entry']['no_bku']
        del data['entry']['jenis_bku']

    return JsonResponse(data, safe=False)
# 

def browse(rq):
    data = []
    try:
        jenis_bku = rq.GET['jenis_bku']
        cond = (
            rq.GET['tahun'],
            rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
            jenis_bku,
        )
    except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

    if jenis_bku == 'PELIMPAHAN':
        with querybuilder() as qb:
            qb.execute(
            """
                SELECT
                a.no_bku, a.tgl_bku,
                a.bukti, a.tgl_bukti,
                a.urai,
                a.pengeluaran AS jumlah,
                a.simpananbank, a.is_pihak_ketiga

                FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
                AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
                AND a.jenis_bku = %s
                AND NOT EXISTS (
                    SELECT 1 FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
                    AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
                    AND b.jenis_bku = a.jenis_bku

                    AND b.bukti = a.bukti
                    AND b.penerimaan <> 0
                )
            """, cond)
            qb.result_many(data)

    else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain')

    return JsonResponse(data, safe=False)

def browse_bendaKeluar(rq):
    data = []

    try:
        jenis_bku = rq.GET['jenis_bku'].upper()
        cond = (
            rq.GET['tahun'],
            rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
        )
    except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

    if jenis_bku == 'PELIMPAHAN':
        with querybuilder() as qb:
            qb.execute(
            """
                SELECT tahun, uname, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, nama_bendahara_pembantu  
                FROM penatausahaan.pengguna 
                WHERE tahun = %s and kodeurusan = %s and kodesuburusan =%s and kodeorganisasi = %s and kodeunit = %s and is_bendahara_pembantu = 'Y'
            """, cond)
            qb.result_many(data)

    else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain')

    return JsonResponse(data, safe=False)

def save_pelimpahan(rq):
    
    jenis_bku_alt = rq.POST['jenis_bku_alt']
    tahun = rq.POST['tahun']
    kodeurusan = rq.POST['kodeurusan']
    kodesuburusan = rq.POST['kodesuburusan']
    kodeorganisasi = rq.POST['kodeorganisasi']
    kodeunit = rq.POST['kodeunit']
    jumlah = rq.POST['penerimaan']
    bukti = rq.POST['bukti']
    no_bku = rq.POST['no_bku']
    tgl_bku = rq.POST['tgl_bku']
    urai = rq.POST['urai']
    tgl_bukti = rq.POST['tgl_bukti']
    
    if jenis_bku_alt == 'TERIMA':
        with connections[tahun_log(rq)].cursor() as cursor:
            cursor.execute("""
                            INSERT INTO pertanggungjawaban.skpd_bku (tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, tgl_bku, urai, 
                            jenis_bku, penerimaan, bukti, tgl_bukti, uname, is_bendahara_pembantu, bendahara_pembantu)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,[tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, tgl_bku, urai,
                            'PELIMPAHAN', jumlah, bukti, tgl_bukti, username(rq), 'T', ''])

        with connections[tahun_log(rq)].cursor() as cursor:
            cursor.execute("""
                            INSERT INTO pertanggungjawaban.skpd_bkurincian (tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, 
                            kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, kodesubkeluaran,
                            kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, penerimaan, uname, is_bendahara_pembantu)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,[tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, 
                            '', 0, '0', 0, 0,
                            1,1,1,3,1,1, jumlah, username(rq), 'T'])
    elif jenis_bku_alt == 'KELUAR':
        pass
        frm_benda_bantu = rq.POST['frm_benda_bantu']
        frm_benda_bantu_uname = rq.POST['frm_benda_bantu_uname']
        with connections[tahun_log(rq)].cursor() as cursor:
            cursor.execute("""
                            INSERT INTO pertanggungjawaban.skpd_bku (tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, tgl_bku, urai, 
                            jenis_bku, pengeluaran, bukti, tgl_bukti, uname, is_bendahara_pembantu, bendahara_pembantu, uname_bantu)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,[tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, tgl_bku, urai,
                            'PELIMPAHAN', jumlah, bukti, tgl_bukti, username(rq), 'Y', frm_benda_bantu, frm_benda_bantu_uname])

        with connections[tahun_log(rq)].cursor() as cursor:
            cursor.execute("""
                            INSERT INTO pertanggungjawaban.skpd_bkurincian (tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, 
                            kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, kodesubkeluaran,
                            kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, pengeluaran, uname, is_bendahara_pembantu, bandahara_pembantu, uname_bantu)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,[tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_bku, 
                            '', 0, '0', 0, 0,
                            1,1,1,3,1,1, jumlah, username(rq), 'Y', frm_benda_bantu, frm_benda_bantu_uname])
    data = {
        'status':200,
    }
    return JsonResponse(data)
# 
