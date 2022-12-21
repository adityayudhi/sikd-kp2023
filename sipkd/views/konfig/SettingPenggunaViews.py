from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection,connections
from sipkd.config import *

def settingpengguna(request):
	akses = hakakses(request)
	tahun = tahun_log(request)
	user_list = ''

	with connections[tahun_log(request)].cursor() as cursor:
		if akses=='ADMIN':
			cursor.execute("SELECT * FROM penatausahaan.fc_sipkd_view_pengguna(%s) \
				WHERE hakakses NOT IN ('ADMIN','NONAKSES','SKPD','PPKD')",[tahun])
			user_list = dictfetchall(cursor)

		elif akses=='OPERATORSKPD':
			cursor.execute("SELECT * FROM penatausahaan.fc_sipkd_view_pengguna(%s) \
				WHERE hakakses NOT IN ('ADMIN','NONAKSES','SKPD','PPKD') \
				AND kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit = %s\
				AND uname <> %s",[tahun, sipkd_listorganisasi(request), username(request)])
			user_list = dictfetchall(cursor)

	data = {'user_list':user_list}
	return render(request, 'konfig/settingpengguna.html',data)




