from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def get_noAdvis(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()

	if(akses_x == 'ADMIN') or (akses_x == 'KABIDBELANJA') or (akses_x == 'BELANJA'):
		pisibel = 1
	else:
		pisibel = 0

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM penatausahaan.fc_otomatis_advis(%s)",[tahun_x])
		automatic = dictfetchall(cursor)

	urut_x = automatic[0]['hasil'].split("/")[0]

	data = { 'hasil':automatic[0]['hasil'], 'urutan':int(urut_x), 'pisibel':pisibel}
	# data = { 'hasil':automatic[0]['hasil'], 'urutan':automatic[0]['urutan'], 'pisibel':pisibel}

	return JsonResponse(data)

def advissp2d(request):
	data 	= request.POST
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	frm_tgl = getTgl_advis_sp2d(tahun_x)
	pejabat = get_pejabat_pengesah(request)

	if(akses_x == 'ADMIN') or (akses_x == 'KABIDBELANJA') or (akses_x == 'BELANJA'):
		pisibel = 1
	else:
		pisibel = 0

	arrDT = {'set_tgl':frm_tgl, 'pjbt_data':pejabat, 'pisibel':pisibel}

	return render(request,'sp2d/advissp2d.html',arrDT)

def sp2d_advis_tabel(request, jenis):
	data 	= request.POST
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	tanggal = data.get('tgl')
	arrRinc = arrAdv = []

	if jenis.lower() == 'draft': # DRAFT ADVIS ========================================
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT nosp2d, skpd, tanggal, jumlah, sumberdana \
				FROM penatausahaan.fc_view_cek_advis(%s,%s,%s) \
				WHERE ada = 0 ",[tahun_x, tanggal, 0])
			arrRinc = ArrayFormater(dictfetchall(cursor))

	elif jenis.lower() == 'advis': # SUDAH JADI ADVIS ========================================
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT noadvis, nosp2d, skpd, tanggal, jumlah, sumberdana, cetak, urutan \
				FROM penatausahaan.fc_view_cek_advis(%s,%s,%s) ",[tahun_x, tanggal, 1])
			arrAdv = ArrayFormater(dictfetchall(cursor))

		for i in range(len(arrAdv)):
			if str(arrAdv[i]['nosp2d']) != '':
				cekbx   = 'hidden'
				isbold  = ''
			else:
				cekbx   = ''
				isbold  = 'bold'

			arrAdv[i]['tanggal'] = arrAdv[i]['tanggal'] if arrAdv[i]['tanggal'] != '0,00' else ''
			val = str(arrAdv[i]['noadvis'])+"|"+str(arrAdv[i]['jumlah'])+"|"+str(arrAdv[i]['cetak'])+"|"+str(arrAdv[i]['urutan'])
			arrAdv[i].update({'cekbx':cekbx,'isbold':isbold,'value':val})

	arrDT = {'page':jenis.lower(), 'tab_1':arrRinc, 'tab_2':arrAdv}
	return render(request,'sp2d/tabel/advissp2d.html',arrDT)

def sp2d_advis_modal(request, jenis):
	data 	= request.GET
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	pejabat = get_pejabat_pengesah(request)
	noadvis = data.get('ad')
	tanggal = data.get('tg')
	arrRinc = []

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT DISTINCT nama, nip, pangkat FROM penatausahaan.advis_sp2d\
			WHERE tahun = %s AND noadvis = %s ",[tahun_x, noadvis])
		advis = dictfetchall(cursor)

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT nosp2d,noadvis,tanggal,jumlah,skpd,ada,cetak,urutan,informasi,jenissp2d, \
			CASE WHEN sumberdana IS null THEN 'Tidak Terklasifikasi' ELSE sumberdana END AS sumberdana \
			FROM penatausahaan.fc_edit_advis(%s,%s,%s) WHERE nosp2d not in (\
				select nosp2d from penatausahaan.advis_sp2d where tahun=%s and tanggal=%s and noadvis<>%s) \
			ORDER BY nosp2d,noadvis ASC ",[tahun_x, tanggal, noadvis, tahun_x, tanggal, noadvis])
		rinci = ArrayFormater(dictfetchall(cursor))

	arrDT = {'pjbt_data':pejabat, 'nama_pjbt':advis[0]['nama'], 'tabel':rinci}

	return render(request,'sp2d/modal/edit_advis.html',arrDT)

def sp2d_advis_simpan(request, jenis):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()

# SIMPAN DRAFT ADVIS =============================================
	if jenis.lower() == 'draft':
		data 		= request.POST
		tanggal 	= data.get('per_tgl_advis')
		noadvis 	= data.get('no_advis')
		urutan  	= data.get('advis_urut').replace(".","")
		pengesah 	= data.get('pengesah_x')
		nama 		= data.get('nama_pejabat')
		nip 		= data.get('nip_pejabat')
		pangkat 	= data.get('pangkat_pejabat')
		cekbox 		= data.getlist('chk_draft')

		# CEK NOMOR ADVIS SUDAH ADA APA BELUM =====================
		def cek_noadvis():
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT COUNT(noadvis) AS jml FROM penatausahaan.advis_sp2d \
					WHERE tahun = %s AND noadvis = %s ",[tahun_x, noadvis])
				balik = dictfetchall(cursor)
			return balik[0]['jml']

		if noadvis.upper() == '':
			pesan = 'Nomor Advis SP2D masih kosong !!'
		elif cek_noadvis() >= 1:
			pesan = 'Nomor Advis '+noadvis+' sudah ada !!'
		elif len(cekbox) == 0:
			pesan = 'Belum ada Draft Advis yang dipilih !!'
		else:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.advis_sp2d \
					WHERE tahun = %s AND noadvis = %s AND tanggal = %s ",[tahun_x, noadvis, tanggal])

			for sv in cekbox:
				obj  = sv.split('|')
				uang = toAngkaDec(obj[2])

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.advis_sp2d \
						(tahun,noadvis,nosp2d,tanggal,jumlah,pengesah,nama,nip,pangkat,sumberdana,urutan) \
						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun_x,noadvis,obj[0],tanggal,uang,pengesah,nama,nip,pangkat,obj[3],urutan])

			pesan = 'Nomor Advis '+noadvis+' berhasil disimpan.'

		return HttpResponse(pesan)

