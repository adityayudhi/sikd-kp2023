from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json

def rinci_spm(request):
	hasil = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	nospd = request.POST.get('nospd','')

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and nospd != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nospd = %s',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,nospd])
			hasil = dictfetchall(cursor)
	data = {
		'hasil':hasil,
	}
	return JsonResponse(data)

def link_tabel_rinci_spm(request):
	data_rincian = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	nospd = request.POST.get('nospd','')
	bulan = request.POST.get('bulan','')
	jenisdpa = request.POST.get('jenisdpa','')

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT o_nodpa, o_urai, o_anggaran, o_lalu, o_sekarang, o_jumlah, o_sisa  FROM penatausahaan.fc_view_spdrincian(%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,nospd,bulan,bulan,jenisdpa])
			data_rincian = dictfetchall(cursor)
	data = {
		'data_rincian':convert_tuple(data_rincian),
	}
	
	return JsonResponse(data)

def simpan_spm(request):
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	nospd = request.POST.get('nospd','')
	bulan = request.POST.get('bulan','')
	jenisdpa = request.POST.get('jenisdpa','')
	jumlah_total = request.POST.get('jumlah_total','')
	tanggal_draft =  request.POST.get('tanggal_draft','') 
	bendahara = request.POST.get('bendahara','')
	isSimpan = request.POST.get('isSimpan','')

	jumlah = ''
	hasil = ''
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '':
		with connections[tahun_log(request)].cursor() as cursor:

			def cek_data():
				if jenisdpa=='DPA-SKPD' or jenisdpa=='DPPA-SKPD':
					cursor.execute("SELECT count(*) as jumlah, nospd  FROM penatausahaan.spd WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and jenisdpa in ('DPA-SKPD','DPPA-SKPD') and  BULAN_AWAL=%s AND BULAN_AKHIR=%s GROUP BY nospd",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,bulan,bulan])
					jumlah = cursor.fetchone()
				else:
					cursor.execute("SELECT count(*) as jumlah,nospd  FROM penatausahaan.spd WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and jenisdpa in ('DPA-PPKD','DPPA-PPKD') and  BULAN_AWAL=%s AND BULAN_AKHIR=%s GROUP BY nospd",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,bulan,bulan])
					jumlah = cursor.fetchone()
				return jumlah

			# Kalau buat SPD baru
			if isSimpan=='true': 
				if cek_data()[0]!=0:
					hasil = 'SPD pada bulan ini sudah pernah dibuat !'
				else:
					if nospd!='' or jenisdpa!='' or bendahara!='':
						try:
							cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,nospd,tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft), bendahara, bulan,bulan,jenisdpa, jumlah_total,username(request)])
							hasil = 'Simpan SPD berhasil !'
						except IntegrityError as e:
							hasil = 'Nomor SPD sudah ada !'
					else:
						hasil = 'Lengkapi data terlebih dahulu !'
			# Kalau update data SPD
			else:
				if cek_data()[0]!=0:
					cursor.execute('UPDATE penatausahaan.spd set nospd=%s, tanggal_draft=%s, tanggal=%s, tgldpa=%s, bendaharapengeluaran=%s, jenisdpa=%s, jumlahspd=%s, uname = %s WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nospd = %s',[nospd, tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft), bendahara, jenisdpa, jumlah_total,username(request),tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,cek_data()[1]])
					hasil = 'Simpan SPD berhasil !'
				else:
					if nospd!='' or jenisdpa!='' or bendahara!='':
						try:
							cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,nospd,tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft), bendahara, bulan,bulan,jenisdpa, jumlah_total,username(request)])
							hasil = 'Simpan SPD berhasil !'
						except IntegrityError as e:
							hasil = 'Nomor SPD sudah ada !'
	return HttpResponse(hasil)
