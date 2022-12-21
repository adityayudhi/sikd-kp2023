from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def sp2d_ppkdnonangg(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)

	arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]

	arrData = { 'akses':akses_x, 
		'perubahan':str(sipkd_perubahan), 
		'arrPerubahan':arrPerubahan, 'ppkd':get_PPKD(request)[0]}

	return render(request,'sp2d/sp2d_nonangg.html',arrData)

def sp2d_nona_tabel(request):
	data 	= request.POST
	skpd 	= data.get('skpd').split('.')
	nospm 	= data.get('nospm_x').upper()
	nosp2d 	= data.get('nosp2d_x').upper()
	tanggal = tgl_short(data.get('tgl'))
	asal 	= data.get('asal').upper()
	tahun 	= tahun_log(request)
	kd_rekening  = ''
	tot_sekarang = 0
	hasil = ''


	if data.get('skpd') != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,koderekening,urai,\
				CASE WHEN lalu IS NULL THEN 0 ELSE lalu END,CASE WHEN sekarang IS NULL THEN 0 ELSE sekarang END,\
				CASE WHEN jumlah IS NULL THEN 0 ELSE jumlah END,CASE WHEN pilih IS NULL THEN 0 ELSE pilih END\
				FROM penatausahaan.fc_view_sp2dnonanggaran_rincian(%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun, skpd[0],skpd[1],skpd[2],nosp2d,tanggal,nospm,asal])
			hasil = dictfetchall(cursor)

		for i in range(len(hasil)):
			hasil[i].update({'nomer':1+i})
			tot_sekarang += hasil[i]['sekarang']

			if(hasil[i]['pilih'] == 1):
				kd_rekening  += ",%"+hasil[i]['koderekening']+"%"
	else:
		tot_sekarang = 0.00

	data = { 'kd_rekening':kd_rekening[1:], 'tabel':hasil,
		'rupiah':tot_sekarang, 'terbilang':terbilang(tot_sekarang) }

	return render(request,'sp2d/tabel/sp2d_nonangg.html',data)

def sp2d_nona_sumberdana(request):
	data 	= request.POST

	if data.get('skpd') != "":
		skpd = data.get('skpd').split('.')
	else:
		skpd = '0.0.0.0'.split('.')

	tahun 	= tahun_log(request)
	nospm 	= data.get('nospm_x').upper()
	nosp2d 	= data.get('nosp2d_x').upper()
	tanggal = tgl_short(data.get('tgl'))
	kdreken = str(data.get('kdrek').replace("%","'")) 
	aksi 	= data.get('aksi')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT distinct kodesumberdana,urai FROM penatausahaan.sumberdanarekening \
			WHERE kodesumberdana = 0 ORDER BY kodesumberdana")
		hasil = dictfetchall(cursor)

	kd_sumdan = nm_sumdan = ""

	for val in hasil:
		kdSD = str(val['kodesumberdana'])
		if(kdSD < "0" or kdSD == "None" or kdSD == ""): kode = "0"
		else: kode = kdSD

		kd_sumdan += ",%"+kode+"%"
		nm_sumdan += ",%"+val['urai']+"%"

	data = {
		"KD_SUMBERDANA" : kd_sumdan[1:],
		"NM_SUMNERDANA" : nm_sumdan[1:],
	}

	return JsonResponse(data)

def sp2d_nona_rekening(request):
	data  = request.POST
	selek = ''

	if data.get('kode') != "":
		kdsumda = str(data.get('kode').replace("%","'"))
	else:
		kdsumda = "''"

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.SUMBERDANAREKENING \
			WHERE KODESUMBERDANA::text IN ("+kdsumda+") AND rekening LIKE '%GAJI%'")
		hasil = dictfetchall(cursor)

	if len(hasil) >= 1:
		for val in hasil:
			pelyu = str(val['kodesumberdana'])+"|"+val['urai']+"|"+val['rekening']+"|"+val['bank_asal']+"|"+val['bank']
			selek += "<option value='"+pelyu+"'>"+val['rekening']+"</option>"
	else:
		selek = '<option value="0">No. Rekening Bank Asal</option>'

	return HttpResponse(selek)

