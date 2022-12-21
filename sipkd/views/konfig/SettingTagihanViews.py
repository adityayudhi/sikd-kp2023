from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages

def settingtagihan(request):
	view_tagihan_non = '' 
	view_tagihan = ''
	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT bel_non_fisik, bel_fisik FROM penatausahaan.konfig_tgl_penagihan WHERE tahun = %s",[tahun_log(request)])
		hasil = dictfetchall(cursor)
		for hasilnya in hasil:
				view_tagihan_non = tgl_indo(hasilnya['bel_non_fisik'])
				view_tagihan = tgl_indo(hasilnya['bel_fisik'])
		
	data = {
		'view_tagihan_non':view_tagihan_non,
		'view_tagihan':view_tagihan
	}
	return render(request, 'konfig/modal/tagihan.html', data)

def savesettingtagihan(request):
	pesan = ''
	view_tagihan_non = ''
	view_tagihan = ''
	close=''
	hasil = ''
	if request.method == 'POST':
		non_fisik = request.POST.get('non_fisik', None)
		fisik = request.POST.get('fisik', None)

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT bel_non_fisik, bel_fisik FROM penatausahaan.konfig_tgl_penagihan WHERE tahun = %s",[tahun_log(request)])
			hasil = dictfetchall(cursor)
			for hasilnya in hasil:
					view_tagihan_non = tgl_indo(hasilnya['bel_non_fisik'])
					view_tagihan = tgl_indo(hasilnya['bel_fisik'])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("UPDATE penatausahaan.konfig_tgl_penagihan SET bel_non_fisik = %s, bel_fisik =%s WHERE tahun=%s",[tgl_to_db(non_fisik),tgl_to_db(fisik),tahun_log(request)])
			pesan = 'Setting Tagihan Berhasil Diganti'
			close = 'yes'
		messages.success(request, "Data berhasil Diubah!")

	data = {
        'pesan': pesan,
        'close': close
    }
	return JsonResponse(data)