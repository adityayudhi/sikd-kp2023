from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def sp2d_in_pengesahlpj(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	uname_x = username(request).upper()
	us_SKPD = ARGTEX = ""
	arrTab 	= []

	if akses_x == "BELANJA":
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM public.view_organisasi_hakakses(%s,%s,%s)",[tahun_x,uname_x,2])
			otpot = dictfetchall(cursor)

			for w in otpot:
				us_SKPD += ",'"+w['output']+"'"

		if us_SKPD != "":
			ARGTEX = "WHERE a.kodeurusan||'.'||a.kodesuburusan||'.'||a.kodeorganisasi in ("+us_SKPD[1:]+")"
		else:
			ARGTEX = "WHERE a.kodeurusan||'.'||a.kodesuburusan||'.'||a.kodeorganisasi in ('')"
	else:
		us_SKPD = ARGTEX = ""


	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT 0 as CEK, row_number() over(order by a.tglspj desc) as nomor,\
			nospj,tglspj,skpd,keperluan,nosp2d,jumlah,jenis,status \
			FROM penatausahaan.fc_view_spj_sp2d(%s) as a "+ARGTEX,[tahun_x])
		tabel = dictfetchall(cursor)

	for i in range(len(tabel)):
		tabel[i].update({'warna':'kuning'})

	for dt in tabel:
		dt['tglspj']  = tgl_indo(dt['tglspj'])
		dt['nosp2d']  = dt['nosp2d'] if dt['nosp2d'] != None else ''
		dt['warna']   = dt['warna'] if dt['status'] != 1 else 'hijau' 
		arrTab.append(dt)

	arrDT = {'us_SKPD':us_SKPD[1:], 'arrTabel':arrTab}

	return render(request,'sp2d/persetujuanlpj_in.html',arrDT)

def sp2d_pengesahlpj_modal(request):
	tahun_x = tahun_log(request)
	data 	= request.GET
	dari 	= data.get('f').upper()
	aksi 	= int(data.get('a'))
	org = kd_org = ur_org = nospj = nosp2d = nolpj = tglspj = uraian = ""
	kuncix = 1

	if aksi >= 1:
		data_x 	= str(data.get("dt").replace("'","").replace("_","/").replace("+"," ")).split("|")
		org 	= data_x[2]
		kd_org 	= org.split("-")[0]
		ur_org 	= org.split("-")[1]
		skpd 	= org.split("-")[0].split(".")
		nospj 	= data_x[0]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT nospj,tglspj,nosp2d,nolpj,keperluan,\
				case when status >= 1 then '-1' else '1' end as status FROM penatausahaan.spj_pkd\
				WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
				AND jenis = %s AND nospj = %s",
				[tahun_x,skpd[0],skpd[1],skpd[2],dari,nospj])
			hasil = dictfetchall(cursor)

		for dt in hasil:
			tglspj 	= tgl_indo(dt['tglspj'])
			nosp2d 	= dt['nosp2d']
			nolpj 	= dt['nolpj']
			uraian 	= dt['keperluan']
			kuncix 	= dt['status']

	arrDT 	= {'from':dari,'aksi':aksi,'dx_org':org,'kd_org':kd_org,'ur_org':ur_org,'dx_nospj':nospj,
		'dx_nosp2d':nosp2d,'dx_nolpj':nolpj,'tglsekarang':tglspj,'uraian':uraian, 'kuncix':kuncix}

	return render(request,'sp2d/modal/persetujuanlpj_in.html',arrDT)

