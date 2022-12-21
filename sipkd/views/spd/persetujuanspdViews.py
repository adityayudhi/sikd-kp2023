from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json

def persetujuanspd(request):
	return render(request, 'spd/persetujuanspd.html')

def load_draft_spd(request):
	draft = ''
	setuju = ''
	arg = ''

	if hakakses(request)=='OPERATORANGGARAN':
		if username(request) != '':
			arg = "and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ('+username(request)+')"
		else:
			arg = "and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ('')"
	else:
		arg = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT lht.nospd,lht.tglspd, lht.kodeurusan||'.'||lht.kodesuburusan||'.'||\
			lht.kodeorganisasi||'.'||lht.kodeunit||' - '||lht.skpd as skpd, lht.jenisdpa, lht.bulanawal||'-'||\
			lht.bulanakhir, lht.jumlahspd, lht.uname, 0 as CEK FROM penatausahaan.fc_view_spd_all(%s) as lht \
			WHERE LOCKED = 'T' "+arg+" and jumlahspd<>0",[tahun_log(request)])
		draft = dictfetchall(cursor)

		cursor.execute("SELECT lht.nospd,lht.tglspd, lht.kodeurusan||'.'||lht.kodesuburusan||'.'||\
			lht.kodeorganisasi||'.'||lht.kodeunit||' - '||lht.skpd as skpd, lht.jenisdpa, lht.bulanawal||'-'||\
			lht.bulanakhir, lht.jumlahspd, lht.uname, 0 as CEK FROM penatausahaan.fc_view_spd_all(%s) as lht \
			WHERE LOCKED = 'Y' "+arg+" and jumlahspd<>0",[tahun_log(request)])
		setuju = dictfetchall(cursor)


	data = {
		'draft':convert_tuple(draft),
		'setuju':convert_tuple(setuju),
	}
	return JsonResponse(data)

def setuju_draft_spd(request):
	hasil = ''
	array_draft = json.loads(request.POST.get('array_draft'))
	array_unlock = json.loads(request.POST.get('array_unlock'))
	aksi = request.POST.get('aksi','')

	if aksi != '':
		if len(array_draft)!=0 or len(array_unlock)!=0:
			if aksi == 'draft':
				for x in range(len(array_draft)):
					nospd = array_draft[x].split('_')[0]
					kdurusan = array_draft[x].split('_')[1].split(' - ')[0].split('.')[0]
					kdsuburusan = array_draft[x].split('_')[1].split(' - ')[0].split('.')[1]
					kdorganisasi = array_draft[x].split('_')[1].split(' - ')[0].split('.')[2]
					kdunit = array_draft[x].split('_')[1].split(' - ')[0].split('.')[3]

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.spd SET locked = 'Y' WHERE tahun = %s \
							and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s \
							and kodeunit = %s and nospd = %s",
							[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
						hasil = 'Data SPD berhasil disetujui'
			elif aksi == 'unlock':
				for x in range(len(array_unlock)):
					nospd = array_unlock[x].split('_')[0]
					kdurusan = array_unlock[x].split('_')[1].split(' - ')[0].split('.')[0]
					kdsuburusan = array_unlock[x].split('_')[1].split(' - ')[0].split('.')[1]
					kdorganisasi = array_unlock[x].split('_')[1].split(' - ')[0].split('.')[2]
					kdunit = array_unlock[x].split('_')[1].split(' - ')[0].split('.')[3]

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.spd SET locked = 'T' WHERE tahun = %s \
							and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s \
							and kodeunit = %s and nospd = %s",
							[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
						hasil = 'Data SPD berhasil diunlock'

	return HttpResponse(hasil)