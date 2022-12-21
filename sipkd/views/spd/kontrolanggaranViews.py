from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def kontrolanggaran(request):
	return render(request, 'spd/kontrolanggaran.html')

def load_kontrolanggaran(request):
	list_kontrol_anggaran = ''
	kode = request.POST.get('kode','')
	isskpd = request.POST.get('isskpd','')
	jenis_load = request.POST.get('jenis_load','')

	if kode != '':
		kodeurusan = kode.split('.')[0]
		kodesuburusan = kode.split('.')[1]
		kodeorganisasi = kode.split('.')[2]

		if jenis_load=='keg':
			if isskpd == '0':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT 0, o_koderekening, o_uraian, o_pagu, o_spdkegiatan, o_sp2dkegiatan, o_sisaspdkeg, o_sisaanggaran FROM penatausahaan.fc_view_kontrol_anggaran(%s,%s,%s,%s,%s) WHERE o_isbold = 0",[tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, isskpd])
					list_kontrol_anggaran = dictfetchall(cursor)
			elif isskpd == '1':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT 0, o_koderekening, o_uraian, o_pagu, o_spdkegiatan, o_sp2dkegiatan, o_sisaspdkeg, o_sisaanggaran FROM penatausahaan.fc_view_kontrol_anggaran_ppkd(%s,%s,%s,%s,%s) WHERE o_isbold = 0",[tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, isskpd])
					list_kontrol_anggaran = dictfetchall(cursor)

		elif jenis_load=='rinci':
			array_keg = json.loads(request.POST.get('kode_keg'))
			kodekegiatan = ",".join( repr(e) for e in array_keg)

			if isskpd == '0':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT o_koderekening, o_uraian, o_pagurekening, o_spdrekening, o_sp2drekening, o_sisaspdrek, o_sisarekening,0 FROM penatausahaan.fc_view_kontrol_anggaran(%s,%s,%s,%s,%s) WHERE o_XKODEKEGIATAN IN ("+kodekegiatan+") order by o_koderekening",[tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, isskpd])
					list_kontrol_anggaran = dictfetchall(cursor)
			elif isskpd == '1':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT o_koderekening, o_uraian, o_pagurekening, o_spdrekening, o_sp2drekening, o_sisaspdrek, o_sisarekening,0 FROM penatausahaan.fc_view_kontrol_anggaran_ppkd(%s,%s,%s,%s,%s) WHERE o_XKODEKEGIATAN IN ("+kodekegiatan+") order by o_koderekening",[tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, isskpd])
					list_kontrol_anggaran = dictfetchall(cursor)

	data = {
		'list_kontrol_anggaran':convert_tuple(list_kontrol_anggaran),
	}
	return JsonResponse(data)