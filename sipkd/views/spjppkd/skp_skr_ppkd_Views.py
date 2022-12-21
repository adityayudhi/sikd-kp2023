from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def get_skp_skr_ppkd(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)

	arrDT = {'ppkd':get_PPKD(request)[0], 'akses':akses_x, 'perubahan':str(sipkd_perubahan), 'jenis':'all'}
	return render(request,'spjppkd/skp_skr_ppkd.html',arrDT)

def skpskr_ppkd_get_tbl_awal(request):
	tahun_x = tahun_log(request)
	data  	= request.POST
	jenis 	= int(data.get("jenis"))
	arrTBL  = []

	if len(data.get("skpd"))>0:
		skpd = data.get("skpd").split(".")

		if jenis == 1: argtex = "and jenis = 'SKP'"
		elif jenis == 2: argtex = "and jenis = 'SKR'"
		else: argtex = ""

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT 0 as CEK, row_number() over(order by tanggal desc) as nomer, \
				nomor as no_skpskr, tanggal, jenis, uraian, (select sum(jumlah) from penatausahaan.skp_rincian b \
				where b.tahun = a.tahun and b.kodeurusan = a.kodeurusan and b.kodesuburusan = a.kodesuburusan \
				and b.kodeorganisasi = a.kodeorganisasi and b.nomor = a.nomor and b.ISSKPD = a.ISSKPD) \
				as jumlah from penatausahaan.skp a where a.tahun = %s and a.kodeurusan = %s \
				and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.ISSKPD = 1 "+argtex,
				[tahun_x,int(skpd[0]),int(skpd[1]),str(skpd[2])])
			arrTBL = ArrayFormater(dictfetchall(cursor))

	arrDT = {'arrTabel':arrTBL}
	return render(request,'spjppkd/tabel/skp_skr_ppkd.html',arrDT)

def skpskr_ppkd_modal_in(request):
	tahun_x  = tahun_log(request)
	aksi 	 = str(request.GET.get("ax").lower())
	skpd 	 = request.GET.get('id').split('.')
	nomorSKP = ""
	hasil 	 = []

	arrJenis = [{'kode':'0','nama':'SKP (Surat Ketetapan Pajak)'},{'kode':'1','nama':'SKR (Surat Ketetapan Retribusi)'}]
	arrMasa  = [{'kode':'1','nama':'Januari'}, {'kode':'2','nama':'Februari'}, {'kode':'3','nama':'Maret'}, 
		{'kode':'4','nama':'April'}, {'kode':'5','nama':'Mei'}, {'kode':'6','nama':'Juni'}, {'kode':'7','nama':'Juli'}, 
		{'kode':'8','nama':'Agustus'}, {'kode':'9','nama':'September'}, {'kode':'10','nama':'Oktober'}, 
		{'kode':'11','nama':'November'}, {'kode':'12','nama':'Desember'}]

	if aksi == "false":
		nomorSKP = str(request.GET.get("dt").replace("_","/").replace("+"," "))
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over() as nomer, urai as uraian,jumlah,\
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0') AS koderekening\
				FROM penatausahaan.skp_rincian a JOIN master.master_rekening b ON b.tahun = a.tahun and b.kodeakun = a.kodeakun\
				and b.kodekelompok = a.kodekelompok and b.kodejenis = a.kodejenis and b.kodeobjek = a.kodeobjek and b.koderincianobjek = a.koderincianobjek \
				WHERE a.tahun = %s AND UPPER(a.nomor) = %s \
				AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND a.isskpd = 1",
				[tahun_x,nomorSKP,skpd[0],skpd[1],skpd[2]])
			hasil = ArrayFormater(dictfetchall(cursor))


	arrDT = {'arrJenis':arrJenis, 'arrMasa':arrMasa, 'aksi':aksi, 'no_skpskr':nomorSKP, 
		'arrTBL':hasil, 'lengTBL':len(hasil)}
	return render(request,'spjppkd/modal/skp_skr_ppkd_input.html',arrDT)

