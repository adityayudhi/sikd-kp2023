from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json
import time	
kd_org_bendterima = ''
xbulan = ''

def akuntansiakrualppkd(request):
	jenis_akrual = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT ID,URAIAN FROM akuntansi.AKRUAL_JENIS_JURNAL where isskpd=0 ORDER BY ID")
		jenis_akrual = dictfetchall(cursor)
	print(cbjenischange(request,0))
	data = {
		'jenis_akrual':jenis_akrual,
		'disenab':cbjenischange(request,0),
	}
	return render(request, 'akuntansi/akuntansiakrualppkd.html', data)

def cbjenischange(request,jenis):
	enabled = ''
	if jenis == 0 or jenis == 1 or jenis == 2 or jenis == 3 or jenis == 5 or jenis == 6:
		enabled = ''
	else:
		enabled = 'disabled = "disabled"'
	ambilData(request)
	return enabled

def ambilData(request,jen):
	arg = ''
	if jen == 1 or jen == 2 or jen == 3 or jen == 4 or jen == 6 or jen == 7:
		arg = "WHERE IDJURNAL= "+jen+""
	elif jen == 5:
		arg = "WHERE IDJURNAL in(1,5,6,7)"
	return 'hahah'