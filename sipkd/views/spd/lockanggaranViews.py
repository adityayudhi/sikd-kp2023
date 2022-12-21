from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def lockanggaran(request):
	return render(request, 'spd/lockanggaran.html')

def ambil_skpkd(request):
	hasil = ''
	kdurusan = request.POST.get('kode','').split('.')[0]
	kdsuburusan = request.POST.get('kode','').split('.')[1]
	kdorganisasi = request.POST.get('kode','').split('.')[2]
	kdunit = request.POST.get('kode','').split('.')[3]
	kdprogram = ''
	kdkegiatan = ''
	array = array_keg = []
	jenis = request.POST.get('jenis','')
	jenis_load = request.POST.get('jenis_load','')

	if jenis_load == 'rinci':
		array_keg = json.loads(request.POST.get('kode_keg'))

	if kdurusan != '' and kdsuburusan != '' and kdorganisasi != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select SKPKD,URAI from master.master_organisasi where tahun=%s and kodeurusan=%s \
				and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit])
			hasil = dictfetchall(cursor)

		if hasil[0]['skpkd'] == 0:
			array = ['DPA-SKPD','DPPA-SKPD']
		elif hasil[0]['skpkd'] == 1:
			array = ['DPA-SKPD','DPPA-SKPD','DPA-PPKD','DPPA-PPKD']
	
	data = {
		'array':array,
		'hasil':hasil,
		'kegiatan':convert_tuple(ambil_kegiatan(request, kdurusan,kdsuburusan,kdorganisasi,kdunit,jenis,jenis_load, ",".join( repr(e.split('_')[1]) for e in array_keg))),
	}
	return JsonResponse(data)

def ambil_kegiatan(request,kdurusan,kdsuburusan,kdorganisasi, kdunit, jenis, jenis_load, kode):
	hasil = ''
	
	if kdurusan != '' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and jenis != '' and jenis_load != '':
		if jenis_load == 'keg':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("select 0, o_koderekening, o_uraian, o_pagu, o_realisasisp2d, o_sisa, \
					o_keterangan, o_x, 0 as pilihkegiatan, o_kodebidang, o_kodeprogram, o_kodekegiatan \
					from penatausahaan.fc_view_otorisasi_anggaran(%s, %s, %s, %s, %s) WHERE o_isbold = '0'",
					[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, jenis])
				hasil = dictfetchall(cursor)

		elif jenis_load == 'rinci':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("select o_pilih, o_koderekening, o_uraian, o_pagurekening, o_realisasirekening, \
					o_sisarekening, '', o_x, 0 as pilihkegiatan, o_pagu, o_realisasisp2d, o_sisa, o_kodebidang, \
					o_kodeprogram, o_kodekegiatan from penatausahaan.fc_view_otorisasi_anggaran(%s, %s, %s, %s, %s) \
					WHERE split_part(o_koderekening, '-', 1) IN ("+kode+") ORDER BY o_koderekening",
					[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, jenis])
				hasil = dictfetchall(cursor)
				
	return hasil

def insert_lock(request):
	hasil = ''
	kode_org = request.POST.get('kode_org','');
	array_rinci = json.loads(request.POST.get('kode_rinci'))
	array_keg = json.loads(request.POST.get('kode_keg'))
	kdurusan = ''
	kdsuburusan = ''
	kdorganisasi = ''
	kdbidang = ''
	kdprogram = ''
	kdkegiatan = ''
	kdakun = ''
	kdkelompok = ''
	kdjenis = ''
	kdobjek = ''
	kdrincianobjek = ''

	# ['1.01&1&1_1.01.01.1.1', '&0&0_1.01.01.0.0']
	if kode_org!='':
		kdurusan = kode_org.split('.')[0]
		kdsuburusan = kode_org.split('.')[1]
		kdorganisasi = kode_org.split('.')[2]

		for x in range(len(array_keg)):
			kdbidang = array_keg[x].split('_')[0].split('&')[0]
			kdprogram = array_keg[x].split('_')[0].split('&')[1]
			kdkegiatan = array_keg[x].split('_')[0].split('&')[2]
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.otorisasi_anggaran WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodebidang=%s and kodeprogram=%s and kodekegiatan=%s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdbidang, kdprogram, kdkegiatan])
		
		for x in range(len(array_rinci)):
			kdbidang = array_rinci[x].split('_')[0].split('&')[0]
			kdprogram = array_rinci[x].split('_')[0].split('&')[1]
			kdkegiatan = array_rinci[x].split('_')[0].split('&')[2]

			kdakun = array_rinci[x].split('_')[1].split('-')[1].split('.')[0]
			kdkelompok = array_rinci[x].split('_')[1].split('-')[1].split('.')[1]
			kdjenis = array_rinci[x].split('_')[1].split('-')[1].split('.')[2]
			kdobjek = array_rinci[x].split('_')[1].split('-')[1].split('.')[3]
			kdrincianobjek = array_rinci[x].split('_')[1].split('-')[1].split('.')[4]

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO penatausahaan.otorisasi_anggaran (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodebidang,kodeprogram,kodekegiatan,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,uname) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdbidang, kdprogram, kdkegiatan, kdakun, kdkelompok, kdjenis, kdobjek, kdrincianobjek, username(request)])
				hasil = "Proses Berhasil"

	return HttpResponse(hasil)