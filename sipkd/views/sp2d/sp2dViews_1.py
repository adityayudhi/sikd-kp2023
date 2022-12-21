from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def cek_nosp2d(request):
	tahun  = tahun_log(request)
	nosp2d = request.POST.get('nosp2d').upper()
	cinta  = ck_no_sp2d(tahun, nosp2d)

	return HttpResponse(cinta)

def sp2d_ppkdbtl(request):

	sipkd_perubahan = perubahan(request)

	arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]
	arrPeriod 	 = [{'kode':'0','nama':'-- Pilih Triwulan --'}, 
		{'kode':'1','nama':'Triwulan I'}, {'kode':'2','nama':'Triwulan II'},
		{'kode':'3','nama':'Triwulan III'}, {'kode':'4','nama':'Triwulan IV'}]

	data = {
		'ppkd':get_PPKD(request)[0],
		'perubahan':str(sipkd_perubahan),
		'arrPerubahan':arrPerubahan,
		'arrPeriode':arrPeriod,
	}
	return render(request,'sp2d/ppkdbtl.html',data)

def sp2d_ppkdbtl_tabel(request):
	data 	= request.POST
	skpd 	= data.get('skpd').split('.')
	nospm 	= data.get('nospm_x').upper()
	nosp2d 	= data.get('nosp2d_x').upper()
	tanggal = tgl_short(data.get('tgl'))
	asal 	= data.get('asal').upper()
	tahun 	= tahun_log(request)

	with connections[tahun_log(request)].cursor() as cursor:
		if(asal == 'SP2D'):
			cursor.execute("SELECT * FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun, skpd[0],skpd[1],skpd[2],nosp2d,'',0,0,tanggal,'LS_PPKD'])
		elif(asal == 'SPM'):
			cursor.execute("SELECT * FROM penatausahaan.fc_view_spm_rincian_to_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun, skpd[0],skpd[1],skpd[2],nospm,'',0,0,tanggal,'LS_PPKD'])
		hasil = dictfetchall(cursor)

	kd_rekening  = ''
	tot_sekarang = 0

	for i in range(len(hasil)):
		hasil[i].update({'nomer':1+i})
		tot_sekarang += hasil[i]['sekarang']

		if(hasil[i]['cek'] == 1):
			kd_rekening  += ",%"+hasil[i]['koderekening']+"%"

	data = {
		'kd_rekening':kd_rekening[1:],
		'tabel':hasil,
		'rupiah':tot_sekarang,
		'terbilang':terbilang(tot_sekarang)
	}

	return render(request,'sp2d/tabel/ppkdbtl.html',data)

def sp2d_ppkdbtl_sumberdana(request):
	data 	= request.POST
	tahun 	= tahun_log(request)
	skpd 	= data.get('skpd').split('.')
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
			[tahun, skpd[0],skpd[1],skpd[2],nosp2d,'',0,0,tanggal,'LS_PPKD'])
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

def sp2d_ppkdbtl_rekening(request):
	data 	= request.POST
	kdsumda = str(data.get('kode').replace("%","'"))

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.SUMBERDANAREKENING WHERE KODESUMBERDANA IN ("+kdsumda+")")
		hasil = dictfetchall(cursor)

	selek = ""
	for val in hasil:
		pelyu = str(val['kodesumberdana'])+"|"+val['urai']+"|"+val['rekening']+"|"+val['bank_asal']+"|"+val['bank']
		selek += "<option value='"+pelyu+"'>"+val['rekening']+"</option>"

	return HttpResponse(selek)

def sp2d_ppkdbtl_ambil_spm(request):
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

def sp2d_ppkdbtl_ambil_sp2d(request):
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

	print(nosp2d)

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

def sp2d_ppkdbtl_frm_lap(request):

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

def sp2d_ppkdbtl_simpan(request, jenis):
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun 	 = tahun_log(request)

	if jenis.lower() == 'upper': # JENIS UNTUK ADD dan EDIT ============================
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

		if(enpewepe == "00.000.000.0-000.000") or (enpewepe == ""): 
			npwp_x = "-"
		else: 
			npwp_x = enpewepe

		if aksi.lower() == 'true': # AKSI ADD -> INSERT ===============================
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
								tgl_saiki,'LS_PPKD',sumdana,data.get('status_keperluan'),
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

		else: # AKSI EDIT -> UPDATE ====================================================
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

		# print(rincian)

		with connections[tahun_log(request)].cursor() as cursor:
			# HAPUS TABEL RINCIAN WHERE NO.SP2D
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

	else: # UNTUK DELETE ======================================================
		skpd 	= data.get('skpd').split('.')
		nosp2d 	= data.get('nosp2d').upper()

		where 	= " WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
			AND kodeorganisasi = %s AND nosp2d = %s"

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.SP2D"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])
			cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])
			cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN"+where,[tahun,skpd[0],skpd[1],skpd[2],nosp2d])

		isSimpan = 0
		pesan = 'Data SP2D Dengan Nomor : '+nosp2d+', berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)