def skpskr_ppkd_modal_edit(request):
	tahun_x = tahun_log(request)
	data  	= request.POST
	skpd 	= data.get('skpd').split('.')
	nomor 	= data.get('nomor').upper()

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT *,case when UPPER(jenis)='SKP' then 0 else 1 end as pilih \
			FROM penatausahaan.skp WHERE tahun = %s AND UPPER(nomor) = %s \
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND isskpd = 1 limit 1",
			[tahun_x,nomor,skpd[0],skpd[1],skpd[2]])
		hasil = ArrayFormater(dictfetchall(cursor))

	return JsonResponse(hasil[0])

def skpskr_ppkd_modal_rek(request):
	data 	= request.GET
	tahun_x = tahun_log(request)
	aidirow = data.get("i")

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT KODEAKUN||'.'||KODEKELOMPOK||'.'||KODEJENIS||'.'||LPAD(KODEOBJEK::text,2,'0')||'.'||LPAD(KODERINCIANOBJEK::text,2,'0') AS KODEREKENING, URAI,0 as JUMLAH \
			FROM master.master_rekening WHERE TAHUN = %s AND KODEAKUN = 4 AND KODEKELOMPOK NOT IN (0,1) \
			AND KODEJENIS <> 0 AND KODEOBJEK <> 0 AND KODERINCIANOBJEK <> 0 \
			ORDER BY KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK",[tahun_x])
		hasil = ArrayFormater(dictfetchall(cursor))

	ArrDT = {'aidirow':aidirow, 'hasil':hasil}
	return render(request,'spjppkd/modal/skp_skr_ppkd_rekening.html',ArrDT)

