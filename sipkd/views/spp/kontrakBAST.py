from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
from django.db import IntegrityError
from datetime import datetime
import urllib.parse
import pprint

pp = pprint.PrettyPrinter()

def kontrak(request):
	skpd = set_organisasi(request)     
	if skpd["kode"] == '':
		kode = 0
	else:
		kode = skpd["kode"]

	data = {
		'skpd':set_organisasi(request)['skpd'],
		'kd_org': kode,
		'ur_org':skpd["urai"]
	}

	return render(request, 'spp/kontrak.html', data)

def bast(request):
	skpd = set_organisasi(request)     
	if skpd["kode"] == '':
		kode = 0
	else:
		kode = skpd["kode"]

	data = {
		'skpd':set_organisasi(request)['skpd'],
		'kd_org': kode,
		'ur_org':skpd["urai"]
	}
	return render(request, 'spp/bast.html', data)

def tabel_kontrak(request):
	tahun_x = tahun_log(request)
	data    = request.POST
	skpd    = data.get('skpd')

	arrTBL  = []
	if skpd != '' and skpd != '0':
		skpd = skpd.split('.')
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""SELECT 0 as CEK, row_number() over() as nomer, *,
			(select case when sum(jumlah) is null then 0 else sum(jumlah) end 
			from penatausahaan.kontrakrincian where tahun=a.tahun  and kodeurusan=a.kodeurusan and kodesuburusan=a.kodesuburusan and 
			kodeorganisasi=a.kodeorganisasi and kodeunit=a.kodeunit and UPPER(nokontrak)=UPPER(a.nokontrak)) as jumlahkontrak
			from penatausahaan.kontrak a where a.tahun = %s and a.kodeurusan = %s 
			and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s""",
			[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3]])

			arrTBL = ArrayFormater(dictfetchall(cursor))
	arrDT = {'arrTabel':arrTBL}
	return render(request,'spp/tabel/tabel_kontrak.html',arrDT)

def tabel_bast(request):
	tahun_x = tahun_log(request)
	data    = request.POST
	skpd    = data.get('skpd')
	arrTBL  = []
	if skpd != '' and skpd != '0':
		skpd = skpd.split('.')
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""SELECT 0 as CEK, row_number() over() as nomer, *,
			(select case when sum(jumlah) is null then 0 else sum(jumlah) end 
			from penatausahaan.bastrincian where tahun=a.tahun  and kodeurusan=a.kodeurusan and kodesuburusan=a.kodesuburusan and 
			kodeorganisasi=a.kodeorganisasi and kodeunit=a.kodeunit and UPPER(nobast)=UPPER(a.nobast)) as jumlahbast
			from penatausahaan.bast a where a.tahun = %s and a.kodeurusan = %s 
			and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s""",
			[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3]])

			arrTBL = ArrayFormater(dictfetchall(cursor))
	arrDT = {'arrTabel':arrTBL}
	return render(request,'spp/tabel/tabel_bast.html',arrDT)

def kontrak_modal(request):
	tahun_x  = tahun_log(request)
	aksi     = str(request.GET.get("ax").lower())
	skpd     = request.GET.get('id').split('.')
	nomor_kontrak = ""
	hasil    = []

	if aksi == "false":
		# nomor_kontrak = str(request.GET.get("dt").replace("_","/").replace("+"," "))
		nomor_kontrak = urllib.parse.unquote(request.GET.get("dt"))
	arrDT = {'aksi':aksi, 'skpd':request.GET.get('id'), 'nokontrak':nomor_kontrak, 'arrTBL':hasil, 'lengTBL':len(hasil)}

	return render(request,'spp/modal/modal_kontrak_input.html',arrDT)

def bast_modal(request):
	tahun_x  = tahun_log(request)
	aksi     = str(request.GET.get("ax").lower())
	skpd     = request.GET.get('id').split('.')
	nomor_bast = ""
	hasil    = []

	if aksi == "false":
		# nomor_bast = str(request.GET.get("dt").replace("_","/").replace("+"," "))
		nomor_bast = urllib.parse.unquote(request.GET.get("dt"))

	arrDT = {'aksi':aksi, 'skpd':request.GET.get('id'), 'nobast':nomor_bast, 'arrTBL':hasil, 'lengTBL':len(hasil)}

	return render(request,'spp/modal/modal_bast_input.html',arrDT)

