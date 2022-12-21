from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def sp2d_gaji(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)

	arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]
	arrPeriod 	 = [{'kode':'0','nama':'-- Pilih Triwulan --'}, 
		{'kode':'1','nama':'Triwulan I'}, {'kode':'2','nama':'Triwulan II'},
		{'kode':'3','nama':'Triwulan III'}, {'kode':'4','nama':'Triwulan IV'}]

	arrData = { 'akses':akses_x, 'perubahan':str(sipkd_perubahan),
		'arrPerubahan':arrPerubahan, 'arrPeriode':arrPeriod, }

	return render(request,'sp2d/sp2d_gaji.html',arrData)

def sp2d_gaji_tabel(request):
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
	arrOne = []

	if data.get('skpd') != '':
		with connections[tahun_log(request)].cursor() as cursor:
			if(asal == 'SP2D'):
				cursor.execute("SELECT * FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun, skpd[0],skpd[1],skpd[2],nosp2d,'',0,0,tanggal,'GJ'])
			elif(asal == 'SPM'):
				cursor.execute("SELECT * FROM penatausahaan.fc_view_spm_rincian_to_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun, skpd[0],skpd[1],skpd[2],nospm,'',0,0,tanggal,'GJ'])
			hasil = dictfetchall(cursor)

		for i in range(len(hasil)):
			hasil[i].update({'nomer':1+i})
			tot_sekarang += hasil[i]['sekarang']

			if(hasil[i]['cek'] == 1):
				kd_rekening  += ",%"+hasil[i]['koderekening']+"%"

		for dt in hasil:
			dt['batas'] = dt['batas'] if dt['batas'] != None else '0,00'
			arrOne.append(dt)

	else:
		tot_sekarang = 0.00

	data = { 'kd_rekening':kd_rekening[1:], 'tabel':arrOne,
		'rupiah':tot_sekarang, 'terbilang':terbilang(tot_sekarang) }

	return render(request,'sp2d/tabel/ppkdbtl.html',data)

def sp2d_gaji_sumberdana(request):
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

	if(aksi == 'true'): ARG = " "
	else: 
		ARG = "WHERE koderekening IN ("+kdreken+")"

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT distinct kodesumberdana,sumberdana "\
			"FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "+ARG+" "\
			"GROUP BY kodesumberdana,sumberdana ORDER BY kodesumberdana ASC",
			[tahun, skpd[0],skpd[1],skpd[2],nosp2d,'',0,0,tanggal,'GJ'])
		hasil = dictfetchall(cursor)

	kd_sumdan = nm_sumdan = ""

	for val in hasil:
		kdSD = str(val['kodesumberdana'])
		if(kdSD < "0" or kdSD == "None" or kdSD == ""): kode = "0"
		else: kode = kdSD

		kd_sumdan += ",%"+kode+"%"
		nm_sumdan += ",%"+val['sumberdana']+"%"

	data = {
		"KD_SUMBERDANA" : kd_sumdan[1:],
		"NM_SUMNERDANA" : nm_sumdan[1:],
	}

	return JsonResponse(data)

def sp2d_gaji_rekening(request):
	data  = request.POST
	selek = ''

	if data.get('kode') != "":
		kdsumda = str(data.get('kode').replace("%","'"))
	else:
		kdsumda = "''"

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.SUMBERDANAREKENING \
			WHERE KODESUMBERDANA::text IN ("+kdsumda+")")
		hasil = dictfetchall(cursor)

	if len(hasil) >= 1:
		for val in hasil:
			pelyu = str(val['kodesumberdana'])+"|"+val['urai']+"|"+val['rekening']+"|"+val['bank_asal']+"|"+val['bank']
			selek += "<option value='"+pelyu+"'>"+val['rekening']+"</option>"
	else:
		selek = '<option value="0">No. Rekening Bank Asal</option>'

	return HttpResponse(selek)

def sp2d_gaji_ambil_spm(request):
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

def sp2d_gaji_ambil_sp2d(request):
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

def sp2d_gaji_potongan(request):
	data 	= request.POST

	if data.get('skpd') != "":
		skpd = data.get('skpd').split('.')
	else:
		skpd = '0.0.0.0'.split('.')

	tahun_x = tahun_log(request)
	nospm   = data.get('nospm').upper()
	nosp2d 	= data.get('nosp2d').upper()
	asal 	= data.get('asal').upper()
	arrJns  = [{'kode':'0','nama':'PPn'},{'kode':'1','nama':'PPh-21'},{'kode':'2','nama':'PPh-22'},
		{'kode':'3','nama':'PPh-23'},{'kode':'4','nama':'Potongan'}]

	with connections[tahun_log(request)].cursor() as cursor:
		if asal == "SP2D":
			cursor.execute("select row_number() over() as nomor,\
				s.rekeningpotongan,s.jumlah as jumlahpotongan,s.jenispotongan,''as keterangan,\
				( select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun \
				and  r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||lpad(r.kodeobjek::text,2,'0')\
				||'.'||lpad(r.koderincianobjek::text,2,'0')=s.rekeningpotongan) from penatausahaan.sp2dpotongan s\
				where s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s\
				and s.kodeorganisasi = %s and s.nosp2d = %s",[tahun_x, skpd[0], skpd[1], skpd[2], nosp2d])

		elif asal == "SPM":
			cursor.execute("select row_number() over() as nomor,\
				s.rekeningpotongan,s.jumlah as jumlahpotongan,s.jenispotongan,''as keterangan,\
				(select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun \
				and  r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||LPAD(r.kodeobjek::text,2,'0')\
				||'.'||LPAD(r.koderincianobjek::text,2,'0')=s.rekeningpotongan) from penatausahaan.spmpotongan s\
				where s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s\
				and s.kodeorganisasi = %s and s.nospm = %s",[tahun_x, skpd[0], skpd[1], skpd[2], nospm])

		hasil = dictfetchall(cursor)

	# skpd nospm

	ArrDT = {'potongan':hasil, 'jnsPot':arrJns}

	return render(request,'sp2d/tabel/sp2d_potongan.html',ArrDT)

def sp2d_gaji_mdl_cut(request):
	data 	= request.GET
	tahun_x = tahun_log(request)
	aidirow = data.get("i")

	# with connections[tahun_log(request)].cursor() as cursor:
	# 	cursor.execute("SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0') \
	# 		||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,3,'0') AS rekeningpotongan,urai \
	# 		FROM master.master_rekening WHERE tahun = %s AND kodeakun = 2 AND kodekelompok = 1 \
	# 		AND kodejenis IN (1) AND kodesubrincianobjek <> 0 ",[tahun_x])
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select kdrek as rekeningpotongan,nmpajak as urai,kdpajak,koderekening,namarekening from master.mpajak")
		hasil = dictfetchall(cursor)

	ArrDT = {'aidirow':aidirow, 'hasil':hasil}
	return render(request,'sp2d/modal/sp2d_potongan.html',ArrDT)

def sp2d_gaji_frm_lap(request):

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

def sp2d_gaji_simpan(request, jenis):
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
		pot_kdrek 		= data.getlist('cut_kdrek')
		pot_jumlah 		= data.getlist('jml_pot')
		pot_jenis 		= data.getlist('jns_cut')

		if(enpewepe == "00.000.000.0-000.000") or (enpewepe == ""): 
			npwp_x = "-"
		else: 
			npwp_x = enpewepe
# AKSI ADD -> INSERT ===============================
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
								data.get('bendahara'),data.get('bendahara'),'',0,0,data.get('inpt_triwulan'),
								tgl_saiki,'GJ',sumdana,data.get('status_keperluan'),
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
						sumdana,data.get('bendahara'),data.get('inpt_triwulan'),tgl_saiki,data.get('status_keperluan'),
						data.get('status_keperluan'),data.get('inpt_perubahan'),data.get('status_keperluan'),
						data.get('bank_asal'),norekbankasal,data.get('norek_bendahara'),data.get('bank_bendahara'),
						npwp_x,tahun,skpd[0],skpd[1],skpd[2],nosp2d_x])

				isSimpan = 1
				pesan = 'Perubahan nomor SP2D : '+nosp2d_x+' berhasil disimpan !'

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN WHERE NO.SP2D
				cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND nosp2d = %s ",
					[tahun,skpd[0],skpd[1],skpd[2],nosp2d])

				# HAPUS TABEL POTONGAN WHERE NO.SP2D
				cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN WHERE tahun = %s \
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

				for p in range(len(pot_kdrek)):
					if pot_kdrek[p] != "":
						cursor.execute("INSERT INTO penatausahaan.SP2DPOTONGAN (TAHUN,KODEURUSAN,KODESUBURUSAN,\
							KODEORGANISASI,NOSP2D,TANGGAL,REKENINGPOTONGAN,JUMLAH,JENISPOTONGAN) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,skpd[0],skpd[1],skpd[2],nosp2d,tglsp2d,
							pot_kdrek[p],toAngkaDec(pot_jumlah[p]),pot_jenis[p]])


			
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