# CETAK LAPORAN ADVIS ===========================================
	elif jenis.lower() == 'advis':

		if request.method == 'POST':
			data 	= request.POST
			advis 	= data.get('inp_advis').split('|')
			tanggal = data.get('inp_tgl_advis')
			lapParm = {}

			if advis[2].upper() != 'Y':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.advis_sp2d SET cetak = %s \
						WHERE tahun = %s AND noadvis = %s ",['Y', tahun_x, advis[0]])

			lapParm['report_type'] 		= 'pdf'
			lapParm['file'] 			= 'penatausahaan/sp2d/advissp2d.fr3'
			lapParm['tahun'] 			= "'"+tahun_x+"'"
			lapParm['noadvis'] 			= "'"+advis[0]+"'"
			lapParm['tanggal'] 			= "'"+tanggal+"'"
			lapParm['urutan'] 			= advis[3]

			return HttpResponse(laplink(request, lapParm))

# SIMPAN EDIT ADVIS [from Modal] ==========================================
	elif jenis.lower() == 'edadvis':
		data 		= request.POST
		tanggal 	= data.get('tgl_advis_x')
		noadvis 	= data.get('no_advis_x')
		noadvis_ori = data.get('no_advis_ori')
		urutan  	= data.get('no_advis_x').split("/")[0].replace(".","")
		pengesah 	= data.get('pengesah_x_x')
		nama 		= data.get('nama_pejabat_x')
		nip 		= data.get('nip_pejabat_x')
		pangkat 	= data.get('pangkat_pejabat_x')
		cekbox 		= data.getlist('chk_adv_edit')
		
		if noadvis.upper() == '':
			pesan = 'Nomor Advis SP2D masih kosong !!'
		else:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.advis_sp2d \
					WHERE tahun = %s AND noadvis = %s AND tanggal = %s ",[tahun_x, noadvis, tanggal])
			
			for sv in cekbox:
				obj  = sv.split('|')
				uang = toAngkaDec(obj[2])

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.advis_sp2d \
						(tahun,noadvis,nosp2d,tanggal,jumlah,pengesah,nama,nip,pangkat,sumberdana,urutan) \
						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun_x,noadvis,obj[0],tanggal,uang,pengesah,nama,nip,pangkat,obj[3],urutan])

			pesan = 'Nomor Advis '+noadvis+' berhasil disimpan.'

		return HttpResponse(pesan)
