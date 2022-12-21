from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def tu(request):

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT rekening FROM penatausahaan.sumberdanarekening GROUP BY rekening ")
		rekening = dictfetchall(cursor)

	data = {
		'rekening':rekening,
	}
	return render(request, 'sp2d/tu.html', data)

def cekTU(request):
	hasil_cektu = ''
	skpd = request.POST.get('skpd','')
	if skpd!='':
		kd_urusan = skpd.split('.')[0]
		kd_suburusan = skpd.split('.')[1]
		kd_organisasi = skpd.split('.')[2]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select o_nosp2d from penatausahaan.fc_REPORT_REGISTER_SP2D_TU_NOTSPJ (%s)\
							where o_kodeurusan=%s  and o_kodesuburusan=%s\
							and o_kodeorganisasi=%s and o_jumlahspj=0  group by o_nosp2d",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi])
			hasil_cektu = dictfetchall(cursor)
	data = {
		'hasil_cektu':convert_tuple(hasil_cektu),
	}
	return JsonResponse(data)