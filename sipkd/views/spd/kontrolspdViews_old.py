from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json
import re

def kontrolspd(request):
	disable = ''
	list_user = ''
	cek_semua = ''

	if hakakses(request) != '' or hakakses(request) != None:
		if hakakses(request) == 'ANGGARAN':
			cek_semua = ''
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT uname, hakakses FROM penatausahaan.pengguna WHERE hakakses IN ('KABIDANGGARAN','ANGGARAN') and uname = %s GROUP BY uname, hakakses",[username(request)])
				list_user = dictfetchall(cursor)
			disable = 'disable'
		elif hakakses(request) == 'KABIDANGGARAN' or hakakses(request) == 'ADMIN':
			
			cek_semua = '<div class="col-xs-12 col-sm-2 col-md-2 col-lg-2 checkbox" id="cek_ppkd">\
		                    <label><input type="checkbox" id="semua_checked" onClick="ambil_spd()" checked>&nbsp;Semua</label>\
		                </div>'

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT uname,hakakses FROM penatausahaan.pengguna WHERE hakakses IN ('KABIDANGGARAN','ANGGARAN') GROUP BY uname,hakakses")
				list_user = dictfetchall(cursor)
			disable = ''
	data = {
		'list_user': list_user,
		'disable': disable,
		'cek_semua' : cek_semua,
	}
	return render(request, 'spd/kontrolspd.html', data)

def ambil_spd_kontrol(request):
	list_kontrol_spd = ""
	check_semua = request.POST.get('check_semua','')

	if hakakses(request) == 'ANGGARAN':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT o_urut, o_skpd, o_spd1, o_tgl1,o_spd2, o_tgl2,o_spd3, o_tgl3,o_spd4, o_tgl4,o_spd5, o_tgl5,o_spd6, o_tgl6,o_spd7, o_tgl7,o_spd8, o_tgl8,o_spd9, o_tgl9,o_spd10, o_tgl10,o_spd11, o_tgl11,o_spd12, o_tgl12, o_pembuat FROM penatausahaan.fc_view_kontrol_spd(%s) WHERE o_pembuat = %s",[tahun_log(request), username(request)])
			list_kontrol_spd = dictfetchall(cursor)
	elif hakakses(request) == 'KABIDANGGARAN' or hakakses(request) == 'ADMIN':
		with connections[tahun_log(request)].cursor() as cursor:
			if check_semua == 'true':
				cursor.execute("SELECT o_urut, o_skpd, o_spd1, o_tgl1,o_spd2, o_tgl2,o_spd3, o_tgl3,o_spd4, o_tgl4,o_spd5, o_tgl5,o_spd6, o_tgl6,o_spd7, o_tgl7,o_spd8, o_tgl8,o_spd9, o_tgl9,o_spd10, o_tgl10,o_spd11, o_tgl11,o_spd12, o_tgl12, o_pembuat FROM penatausahaan.fc_view_kontrol_spd(%s)",[tahun_log(request)])
				list_kontrol_spd = dictfetchall(cursor)
			else:
				cursor.execute("SELECT o_urut, o_skpd, o_spd1, o_tgl1,o_spd2, o_tgl2,o_spd3, o_tgl3,o_spd4, o_tgl4,o_spd5, o_tgl5,o_spd6, o_tgl6,o_spd7, o_tgl7,o_spd8, o_tgl8,o_spd9, o_tgl9,o_spd10, o_tgl10,o_spd11, o_tgl11,o_spd12, o_tgl12, o_pembuat FROM penatausahaan.fc_view_kontrol_spd(%s) WHERE o_pembuat = %s",[tahun_log(request), username(request)])
				list_kontrol_spd = dictfetchall(cursor)

	data = {
		'list_kontrol_spd': convert_tuple(list_kontrol_spd),
	}
	return JsonResponse(data)

def ambilSPDUser(request):
	user = request.POST.get('user','')
	arg = ''
	list_spd_user = ''
	if user != '':
		if hakakses(request) == 'ADMIN':
			arg = ''
		else:
			if hakakses_user(request, user)['hakakses'] == 'ANGGARAN':
				daftarnya = hakakses_user(request, user)['kode']
				
				arg = " where o_kodeurusan||'.'||o_kodesuburusan||'.'||o_kodeorganisasi in ("+daftarnya+")"
			else:
				arg = ''
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT o_urut, o_skpd, o_spd1, o_tgl1, o_spd2, o_tgl2,o_spd3, o_tgl3,o_spd4, o_tgl4,o_spd5, o_tgl5,o_spd6, o_tgl6,o_spd7, o_tgl7,o_spd8, o_tgl8,o_spd9, o_tgl9,o_spd10, o_tgl10,o_spd11, o_tgl11,o_spd12, o_tgl12, o_pembuat FROM penatausahaan.fc_view_kontrol_spd(%s)'+arg+'',[tahun_log(request)])
			list_spd_user = dictfetchall(cursor)

	data = {
		'list_spd_user': convert_tuple(list_spd_user),
	}
	return JsonResponse(data)