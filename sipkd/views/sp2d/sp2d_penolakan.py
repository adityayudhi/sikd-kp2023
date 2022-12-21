from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def cek_nomor(tahun, notol):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT CASE WHEN count(kodeurusan) >= 1 THEN 'ya' ELSE 'tidak' END as ada \
			FROM penatausahaan.sp2dtolak WHERE tahun = %s AND notolak = %s",[str(tahun),str(notol)])
		hasil = dictfetchall(cursor)
	return hasil[0]['ada']

def cek_sp2d_tolak(tahun, notol, notol_x, aksi):

	if aksi == "false":
		if notol != notol_x:
			hasilnya = cek_nomor(tahun, notol)
		else:
			hasilnya = 'tidak'
	else:
		hasilnya = cek_nomor(tahun, notol)

	return hasilnya
	

def sp2d_penolakan(request):
	tahun_x = tahun_log(request)
	arrAfek = []
	pesan 	= request.POST.get("pesan")

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT row_number() over(ORDER BY tanggal_tolak ASC) as nomor, \
			st.kodeurusan, st.kodesuburusan, st.kodeorganisasi, urai, \
			st.kodeurusan||'.'||st.kodesuburusan||'.'||st.kodeorganisasi||'-'||urai as organisasi,\
			notolak, nospm, tanggal_tolak, tanggal_spm, sebab_tolak, keterangan_tolak, jumlahtolak, \
			jenisspm FROM penatausahaan.sp2dtolak st JOIN master.master_organisasi mo \
			ON mo.kodeurusan = st.kodeurusan AND mo.kodesuburusan = st.kodesuburusan \
			AND mo.kodeorganisasi = st.kodeorganisasi \
			WHERE st.tahun = %s ",[tahun_x])
		afektasi = dictfetchall(cursor)

		for afek in afektasi:
			afek['tanggal_tolak'] 	= tgl_indo(afek['tanggal_tolak'])
			afek['tanggal_spm'] 	= tgl_indo(afek['tanggal_spm'])
			afek['jumlahtolak'] 	= format_rp(afek['jumlahtolak'])
			
			arrAfek.append(afek)

	arrDT = {'arrAfek':arrAfek, 'pesan':pesan}

	return render(request,'sp2d/sp2d_penolakan.html',arrDT)

def sp2d_penolakan_mdl_input(request):
	tahun_x  = tahun_log(request)
	aksi 	 = str(request.GET.get("ax").lower())
	opd = kd_opd = ur_opd = notolak = tgl_tolak = nospm = tgl_spm = ''
	jumlah = jenisspm = uraian = sebab = keterangan = ''

	arrJns  = [{'kode':'nol','nama':'-- Pilih --'}, {'kode':'LS_PPKD','nama':'SPM LS-PPKD'},
		{'kode':'UP','nama':'SPM UP'}, {'kode':'GU','nama':'SPM GU'}, {'kode':'TU','nama':'SPM TU'}, 
		{'kode':'LS','nama':'SPM LS-BARJAS'}, {'kode':'GJ','nama':'SP2D LS-GAJI'}]

	if aksi == "false":
		data 		= str(request.GET.get("dt").replace("_","/").replace("+"," ")).split("|")
		skpd 		= data[1].split("-")[0].split(".")
		no_tolak 	= data[0]
		opd 		= data[1].title()
		kd_opd 		= data[1].split("-")[0]
		ur_opd 		= data[1].split("-")[1].title()

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over(ORDER BY notolak,tanggal_tolak) as nomor, \
				notolak, tanggal_tolak AS tgl_tolak, nospm, tanggal_spm AS tgl_spm, \
				TRIM(jenisspm) AS jenisspm, jumlahtolak AS jumlah, sebab_tolak, keterangan_tolak, \
				deskripsispm FROM penatausahaan.sp2dtolak \
				WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
				AND UPPER(notolak) = %s ",[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],no_tolak])
			afektasi = dictfetchall(cursor)

			for afek in afektasi:
				notolak 	= afek['notolak']
				tgl_tolak 	= tgl_indo(afek['tgl_tolak'])
				nospm 		= afek['nospm']
				tgl_spm 	= tgl_indo(afek['tgl_spm'])
				jumlah 		= format_rp(afek['jumlah'])
				jenisspm 	= afek['jenisspm'].upper()
				uraian		= afek['deskripsispm']
				sebab		= afek['sebab_tolak']
				keterangan	= afek['keterangan_tolak']

	arrDT = {'halaman':'input','aksi':aksi, 'arrJns':arrJns, 'opd':opd, 'kd_opd':kd_opd, 'ur_opd':ur_opd, 
		'notolak':notolak, 'tgl_tolak':tgl_tolak, 'nospm':nospm, 'tgl_spm':tgl_spm, 'jumlah':jumlah, 
		'jenisspm':jenisspm, 'uraian':uraian, 'sebab':sebab, 'keterangan':keterangan}

	return render(request,'sp2d/modal/sp2d_penolakan.html',arrDT)