def modal_kontrak_edit(request):
	tahun_x = tahun_log(request)
	data    = request.POST
	skpd    = data.get('skpd').split('.')
	nomor   = data.get('nomor').upper()
	urai_kegiatan = []
	kegiatan = []
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT * FROM penatausahaan.kontrak WHERE tahun = %s AND UPPER(nokontrak) = %s 
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s limit 1""",
			[tahun_x,nomor,skpd[0],skpd[1],skpd[2],skpd[3]])
		hasil = ArrayFormater(dictfetchall(cursor))

		cursor.execute("""SELECT DISTINCT kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan 
					FROM penatausahaan.kontrakrincian
					WHERE tahun=%s and kodeurusan=%s  and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nokontrak=%s""",
			[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],nomor])
		kegiatan = ArrayFormater(dictfetchall(cursor))
		if len(kegiatan)>0:
			cursor.execute("""SELECT urai  
						FROM penatausahaan.kegiatan
						WHERE tahun=%s and kodeurusan=%s  and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and 
						kodebidang=%s  and kodeprogram=%s and kodekegiatan=%s and kodesubkegiatan=%s and kodesubkeluaran=0""",
				[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],kegiatan[0]['kodebidang'],kegiatan[0]['kodeprogram'],kegiatan[0]['kodekegiatan'],kegiatan[0]['kodesubkegiatan']])
			urai_kegiatan = ArrayFormater(dictfetchall(cursor))
	
	if len(kegiatan)>0:
		return JsonResponse({'rinci':hasil[0],'kegiatan': kegiatan[0],'urai_kegiatan': urai_kegiatan[0]})
	else:
		return JsonResponse({'rinci':hasil[0],'kegiatan': '','urai_kegiatan': ''})

def modal_bast_edit(request):
	tahun_x = tahun_log(request)
	data    = request.POST
	skpd    = data.get('skpd').split('.')
	nomor   = data.get('nomor').upper()

	urai_kegiatan = []
	kegiatan = []
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT * FROM penatausahaan.bast WHERE tahun = %s AND UPPER(nobast) = %s 
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s limit 1""",
			[tahun_x,nomor,skpd[0],skpd[1],skpd[2],skpd[3]])
		hasil = ArrayFormater(dictfetchall(cursor))

		cursor.execute("""SELECT DISTINCT kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan 
					FROM penatausahaan.bastrincian
					WHERE tahun=%s and kodeurusan=%s  and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nobast=%s""",
			[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],nomor])
		kegiatan = ArrayFormater(dictfetchall(cursor))
		
		if len(kegiatan)>0:
			cursor.execute("""SELECT urai  
						FROM penatausahaan.kegiatan
						WHERE tahun=%s and kodeurusan=%s  and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and 
						kodebidang=%s  and kodeprogram=%s and kodekegiatan=%s and kodesubkegiatan=%s and kodesubkeluaran=0""",
				[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],kegiatan[0]['kodebidang'],kegiatan[0]['kodeprogram'],kegiatan[0]['kodekegiatan'],kegiatan[0]['kodesubkegiatan']])
			urai_kegiatan = ArrayFormater(dictfetchall(cursor))
	if len(kegiatan)>0:
		return JsonResponse({'rinci':hasil[0],'kegiatan': kegiatan[0],'urai_kegiatan': urai_kegiatan[0]})
	else:
		return JsonResponse({'rinci':hasil[0],'kegiatan': '','urai_kegiatan': ''})

def get_rekening_kontrak(request):
	skpd = request.POST.get('skpd')
	nokontrak = request.POST.get('nokontrak')
	kdunit = request.POST.get('kdunit')
	bidang = request.POST.get('bidang') 
	program = request.POST.get('program') 
	kegiatan = request.POST.get('kegiatan')
	subkegiatan = request.POST.get('subkegiatan')
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
			"(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
			"(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
			"(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
			"(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
			"(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
			"(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
			" FROM penatausahaan.fc_view_spp_rincian(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) ",
			[tahun_log(request),skpd[0],skpd[1],skpd[2],kdunit,nokontrak.upper(),bidang,program,kegiatan,subkegiatan])
		list_spp = dictfetchall(cursor)
	kodekegiatan = ''
	for x in range(len(list_spp)):
		if (list_spp[x]['cek']==1):
			if(list_spp[x]['uraian']!=None):
				objek = list_spp[x]['koderekening']
				objek1 = objek.split('-') 
				koderekening = objek1[0].split('.')
				kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"
	data = {'list_spp' : ArrayFormater(list_spp),'kodekegiatan':kodekegiatan,}
	
	return render(request, 'spp/tabel/tabel_rekening_kontrak.html', data)
	
