from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import datetime, decimal

def data_spj_skpd(request,jenis_data_spj_skpd):
    tahun   = tahun_log(request)
    skpd = set_organisasi(request)
    path = ''

    if skpd["kode"] == '': 
        kode = 0
    else: 
        kode = skpd["kode"]

    if jenis_data_spj_skpd=='data_lra':
        path = 'data_lra.html'
    elif jenis_data_spj_skpd=='data_lo':
        path = 'data_lo.html'
    elif jenis_data_spj_skpd=='data_lpe':
        path = 'data_lpe.html'

    data = {'organisasi':skpd["skpd"],
            'kd_org':kode, 
            'ur_org':skpd["urai"]
            }
    return render(request, 'spjskpd/'+path+'',data)

def get_data_spjskpd(request,jenis_data_spj_skpd):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)   
        data = request.GET.get('jenis_data', None)   

        if ((gets != '0') or (gets != '') or (gets != '0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0'
            aidi = skpd.split('.')

        if data=='data_lra':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis as koderekening, uraian, real_kemarin as jumlah FROM penatausahaan.fc_report_akrual_lra(%s,%s,%s,%s,%s,%s,%s)"
                    "  where kodejenis is not null and kodejenis<>0 ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun']), 0])
                list_data = dictfetchall(cursor)

        elif data=='data_lo':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis as koderekening, uraian, real_kemarin as jumlah FROM penatausahaan.fc_report_akrual_lo(%s,%s,%s,%s,%s,%s,%s)"
                    "  where kodejenis is not null and kodejenis<>0 ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun']), 0])
                list_data = dictfetchall(cursor)

        elif data=='data_lpe':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select NOMOR as koderekening ,uraian,REAL_KEMARIN as jumlah FROM penatausahaan.fc_report_akrual_lpe(%s,%s,%s,%s,%s,%s,%s)",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2], tgl_short(tanggal(request)['awal_tahun']), tgl_short(tanggal(request)['akhir_tahun']), 0])
                list_data = dictfetchall(cursor)

        data = {'data_spjskpd': list_data}

        return render(request, 'spjskpd/tabel/list_data_spjskpd.html', data)
    else:
        return redirect('sipkd:index')


def simpan_data_spjskpd(request,jenis_data_spj_skpd):
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
            total                = request.POST.get('total_jumlah', '')
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''

            if data=='data_lra':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lra_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 0])

                for x in range(len(rekening)):
                    pisah_rekening      = rekening[x].split('.')
                    kdakun              = pisah_rekening[0]
                    kdkelompok          = pisah_rekening[1]
                    kdjenis             = pisah_rekening[2]
                    new_jumlah = jumlah[x]

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lra_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,JUMLAH,ISSKPD)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdakun,kdkelompok,kdjenis,0,new_jumlah,0])
                        hasil = "Data LRA berhasil disimpan!"

            elif data=='data_lo':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lo_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 0])

                for x in range(len(rekening)):
                    pisah_rekening      = rekening[x].split('.')
                    kdakun              = pisah_rekening[0]
                    kdkelompok          = pisah_rekening[1]
                    kdjenis             = pisah_rekening[2]
                    new_jumlah = jumlah[x]

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lo_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,JUMLAH,ISSKPD,JUMLAHN)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdakun,kdkelompok,kdjenis,0,new_jumlah,0,total])
                        hasil = "Data LO berhasil disimpan!"

            elif data=='data_lpe':

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM akuntansi.lpe_kemarin "
                        "where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and ISSKPD = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, 0])

                for x in range(len(rekening)):
                    new_jumlah = jumlah[x]

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO akuntansi.lpe_kemarin (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODE,JUMLAH,ISSKPD,JUMLAHN)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,rekening[x],new_jumlah,0,total])
                        hasil = "Data LPE berhasil disimpan!"
            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')