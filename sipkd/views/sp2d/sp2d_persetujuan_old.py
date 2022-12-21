from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

# PERSETUJUAN SP2D ========================================================================================
def persetujuansp2d(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	uname_x = username(request).upper()
	us_SKPD = ""

	if akses_x == "BELANJA":
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM public.view_organisasi_hakakses(%s,%s,%s)",[tahun_x,uname_x,2])
			otpot = dictfetchall(cursor)

			for w in otpot:
				us_SKPD += ",'"+w['output']+"'"

	else:
		us_SKPD = ","

		tgl_lod = getTgl_sp2d(tahun_x,us_SKPD[1:])
		frm_tgl = tgl_lod[0]['todb']

		# frm_tgl = datetime.datetime.now()
		# frm_tgl = frm_tgl.strftime('dd-MMM-yyyy') ##10-Feb-2021
	

	arrDT = {'us_SKPD':us_SKPD[1:], 'lastDT':frm_tgl}	

	return render(request,'sp2d/persetujuansp2d.html',arrDT)

def sp2d_persetujuan_tabel(request):
	data 	= request.POST
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	tanggal = data.get("tgl","")
	us_SKPD = data.get("usr","")
	frm_tgl = getTgl_sp2d(tahun_x,us_SKPD)

	print(data)

	if(akses_x == 'ADMIN') or (akses_x == 'KABIDBELANJA') or (akses_x == 'BELANJA'):
		disable = 1
	else:
		disable = 0

	if akses_x == "BELANJA":
		if us_SKPD != "":
			ARGTEX = " and s.kodeurusan||'.'||s.kodesuburusan||'.'||s.kodeorganisasi||'.'||s.kodeunit in ("+us_SKPD+")"
		else:
			ARGTEX = " and s.kodeurusan||'.'||s.kodesuburusan||'.'||s.kodeorganisasi||'.'||s.kodeunit in ('') order by s.nosp2d"
	else:
		ARGTEX = ""

	tab_1 = tab_2 = ""

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT s.nosp2d,s.tanggal as tanggal,s.jenissp2d, \
			(select sum (jumlah) from penatausahaan.sp2drincian sr where sr.tahun=s.tahun \
			    and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan \
			    and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d) as jumlah, \
			urai as organisasi,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,0 as pilih \
			from penatausahaan.sp2d s \
			join master.master_organisasi m on (m.tahun=s.tahun and m.kodeurusan=s.kodeurusan \
			    and m.kodesuburusan=s.kodesuburusan and m.kodeorganisasi=s.kodeorganisasi and m.kodeunit=s.kodeunit) \
			where s.tahun = %s and s.locked = 'T' AND tanggal = %s "+ARGTEX,[tahun_x,tanggal])
		hsl_1 = dictfetchall(cursor)

		cursor.execute("SELECT s.nosp2d,s.tanggal as tanggal,s.jenissp2d, \
			(select sum (jumlah) from penatausahaan.sp2drincian sr where sr.tahun=s.tahun \
				and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan \
				and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d) as jumlah, \
			urai as organisasi,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,0 as pilih \
			from penatausahaan.sp2d s \
			join master.master_organisasi m on (m.tahun=s.tahun and m.kodeurusan=s.kodeurusan \
			    and m.kodesuburusan=s.kodesuburusan and m.kodeorganisasi=s.kodeorganisasi and m.kodeunit=s.kodeunit) \
			where s.tahun = %s and s.locked = 'Y' AND tanggal = %s "+ARGTEX,[tahun_x,tanggal])
		hsl_2 = dictfetchall(cursor)


	arrDT = {'set_tgl':frm_tgl,'tab_1':ArrayFormater(hsl_1),'tab_2':ArrayFormater(hsl_2), 'pil_tgl':tanggal, 'disable':disable}

	return render(request,'sp2d/tabel/persetujuansp2d.html',arrDT)

def sp2d_persetujuan_simpan(request, jenis):
	data 	= request.POST
	tahun_x = tahun_log(request)
	lockd   = ''

	if jenis.lower() == 'draft':
		if data.get('inp_draft') != '':
			rinci = data.getlist('chk_draft')
			lockd = 'Y'
		else:
			lockd   = ''
			pesan = 'Draft SP2D belum ada yang dipilih !'

	elif jenis.lower() == 'unlock':
		if data.get('inp_unlock') != '':
			rinci = data.getlist('chk_unlock')
			lockd = 'T'
		else:
			lockd   = ''
			pesan = 'Nomor SP2D belum ada yang dipilih !'

	if lockd != '':
		for y in rinci:
			ojk = y.split("|")
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.sp2d SET locked = %s WHERE tahun = %s AND kodeurusan = %s \
					AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nosp2d = %s",
					[lockd,tahun_x,ojk[1],ojk[2],ojk[3],ojk[4],ojk[0]])

				pesan = 'SP2D berhasil disimpan.'
	
	return HttpResponse(pesan)