def load_kontrak(request):
	org = request.GET.get('id').split('.')     
	asal = request.GET.get('asal', None)
	args = ''

	if asal is not None:
		if asal == 'spp_barjas':
			args = """AND (select case when count(nokontrak) is null then 0 else count(nokontrak) end from penatausahaan.spp where tahun=a.tahun and kodeurusan=a.kodeurusan and kodesuburusan=a.kodesuburusan and
		kodeorganisasi=a.kodeorganisasi and kodeunit=a.kodeunit and nokontrak=a.nokontrak)<1"""
	else:
		args = """AND (select case when count(nokontrak) is null then 0 else count(nokontrak) end from penatausahaan.bast where tahun=a.tahun and kodeurusan=a.kodeurusan and kodesuburusan=a.kodesuburusan and
		kodeorganisasi=a.kodeorganisasi and kodeunit=a.kodeunit and nokontrak=a.nokontrak)<1"""
		
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute(f"""SELECT *,
		(select case when sum(jumlah) is null then 0 else sum(jumlah) end 
		from penatausahaan.kontrakrincian where tahun=a.tahun  and kodeurusan=a.kodeurusan and kodesuburusan=a.kodesuburusan and 
		kodeorganisasi=a.kodeorganisasi and kodeunit=a.kodeunit and UPPER(nokontrak)=UPPER(a.nokontrak)) as jumlahkontrak
		from penatausahaan.kontrak a where a.tahun = %s and a.kodeurusan = %s 
		and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
		{args}""",
		[tahun_log(request),org[0],org[1],org[2],org[3]])
		list_kontrak = dictfetchall(cursor)

	data = {'list_kontrak' : list_kontrak}
	return render(request,'spp/modal/modal_list_kontrak.html',data)

def loadkegiatan_kontrak(request):
	org = request.GET.get('id').split('.')     

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute(" SELECT k.KODEUNIT,k.kodeurusan||'.'||lpad(k.kodesuburusan::text,2,'0') as kodebidang,\
			0 as kodeprogram,'0' as KODEKEGIATAN,0 as KODESUBKEGIATAN,'PENGELUARAN PEMBIAYAAN' URAI,\
			(select urai from master.master_organisasi ms where ms.tahun = k.tahun \
			and ms.kodeurusan = k.kodeurusan and ms.kodesuburusan = k.kodesuburusan \
			and ms.kodeorganisasi = k.kodeorganisasi and ms.kodeunit = k.kodeunit)as URAIUNIT \
			FROM PENATAUSAHAAN.pembiayaan k WHERE k.tahun=%s and k.KODEURUSAN=%s and k.KODESUBURUSAN=%s\
			and k.KODEORGANISASI=%s and k.kodeunit=%s and k.kodeakun=6  and k.kodekelompok=2 union \
			SELECT k.KODEUNIT,k.KODEBIDANG,k.KODEPROGRAM,k.KODEKEGIATAN,k.KODESUBKEGIATAN,k.URAI,\
			(select urai from master.master_organisasi ms where ms.tahun = k.tahun \
			and ms.kodeurusan = k.kodeurusan and ms.kodesuburusan = k.kodesuburusan \
			and ms.kodeorganisasi = k.kodeorganisasi and ms.kodeunit = k.kodeunit)as URAIUNIT \
			FROM PENATAUSAHAAN.KEGIATAN k WHERE k.tahun=%s and k.KODEURUSAN=%s and k.KODESUBURUSAN=%s\
			and k.KODEORGANISASI=%s and k.kodeunit=%s and k.kodesubkegiatan<>0 and k.kodesubkeluaran=0 \
			ORDER BY KODEUNIT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan",
			[tahun_log(request),org[0],org[1],org[2],org[3],tahun_log(request),org[0],org[1],org[2],org[3]])
		list_keg = dictfetchall(cursor)
	

	data = {'list_keg' : list_keg}
	return render(request,'spp/modal/modal_kegiatan_kontrak.html',data)
	