def sp2d_nona_ambil_spm(request):
	data 	= request.POST
	tahun 	= tahun_log(request)
	nospm 	= data.get('nospm').upper()
	skpd 	= data.get('skpd').split('.')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select nospm, tanggal, informasi, norekbank, bank, npwp, namayangberhak, triwulan\
			from penatausahaan.spm where tahun = %s \
			and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nospm = %s",
			[tahun,skpd[0],skpd[1],skpd[2],nospm])
		hasil = dictfetchall(cursor)

	for val in hasil:
		if(val['npwp'] == '-' or val['npwp'] == ''): x_npwp = '00.000.000.0-000.000'
		else: x_npwp = val['npwp']

		nmrspm 	= val['nospm']
		tanggal = tgl_indo(val['tanggal'])
		info 	= val['informasi']
		norek 	= val['norekbank']
		bank 	= val['bank']
		npwp 	= x_npwp
		berhak 	= val['namayangberhak']
		triwul 	= val['triwulan']

	data = {'nmrspm':nmrspm, 'tanggal':tanggal, 'info':info, 'norek':norek,
		'bank':bank, 'npwp':npwp, 'berhak':berhak, 'triwul':triwul,}

	return JsonResponse(data)

def sp2d_nona_ambil_sp2d(request):
	data 	= request.POST
	tahun 	= tahun_log(request)
	nosp2d 	= data.get('nosp2d').upper()
	skpd 	= data.get('skpd').split('.')
	akses 	= hakakses(request).upper()

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.sp2d where tahun = %s \
			and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nosp2d = %s",
			[tahun,skpd[0],skpd[1],skpd[2],nosp2d])
		hasil = dictfetchall(cursor)

	if(hasil):
		for hsl in hasil:
			if(hsl['locked'] == 'T'):
				KUNCI 	= '(DRAFT)'
				PESAN 	= ''
				SIMPAN 	= '1'
				if(akses == 'BELANJA'): HAPUS = '-1' 
				else:  HAPUS = '1'
			else:
				KUNCI 	= '(DISETUJUI)'
				PESAN 	= 'SP2D Nomor: '+hsl['nosp2d']+' telah di ACC oleh pimpinan. Anda tidak diperkenankan mengedit dan menghapus SP2D tersebut!'
				SIMPAN = '-1'
				HAPUS  = '-1'

			if(hsl['npwp'] == '-' or hsl['npwp'] == ''): x_npwp = '00.000.000.0-000.000'
			else: x_npwp = hsl['npwp']

			ArrDT = {
				"NOSP2D" 		 : hsl["nosp2d"],
				"KUNCI" 		 : KUNCI,
				"LOCKED" 		 : hsl["locked"],
				"TANGGAL" 		 : tgl_indo(hsl["tanggal"]),
				"TGLSPM" 		 : tgl_indo(hsl["tglspm"]),
				"NOSPM" 		 : hsl["nospm"],
				"DESKRIPSISPM" 	 : hsl["deskripsispm"],
				"BANKASAL" 		 : hsl["bankasal"],
				"NOREKBANKASAL"  : hsl["norekbankasal"],
				"NAMAYANGBERHAK" : hsl["namayangberhak"],
				"SUMBERDANA" 	 : hsl["sumberdana"],
				"NOREKBANK" 	 : hsl["norekbank"],
				"BANK" 			 : hsl["bank"],
				"NPWP" 			 : x_npwp,
				"PERUBAHAN" 	 : hsl["perubahan"],
				"TRIWULAN" 		 : hsl["triwulan"],
				"PESAN" 		 : PESAN,
				"BTN_SIMPAN" 	 : SIMPAN,
				"BTN_HAPUS" 	 : HAPUS,
			}
	else:
		ArrDT = {'PESAN':'Data SP2D tidak ditemukan'}
		
	return JsonResponse(ArrDT)

