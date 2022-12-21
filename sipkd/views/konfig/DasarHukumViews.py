from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import json
from support.support_sipkd import *


def dasarhukum(request):
    skpd = set_organisasi(request)
    if skpd["kode"] == '':
        kode = 0
    else:
        kode = skpd["kode"]

    data = {'organisasi': skpd["skpd"], 'kd_org': kode, 'ur_org': skpd["urai"]}
    return render(request, 'konfig/dasarhukum.html', data)


# tambah ubah dasar hukum
def adddasarhukum(request):
    action = request.GET.get('act')
    nourut = request.GET.get('id')
    organisasi = request.GET.get('org')
    jenishukum = request.GET.get('jenishukum')
    nomordasarhukum = dasarhukum = tanggal = tentang = jenisdpa = ''
    max_kdtpad = []
    hasil = []
    # master dasar hukum
    if jenishukum == '0':
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT CASE WHEN max(nourut)is null THEN COALESCE(max(nourut),1) ELSE \
                    MAX(nourut)+1 END AS nourut FROM MASTER.MASTER_DASARHUKUM WHERE tahun=%s \
                    and kodeurusan = 0 and kodesuburusan = 0 and kodeorganisasi = '' and kodeunit = ''",
                    [tahun_log(request)])
                max_kdtpad = dictfetchall(cursor)
                for result in max_kdtpad:
                    nourut = result['nourut']

        if action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT * FROM MASTER.MASTER_DASARHUKUM where tahun=%s and nourut=%s \
                    and kodeurusan = 0 and kodesuburusan = 0 and kodeorganisasi = '' and kodeunit = ''",
                    [tahun_log(request), nourut])
                hasil = dictfetchall(cursor)
                for result in hasil:
                    nourut = result['nourut']
                    nomordasarhukum = result['nomordasarhukum']
                    dasarhukum = result['dasarhukum']
                    tanggal = tgl_indo(result['tanggal'])
                    tentang = result['tentang']
    elif jenishukum == '1':
        try:
            if action == 'add':
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("SELECT coalesce(max(nourut)+ 1, 1) as nourut FROM MASTER.MASTER_DASARHUKUM where tahun=%s and "
                                   "kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s", 
                                   [tahun_log(request), organisasi])
                    max_kdtpad = dictfetchall(cursor)
                    for result in max_kdtpad:
                        nourut = result['nourut']
            if action == 'edit':
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("SELECT * FROM MASTER.MASTER_DASARHUKUM where tahun=%s and nourut=%s and "
                                   "kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s",
                                   [tahun_log(request), nourut, organisasi])
                    hasil = dictfetchall(cursor)

                for result in hasil:
                    nourut = result['nourut']
                    nomordasarhukum = result['nomordasarhukum']
                    dasarhukum = result['dasarhukum']
                    tanggal = tgl_indo(result['tanggal'])
                    tentang = result['tentang']
                    jenisdpa = result['jenisdpa']
        except:
            print('An error occured.')

    pilihan_jenisdpa = ['DPA-SKPD', 'DPA-PPKD', 'DPPA-SKPD', 'DPPA-PPKD']
    data = {'nourut': nourut, 'action': action, 'nomordasarhukum': nomordasarhukum, 'dasarhukum': dasarhukum, 'tanggal': tanggal,
            'tentang': tentang,
            'jenisdpa': jenisdpa,
            'jenishukum': jenishukum,
            'organisasi': organisasi,
            'pilihan_jenisdpa': pilihan_jenisdpa}
    return render(request, 'konfig/modal/adddasarhukum.html', data)


def getdasarhukum(request):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)
        jenisHukum = request.GET.get('jenisHukum', None)
        list_hkm = []

        if jenisHukum == '0':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("select *,to_char(tanggal, 'YYYY-mm-dd') as tanggal1 from master.master_dasarhukum \
                    where tahun = %s and kodeurusan = 0 and kodesuburusan = 0 and kodeorganisasi = '' and kodeunit = '' \
                    ORDER BY nourut ASC", [tahun_log(request)])
                list_hkm = ArrayFormater(dictfetchall(cursor))
                
        elif jenisHukum == '1':

            try:
                if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
                    aidi = gets.split('.')
                else:
                    skpd = '0.0.0.0'
                    aidi = skpd.split('.')
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("select ROW_NUMBER () OVER (ORDER BY nourut) as no, kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit as organisasi,"
                                   "* from master.master_dasarhukum where tahun = %s and kodeurusan = %s  and kodesuburusan = %s and kodeorganisasi = lpad(%s,2,'0') "
                                   " and kodeunit=%s order by nourut",
                                   [tahun_log(request), aidi[0], aidi[1], aidi[2],aidi[3]])
                    list_hkm = ArrayFormater(dictfetchall(cursor))
            except:
                print('An error occured.')

        data = {'list_hkm': list_hkm, 'jenisHukum': jenisHukum}

        return render(request, 'konfig/list_dasarhukum.html', data)

    else:
        return redirect('sipkd:index')