def load_sumberdana_kontrak(request):
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0')||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,4,'0')  as kodesumberdana, 
			urai
			FROM master.master_sumberdana k WHERE k.tahun=%s
			ORDER BY KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK""",
			[tahun_log(request)])
		sumberdana = dictfetchall(cursor)

	data = {'list_sumberdana' : sumberdana}
	return render(request,'spp/modal/modal_sumberdana_kontrak.html',data)
	
def load_rekening_pendapatan(request):
	data 	= request.GET
	skpd 	= data.get('organisasi').split('.')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0')||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,4,'0')  as koderekening, 
			(select a.urai from master.master_rekening a where a.tahun = k.tahun and a.kodeakun=k.kodeakun and a.kodekelompok=k.kodekelompok and a.kodejenis=k.kodejenis and a.kodeobjek=k.kodeobjek and a.koderincianobjek=k.koderincianobjek and a.kodesubrincianobjek=k.kodesubrincianobjek) as urai
			FROM penatausahaan.pendapatan k   WHERE k.tahun=%s and k.kodeurusan =%s and k.kodesuburusan= %s and k.kodeorganisasi=%s and k.kodeunit = %s
			ORDER BY k.KODEAKUN,k.KODEKELOMPOK,k.KODEJENIS,k.KODEOBJEK,k.KODERINCIANOBJEK,k.KODESUBRINCIANOBJEK""",
			[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3]])
		pendapatan = dictfetchall(cursor)

	data = {'list_pendapatan' : pendapatan}
	return render(request,'spp/modal/modal_rekening_pendapatan.html',data)

def check_no_kontrak(tahun, nomor):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT count(nokontrak) as jml FROM penatausahaan.kontrak \
			WHERE tahun = %s AND UPPER(nokontrak) = %s ", [tahun, nomor])
		hasil = dictfetchall(cursor)
	lope = hasil[0]['jml']

	return lope

def check_no_bast(tahun, nomor):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT count(nobast) as jml FROM penatausahaan.bast \
			WHERE tahun = %s AND UPPER(nobast) = %s ", [tahun, nomor])
		hasil = dictfetchall(cursor)
	lope = hasil[0]['jml']

	return lope

def update_kontrak(request, arrayDT):
	try:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""UPDATE penatausahaan.kontrak SET NOKONTRAK = %s, TGLMULAI = %s, TGLSELESAI = %s, DESKRIPSIPEKERJAAN = %s, 
				JUMLAHKONTRAK = %s, NAMAPERUSAHAAN = %s, BENTUKPERUSAHAAN = %s, ALAMATPERUSAHAAN = %s, NAMAPIMPINANPERUSAHAAN = %s, 
				NOREKPERUSAHAAN = %s, NAMAREKENINGBANK = %s, PEMILIKREKENINGPERUSAHAAN = %s, NAMABANKPERUSAHAAN = %s,
				NPWPPERUSAHAAN = %s, USERNAME = %s, SUMBERDANA = %s
				WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s 
				AND NOKONTRAK = %s """,arrayDT)
			pesan = 1
	except IntegrityError as e:
		pesan = 0
	except:
		pesan=0
	return pesan

def update_bast(request, arrayDT):
	try:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""UPDATE penatausahaan.bast SET NOBAST=%s, NOKONTRAK = %s, TGLBAST=%s, TGLMULAI = %s, TGLSELESAI = %s, DESKRIPSIPEKERJAAN = %s, 
				JUMLAHKONTRAK = %s, NAMAPERUSAHAAN = %s, BENTUKPERUSAHAAN = %s, ALAMATPERUSAHAAN = %s, NAMAPIMPINANPERUSAHAAN = %s, 
				NOREKPERUSAHAAN = %s, NAMAREKENINGBANK = %s, PEMILIKREKENINGPERUSAHAAN = %s, NAMABANKPERUSAHAAN = %s,
				NPWPPERUSAHAAN = %s, USERNAME = %s, SUMBERDANA = %s
				WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s 
				AND NOBAST = %s """,arrayDT)
			pesan = 1
	except IntegrityError as e:
		pesan = 0
	return pesan