# FUNGSI LAPORAN SP2D [MODAL] =====================================================================================
def sp2d_laporan(request):
	akses 	= hakakses(request).upper()
	tahun 	= tahun_log(request)
	arrBln  = []

# PANGGIL CETAK LAPORAN =============================================================
	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		kd_uru  = kd_subur = kd_org = sumda_kd = jspj_ky = ''
		kd_bid  = kd_prog  = kd_keg = sumda_ur = jspj_kd = ''

		if data.get('organisasi') != "":
			skpd 	 = data.get('organisasi').split('.')
			kd_uru   = skpd[0]
			kd_subur = skpd[1]
			kd_org 	 = skpd[2]

		if data.get('kegiatan') != "":
			kegiatan = data.get('kegiatan').split('.')
			if len(kegiatan) <= 2:
				kd_bid 	 = ''
				kd_prog  = kegiatan[0]
				kd_keg 	 = kegiatan[1]
			else:
				kd_bid 	 = str(kegiatan[0]+"."+kegiatan[1])
				kd_prog  = kegiatan[2]
				kd_keg 	 = kegiatan[3]

		if data.get('sumberdana') != "":
			sumdan 	 = data.get('sumberdana').split("|")
			sumda_kd = sumdan[0]
			sumda_ur = sumdan[1]

		if data.get('jenis_spj') != "":
			jns_spj  = data.get('jenis_spj').split("|")
			jspj_ky  = jns_spj[1]
			jspj_kd  = jns_spj[0]

		jenisLap = int(data.get('jsn_lap'))
		
		lapParm['report_type'] 		= 'pdf'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['id'] 				= data.get("id_pejabat")
		lapParm['KODEURUSAN'] 		= kd_uru
		lapParm['KODESUBURUSAN'] 	= kd_subur
		lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
		lapParm['KODEORGANISASI2'] 	= kd_org
		lapParm['ORGANISASI'] 		= data.get("org_urai")
		lapParm['PERIODE'] 			= data.get("bulan_dari")+" - "+data.get("bulan_sampai")
		lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
		lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
		lapParm['tglto2'] 			= "'"+data.get("bulan_sampai")+"'"
		lapParm['ISPPKD'] 			= data.get("is_skpkd")
		lapParm['isppkd'] 			= data.get("is_skpkd")
		lapParm['KODEBIDANG'] 		= "'"+kd_bid+"'"
		lapParm['KODEBIDANG2'] 		= kd_bid
		lapParm['KODEPROGRAM'] 		= kd_prog
		lapParm['KODEKEGIATAN'] 	= kd_keg
		lapParm['KEGIATAN'] 		= data.get("keg_urai")
		lapParm['TGLCETAK'] 		= data.get("tgl_cetak_lap")

		if jenisLap == 0:
			lapParm['file'] 		= 'AKUNTANSI/KartuPengawasanUP.fr3'
		elif jenisLap == 1:
			lapParm['file'] 		= 'AKUNTANSI/KartuPengawasanTU.fr3'
		elif jenisLap == 2:
			lapParm['file'] 		= 'AKUNTANSI/KartuPengawasanRealisasiAnggaran.fr3'
			lapParm['PERIODEawal'] 	= data.get("bulan_dari")
			lapParm['periodeakhir'] = data.get("bulan_sampai")
		elif jenisLap == 3:
			lapParm['file'] 		= 'AKUNTANSI/RegisterSP2D.fr3'
		elif jenisLap == 4:
			lapParm['file'] 		= 'AKUNTANSI/RegisterSP2DRincian.fr3'
		elif jenisLap == 5:
			lapParm['file'] 		= 'AKUNTANSI/KartuPengawasanBelanja.fr3'
		elif jenisLap == 6:
			lapParm['file'] 		= 'AKUNTANSI/RekapBelanjaPPKDRincian.fr3'
			lapParm['tglfrom2'] 	= data.get("bulan_dari")
			lapParm['tglto2'] 		= data.get("bulan_sampai")
		elif jenisLap == 7:
			lapParm['file'] 		= 'AKUNTANSI/RekapBelanjaPPKD.fr3'
		elif jenisLap == 8:
			lapParm['file'] 		= 'AKUNTANSI/RekapBelanjaPPKDRincianBupatiVersion.fr3'
			lapParm['periodeawal'] 	= data.get("bulan_dari")
			lapParm['periodeakhir'] = data.get("bulan_sampai")
		elif jenisLap == 9:
			lapParm['file'] 		= 'AKUNTANSI/RekapBelanjaPPKDBupatiVersion.fr3'
		elif jenisLap == 10:
			lapParm['file'] 		= 'AKUNTANSI/RegisterSP2DAll.fr3'
		elif jenisLap == 11:
			lapParm['file'] 		= 'penatausahaan/sp2d/REKAP_REAL_SKPD_SP2D.fr3'
		elif jenisLap == 12 or jenisLap == 13:
			if jenisLap == 12:
				lapParm['file'] 	= 'penatausahaan/SPD/RekapRealisasiRekening.fr3'
			elif jenisLap == 13:
				if int(data.get("jns_belanja")) == 0:
					lapParm['file'] = 'penatausahaan/SPD/RekapRealisasiRekeningBtl.fr3'
				else:
					lapParm['file'] = 'penatausahaan/SPD/RekapRealisasiRekeningBl.fr3'
			lapParm['tglawal'] 		= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglakhir'] 	= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['PERIODEawal'] 	= data.get("bulan_dari")
			lapParm['periodeakhir'] = data.get("bulan_sampai")
			lapParm['idjenis'] 		= data.get("jns_belanja")
		elif jenisLap == 14 or jenisLap == 15:
			if jenisLap == 14:
				lapParm['file'] 	= 'SP2D/RealisasiPerSKPDPerSumberDana.fr3'
			elif jenisLap == 15:
				lapParm['file'] 	= 'SP2D/RekapPerSKPDPerSumberDana.fr3'
			lapParm['tglawal'] 		= "'"+tgl_to_db(data.get("bulan_dari"))+"'"
			lapParm['tglakhir'] 	= "'"+tgl_to_db(data.get("bulan_sampai"))+"'"
			lapParm['PERIODEawal'] 	= data.get("bulan_dari")
			lapParm['periodeakhir'] = data.get("bulan_sampai")
			lapParm['kodesumberdana'] = sumda_kd
			lapParm['sumberdana'] 	= sumda_ur
		elif jenisLap == 16 or jenisLap == 17:
			if jenisLap == 16:
				lapParm['file'] 	= 'SP2D/REKAP_PENOLAKAN_SP2D.fr3'
			elif jenisLap == 17:
				lapParm['file'] 	= 'SP2D/REGISTER_PENOLAKAN_SP2D.fr3'
			lapParm['tglawal'] 		= "'"+tgl_to_db(data.get("bulan_dari"))+"'"
			lapParm['tglakhir'] 	= "'"+tgl_to_db(data.get("bulan_sampai"))+"'"
			lapParm['PERIODEawal'] 	= data.get("bulan_dari")
			lapParm['periodeakhir'] = data.get("bulan_sampai")
		elif jenisLap == 18:
			lapParm['file'] 		= 'AKUNTANSI/RegisterSPJ.fr3'
			lapParm['jenis'] 		= jspj_ky
			lapParm['jenis1'] 		= jspj_kd
		elif jenisLap == 19:
			lapParm['file'] 		= 'AKUNTANSI/RekapSP2dTUNonSPJ.fr3'
			lapParm['qry'] 			= "where kodeurusan='"+kd_uru+"' and kodesuburusan='"+kd_subur+"' \
				and kodeorganisasi='"+kd_org+"' and jumlahspj=0 and tglkasda is not null"
		elif jenisLap == 20:
			lapParm['file'] 		= 'AKUNTANSI/RekapSP2dTUSPJ.fr3'
			lapParm['qry'] 			= "where kodeurusan='"+kd_uru+"' and kodesuburusan='"+kd_subur+"' \
				and kodeorganisasi='"+kd_org+"' and tglkasda is not null"
		elif jenisLap == 21:
			if int(data.get("is_skpkd")) == 0 and int(data.get("radiobaten")) == 0:
				lapParm['file'] 	= 'AKUNTANSI/SuratPengesahanSPJ.fr3'
			elif int(data.get("radiobaten")) == 1:
				lapParm['file'] 	= 'AKUNTANSI/SuratPengesahanSPJPenerimaanSKPD.fr3'
			elif int(data.get("is_skpkd")) == 1 and int(data.get("radiobaten")) == 1:
				lapParm['file'] 	= 'AKUNTANSI/SuratPengesahanSPJPPKD.fr3'
			lapParm['bulan']		= data.get("bulan_lap")
		elif jenisLap == 22:
			lapParm['file'] 		= 'AKUNTANSI/kertaskerjaverifikasi.fr3'
		elif jenisLap == 23:
			lapParm['file'] 		= 'SP2D/RekapPenerbitanSp2d.fr3'
			lapParm['bulan']		= data.get("bulan_lap")
			if int(data.get("bulan_lap")) == 2:
				lapParm['periodebulan']	= 'FEBRUARI'
			else:
				lapParm['periodebulan']	= 'JANUARI'

		return HttpResponse(laplink(request, lapParm))