def tgldasarhukum(request):
    if 'sipkd_username' in request.session:
        aidi = request.GET.get('id', None)

        tanggalan = "<div class='input-group'>"\
            "<input type='text' class='form-control input-sm' value='"+tglblntahun+"' placeholder='Tanggal' "\
            "id='tanggal_"+aidi+"' name='tanggal' style='cursor: pointer; text-align:center; height:22px; "\
            "font-size:11px;' readonly> <label class='input-group-addon' for='tanggal_"+aidi+"' "\
            "style='cursor: pointer; font-size:8px;'><i class='fa fa-calendar-o'></i></label></div>"

        return HttpResponse(tanggalan)

    else:
        return redirect('sipkd:index')


def savedasarhukum(request):
    hasil = ''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            action = request.POST.get('action')
            nourut = request.POST.get('nourut')
            nomordasarhukum = request.POST.get('nomordasarhukum')
            dasarhukum = request.POST.get('dasarhukum')
            tanggal = request.POST.get('tanggal')
            tentang = request.POST.get('tentang')
            jenishukum = request.POST.get('jenishukum')
            jenisdpa = request.POST.get('jenisdpa')

            if jenishukum == '0':
                if action == 'add':
                	with connections[tahun_log(request)].cursor() as cursor:
                		cursor.execute("INSERT INTO MASTER.MASTER_DASARHUKUM(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT, "
                                       "NOURUT,NOMORDASARHUKUM,DASARHUKUM,TANGGAL,TENTANG) "
                                       "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                       [tahun_log(request),0,0,'','',nourut, nomordasarhukum, dasarhukum, tgl_to_db(tanggal), tentang])
                		hasil = "Data berhasil disimpan!"
                if action == 'edit':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE MASTER.MASTER_DASARHUKUM set NOMORDASARHUKUM=%s, DASARHUKUM=%s,"
                                       "TANGGAL=%s, TENTANG=%s where tahun=%s and NOURUT=%s "
                                       "and kodeurusan = 0 and kodesuburusan = 0 and kodeorganisasi = '' and kodeunit = ''",
                                       [nomordasarhukum, dasarhukum, tgl_to_db(tanggal), tentang, tahun_log(request), nourut])
                    hasil = "Data berhasil diubah!"
            elif jenishukum == '1':
            	organisasi = request.POST.get('organisasi', None).split('.')
            	try:
	                if action == 'add':
	                    with connections[tahun_log(request)].cursor() as cursor:
	                    	cursor.execute("INSERT INTO MASTER.MASTER_DASARHUKUM(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI, "
                                       "KODEUNIT,NOURUT,NOMORDASARHUKUM,DASARHUKUM,TANGGAL,TENTANG, jenisdpa) "
                                       "VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s)",
                                       [tahun_log(request), organisasi[0], organisasi[1], organisasi[2],organisasi[3], nourut, nomordasarhukum, dasarhukum, tgl_to_db(tanggal), tentang, jenisdpa])
	                    hasil = "Data berhasil disimpan!"
	                if action == 'edit':
	                	
	                	with connections[tahun_log(request)].cursor() as cursor:
	                		cursor.execute("UPDATE MASTER.MASTER_DASARHUKUM set NOMORDASARHUKUM=%s, DASARHUKUM=%s,"
	                			"TANGGAL=%s, TENTANG=%s, JENISDPA=%s where tahun=%s and kodeurusan=%s and kodesuburusan=%s and lpad(kodeorganisasi,2,'0')=%s and kodeunit=%s and NOURUT=%s",
	                			[nomordasarhukum, dasarhukum, tgl_to_db(tanggal), tentang, jenisdpa, tahun_log(request), organisasi[0], organisasi[1], organisasi[2],organisasi[3], nourut])
	                		hasil = "Data berhasil diubah!"
            	except NameError:
            		print('An error occured.')
        return HttpResponse(hasil)

    else:
        return redirect('sipkd:index')


def deletedasarhukum(request):
    # get id
    aidi = request.POST.get('nourut')
    jenishukum = request.POST.get('jenishukum')
    organisasi = request.POST.get('org')
    hasil = ''

    if jenishukum == '0':
    	with connections[tahun_log(request)].cursor() as cursor:
    		cursor.execute("DELETE FROM MASTER.MASTER_DASARHUKUM where TAHUN=%s and NOURUT=%s \
                and kodeurusan = 0 and kodesuburusan = 0 and kodeorganisasi = '' and kodeunit = ''", 
                [tahun_log(request), aidi])
    	hasil = "Data berhasil dihapus!"
    elif jenishukum == '1':
    	with connections[tahun_log(request)].cursor() as cursor:
    		cursor.execute("DELETE FROM MASTER.MASTER_DASARHUKUM where TAHUN=%s and NOURUT=%s and "
    			"kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s ",
                [tahun_log(request), aidi, organisasi])
    	hasil = "Data berhasil dihapus!"
    # print("DELETE FROM MASTER.MASTER_DASARHUKUM where TAHUN=%s and NOURUT=%s",[tahun_log(request), aidi])
    # print(organisasi)
    return HttpResponse(hasil)