def sp2d_pengesahlpj_tabel(request):
	tahun_x = tahun_log(request)
	data 	= request.POST
	dari	= str(data.get('from').upper())
	nosp2d 	= str(data.get('sp2d'))
	nospj 	= str(data.get('spj'))
	nolpj 	= str(data.get('lpj'))
	tglspj 	= tgl_short(str(data.get('tgl')))
	kdKeg 	= str(data.get('keg')).replace("'","'")
	tabs_to = str(data.get('too')).lower()
	headtxt = 'Pagu'
	arrREK 	= []
	arrTBL  = []
	jmlsp2d = ''
	aksi 	= str(data.get('aksi')).lower()

	if aksi == 'true': statusSPJ = '2'
	else: statusSPJ = '1'

	if data.get('skpd') != "":
		skpd = str(data.get('skpd')).split('.')
	else:
		skpd = '0.0.0.0'.split('.')

	if dari == "TU":
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over(ORDER BY kode ASC) as nomor,cek,kode,urai,anggaran,sp2dlain,\
				spjsebelum,sp2dsekarang,spjsekarang,sisasp2d,sisa,sp2dlalu \
				FROM penatausahaan.fc_view_keg_rekening_for_spj_tu(%s,%s,%s,%s,%s,%s,%s)",
				[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],nosp2d,nospj,tglspj])
			arrTBL = dictfetchall(cursor)

	elif dari == "GU":
		if int(skpd[0]) != 0:
			if tabs_to == 'rekening':
				if aksi == 'true': nospj_lpj = nolpj
				else: nospj_lpj = nospj

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT row_number() over() as nomor,\
						pilih,koderekening,urai,anggaran,sp2dlain,sp2dlalu,sp2dsekarang,\
						spjsebelum,spjsekarang,sisa,sisasp2d,(sp2dlain+spjsebelum) as total \
						FROM penatausahaan.fc_view_keg_rekening_for_spj(%s,%s,%s,%s,%s,%s,%s) \
						WHERE kode IN ("+kdKeg+")",
						[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],nospj_lpj,dari,statusSPJ])
					arrREK = dictfetchall(cursor)

					cursor.execute("SELECT jumlahsp2d FROM penatausahaan.sp2d WHERE tahun = %s \
						AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND jenissp2d = %s",
						[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],'UP'])
					jumlah = dictfetchall(cursor)

					if len(jumlah) > 0: jmlsp2d = format_rp(jumlah[0]['jumlahsp2d'])
					else: jmlsp2d = '0,00'
			else:
				if nolpj != "" and aksi == 'true':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("SELECT row_number() over(ORDER BY kodebidang,kodeprogram,kodekegiatan ASC) as nomor, \
							1 AS cek,koderekening,urai,jumlah AS pagu,\
							kodebidang,kodeprogram,kodekegiatan FROM penatausahaan.fc_report_lpjup(%s,%s,%s,%s,%s)",
							[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],nolpj])
						arrTBL = dictfetchall(cursor)
						headtxt = 'Jumlah LPJ'
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("SELECT row_number() over(ORDER BY kodebidang,kodeprogram,kodekegiatan ASC) as nomor,* \
							FROM penatausahaan.fc_view_kegiatan_spj(%s,%s,%s,%s,%s)",
							[tahun_x,int(skpd[0]),int(skpd[1]),skpd[2],nospj])
						arrTBL = dictfetchall(cursor)

	arrDT = {'from':dari, 'arrTabel':arrTBL, 'arrREK':arrREK, 'headtxt':headtxt, 'tabs_to':tabs_to,
		'jmlsp2d':jmlsp2d}

	return render(request,'sp2d/tabel/persetujuanlpj_in.html',arrDT)

def sp2d_pengesahlpj_simpan(request, jenis0, jenis1):
	uname_x = username(request).upper()
	tahun_x = tahun_log(request)
	jenis_0 = str(jenis0.lower())
	jenis_1 = str(jenis1.upper())
	data 	= request.POST

	if jenis0 == "upper":
		aksi 	= str(data.get('aksi').lower())
		skpd 	= str(data.get('organisasi')).split('.')
		nolpj 	= str(data.get('no_lpj_skpd').upper())
		nospj 	= str(data.get('no_spj').upper())
		nospj_x = str(data.get('no_spj_x').upper())
		tglspj  = tgl_short(data.get('tgl_sp2d_spj'))
		uraian 	= str(data.get('uraian_informasi'))
		cek_ada = cek_nomor_spj(tahun_x,nospj)

		if jenis1 == "TU": 
			nosp2d 	= str(data.get('no_sp2d_x').upper())
			rincian = data.getlist('checkbox')
		else: 
			nosp2d 	= ''
			rincian = data.getlist('chk_rekening')