def simpan_kontrak(request, jenis):
	isSimpan = 0
	data     = request.POST

	uname_x  = username(request)
	tahun    = tahun_log(request)

	if jenis.lower() == 'upper': # JENIS UNTUK ADD dan EDIT ============================
		aksi                                    = data.get('aksi')
		skpd                                    = data.get('skpd').split(' - ')[0].split('.')
		nokontrak                               = data.get('nokontrak').upper()
		nokontrak_x                             = data.get('nokontrak_x').upper()
		tgl_mulai                               = tgl_short(data.get('tgl_mulai'))  
		tgl_selesai                             = tgl_short(data.get('tgl_selesai'))    
		deskripsipekerjaan                      = data.get('deskripsipekerjaan')    
		kode_unit                               = data.get('kode_unit') 
		kode_bidang                             = data.get('kode_bidang')   
		kode_program                            = data.get('kode_program')  
		kode_kegiatan                           = data.get('kode_kegiatan') 
		kodesubkegiatan                         = data.get('kode_subkegiatan')  
		nama_perusahaan                         = data.get('nama_perusahaan')   
		bentuk_perusahaan                       = data.get('bentuk_perusahaan') 
		pimpinan_perusahaan                     = data.get('pimpinan_perusahaan')   
		alamat_perusahaan                       = data.get('alamat_perusahaan') 
		bank_perusahaan                         = data.get('nama_bank')   
		npwp_perusahaan                         = data.get('npwp_perusahaan')   
		norek_perusahaan                        = data.get('norek_perusahaan')  
		nama_pemilik_rekening_bank_perusahaan   = data.get('nama_pemilik_rekening_bank_perusahaan') 
		nama_rekening_bank_perusahaan           = data.get('nama_rekening_bank_perusahaan')
		sumberdana                              = data.get('kode_sumberdana')
		rincian = request.POST.getlist('afektasikontrak')


		if aksi.lower() == 'true': # AKSI ADD -> INSERT ==========================================================
			if nokontrak != '' and data.get('skpd') != '':
				if check_no_kontrak(tahun, nokontrak) >= 1:
					isSimpan = 0
					pesan    = 'Kontrak dengan nomor : "'+nokontrak+'", sudah digunakan !!'
				else:
					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("""INSERT INTO penatausahaan.kontrak(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
								NOKONTRAK,TGLMULAI,TGLSELESAI,DESKRIPSIPEKERJAAN,JUMLAHKONTRAK,NAMAPERUSAHAAN,BENTUKPERUSAHAAN,ALAMATPERUSAHAAN,
								NAMAPIMPINANPERUSAHAAN,NOREKPERUSAHAAN,NAMAREKENINGBANK,PEMILIKREKENINGPERUSAHAAN,NAMABANKPERUSAHAAN,NPWPPERUSAHAAN,
								USERNAME ,sumberdana) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
								[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nokontrak,tgl_mulai,tgl_selesai,deskripsipekerjaan,0,
								nama_perusahaan,bentuk_perusahaan,alamat_perusahaan,pimpinan_perusahaan,norek_perusahaan, nama_rekening_bank_perusahaan,
								nama_pemilik_rekening_bank_perusahaan, bank_perusahaan, npwp_perusahaan, uname_x, sumberdana])
						
						isSimpan = 1
						pesan    = 'Kontrak dengan nomor : "'+nokontrak+'", berhasil disimpan !'
					except IntegrityError as e:
						isSimpan = 0
						pesan    = 'Kontrak dengan nomor : "'+nokontrak+'", sudah ada !'    

		else: # AKSI EDIT -> UPDATE =============================================================================
			arrayDT =[nokontrak,tgl_mulai,tgl_selesai,deskripsipekerjaan,0,nama_perusahaan,bentuk_perusahaan,alamat_perusahaan,pimpinan_perusahaan,
				norek_perusahaan, nama_rekening_bank_perusahaan,nama_pemilik_rekening_bank_perusahaan, bank_perusahaan, npwp_perusahaan, uname_x,sumberdana,tahun,
				skpd[0],skpd[1],skpd[2],skpd[3],nokontrak_x]
			
			if (nokontrak != nokontrak_x):
				if check_no_kontrak(tahun, nokontrak) >= 1:
					isSimpan = 0
					pesan    = 'Kontrak dengan nomor : "'+nokontrak+'", sudah digunakan !!'
				else:
					isSimpan = update_kontrak(request, arrayDT)
					pesan = 'Perubahan nomor  : '+nokontrak_x+', berhasil disimpan !'
					if isSimpan == 0:
						pesan = 'Perubahan tidak dapat disimpan karena Kontrak sudah digunakan di BAST'
			else:
				isSimpan = update_kontrak(request, arrayDT)
				pesan = 'Perubahan nomor  : '+nokontrak_x+', berhasil disimpan !'
				if isSimpan == 0:
						pesan = 'Perubahan tidak dapat disimpan karena Kontrak sudah digunakan di BAST'

		if isSimpan == 1:
			print('berhasil')
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN
				cursor.execute("""DELETE FROM penatausahaan.kontrakrincian WHERE tahun = %s 
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nokontrak = %s""",
					[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nokontrak])

				# INSERT INTO TABEL RINCIAN
				for x in range(len(rincian)):
					rinciannya = rincian[x].split("|")
					uange   = toAngkaDec(rinciannya[1])
					kegiatane = rinciannya[0].split('-')[0].split('.')
					rekeninge = rinciannya[0].split('-')[1].split('.')

					if uange != '0.00':
						cursor.execute("""INSERT INTO penatausahaan.kontrakrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
							NOKONTRAK,KODEBIDANG, KODEPROGRAM, KODEKEGIATAN, KODESUBKEGIATAN,KODESUBKELUARAN,
							KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH) 
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nokontrak,f'{kegiatane[0]}.{kegiatane[1]}', kegiatane[2], f'{kegiatane[3]}.{kegiatane[4]}',kegiatane[5],0,
							rekeninge[0],rekeninge[1],rekeninge[2],rekeninge[3],rekeninge[4],rekeninge[5],uange])
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("""select case when sum(jumlah) is null then 0 else sum(jumlah) end as jumlahkontrak 
								from penatausahaan.kontrakrincian where tahun=%s  and kodeurusan=%s and kodesuburusan=%s and 
								kodeorganisasi=%s and kodeunit=%s and UPPER(nokontrak)=UPPER(%s) """, [tahun,skpd[0],skpd[1],skpd[2],skpd[3],nokontrak])
				hasil = dictfetchall(cursor)
				jumlahnya = hasil[0]['jumlahkontrak']
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("""UPDATE penatausahaan.kontrak SET JUMLAHKONTRAK = %s
						WHERE TAHUN = %s AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s 
						AND NOKONTRAK = %s """,[jumlahnya, tahun,skpd[0],skpd[1],skpd[2],skpd[3],nokontrak])

	else: # UNTUK DELETE ======================================================
		data  = request.POST
		skpd  = data.get('skpd').split('.')
		nokontrak = data.get('nokontrak').upper()
		try:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.kontrak WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s and kodeunit=%s \
					AND nokontrak IN ("+str(nokontrak)+")",
					[tahun,skpd[0],skpd[1],skpd[2],skpd[3]])
				isSimpan = 0
				pesan = 'Data Kontrak berhasil dihapus'
		except:
			isSimpan = 0
			pesan = 'Data kontrak gagal dihapus karena sudah digunakan di BAST!!!'

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def simpan_bast(request, jenis):
	isSimpan = 0
	data     = request.POST

	uname_x  = username(request)
	tahun    = tahun_log(request)

	if jenis.lower() == 'upper': # JENIS UNTUK ADD dan EDIT ============================
		aksi                                    = data.get('aksi')
		skpd                                    = data.get('skpd').split(' - ')[0].split('.')
		nobast                                  = data.get('nobast').upper()
		nokontrak                               = data.get('nokontrak').upper()
		nobast_x                                = data.get('nobast_x').upper()
		tgl_bast                               = tgl_short(data.get('tgl_bast'))  
		tgl_mulai                               = tgl_short(data.get('tgl_mulai'))  
		tgl_selesai                             = tgl_short(data.get('tgl_selesai'))    
		deskripsipekerjaan                      = data.get('deskripsipekerjaan')    
		kode_unit                               = data.get('kode_unit') 
		kode_bidang                             = data.get('kode_bidang')   
		kode_program                            = data.get('kode_program')  
		kode_kegiatan                           = data.get('kode_kegiatan') 
		kodesubkegiatan                         = data.get('kode_subkegiatan')  
		nama_perusahaan                         = data.get('nama_perusahaan')   
		bentuk_perusahaan                       = data.get('bentuk_perusahaan') 
		pimpinan_perusahaan                     = data.get('pimpinan_perusahaan')   
		alamat_perusahaan                       = data.get('alamat_perusahaan') 
		bank_perusahaan                         = data.get('bank_perusahaan')   
		npwp_perusahaan                         = data.get('npwp_perusahaan')   
		norek_perusahaan                        = data.get('norek_perusahaan')  
		nama_pemilik_rekening_bank_perusahaan   = data.get('nama_pemilik_rekening_bank_perusahaan') 
		nama_rekening_bank_perusahaan           = data.get('nama_rekening_bank_perusahaan')
		sumberdana                              = data.get('kode_sumberdana')
		rincian = request.POST.getlist('afektasikontrak')


		if aksi.lower() == 'true': # AKSI ADD -> INSERT ==========================================================
			if nobast != '' and data.get('skpd') != '':
				if check_no_bast(tahun, nobast) >= 1:
					isSimpan = 0
					pesan    = 'BAST dengan nomor : "'+nobast+'", sudah digunakan !!'
				else:
					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("""INSERT INTO penatausahaan.bast(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
								NOBAST,NOKONTRAK,TGLBAST,TGLMULAI,TGLSELESAI,DESKRIPSIPEKERJAAN,JUMLAHKONTRAK,NAMAPERUSAHAAN,BENTUKPERUSAHAAN,ALAMATPERUSAHAAN,
								NAMAPIMPINANPERUSAHAAN,NOREKPERUSAHAAN,NAMAREKENINGBANK,PEMILIKREKENINGPERUSAHAAN,NAMABANKPERUSAHAAN,NPWPPERUSAHAAN,
								USERNAME ,sumberdana) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
								[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nobast,nokontrak,tgl_bast,tgl_mulai,tgl_selesai,deskripsipekerjaan,0,
								nama_perusahaan,bentuk_perusahaan,alamat_perusahaan,pimpinan_perusahaan,norek_perusahaan, nama_rekening_bank_perusahaan,
								nama_pemilik_rekening_bank_perusahaan, bank_perusahaan, npwp_perusahaan, uname_x, sumberdana])
						
						isSimpan = 1
						pesan    = 'BAST dengan nomor : "'+nobast+'", berhasil disimpan !'
					except IntegrityError as e:
						isSimpan = 0
						pesan    = 'BAST dengan nomor : "'+nobast+'", sudah ada !'  

		else: # AKSI EDIT -> UPDATE =============================================================================
			arrayDT =[nobast,nokontrak,tgl_bast,tgl_mulai,tgl_selesai,deskripsipekerjaan,0,nama_perusahaan,bentuk_perusahaan,alamat_perusahaan,pimpinan_perusahaan,
				norek_perusahaan, nama_rekening_bank_perusahaan,nama_pemilik_rekening_bank_perusahaan, bank_perusahaan, npwp_perusahaan, uname_x,sumberdana,tahun,
				skpd[0],skpd[1],skpd[2],skpd[3],nobast_x]
			
			if (nokontrak != nobast_x):
				if check_no_bast(tahun, nokontrak) >= 1:
					isSimpan = 0
					pesan    = 'Kontrak dengan nomor : "'+nokontrak+'", sudah digunakan !!'
				else:
					isSimpan = update_bast(request, arrayDT)
					pesan = 'Perubahan nomor  : '+nobast_x+', berhasil disimpan !'
			else:
				isSimpan = update_bast(request, arrayDT)
				pesan = 'Perubahan nomor  : '+nobast_x+', berhasil disimpan !'

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN
				cursor.execute("""DELETE FROM penatausahaan.bastrincian WHERE tahun = %s 
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nobast = %s""",
					[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nobast])

				# INSERT INTO TABEL RINCIAN
				for x in range(len(rincian)):
					rinciannya  = rincian[x].split("|")
					uange       = toAngkaDec(rinciannya[1])
					kegiatane   = rinciannya[0].split('-')[0].split('.')
					rekeninge   = rinciannya[0].split('-')[1].split('.')

					if uange != '0.00':
						cursor.execute("""INSERT INTO penatausahaan.bastrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
							NOBAST,KODEBIDANG, KODEPROGRAM, KODEKEGIATAN, KODESUBKEGIATAN,KODESUBKELUARAN,
							KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH) 
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nobast,f'{kegiatane[0]}.{kegiatane[1]}', kegiatane[2], f'{kegiatane[3]}.{kegiatane[4]}',kegiatane[5],0,
							rekeninge[0],rekeninge[1],rekeninge[2],rekeninge[3],rekeninge[4],rekeninge[5],uange])

	else: # UNTUK DELETE ======================================================
		data  = request.POST
		skpd  = data.get('skpd').split('.')
		nobast = data.get('nobast').upper()
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.bast WHERE tahun = %s \
				AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s and kodeunit=%s \
				AND nobast IN ("+str(nobast)+")",
				[tahun,skpd[0],skpd[1],skpd[2],skpd[3]])
			

		isSimpan = 0
		pesan = 'Data BAST berhasil dihapus'

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def listafektasi_kontrak(request):
	skpd = request.POST.get('skpd', None).split('.')
	nokontrak = request.POST.get('nokontrak', '')
	tgl = request.POST.get('tgl', '')

	if tgl == '': 
		tgl = datetime.today().strftime('%Y-%m-%d')
	else:
		tgl = tgl_short(request.POST.get('tgl'))
	bidang = request.POST.get('bidang') 
	program = request.POST.get('program') 
	kegiatan = request.POST.get('kegiatan')
	subkegiatan = request.POST.get('subkegiatan')
	jenis = str(request.POST.get('jenis', ''))

	with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""SELECT * FROM penatausahaan.fc_view_kontrak_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,
				[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],nokontrak.upper(),bidang,program,kegiatan,subkegiatan,tgl,])
			list_kontrak = dictfetchall(cursor)
			
	kodekegiatan = ''
	# for x in range(len(list_kontrak)):
	#   if (list_kontrak[x]['cek']==1):
	#       if(list_kontrak[x]['uraian']!=None):
	#           objek = list_kontrak[x]['koderekening']
	#           objek1 = objek.split('-') 
	#           koderekening = objek1[0].split('.')
	#           kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"

	# kodekegiatan = "("+kodekegiatan[1:len(kodekegiatan)]+")"

	data = {'list_kontrak' : ArrayFormater(list_kontrak),'kodekegiatan':kodekegiatan, 'jenis':jenis}
	return render(request, 'spp/tabel/tabel_afektasi_kontrak.html', data)