def sp2d_nona_frm_lap(request):

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		skpd 	= data.get('id_skpd').split('.')
		tahun 	= tahun_log(request)
		nosp2d 	= data.get('no_sp2d_lap').upper()
		aidi 	= data.get('id_pejabat')
		sumdana	= str(data.get('lap_sumberdana').replace("%",""))

		lapParm['report_type'] 		= 'pdf'
		lapParm['file'] 			= 'penatausahaan/sp2d/sp2d.fr3'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['nosp2d'] 			= "'"+nosp2d+"'"
		lapParm['kodeurusan'] 		= skpd[0]
		lapParm['kodesuburusan'] 	= skpd[1]
		lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
		lapParm['id'] 				= aidi
		lapParm['sumberdana'] 		= sumdana

		return HttpResponse(laplink(request, lapParm))

	else:
		list_pejabat = get_pejabat_pengesah(request)
		data = { 'ls_data':list_pejabat }

		return render(request,'sp2d/laporan/btlppkd.html',data)

def sp2d_nona_simpan(request, jenis):
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun 	 = tahun_log(request)

# JENIS UNTUK ADD dan EDIT ============================
	if jenis.lower() == 'upper': 
		aksi 			= data.get('aksi')
		skpd 			= data.get('organisasi').split('.')
		nosp2d 			= data.get('no_sp2d').upper()
		nosp2d_x 		= data.get('no_sp2d_x').upper()
		tglsp2d 		= tgl_short(data.get('tgl_sp2d'))
		tglspm  		= tgl_short(data.get('tgl_spm'))
		tgl_saiki		= tgl_short(tgl_indo(datetime.datetime.now()))
		sumdana			= data.get('nm_sumberdana').replace("%","")
		norekbankasal 	= data.get('norek_bankasal').split('|')[2]
		duite 			= toAngkaDec(data.get('tot_sekarang'))
		rincian 		= data.getlist('checkbox')
		enpewepe 		= data.get('npwp_bendahara')

		triwul = int(arrMonth[data.get('tgl_sp2d').split(" ")[1]])
		if triwul <= 3: twln = 1
		elif triwul <= 6: twln = 2
		elif triwul <= 9: twln = 3
		else: twln = 4

		if(enpewepe == "00.000.000.0-000.000") or (enpewepe == ""): 
			npwp_x = "-"
		else: 
			npwp_x = enpewepe
# # AKSI ADD -> INSERT ===============================
		if aksi.lower() == 'true': 
			with connections[tahun_log(request)].cursor() as cursor:
				if nosp2d != '' and data.get('no_spm') != '' and data.get('organisasi') != '':
					if ck_no_sp2d(tahun, nosp2d) >= 1:
						isSimpan = 0
						pesan 	 = 'SP2D dengan nomor : '+nosp2d+', sudah digunakan !!'
					else:
						if norekbankasal != '' and data.get('bendahara') != '':
							try:
								cursor.execute("INSERT INTO penatausahaan.sp2d(tahun,kodeurusan,kodesuburusan,kodeorganisasi,\
								nosp2d,tanggal,tanggal_draft,norekbank,bank,npwp,nospm,tglspm,jumlahspm,\
								pemegangkas,namayangberhak,kodebidang,kodeprogram,kodekegiatan,triwulan,\
								lastupdate,jenissp2d,sumberdana,informasi,deskripsispm,perubahan,\
								rekeningpengeluaran,statuskeperluan,jumlahsp2d,norekbankasal,bankasal,uname) \
								values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun,skpd[0],skpd[1],skpd[2],nosp2d,tglsp2d,tglsp2d,data.get('norek_bendahara'),
								data.get('bank_bendahara'),npwp_x,data.get('no_spm'),tglspm,duite,
								data.get('bendahara'),data.get('bendahara'),'',0,0,twln,
								tgl_saiki,'NON ANGG',sumdana,data.get('status_keperluan'),
								data.get('status_keperluan'),data.get('inpt_perubahan'),'1.1.1.01.0 - Kas Daerah',
								data.get('status_keperluan'),duite,norekbankasal,
								data.get('bank_asal'),uname_x])
								
								isSimpan = 1
								pesan 	 = 'Nomor SP2D : '+nosp2d+' berhasil disimpan !'
							except IntegrityError as e:
								isSimpan = 0
								pesan 	 = 'Nomor SP2D : '+nosp2d+' sudah ada !'
						else:
							isSimpan = 0
							pesan 	 = 'Lengkapi data terlebih dahulu !'
				else:
					isSimpan = 0
					pesan 	 = 'Lengkapi data terlebih dahulu !'		
