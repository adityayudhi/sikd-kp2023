from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods

import datetime
import json

def get_skp_skr(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)
	skpd = set_organisasi(request) 

	if skpd["kode"] == '': kode = 0
	else: kode = skpd["kode"]

	arrDT = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"],
		'akses':akses_x, 'perubahan':str(sipkd_perubahan), 'jenis':'all'}
	return render(request,'spjskpd/skp_skr.html',arrDT)

def skpskr_get_tbl_awal(request):
	tahun_x = tahun_log(request)
	data  	= request.POST
	jenis 	= int(data.get("jenis"))
	arrTBL  = []

	# print(data)

	if len(data.get("skpd"))>1:
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
				and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s and a.ISSKPD = 0 "+argtex,
				[tahun_x,int(skpd[0]),int(skpd[1]),str(skpd[2]),str(skpd[3])])
			arrTBL = ArrayFormater(dictfetchall(cursor))

	arrDT = {'arrTabel':arrTBL}
	return render(request,'spjskpd/tabel/skp_skr.html',arrDT)

def skpskr_modal_in(request):
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
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')\
				||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||a.kodesubrincianobjek AS koderekening \
				FROM penatausahaan.skp_rincian a JOIN master.master_rekening b ON b.tahun = a.tahun \
				and b.kodeakun = a.kodeakun and b.kodekelompok = a.kodekelompok and b.kodejenis = a.kodejenis \
				and b.kodeobjek = a.kodeobjek and b.koderincianobjek = a.koderincianobjek \
				and b.kodesubrincianobjek = a.kodesubrincianobjek \
				WHERE a.tahun = %s AND UPPER(a.nomor) = %s  AND kodeurusan = %s AND kodesuburusan = %s \
				AND kodeorganisasi = %s AND kodeunit = %s AND a.isskpd = 0",
				[tahun_x,nomorSKP,skpd[0],skpd[1],skpd[2],skpd[3]])
			hasil = ArrayFormater(dictfetchall(cursor))


	arrDT = {'arrJenis':arrJenis, 'arrMasa':arrMasa, 'aksi':aksi, 'no_skpskr':nomorSKP, 
		'arrTBL':hasil, 'lengTBL':len(hasil)}
	return render(request,'spjskpd/modal/skp_skr_input.html',arrDT)

def skpskr_modal_edit(request):
	tahun_x = tahun_log(request)
	data  	= request.POST
	skpd 	= data.get('skpd').split('.')
	nomor 	= data.get('nomor').upper()

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT *,case when UPPER(jenis)='SKP' then 0 else 1 end as pilih \
			FROM penatausahaan.skp WHERE tahun = %s AND UPPER(nomor) = %s \
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
			AND kodeunit = %s AND isskpd = 0 limit 1",
			[tahun_x,nomor,skpd[0],skpd[1],skpd[2],skpd[3]])
		hasil = ArrayFormater(dictfetchall(cursor))

	return JsonResponse(hasil[0])

def skpskr_modal_rek(request):
	ArrDT = {'aidirow':request.GET.get("i")}
	return render(request,'spjskpd/modal/skp_skr_rekening.html',ArrDT)

def skpskr_modal_rek_srvside(request):
	tahun_x = tahun_log(request)
	arrRinc = []
	keyword = request.GET.get('search[value]')
	dtlimit = request.GET.get('length')
	dtofset = request.GET.get('start')

	# JIKA KOLOM PENCARIAN DIISI =======
	if keyword != "":
		arg = f"and lower(KODEAKUN::text||'.'||KODEKELOMPOK::text||'.'||KODEJENIS::text\
			||'.'||LPAD(KODEOBJEK::text,2,'0')||'.'||LPAD(KODERINCIANOBJEK::text,2,'0')\
			||'.'||KODESUBRINCIANOBJEK||URAI) like '%%{keyword.lower()}%%'"
	else:
		arg = ''

	# GET JUMLAH DATA =======
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(KODEAKUN) FROM master.master_rekening WHERE TAHUN = %s \
			AND KODEAKUN = 4 AND KODEKELOMPOK <> 0 AND KODEJENIS <> 0 AND KODEOBJEK <> 0 \
			AND KODERINCIANOBJEK <> 0 AND KODESUBRINCIANOBJEK <> 0 "+arg, [tahun_x])
		hasil_row = cursor.fetchone()[0]

	# GET DATA ============================================
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT KODEAKUN||'.'||KODEKELOMPOK||'.'||KODEJENIS||'.'||LPAD(KODEOBJEK::text,2,'0')\
			||'.'||LPAD(KODERINCIANOBJEK::text,2,'0')||'.'||KODESUBRINCIANOBJEK AS KODEREKENING, URAI,\
			0 as JUMLAH FROM master.master_rekening WHERE TAHUN = %s AND KODEAKUN = 4 AND KODEKELOMPOK <> 0 \
			AND KODEJENIS <> 0 AND KODEOBJEK <> 0 AND KODERINCIANOBJEK <> 0 AND KODESUBRINCIANOBJEK <> 0 \
			"+arg+" ORDER BY KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK \
			LIMIT %s OFFSET %s", [tahun_x, dtlimit, dtofset])

		hasil = ArrayFormater(dictfetchall(cursor))

	for xs in hasil:
		arrRinc.append((xs['koderekening'],xs['urai'],0 if xs['jumlah'] is None else xs['jumlah']))

	data_query = [list(i) for i in arrRinc]

	data = {
		"recordsTotal": hasil_row,
	 	"recordsFiltered": hasil_row,
	 	"data": data_query
	}
	return JsonResponse(data)