def sp2d_penolakan_mdl_cari(request):
	tahun_x 	= tahun_log(request)
	seko_endi 	= str(request.GET.get("cr").lower()) #src_tolak  src_spm
	organisasi 	= str(request.GET.get("or").lower())
	skpd 		= organisasi.split(".")
	arrAfek 	= []

	with connections[tahun_log(request)].cursor() as cursor:
		if seko_endi == "src_spm":
			cursor.execute("SELECT row_number() over(ORDER BY sp.nospm,sp.tanggal) as nomor, \
				sp.nospm,sp.tanggal AS tgl_spm, sp.kodeurusan,sp.kodesuburusan,sp.kodeorganisasi,mo.urai,\
				TRIM(sp.jenisspm) AS jenisspm,sp.informasi,''AS notolak,''AS tgl_tolak,\
				(SELECT sum(jumlah) FROM penatausahaan.spmrincian WHERE tahun = sp.tahun AND kodeurusan = sp.kodeurusan \
				AND kodesuburusan = sp.kodesuburusan AND kodeorganisasi = sp.kodeorganisasi AND nospm = sp.nospm)AS jumlah \
				FROM penatausahaan.spm sp JOIN master.master_organisasi mo \
				ON mo.kodeurusan = sp.kodeurusan AND mo.kodesuburusan = sp.kodesuburusan AND mo.kodeorganisasi = sp.kodeorganisasi \
				WHERE sp.tahun = %s AND sp.kodeurusan = %s AND sp.kodesuburusan = %s AND sp.kodeorganisasi = %s \
				AND sp.locked = 'Y' AND sp.jenisspm NOT IN ('GU_NIHIL','TU_NIHIL') AND (sp.nospm NOT IN (SELECT nospm FROM penatausahaan.sp2dtolak \
				WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s))",
				[tahun_x,skpd[0],skpd[1],skpd[2],tahun_x,skpd[0],skpd[1],skpd[2]])
			afektasi = dictfetchall(cursor)

			for afek in afektasi:
				afek['tgl_spm'] 	= tgl_indo(afek['tgl_spm'])
				afek['jumlah'] 		= format_rp(afek['jumlah'])
				arrAfek.append(afek)

		elif seko_endi == "src_tolak":
			cursor.execute("SELECT row_number() over(ORDER BY notolak,tanggal_tolak) as nomor, \
				notolak, tanggal_tolak AS tgl_tolak, nospm, tanggal_spm AS tgl_spm, \
				TRIM(jenisspm) AS jenisspm, jumlahtolak AS jumlah, sebab_tolak, keterangan_tolak, \
				deskripsispm FROM penatausahaan.sp2dtolak \
				WHERE tahun = %s AND kodeurusan = %s \
				AND kodesuburusan = %s AND kodeorganisasi = %s ",[tahun_x,skpd[0],skpd[1],skpd[2]])
			afektasi = dictfetchall(cursor)

			for afek in afektasi:
				afek['tgl_tolak'] 	= tgl_indo(afek['tgl_tolak'])
				afek['tgl_spm'] 	= tgl_indo(afek['tgl_spm'])
				afek['jumlah'] 		= format_rp(afek['jumlah'])
				arrAfek.append(afek)
		

	arrDT = {'seko':seko_endi, 'arrAfek':arrAfek}

	return render(request,'sp2d/modal/cari_spm_tolak.html',arrDT)