# ADD DATA =========================================================================
		if aksi == 'true':
			if cek_ada >= 1:
				isSimpan = 0
				pesan 	 = 'Nomor SPJ : "'+nospj+'", sudah digunakan !'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.spj_pkd(tahun,kodeurusan,kodesuburusan,kodeorganisasi,nospj,\
						tglspj,nolpj,nosp2d,keperluan,status,username,jenis) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun_x,skpd[0],skpd[1],skpd[2],nospj,tglspj,nolpj,nosp2d,uraian,0,uname_x,jenis_1])

				isSimpan = 1
				pesan 	 = 'Data SPJ berhasil disimpan !'
# EDIT DATA =======================================================================
		else:
			cek_status = cek_spj_status(tahun_x,nospj_x,skpd[0],skpd[1],skpd[2])

			if cek_ada >= 1 and nospj != nospj_x:
				isSimpan = 0
				pesan 	 = 'Nomor SPJ : "'+nospj+'", sudah digunakan !'
			elif cek_status == 1:
				isSimpan = 0
				pesan 	 = 'Nomor SPJ : "'+nospj+'" telah disahkan, Anda tidak bisa mengubah data tersebut!'
			elif cek_status >= 2:
				isSimpan = 0
				pesan 	 = 'Nomor SPJ : "'+nospj+'" sudah dibuat SP2D, Anda tidak bisa menghapus data tersebut!'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE penatausahaan.spj_pkd SET tahun = %s,kodeurusan = %s,kodesuburusan = %s,\
						kodeorganisasi = %s,nospj = %s,tglspj = %s,nolpj = %s,nosp2d = %s,keperluan = %s,\
						username = %s,jenis = %s WHERE tahun = %s AND kodeurusan = %s \
						AND kodesuburusan = %s AND kodeorganisasi = %s AND nospj = %s",
						[tahun_x,skpd[0],skpd[1],skpd[2],nospj,tglspj,nolpj,nosp2d,uraian,uname_x,jenis_1,
						tahun_x,skpd[0],skpd[1],skpd[2],nospj_x])

				isSimpan = 1
				pesan = 'Perubahan data SPJ berhasil disimpan !'

# HAPUS dan INSERT DATA RINCIAN SETELAH ADD atau EDIT DATA ========================================
		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.spj_pkd_rinc WHERE tahun = %s \
					AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND nospj = %s ",
					[tahun_x,skpd[0],skpd[1],skpd[2],nospj])

			for val in rincian:
				hasil  	 = val.split("|")
				objek0 	 = hasil[1].split("-")
				objek1   = objek0[0].split(".")
				objek2 	 = objek0[1].split(".")
				uraian_x = hasil[2]

	# 
				if jenis1 == "TU":
					sp2d_now = toAngkaDec(hasil[0])
					spj_now  = toAngkaDec(hasil[3])

					if (spj_now != '0.00' and spj_now > sp2d_now):
						isSimpan = 0
						pesan 	 = 'Rekening "'+hasil[1]+' '+uraian_x+'", melebihi SP2D TU'
					else:
						if spj_now != '0.00' and isSimpan == 1:
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("INSERT INTO penatausahaan.SPJ_PKD_RINC(TAHUN,KODEURUSAN,KODESUBURUSAN,\
									KODEORGANISASI,NOSPJ,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,\
									KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,JUMLAH) \
									VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
									[tahun_x,skpd[0],skpd[1],skpd[2],nospj,objek1[0]+"."+objek1[1],objek1[3],objek1[4],
									objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],spj_now])
				else:
					anggaran = toAngkaDec(hasil[0])
					total  	 = toAngkaDec(hasil[3])
					spj_now  = toAngkaDec(hasil[4])
					sisasp2d = toAngkaDec(data.get('sisa_sp2d_up'))
					nol_x 	 = toAngkaDec('0,00')

					if sisasp2d < nol_x:
						isSimpan = 0
						pesan 	 = "Sisa UP tidak boleh kurang dari 0 (nol)"
					elif float(total) > float(anggaran):
						isSimpan = 0
						pesan 	 = "Pengisian Rekening "+hasil[1]+uraian_x+", Melebihi Batas Anggaran."
					else:
						if spj_now != '0.00' and isSimpan == 1:
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("INSERT INTO penatausahaan.SPJ_PKD_RINC(TAHUN,KODEURUSAN,KODESUBURUSAN,\
									KODEORGANISASI,NOSPJ,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,\
									KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,JUMLAH) \
									VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
									[tahun_x,skpd[0],skpd[1],skpd[2],nospj,objek1[0]+"."+objek1[1],objek1[3],objek1[4],
									objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],spj_now])

