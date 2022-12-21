from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *

import json
import re

def pengisianskup(request):
	return render(request, 'spd/pengisianskup.html')

def data_skup(request):
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	hasil = ''
	disabled = 1

	if kdurusan!='' and kdsuburusan!='' and kdorganisasi!='' and kdunit!='':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT noskup, to_char(tanggal, 'YYYY-mm-dd') as tanggal, tahun, jumlah, 'aksi' \
				FROM penatausahaan.sk_up WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s \
				and kodeorganisasi = %s and kodeunit = %s",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi,kdunit])
			hasil = dictfetchall(cursor)
		if cek_skup(request, kdurusan, kdsuburusan, kdorganisasi, kdunit)[0]==0:
			disabled = 0
	data = {
		'hasil':convert_tuple(hasil),
		'disabled':disabled,
	}
	return JsonResponse(data)

def modal_tambah_skup(request):
	return render(request, 'spd/modal/modal_tambah_skup.html')

def modal_edit_skup(request):
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	no_skup_db = request.POST.get('no_skup','')
	
	hasil = ''
	no_skup = ''
	tglsekarang = ''
	tahun = ''
	jumlah = ''

	if kdurusan != '' and kdsuburusan != '' and kdorganisasi != '' and kdunit!='' and no_skup_db != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.sk_up \
				WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s \
				and kodeorganisasi = %s and kodeunit = %s and noskup = %s",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_skup_db])
			hasil = dictfetchall(cursor)
	
	for x in range(len(hasil)):
		no_skup = hasil[x]['noskup']
		tglsekarang = tgl_indo(hasil[x]['tanggal'])
		tahun = hasil[x]['tahun']
		jumlah = str(hasil[x]['jumlah'])

	request.session['tahun_skup_edit'] = tahun
	request.session['kdurusan_skup_edit'] = kdurusan
	request.session['kdsuburusan_skup_edit'] = kdsuburusan
	request.session['kdorganisasi_skup_edit'] = kdorganisasi
	request.session['kdunit_skup_edit'] = kdunit
	request.session['noskup_skup_edit'] = no_skup

	data = {
		'no_skup':no_skup,
		'tglsekarang':tglsekarang,
		'tahun':tahun,
		'jumlah':jumlah,
	}
	return render(request, 'spd/modal/modal_tambah_skup.html',data)

def aksi_simpan_skup(request):

	hasil = ''
	tahun = request.POST.get('tahun', '')
	kdurusan = request.POST.get('act', '')
	kdsuburusan = request.POST.get('act', '')
	kdorganisasi = request.POST.get('act', '')
	kdunit = request.POST.get('act', '')
	no_skup = request.POST.get('no_skup', '')
	tanggal = request.POST.get('tanggal_skup', '')
	jumlah_skup = request.POST.get('jumlah', '')
	act = request.POST.get('act','')

	# 'act': ['addxx1.1.01.000 - Dinas Pendidikan']
	
	if kdurusan != '' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and no_skup != '' and tanggal != '' and jumlah_skup != '':
		kdurusan = kdurusan.split('xx')[1].split('.')[0]
		kdsuburusan = kdsuburusan.split('xx')[1].split('.')[1]
		kdorganisasi = re.sub(r"\s", "", kdorganisasi.split('xx')[1].split('.')[2])
		kdunit = re.sub(r"\s", "", kdunit.split('xx')[1].split('.')[3].split('-')[0])
		act = act.split('xx')[0]

		if act=='add':
			if cek_skup(request, kdurusan, kdsuburusan, kdorganisasi, kdunit)[0] == 0:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute('INSERT INTO penatausahaan.sk_up VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
						[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_skup, tgl_to_db(tanggal), toAngkaDec(jumlah_skup)])
					hasil = 'SKUP berhasil ditambahkan'
		elif act == 'edit':
			if request.session.get('tahun_skup_edit')!='' and request.session.get('kdurusan_skup_edit')!='' and request.session.get('kdsuburusan_skup_edit')!='' and request.session.get('kdorganisasi_skup_edit')!='' and request.session.get('noskup_skup_edit')!='':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.sk_up set tahun = %s, noskup = %s, tanggal = %s, jumlah = %s \
						WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and noskup = %s",
						[tahun_log(request), no_skup, tgl_to_db(tanggal), toAngkaDec(jumlah_skup), request.session.get('tahun_skup_edit'), request.session.get('kdurusan_skup_edit'), request.session.get('kdsuburusan_skup_edit'), request.session.get('kdorganisasi_skup_edit'), request.session['kdunit_skup_edit'], request.session.get('noskup_skup_edit')])
					hasil = 'SKUP berhasil diubah'
	
	if act == 'del':
		kdurusan = request.POST.get('kdurusan', '')
		kdsuburusan = request.POST.get('kdsuburusan', '')
		kdorganisasi = request.POST.get('kdorganisasi', '')
		kdunit = request.POST.get('kdunit','')
		no_skup = request.POST.get('no_skup', '')

		if kdurusan != '' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and no_skup != '':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.sk_up WHERE tahun = %s and kodeurusan = %s \
					and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and noskup = %s",
					[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_skup])
				hasil = 'SKUP berhasil dihapus'
	return redirect('sipkd:pengisianskup')

def cek_skup(request, kdurusan, kdsuburusan, kdorganisasi, kdunit):
	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(*) FROM penatausahaan.sk_up \
			WHERE tahun = %s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s",
			[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit])
		hasil = cursor.fetchone()
	return hasil