def skpskr_set_simpan(request, jenis):
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun    = tahun_log(request)

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
		isskpd 		= 0
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
								cursor.execute("INSERT INTO penatausahaan.SKP(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,\
									JENIS,NOMOR,TANGGAL,WAJIBBAYAR,URAIAN,ALAMAT,NOMORPOKOK,MASA,JATUHTEMPO,isskpd) \
									VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
									[tahun,skpd[0],skpd[1],skpd[2],skpd[3],jenisSKP,nomorSKP,tglSKP,wajibBYR,uraianSKP,
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
			arrayDT = [tglSKP,nomorSKP,uraianSKP,jenisSKP,wajibBYR,alamatSKP,noPk_SKP,masa_SKP,tglTEMPO,tahun,skpd[0],skpd[1],skpd[2],skpd[3],nomorSKP_X]

			if (nomorSKP != nomorSKP_X):
				if ck_nomorSKP(tahun, nomorSKP) >= 1:
					isSimpan = 0
					pesan 	 = jenisSKP+' dengan nomor : "'+nomorSKP+'", sudah digunakan !!'
				else:
					isSimpan = update_skpskr(request, arrayDT)
					pesan = 'Perubahan nomor '+jenisSKP+' : '+nomorSKP_X+', berhasil disimpan !'
			else:
				isSimpan = update_skpskr(request, arrayDT)
				pesan = 'Perubahan nomor '+jenisSKP+' : '+nomorSKP_X+', berhasil disimpan !'

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN
				cursor.execute("DELETE FROM penatausahaan.SKP_RINCIAN WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nomor = %s AND isskpd = 0",
					[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nomorSKP])

				# INSERT INTO TABEL RINCIAN
				for x in range(len(KD_rek)):
					kodeArr = KD_rek[x].split(".")
					uange  	= toAngkaDec(jml_rek[x])

					if uange != '0.00':
						cursor.execute("INSERT INTO penatausahaan.SKP_RINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,\
							NOMOR,JUMLAH,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,isskpd) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nomorSKP,uange,
							kodeArr[0],kodeArr[1],kodeArr[2],kodeArr[3],kodeArr[4],kodeArr[5],isskpd])

	else: # UNTUK DELETE ======================================================
		data  = request.POST
		skpd  = data.get('skpd').split('.')
		nomor = data.get('nomer').upper()
		arrTB = {'SKP','SKP_RINCIAN'}

		with connections[tahun_log(request)].cursor() as cursor:
			for tbl in arrTB:
				cursor.execute("DELETE FROM penatausahaan."+tbl+" WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
					AND nomor IN ("+str(nomor)+") AND isskpd = 0",
					[tahun,int(skpd[0]),int(skpd[1]),str(skpd[2])])

		isSimpan = 0
		pesan = 'Data SKP / SKR berhasil dihapus'

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def update_skpskr(request, arrayDT):
	try:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("UPDATE penatausahaan.SKP SET TANGGAL = %s, NOMOR = %s, URAIAN = %s, JENIS = %s, \
				WAJIBBAYAR = %s, ALAMAT = %s, NOMORPOKOK = %s, MASA = %s, JATUHTEMPO = %s \
				WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s \
				AND NOMOR = %s AND isskpd = 0 ",arrayDT)
			pesan = 1
	except IntegrityError as e:
		pesan = 0

	return pesan

def skpskr_frm_lap(request):
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
		lapParm['file'] 			= 'penatausahaan/spjskpd/SKP.fr3'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['nomor'] 			= "'"+nomor+"'"
		lapParm['masa'] 			= masa
		lapParm['jenis'] 			= jenis
		lapParm['kodeurusan'] 		= skpd[0]
		lapParm['kodesuburusan'] 	= skpd[1]
		lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
		lapParm['kodeunit'] 		= "'"+skpd[3]+"'"
		lapParm['idpa'] 			= aidi
		lapParm['isskpd'] 			= 0

		return HttpResponse(laplink(request, lapParm))

	else:
		data 	= request.GET
		skpd 	= data.get('id').split('.')
		masa 	= data.get('ms')
		jenis 	= data.get('js')
		nomor 	= data.get('nm').replace("_","/").replace("+"," ")

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT id,nama,nip,pangkat,jabatan||' ('||nama||')' AS jabatan \
				FROM master.pejabat_skpd WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
				AND kodeorganisasi = %s AND kodeunit = %s AND jenissistem = 2 ",
				[tahun,skpd[0],skpd[1],skpd[2],skpd[3]])
			hasil = ArrayFormater(dictfetchall(cursor))
		
		arrDT = { 'ls_data':hasil, 'skpd':data.get('id'), 'masa':masa, 'nomor':nomor, 'jenis':jenis}

		return render(request,'spjskpd/laporan/skp_skr.html',arrDT)