# PERSETUJUAN LPJ PER TANGGAL ===================================================================================
def sp2d_lockspjtgl(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	uname_x = username(request).upper()
	us_SKPD = ""
	
	if akses_x == "BELANJA":
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM public.view_organisasi_hakakses(%s,%s,%s)",[tahun_x,uname_x,2])
			otpot = dictfetchall(cursor)

			for w in otpot:
				us_SKPD += ",'"+w['output']+"'"

	else:
		us_SKPD = ""

	frm_tgl = getTgl_lpj(tahun_x,us_SKPD[1:])

	if len(frm_tgl)>=1:
		tanggalan = frm_tgl[0]['todb']
	else:
		tanggalan = tgl_short(tglblntahun)

	arrDT = {'us_SKPD':us_SKPD[1:], 'lastDT':tanggalan}	

	return render(request,'sp2d/persetujuanlpj_tgl.html',arrDT)

def sp2d_lockspjtgl_tabel(request):
	data 	= request.POST
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper() 
	us_SKPD = data.get("usr","")
	frm_tgl = getTgl_lpj(tahun_x,us_SKPD)

	if data.get("tgl","") != '':
		tanggal = data.get("tgl","")
	else:
		tanggal = tgl_short(tglblntahun)

	if akses_x == "KABIDAKUNTANSI" or akses_x == "KABIDBELANJA" or akses_x == "VERIFIKASI" or akses_x == "ADMIN":
		btn_visibel = 1
	else: 
		btn_visibel = 0

	if akses_x == "BELANJA":
		if us_SKPD != "":
			ARGTEX = " and a.kodeurusan||'.'||a.kodesuburusan||'.'||a.kodeorganisasi||'.'||a.kodeunit in ("+us_SKPD+")"
		else:
			ARGTEX = " and a.kodeurusan||'.'||a.kodesuburusan||'.'||a.kodeorganisasi||'.'||a.kodeunit in ('')"
	else:
		ARGTEX = ""

	arrOne = []
	arrTwo = []

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT NOSPJ,TGLSPJ AS tanggal,KEPERLUAN,B.URAI AS ORGANISASI,0 AS PILIH,\
			A.KODEURUSAN,A.KODESUBURUSAN,A.KODEORGANISASI,A.KODEUNIT,A.STATUS,jenis\
			FROM penatausahaan.spj_pkd  A, master.master_organisasi B\
			WHERE A.TAHUN = %s \
			AND A.TAHUN=B.TAHUN AND A.KODEURUSAN=B.KODEURUSAN AND A.KODESUBURUSAN=B.KODESUBURUSAN \
			AND A.KODEORGANISASI=B.KODEORGANISASI AND A.KODEUNIT=B.KODEUNIT \
			AND A.STATUS = 0 \
			AND TGLSPJ = %s "+ARGTEX,[tahun_x,tanggal])
		hsl_1 = dictfetchall(cursor)
		for dt in hsl_1:
			dt['tanggal'] = tgl_indo(dt['tanggal'])
			arrOne.append(dt)

		cursor.execute("SELECT NOSPJ,TGLSPJ AS tanggal,KEPERLUAN,B.URAI AS ORGANISASI,0 AS PILIH,\
			A.KODEURUSAN,A.KODESUBURUSAN,A.KODEORGANISASI,A.KODEUNIT,A.STATUS,jenis\
			FROM penatausahaan.spj_pkd  A, master.master_organisasi B\
			WHERE A.TAHUN = %s \
			AND A.TAHUN=B.TAHUN AND A.KODEURUSAN=B.KODEURUSAN AND A.KODESUBURUSAN=B.KODESUBURUSAN \
			AND A.KODEORGANISASI=B.KODEORGANISASI AND A.KODEUNIT=B.KODEUNIT \
			AND A.STATUS in (1,2) \
			AND TGLSPJ = %s "+ARGTEX,[tahun_x,tanggal])
		hsl_2 = dictfetchall(cursor)
		for dt in hsl_2:
			dt['tanggal'] = tgl_indo(dt['tanggal'])
			arrTwo.append(dt)


	arrDT = {'set_tgl':frm_tgl,'tab_1':arrOne,'tab_2':arrTwo,
		'pil_tgl':tanggal,'enabled':btn_visibel}

	return render(request,'sp2d/tabel/persetujuanlpj_tgl.html',arrDT)

def sp2d_lockspjtgl_simpan(request, jenis):
	data 	= request.POST
	tahun_x = tahun_log(request)
	uname_x = username(request).upper()
	lockd 	= pesan = ''

	if jenis.lower() == 'draft':
		if data.get('inp_draft') != '':
			rinci = data.getlist('chk_draft')
			lockd = '1'
		else:
			lockd = ''
			pesan = 'Draft SPJ yang akan disetujui, belum ada yang dipilih!'

	elif jenis.lower() == 'unlock':
		if data.get('inp_unlock') != '':
			rinci = data.getlist('chk_unlock')
			lockd = '0'
		else:
			lockd = ''
			pesan = 'Nomor SPJ belum ada yang dipilih !'

	if lockd != '':
		for y in rinci:
			ojk = y.split("|")

			if jenis.lower() == 'unlock' and int(ojk[4]) == 2:
				Pesan = 'SPJ dengan nomor '+ojk[0]+' ini telah di-GU-kan! anda tidak berhak menggantinya'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.spj_pkd SET status = %s, username = %s \
						WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
						AND kodeorganisasi = %s AND kodeunit = %s AND nospj = %s",
						[lockd,uname_x,tahun_x,ojk[1],ojk[2],ojk[3],ojk[4],ojk[0]])

				pesan = 'SPJ berhasil disimpan.'
	
	return HttpResponse(pesan)

