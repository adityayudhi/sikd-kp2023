from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def gunihil(request):
	rekening = ''

	# if hakakses(request) == 'BELANJA':
	# 	with connections[tahun_log(request)].cursor() as cursor:
	# 		cursor.execute("SELECT * FROM apbd.fc_angg_VIEW_ORGANISASI_HAKAKSES(%s,%s)",[tahun_log(request), username(request)])
	# 		organisasi = dictfetchall(cursor)



	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT rekening FROM penatausahaan.sumberdanarekening GROUP BY rekening ")
		rekening = dictfetchall(cursor)

	data = {
		'rekening':rekening,
	}
	return render(request, 'sp2d/gunihil.html', data)