def skpskr_ppkd_set_simpan(request, jenis):
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun    = tahun_log(request)
	isskpd 	 = 1

	print(data)

	if jenis.lower() == 'upper': # JENIS UNTUK ADD dan EDIT ============================
		aksi 		= data.get('aksi')
		skpd 		= data.get('skpd').split(' - ')[0].split('.')
		jenisSKP 	= data.get('jenisSKP').upper()
		nomorSKP 	= data.get('no_skpskr').upper()
		nomorSKP_X 	= data.get('no_skpskr_x').upper()
		tglSKP 		= tgl_short(data.get('tgl_tetap'))	
		wajibBYR 	= data.get('wajib_skpskr')	
		uraianSKP 	= data.get('uraian')
		alamatSKP 	= data.get('alamat')
		noPk_SKP 	= data.get('no_pokok')	
		masa_SKP 	= int(data.get('masa_skpskr'))	
		tglTEMPO 	= tgl_short(data.get('tgl_tempo'))
		KD_rek 		= data.getlist('cut_kdrek')
		jml_rek 	= data.getlist('jml_pot')

		if aksi.lower() == 'true': # AKSI ADD -> INSERT ==========================================================
			if nomorSKP != '' and data.get('skpd') != '':
				if ck_nomorSKP(tahun, nomorSKP) >= 1:
					isSimpan = 0
					pesan 	 = jenisSKP+' dengan nomor : "'+nomorSKP+'", sudah digunakan !!'
				else:
					if wajibBYR != '' and noPk_SKP != '' and uraianSKP != '':
						try:
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("INSERT INTO penatausahaan.SKP(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,\
									JENIS,NOMOR,TANGGAL,WAJIBBAYAR,URAIAN,ALAMAT,NOMORPOKOK,MASA,JATUHTEMPO,isskpd) \
									VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
									[tahun,skpd[0],skpd[1],skpd[2],jenisSKP,nomorSKP,tglSKP,wajibBYR,uraianSKP,
									alamatSKP,noPk_SKP,masa_SKP,tglTEMPO,isskpd])
							
							isSimpan = 1
							pesan 	 = jenisSKP+' dengan nomor : "'+nomorSKP+'", berhasil disimpan !'
						except IntegrityError as e:
							isSimpan = 0
							pesan 	 = jenisSKP+' dengan nomor : "'+nomorSKP+'", sudah ada !'
					else:
						isSimpan = 0
						pesan 	 = 'Lengkapi data terlebih dahulu !'
			else:
				isSimpan = 0
				pesan 	 = 'Lengkapi data terlebih dahulu !'		

		else: # AKSI EDIT -> UPDATE =============================================================================
			arrayDT = [tglSKP,nomorSKP,uraianSKP,jenisSKP,wajibBYR,alamatSKP,noPk_SKP,masa_SKP,tglTEMPO,tahun,skpd[0],skpd[1],skpd[2],nomorSKP_X,isskpd]

			if (nomorSKP != nomorSKP_X):
				if ck_nomorSKP(tahun, nomorSKP) >= 1:
					isSimpan = 0
					pesan 	 = jenisSKP+' dengan nomor : "'+nomorSKP+'", sudah digunakan !!'
				else:
					isSimpan = update_skpskr_ppkd(arrayDT)
					pesan = 'Perubahan nomor '+jenisSKP+' : '+nomorSKP_X+', berhasil disimpan !'
			else:
				isSimpan = update_skpskr_ppkd(arrayDT)
				pesan = 'Perubahan nomor '+jenisSKP+' : '+nomorSKP_X+', berhasil disimpan !'

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN
				cursor.execute("DELETE FROM penatausahaan.SKP_RINCIAN WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND nomor = %s AND isskpd = %s",
					[tahun,skpd[0],skpd[1],skpd[2],nomorSKP,isskpd])

				# INSERT INTO TABEL RINCIAN
				for x in range(len(KD_rek)):
					kodeArr = KD_rek[x].split(".")
					uange  	= toAngkaDec(jml_rek[x])

					if uange != '0.00':
						cursor.execute("INSERT INTO penatausahaan.SKP_RINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,\
							NOMOR,JUMLAH,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,isskpd) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,skpd[0],skpd[1],skpd[2],nomorSKP,uange,
							kodeArr[0],kodeArr[1],kodeArr[2],kodeArr[3],kodeArr[4],isskpd])

	else: # UNTUK DELETE ======================================================
		data  = request.POST
		skpd  = data.get('skpd').split('.')
		nomor = data.get('nomer').upper()
		arrTB = {'SKP','SKP_RINCIAN'}

		with connections[tahun_log(request)].cursor() as cursor:
			for tbl in arrTB:
				cursor.execute("DELETE FROM penatausahaan."+tbl+" WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
					AND nomor IN ("+str(nomor)+") AND isskpd = %s",
					[tahun,int(skpd[0]),int(skpd[1]),str(skpd[2]),isskpd])

		isSimpan = 0
		pesan = 'Data SKP / SKR berhasil dihapus'

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def update_skpskr_ppkd(arrayDT):
	try:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("UPDATE penatausahaan.SKP SET TANGGAL = %s, NOMOR = %s, URAIAN = %s, JENIS = %s, \
				WAJIBBAYAR = %s, ALAMAT = %s, NOMORPOKOK = %s, MASA = %s, JATUHTEMPO = %s \
				WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
				AND NOMOR = %s AND isskpd = %s ",arrayDT)
			pesan = 1
	except IntegrityError as e:
		pesan = 0

	return pesan

def skpskr_ppkd_frm_lap(request):
	tahun = tahun_log(request)

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		skpd 	= data.get('id_skpd').split('.')
		nomor 	= data.get('id_nomor').upper()
		masa 	= data.get('id_masa')
		jenis 	= data.get('id_jenis')
		aidi 	= data.get('id_pejabat')

		lapParm['report_type'] 		= 'pdf'
		lapParm['file'] 			= 'penatausahaan/spjskpd/SKP_PPKD.fr3'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['nomor'] 			= "'"+nomor+"'"
		lapParm['masa'] 			= masa
		lapParm['jenis'] 			= jenis
		lapParm['kodeurusan'] 		= skpd[0]
		lapParm['kodesuburusan'] 	= skpd[1]
		lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
		lapParm['idpa'] 			= aidi
		lapParm['isskpd'] 			= 1

		return HttpResponse(laplink(request, lapParm))

	else:
		data 	= request.GET
		skpd 	= data.get('id').split('.')
		masa 	= data.get('ms')
		jenis 	= data.get('js')
		nomor 	= data.get('nm').replace("_","/").replace("+"," ")

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT id,nama,nip,pangkat,jabatan||' ('||nama||')' AS jabatan \
				FROM master.pejabat_skpkd WHERE tahun = %s AND jenissistem = 2 ",[tahun])
			hasil = ArrayFormater(dictfetchall(cursor))
		
		arrDT = { 'ls_data':hasil, 'skpd':data.get('id'), 'masa':masa, 'nomor':nomor, 'jenis':jenis}

		return render(request,'spjppkd/laporan/skp_skr_ppkd.html',arrDT)