# AKSI EDIT -> UPDATE ====================================================
		else: 
			cek_lock = cek_isLocked(tahun,nosp2d_x,skpd[0],skpd[1],skpd[2])

			if cek_lock == 'Y':
				isSimpan = 0
				pesan = 'SP2D Nomor : "'+nosp2d_x+'" telah di ACC oleh pimpinan. Anda tidak diperkenankan mengedit SP2D tersebut!'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.SP2D SET nosp2d = %s, tanggal = %s, tanggal_draft = %s, \
						nospm = %s, tglspm = %s, jumlahspm = %s, jumlahsp2d = %s, pemegangkas = %s,\
						sumberdana = %s, namayangberhak = %s, triwulan = %s, lastupdate = %s, informasi = %s, \
					    deskripsispm = %s, perubahan = %s, statuskeperluan = %s, bankasal = %s, \
					    norekbankasal = %s, norekbank = %s, bank = %s, npwp = %s \
						WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
						AND NOSP2D = %s",
						[nosp2d,tglsp2d,tglsp2d,data.get('no_spm'),tglspm,duite,duite,data.get('bendahara'),
						sumdana,data.get('bendahara'),twln,tgl_saiki,data.get('status_keperluan'),
						data.get('status_keperluan'),data.get('inpt_perubahan'),data.get('status_keperluan'),
						data.get('bank_asal'),norekbankasal,data.get('norek_bendahara'),data.get('bank_bendahara'),
						npwp_x,tahun,skpd[0],skpd[1],skpd[2],nosp2d_x])

				isSimpan = 1
				pesan = 'Perubahan nomor SP2D : '+nosp2d_x+' berhasil disimpan !'

		if isSimpan == 1:
		# HAPUS TABEL RINCIAN WHERE NO.SP2D
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND nosp2d = %s ",
					[tahun,skpd[0],skpd[1],skpd[2],nosp2d])

				# INSERT INTO TABEL RINCIAN
				for val in rincian:
					hasil  = val.split("|")
					objek0 = hasil[1].split("-")
					objek1 = objek0[0].split(".")
					objek2 = objek0[1].split(".")
					uange  = toAngkaDec(hasil[2])

					if uange != '0.00':
						cursor.execute("INSERT INTO penatausahaan.SP2DRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,\
							KODEORGANISASI,NOSP2D,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,\
							KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,TANGGAL,JUMLAH) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun,skpd[0],skpd[1],skpd[2],nosp2d,objek1[0]+"."+objek1[1],objek1[3],objek1[4],
							objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],tglsp2d,uange])
			
# UNTUK DELETE ==============================================================================================
	else: 
		skpd 	= data.get('skpd').split('.')
		nosp2d 	= data.get('nosp2d').upper()

		cek_lock = cek_isLocked(tahun,nosp2d,skpd[0],skpd[1],skpd[2])

		if cek_lock == 'Y':
			isSimpan = -1
			pesan = 'SP2D Nomor : "'+nosp2d+'" telah di ACC oleh pimpinan. Anda tidak diperkenankan menghapus SP2D tersebut!'
		else:
			where 	= " WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
				AND kodeorganisasi = %s AND nosp2d = %s AND locked <> 'Y' "

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.SP2D"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])
				##cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])
				##cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])

			isSimpan = 0
			pesan = 'Data SP2D Dengan Nomor : '+nosp2d+', berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)