def sp2d_penolakan_simpan(request,jenis):
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun 	 = tahun_log(request)

	if jenis.lower() == 'upper':
		aksi 		= data.get('aksi')
		skpd 		= data.get('organisasi').split('.')
		no_tolak 	= data.get('no_tolak').upper()
		no_tolak_x 	= data.get('no_tolak_x').upper()
		tgl_tolak 	= tgl_short(data.get('tgl_tolak'))
		no_spm 		= data.get('no_spm').upper()
		tgl_spm 	= tgl_short(data.get('tgl_spm'))
		jumlah_spm 	= toAngkaDec(data.get('jumlah_spm'))
		jenis_spm 	= data.get('jenis_spm').upper()
		uraian 		= data.get('uraian')
		sebab_tolak = data.get('sebab_tolak')
		ket_tolak 	= data.get('ket_tolak')
		cek_tolak 	= cek_sp2d_tolak(tahun, no_tolak, no_tolak_x, aksi)

# AKSI ADD -> INSERT ===============================
		if aksi.lower() == 'true':
			if no_tolak != "" and no_spm != "" and jenis_spm != "":
				if cek_tolak == 'tidak':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO penatausahaan.sp2dtolak(tahun,kodeurusan,kodesuburusan,kodeorganisasi,\
							notolak,nospm,tanggal_tolak,tanggal_spm,sebab_tolak,keterangan_tolak,jumlahtolak,\
							jenisspm,deskripsispm) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,
							skpd[0],skpd[1],skpd[2],no_tolak,no_spm,tgl_tolak,tgl_spm,sebab_tolak,ket_tolak,
							jumlah_spm,jenis_spm,uraian])

						isSimpan = 1
						pesan 	 = 'Penolakan SP2D : '+no_tolak+' berhasil disimpan !'
				else:
					isSimpan = 0
					pesan 	 = 'Nomor Tolak SP2D : '+no_tolak+' SUDAH ADA!'
			else:
				isSimpan = 0
				pesan 	 = 'Lengkapi data terlebih dahulu !'


# AKSI EDIT -> INSERT ===============================
		else: 
			if no_tolak != "" and no_spm != "" and jenis_spm != "":
				if cek_tolak == 'tidak':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.sp2dtolak SET notolak = %s, nospm = %s, tanggal_tolak = %s, \
							tanggal_spm = %s, sebab_tolak = %s, keterangan_tolak = %s, jumlahtolak = %s, \
							jenisspm = %s, deskripsispm = %s WHERE tahun = %s \
							AND kodeurusan = %s AND kodesuburusan = %s \
							AND kodeorganisasi = %s AND notolak = %s",[no_tolak,no_spm,tgl_tolak,tgl_spm,sebab_tolak,ket_tolak,
							jumlah_spm,jenis_spm,uraian,tahun,skpd[0],skpd[1],skpd[2],no_tolak_x])

					isSimpan = 1
					pesan = 'Perubahan Penolakan SP2D : '+no_tolak+' berhasil disimpan !'

				else:
					isSimpan = 0
					pesan 	 = 'Nomor Tolak SP2D : '+no_tolak+', SUDAH ADA!'
			else:
				isSimpan = 0
				pesan 	 = 'Lengkapi data terlebih dahulu !'

# UNTUK DELETE ==============================================================================================
	else:
		arrDT = request.POST.get('arrdt').split(",")

		for nomor in arrDT:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.sp2dtolak WHERE tahun = %s \
					AND notolak = %s ",[tahun,nomor])

		isSimpan = 0
		pesan = 'Data Penolakan SP2D berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def sp2d_penolakan_frm_lap(request):

	if request.method == 'POST':
		tahun 	= tahun_log(request)
		data 	= request.POST
		lapParm = {}

		lapParm['report_type'] 		= 'pdf'
		lapParm['file'] 			= 'penatausahaan/sp2d/sp2d_penolakan.fr3'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['notolak'] 			= data.get('chk_notolak_modal')
		lapParm['opdtolak'] 		= data.get('chk_opdtolak_modal')
		lapParm['id'] 				= data.get('id_pejabat')

		return HttpResponse(laplink(request, lapParm))

	else:
		list_pejabat = get_pejabat_pengesah(request)

		arrDT = {'halaman':'laporan', 'ls_data':list_pejabat}
		return render(request,'sp2d/modal/sp2d_penolakan.html',arrDT)