def load_bank_kontrak(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT kodebank, namabank, keterangan
			FROM master.master_bank""",
			[tahun_log(request)])
		bank = dictfetchall(cursor)

	data = {'list_bank' : bank}
	return render(request,'konfig/modal/modal_bank.html',data)

def combokontrakskpd(request):
	if 'sipkd_username' in request.session:

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select urai from master.masterjabatan where isskpd = 0 and jenissistem = 2 order by urut")
			ms_jbtn = dictfetchall(cursor)

		aidi = request.GET.get('id', None)
		telo = ""
		for dt in ms_jbtn:
			telo += "<option value='" + dt['urai'] + "'>" + dt['urai'] + "</option>"


		combo = "<select class='dropdown-in-table' id='jabatan_" + aidi + "' name='jabatan'>"\
		   "<option value='0'>-- Silahkan Pilih --</option>" + telo + "</select>"

		return HttpResponse(combo)

	else:
		return redirect('sipkd:index')

def load_bank_bast(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT kodebank, namabank, keterangan
			FROM master.master_bank""",
			[tahun_log(request)])
		bank = dictfetchall(cursor)

	data = {'list_bank' : bank}
	return render(request,'konfig/modal/modal_bank.html',data)

def combobastskpd(request):
	if 'sipkd_username' in request.session:

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select urai from master.masterjabatan where isskpd = 0 and jenissistem = 2 order by urut")
			ms_jbtn = dictfetchall(cursor)

		aidi = request.GET.get('id', None)
		telo = ""
		for dt in ms_jbtn:
			telo += "<option value='" + dt['urai'] + "'>" + dt['urai'] + "</option>"


		combo = "<select class='dropdown-in-table' id='jabatan_" + aidi + "' name='jabatan'>"\
		   "<option value='0'>-- Silahkan Pilih --</option>" + telo + "</select>"

		return HttpResponse(combo)

	else:
		return redirect('sipkd:index')

def load_perusahaan(request):
	skpd = request.GET.get('id', None)

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT DISTINCT namaperusahaan, bentukperusahaan, alamatperusahaan, namapimpinanperusahaan,
			norekperusahaan, namarekeningbank, pemilikrekeningperusahaan,
			namabankperusahaan, npwpperusahaan FROM penatausahaan.kontrak
			WHERE tahun = %s AND kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit = %s
			ORDER BY namaperusahaan ASC""",[tahun_log(request),skpd])
		datax = dictfetchall(cursor)

	data = {'datax' : datax}
	return render(request,'spp/modal/cari_perusahaan.html',data)