# TAMPILKAN FORM LAPORAN [MODAL] ====================================================================
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT distinct kodesumberdana,urai FROM master.master_sumberdana ORDER BY kodesumberdana")
			sumda = dictfetchall(cursor)

		arrjns_spj = [{'key':'0','kode':'UP-GU / TU','nama':'Semua ( UP-GU / TU )'},
			{'key':'1','kode':'GU ( Ganti Uang Persediaan )','nama':'UP-GU'},
			{'key':'2','kode':'TU ( Tambahan Uang Persediaan )','nama':'TU'},
		]
		arrjns_lap = [{'kode':'0','nama':'Kartu Pengawas - Uang Persediaan'}, #0 
			{'kode':'1','nama':'Kartu Pengawas - Tambahan Uang Persediaan'}, #1
			{'kode':'2','nama':'Kartu Pengawas - Realisasi Anggaran'}, #2
			{'kode':'3','nama':'Register SP2D Per SKPD'}, #3
			{'kode':'4','nama':'Register SP2D Rincian Per SKPD'}, #4
			{'kode':'5','nama':'Kartu Kendali Belanja'}, #5
			{'kode':'6','nama':'Register PPKD'}, #6
			{'kode':'7','nama':'Rekap Register PPKD'}, #7
			{'kode':'8','nama':'Register PPKD Bupati Version'}, #8
			{'kode':'9','nama':'Rekap Register PPKD Bupati Version'}, #9
			{'kode':'10','nama':'Rekap SP2D SKPD'}, #10
			{'kode':'11','nama':'Rekap Realisasi SP2D SKPD'}, #11
			{'kode':'12','nama':'Realisasi Per SKPD Per Rekening'}, #12
			{'kode':'13','nama':'Rekapitulasi Realisasi Anggaran Per Rekening'}, #13
			{'kode':'14','nama':'Realisasi Per SKPD Persumber Dana'}, #14
			{'kode':'15','nama':'Rekapitulasi Realisasi Anggaran Per Sumber Dana'}, #15
			{'kode':'16','nama':'Rekapitulasi Surat Penolakan SP2D'}, #16
			{'kode':'17','nama':'Register Surat Penolakan SP2D'}, #17
			{'kode':'18','nama':'Register SPJ'}, #18
			{'kode':'19','nama':'Rekap SP2D TU Yang Belum di LPJ-kan'}, #19
			{'kode':'20','nama':'Rekap Sisa SP2D TU Yang di LPJ-kan'}, #20
			{'kode':'21','nama':'LPJ Fungsional Versi Akuntansi'}, #21
			{'kode':'22','nama':'Kertas Kerja'}, #22
			{'kode':'23','nama':'Rekapitulasi Penerbitan dan Pencairan SP2D'}, #23
		]

		pjbt  = get_pejabat_pengesah(request)
		skpkd = get_PPKD(request)

		aidi_bln = 1
		for i in monthList: # monthList -> array from config.py
			arrBln.append({'id':aidi_bln, 'kode':i, 'nama':monthList[i], 'tahun':tahun})
			aidi_bln += 1

		arrData = { 'akses':akses, 'jns_spj':arrjns_spj, 
			'jns_lap':arrjns_lap, 'bulan_lap':arrBln, 
			'ls_data':pjbt, 'sm_dana':sumda, 'skpkd':skpkd[0]['kode']+"|"+skpkd[0]['urai'],
		}

		return render(request,'sp2d/laporan/lap_sp2d.html',arrData)

def sp2d_laporan_skpkd(request):
	tahun = tahun_log(request)
	skpd  = request.POST.get('skpd').split(".")

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT skpkd FROM master.master_organisasi\
			WHERE tahun = %s and kodeurusan = %s \
			and kodesuburusan = %s and kodeorganisasi = %s ",[tahun,skpd[0],skpd[1],skpd[2]])
		skpkd = dictfetchall(cursor)

	return HttpResponse(skpkd[0]["skpkd"])