# HAPUS DATA ==========================================================================
	else:
		arrDT = data.get('arrdt').split(",")

		for dt in arrDT:
			dat = dt.split("|")
			org = dat[2].split("-")[0].split(".")
			cek_status = cek_spj_status(tahun_x,dat[0],org[0],org[1],org[2])

			if(cek_status == 1):
				isSimpan = 0
				pesan 	 = 'Nomor SPJ "'+dat[0]+'" telah disahkan, Anda tidak bisa menghapus data tersebut!'
			elif(cek_status >= 2):
				isSimpan = 0
				pesan 	 = 'Nomor SPJ "'+dat[0]+'" sudah dibuat SP2D, Anda tidak bisa menghapus data tersebut!'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.spj_pkd WHERE tahun = %s \
						AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
						AND nospj = %s AND jenis = %s",[tahun_x,org[0],org[1],org[2],dat[0],dat[3]])

					cursor.execute("DELETE FROM penatausahaan.spj_pkd_rinc WHERE tahun = %s \
						AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s \
						AND nospj = %s",[tahun_x,org[0],org[1],org[2],dat[0]])

				isSimpan = 1
				pesan = 'Data SPJ berhasil dihapus'

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)


# DEF UNTUK MODAL ======================================================
# JOEL 27 Feb 2019 ===================================================
# CARI DATA SP2D UNTUK BKU
def mdl_src_sp2d_for_bku(request, jenis):
	tahun_x = tahun_log(request)
	jenis_x = str(jenis.upper())
	skpd 	= str(request.GET.get('id').lower()).split(".")
	arrTab 	= []

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT row_number() over(ORDER BY nosp2d,tanggal) as nomor,tahun,\
			nosp2d,tanggal,tglkasda,organisasi,informasi,jumlah,kodeurusan,kodesuburusan,kodeorganisasi,\
			kodebidang,kodeprogram,kodekegiatan,jenissp2d,uraikegiatan FROM penatausahaan.fc_sp2d_for_bku(%s,%s,%s,%s) a \
			WHERE jenissp2d = %s AND nosp2d NOT IN (select nosp2d from penatausahaan.spj_skpd where tahun = a.tahun \
			and kodeurusan = a.kodeurusan and kodesuburusan = a.kodesuburusan \
			and kodeorganisasi = a.kodeorganisasi and jenis = a.jenissp2d) \
			AND nosp2d NOT IN (select nosp2d from penatausahaan.spj_pkd where tahun = a.tahun \
			and kodeurusan = a.kodeurusan and kodesuburusan = a.kodesuburusan \
			and kodeorganisasi = a.kodeorganisasi and jenis = a.jenissp2d) ",[tahun_x,skpd[0],skpd[1],skpd[2],jenis_x])
		tabel = ArrayFormater(dictfetchall(cursor))

	arrDT = {'tabel':tabel}
	return render(request,'sp2d/modal/sp2d_for_bku.html',arrDT) 