# PERSETUJUAN LPJ PER SKPD ===================================================================================
def sp2d_lockspjskpd(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	uname_x = username(request).upper()
	us_SKPD = ""

	if akses_x == "BELANJA":
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM public.view_organisasi_hakakses(%s,%s,%s)",[tahun_x,uname_x,2])
			otpot = dictfetchall(cursor)

			for w in otpot:
				us_SKPD += ",'"+w['output']+"'"

	else:
		us_SKPD = ""

	arrDT = {'akses':akses_x,'us_SKPD':us_SKPD[1:]}	

	return render(request,'sp2d/persetujuanlpj_skpd.html',arrDT)

def sp2d_lockspjskpd_tabel(request):
	data 	= request.POST
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper() 
	us_SKPD = data.get("usr","")
	frm_tgl = getTgl_lpj(tahun_x,us_SKPD)
	tab_1 	= tab_2 = ""
	kd_uru  = kd_subur = kd_org = '0'
	arrOne 	= []
	arrTwo 	= []

	if data.get("skpd","") != '':
		skpd 	 = data.get('skpd').split('.')
		kd_uru   = skpd[0]
		kd_subur = skpd[1]
		kd_org 	 = skpd[2]
		kd_unit	 = skpd[3]

	if akses_x == "KABIDAKUNTANSI" or akses_x == "KABIDBELANJA" or akses_x == "VERIFIKASI" or akses_x == "ADMIN":
		btn_visibel = 1
	else: 
		btn_visibel = 0

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT a.*,0 as CEK FROM penatausahaan.fc_view_spj_sp2d(%s) as a WHERE STATUS = 0 \
			AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s",
			[tahun_x,kd_uru,kd_subur,kd_org,kd_unit])
		hsl_1 = dictfetchall(cursor)

		for dt in hsl_1:
			dt['tglspj'] = tgl_indo(dt['tglspj'])
			arrOne.append(dt)

		cursor.execute("SELECT a.*,0 as CEK FROM penatausahaan.fc_view_spj_sp2d(%s) as a WHERE STATUS in (1,2) \
			AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s",
			[tahun_x,kd_uru,kd_subur,kd_org,kd_unit])
		hsl_2 = dictfetchall(cursor)

		for dt in hsl_2:
			dt['tglspj'] = tgl_indo(dt['tglspj'])
			arrTwo.append(dt)

	arrDT = {'set_tgl':frm_tgl,'tab_1':arrOne,'tab_2':arrTwo,
		'pil_tgl':tanggal,'enabled':btn_visibel}

	return render(request,'sp2d/tabel/persetujuanlpj_skpd.html',arrDT)

def sp2d_lockspjskpd_simpan(request, jenis):
	data 	= request.POST
	tahun_x = tahun_log(request)
	uname_x = username(request).upper()
	lockd   = ''

	if jenis.lower() == 'draft':
		if data.get('inp_draft') != '':
			rinci = data.getlist('chk_draft')
			lockd = '1'
		else:
			lockd = ''
			pesan = 'Draft SPJ yang akan disetujui, belum ada yang dipilih!'

	elif jenis.lower() == 'unlock':
		if data.get('inp_unlock') != '':
			rinci = data.getlist('chk_unlock')
			lockd = '0'
		else:
			lockd = ''
			pesan = 'Nomor SPJ belum ada yang dipilih !'

	if lockd != '':
		for y in rinci:
			ojk = y.split("|")

			if jenis.lower() == 'unlock' and int(ojk[4]) == 2:
				Pesan = 'SPJ dengan nomor '+ojk[0]+' ini telah di-GU-kan! anda tidak berhak menggantinya'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.spj_pkd SET status = %s, username = %s \
						WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
						AND kodeorganisasi = %s AND kodeunit = %s AND nospj = %s",
						[lockd,uname_x,tahun_x,ojk[1],ojk[2],ojk[3],ojk[4],ojk[0]])

				pesan = 'SPJ berhasil disimpan.'
	
	return HttpResponse(pesan)