# JOEL 28 Feb 2019 ================================================
# CARI DATA LPJ TU dan GU
def mdl_src_sp2d_lpj_tu_gu(request, jenis):
	tahun_x = tahun_log(request)
	jenis_x = str(jenis.upper())
	skpd 	= str(request.GET.get('id').lower()).split(".")
	arrTab 	= []

	with connections[tahun_log(request)].cursor() as cursor:
		if jenis_x == "GU":
			jenissp2d = "'UP','GU'"
		elif jenis_x == "TU":
			jenissp2d = "'TU'"
			# cursor.execute("SELECT row_number() over(ORDER BY nolpj,tgllpj ASC) as nomor,\
			# 	nolpj,tgllpj,nosp2d,urailpj,jumlah,kodebidang,kodeprogram,kodekegiatan \
			# 	FROM penatausahaan.fc_lihat_lpj(%s,%s,%s,%s,%s) WHERE \
			# 	(nolpj not in (select nolpj from penatausahaan.spj_pkd where tahun = %s \
			# 	and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s))",
			# 	[tahun_x,skpd[0],skpd[1],skpd[2],jenis_x,tahun_x,skpd[0],skpd[1],skpd[2]])

		cursor.execute("SELECT s.nospj as nolpj,s.tglspj as tgllpj,s.keperluan as urailpj,nosp2d,\
			(select sum(sr.jumlah) from penatausahaan.spj_skpd_rinc_sub1 sr \
			where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan \
			and sr.kodeorganisasi=s.kodeorganisasi and sr.nospj=s.nospj) as jumlah \
			from penatausahaan.spj_skpd s where s.tahun=%s and s.kodeurusan=%s \
			and s.kodesuburusan=%s and s.kodeorganisasi=%s and s.jenis in ("+jenissp2d+") \
			and (nospj not in (select nolpj from penatausahaan.spj_pkd where tahun=%s \
			and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and jenis in ("+jenissp2d+")))",
			[tahun_x,skpd[0],skpd[1],skpd[2],tahun_x,skpd[0],skpd[1],skpd[2]])
		tabel = ArrayFormater(dictfetchall(cursor))

	arrDT = {'jenis':jenis_x,'tabel':tabel}
	return render(request,'sp2d/modal/sp2d_lpj_tu_gu.html',arrDT)

# CARI DATA SPJ TU dan GU
def mdl_src_sp2d_spj(request, jenis):
	tahun_x = tahun_log(request)
	jenis_x = str(jenis.upper())
	skpd 	= str(request.GET.get('id').lower()).split(".")
	arrTab 	= []

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT row_number() over(ORDER BY nospj,tglspj ASC) as nomor,\
			nospj,tglspj,nosp2d,nolpj,keperluan,jenis,\
			(SELECT SUM(JUMLAH) FROM penatausahaan.SPJ_PKD_RINC as a \
			WHERE a.TAHUN = tahun AND a.KODEURUSAN = kodeurusan AND a.KODESUBURUSAN = kodesuburusan \
			AND a.KODEORGANISASI = kodeorganisasi AND a.NOSPJ = b.nospj) AS jumlah FROM penatausahaan.spj_pkd b \
			where tahun = %s and jenis = %s \
			and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s ",
			[tahun_x,jenis_x,skpd[0],skpd[1],skpd[2]])
		tabel = ArrayFormater(dictfetchall(cursor))

	arrDT = {'jenis':jenis_x,'tabel':tabel}
	return render(request,'sp2d/modal/cari_spj_tugu.html',arrDT)

# CEK NOMOR SPJ SUDAH ADA ATAU BELUM
def cek_nomor_spj(tahun,spj):

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(kodeurusan) as ada FROM penatausahaan.spj_pkd \
			WHERE tahun = %s AND nospj = %s",[str(tahun),str(spj)])
		hasil = dictfetchall(cursor)

	return hasil[0]['ada']

	
