from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def gu(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)

	arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]
	arrPeriod 	 = [{'kode':'0','nama':'-- Pilih Triwulan --'}, 
		{'kode':'1','nama':'Triwulan I'}, {'kode':'2','nama':'Triwulan II'},
		{'kode':'3','nama':'Triwulan III'}, {'kode':'4','nama':'Triwulan IV'}]

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select rekening,bank,kodesumberdana, urai from kasda.kasda_sumberdanarekening \
			where kodesumberdana <99 order by kodesumberdana")
		no_rekening = dictfetchall(cursor)

	arrData = { 'akses':akses_x, 'perubahan':str(sipkd_perubahan),
		'arrPerubahan':arrPerubahan, 'arrPeriode':arrPeriod, 'no_rekening':no_rekening}

	return render(request, 'sp2d/gu_kepmen.html', arrData)

def sp2d_gu_kepmen_cari_spm_sp2d(request):
	tahun_x = tahun_log(request)
	asal 	= request.POST.get('asal','').lower()
	js_arg 	= json.loads(request.POST.get('js_arg'))
	jnsSPM 	= str(js_arg[1]).upper()

	if js_arg[0]:
		skpd 	= js_arg[0].split(".")
	else:
		skpd = '0.0.0.0'.split('.')

	kdur 	= str(skpd[0])
	kdsub 	= str(skpd[1])
	kdorg 	= str(skpd[2])
	kduni 	= str(skpd[3])
	arrRinc = []

	with connections[tahun_log(request)].cursor() as cursor:
		if asal == 'src_spm':
			cursor.execute("SELECT row_number() over(ORDER BY s.tanggal DESC) as nomor,'' as nosp2d,s.nospm,s.tanggal,\
				(select kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit from master.master_organisasi\
				o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan  and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit<>'') as skpd, \
				(select o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan\
				and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit<>'') as organisasi,\
				(select sum (jumlah) from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm ) as jumlah,\
				(select kodebidang from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1 ) as kodebidang,\
				(select kodeprogram from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1 ) as kodeprogram,\
				(select kodekegiatan from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1 ) as kodekegiatan,\
				(select kodesubkegiatan from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1 ) as kodesubkegiatan,\
				(select kodesubkeluaran from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1 ) as kodesubkeluaran,\
				s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,s.statuskeperluan as keperluan \
				from penatausahaan.spm s where s.tahun= %s and s.kodeurusan = %s and s.kodesuburusan = %s \
				and s.kodeorganisasi = %s and s.kodeunit = %s and s.jenisspm = %s and  locked = 'Y' \
				and (nospm not in (select nospm from penatausahaan.sp2d where tahun = %s \
				and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and jenissp2d = %s))",
				[tahun_x,kdur,kdsub,kdorg,kduni,jnsSPM,tahun_x,kdur,kdsub,kdorg,kduni,jnsSPM])
			hasil = dictfetchall(cursor)

		elif asal == 'src_sp2d':
			# cursor.execute("SELECT row_number() over(ORDER BY s.tanggal DESC) as nomor,s.nosp2d,s.nospm,s.tanggal,s.statuskeperluan as keperluan,\
			# 	(select kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit from master.master_organisasi\
			# 	o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan  and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit<>'' and lpad(o.kodeunit::text,4,'0')='0000') as skpd, \
			# 	(select o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan\
			# 	and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit<>'' and lpad(o.kodeunit::text,4,'0')='0000') as organisasi,\
			# 	(select sum (jumlah) from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan \
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d ) as jumlah,\
			# 	(select kodebidang from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and  sr.nosp2d=s.nosp2d limit 1 ) as kodebidang,\
			# 	(select kodeprogram from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d limit 1 ) as kodeprogram,\
			# 	(select kodekegiatan from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d limit 1 ) as kodekegiatan,\
			# 	(select kodesubkegiatan from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d limit 1 ) as kodesubkegiatan,\
			# 	(select kodesubkeluaran from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
			# 	and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d limit 1 ) as kodesubkeluaran,\
			# 	s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit\
			# 	FROM penatausahaan.sp2d s  where s.tahun = %s and s.jenissp2d = %s",
			# 	[tahun_x,jnsSPM])			
			# hasil = dictfetchall(cursor)		
			if (kdur=='0') :
				cursor.execute("SELECT distinct row_number() over(ORDER BY s.tanggal DESC) as nomor, s.nosp2d,s.nospm,s.tanggal,trim(s.statuskeperluan) as keperluan,\
					s.kodeurusan||'.'||s.kodesuburusan||'.'||s.kodeorganisasi||'.0000' as skpd, o.urai as organisasi, \
					s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,\
					sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.kodesubkeluaran,\
					sum(sr.jumlah) as jumlah \
					FROM penatausahaan.sp2d s join penatausahaan.sp2drincian  sr on\
					(s.tahun=sr.tahun and s.kodeurusan=sr.kodeurusan and s.kodesuburusan=sr.kodesuburusan and s.kodeorganisasi=sr.kodeorganisasi and s.kodeunit=sr.kodeunit and s.nosp2d=sr.nosp2d ) \
					join master.master_organisasi o on \
					(s.tahun=o.tahun and s.kodeurusan=o.kodeurusan and s.kodesuburusan=o.kodesuburusan and s.kodeorganisasi=o.kodeorganisasi and s.kodeunit=o.kodeunit)\
					where s.tahun = %s and s.jenissp2d = %s  \
					group by  s.nosp2d,s.nospm,s.tanggal,statuskeperluan,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,\
					organisasi,sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.kodesubkeluaran\
					order by s.tanggal desc  ",
					[tahun_x,jnsSPM])			
				hasil = dictfetchall(cursor)
			else : 
				cursor.execute("SELECT distinct row_number() over(ORDER BY s.tanggal DESC) as nomor, s.nosp2d,s.nospm,s.tanggal,trim(s.statuskeperluan) as keperluan,\
					s.kodeurusan||'.'||s.kodesuburusan||'.'||s.kodeorganisasi||'.0000' as skpd, o.urai as organisasi, \
					s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,\
					sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.kodesubkeluaran,\
					sum(sr.jumlah) as jumlah \
					FROM penatausahaan.sp2d s join penatausahaan.sp2drincian  sr on\
					(s.tahun=sr.tahun and s.kodeurusan=sr.kodeurusan and s.kodesuburusan=sr.kodesuburusan and s.kodeorganisasi=sr.kodeorganisasi and s.kodeunit=sr.kodeunit and s.nosp2d=sr.nosp2d ) \
					join master.master_organisasi o on \
					(s.tahun=o.tahun and s.kodeurusan=o.kodeurusan and s.kodesuburusan=o.kodesuburusan and s.kodeorganisasi=o.kodeorganisasi and s.kodeunit=o.kodeunit)\
					where s.tahun = %s and s.jenissp2d = %s and s.kodeurusan=%s and s.kodesuburusan=%s and s.kodeorganisasi=%s and s.kodeunit=%s \
					group by  s.nosp2d,s.nospm,s.tanggal,statuskeperluan,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit,\
					organisasi,sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.kodesubkeluaran\
					order by s.tanggal desc  ",
					[tahun_x,jnsSPM,kdur,kdsub,kdorg,kduni])			
				hasil = dictfetchall(cursor)

	for xs in hasil:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT urai FROM penatausahaan.kegiatan WHERE tahun = %s AND kodeurusan = %s \
				AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND kodebidang = %s \
				AND kodeprogram = %s AND kodekegiatan = %s AND kodesubkegiatan = %s AND kodesubkeluaran = %s",
				[tahun_x,xs['kodeurusan'],xs['kodesuburusan'],xs['kodeorganisasi'],xs['kodeunit'],
				xs['kodebidang'],xs['kodeprogram'],xs['kodekegiatan'],xs['kodesubkegiatan'],0])
			x_urai = dictfetchall(cursor)

		if len(x_urai) >= 1: uraian_x = x_urai[0]['urai']
		else: uraian_x = ''

		# eskapede = str(xs['kodeurusan'])+"."+str(xs['kodesuburusan'])+"."+str(xs['kodeorganisasi'])+"."+str(xs['kodeunit'])
		kegiatan = xs['kodebidang']+"|"+str(xs['kodeprogram'])+"|"+str(xs['kodekegiatan'])+"|"+str(xs['kodesubkegiatan'])
		arrRinc.append({'nomor':xs['nomor'],'nosp2d':xs['nosp2d'],'nospm':xs['nospm'],'tanggal':tgl_indo(xs['tanggal']),
			'eskapede':xs['skpd'],'organisasi':xs['organisasi'],'keperluan':xs['keperluan'],'jumlah':xs['jumlah'],'kodeunit':xs['kodeunit'],
			'kegiatan':kegiatan,'uraian':uraian_x })
	
	arrData = {'asal':asal,'hasil':arrRinc}

	return render(request,'sp2d/modal/modal_spm_sp2d.html',arrData)

def sp2d_gu_kepmen_tabel(request):
	data 	= request.POST
	skpd 	= data.get('skpd').split('.')
	nospm 	= data.get('nospm_x').upper()
	nosp2d 	= data.get('nosp2d_x').upper()
	tanggal = tgl_short(data.get('tgl'))
	asal 	= data.get('asal').upper()
	tahun 	= tahun_log(request)
	kodeunit = data.get('kodeunit')


	tot_sekarang = kd_prog = kd_subkeg = 0
	kd_rekening = hasil = kd_keg = kd_bid = ''
	arrOne = []

	if data.get('kegiatan') != "":
		kegiatan = data.get('kegiatan').split('.')
		kd_bid 	= str(kegiatan[0]+"."+kegiatan[1])
		kd_prog = kegiatan[2]
		kd_keg 	= str(kegiatan[3]+"."+kegiatan[4])
		kd_subkeg = kegiatan[5]

	if data.get('skpd') != '' and data.get('kegiatan') != '':
		with connections[tahun_log(request)].cursor() as cursor:
			if(asal == 'SP2D'):
				cursor.execute("SELECT * FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d,kd_bid,kd_prog,kd_keg,kd_subkeg,tanggal,'GU'])
			elif(asal == 'SPM'):
				cursor.execute("SELECT * FROM penatausahaan.fc_view_spm_rincian_to_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nospm,kd_bid,kd_prog,kd_keg,kd_subkeg,tanggal,'GU'])
			hasil = dictfetchall(cursor)

		for i in range(len(hasil)):
			hasil[i].update({'nomer':1+i})
			tot_sekarang += hasil[i]['sekarang']
			
			if(hasil[i]['cek'] == 1):
				kd_rekening  += ",%"+hasil[i]['koderekening']+"%"

		for dt in hasil:
			dt['batas'] = format_rp(dt['batas']) if dt['batas'] != None else '0,00'
			dt['anggaran'] = format_rp(dt['anggaran'])
			dt['lalu'] = format_rp(dt['lalu'])
			dt['sekarang'] = format_rp(dt['sekarang'])
			dt['jumlah'] = format_rp(dt['jumlah'])
			dt['sisa'] = format_rp(dt['sisa'])
			arrOne.append(dt)

	else:
		tot_sekarang = 0.00

	data = { 'kd_rekening':kd_rekening[1:], 'tabel':arrOne,
		'rupiah':format_rp(tot_sekarang), 'terbilang':terbilang(tot_sekarang) }

	return render(request,'sp2d/tabel/ppkdbtl.html',data)

def sp2d_gu_kepmen_sumberdana(request):
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
	kd_bid 	= kd_keg = ''
	kd_prog = kd_subkeg = 0

	if data.get('kegiatan') != "":
		kegiatan = data.get('kegiatan').split('.')
		kd_bid 	= str(kegiatan[0]+"."+kegiatan[1])
		kd_prog = kegiatan[2]
		kd_keg 	= str(kegiatan[3]+"."+kegiatan[4])
		kd_subkeg = kegiatan[5]

	if(aksi == 'true'): ARG = " "
	else: 
		ARG = "WHERE koderekening IN ("+kdreken+")"

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT distinct kodesumberdana,sumberdana "\
			"FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "+ARG+" "\
			"GROUP BY kodesumberdana,sumberdana ORDER BY kodesumberdana ASC",
			[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nosp2d,kd_bid,kd_prog,kd_keg,kd_subkeg,tanggal,'GU'])
		hasil = dictfetchall(cursor)

	kd_sumdan = nm_sumdan = ""

	for val in hasil:
		kdSD = str(val['kodesumberdana'])
		nmSD = str(val['sumberdana'])
		if(kdSD < "0" or kdSD == "None" or kdSD == ""): kode = "0"
		else: kode = kdSD

		if(nmSD < "0" or nmSD == "None" or nmSD == ""): nmSD = ""
		else: nmSD = nmSD

		kd_sumdan += ",%"+kode+"%"
		nm_sumdan += ",%"+nmSD+"%"

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM penatausahaan.load_sumberdanasp2d(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
			[tahun_log(request), skpd[0],skpd[1],skpd[2],skpd[3], kd_bid, kd_prog, kd_keg, kd_subkeg])
		load_sumdan = dictfetchall(cursor)

	urai_sumdan__ = ''
	kd_sumdan__ = ''
	
	if len(load_sumdan) == 1:
		urai_sumdan__ = load_sumdan[0]['out_namasumberdana']
		kd_sumdan__ = load_sumdan[0]['out_kodesumberdana']
	
	data = {
		"KD_SUMBERDANA" : kd_sumdan[1:],
		"NM_SUMNERDANA" : nm_sumdan[1:],
		"jml_sumdan": len(load_sumdan),
		"urai_sumdan__": urai_sumdan__,
		"kd_sumdan__": kd_sumdan__,
	}

	return JsonResponse(data)

def sp2d_gu_kepmen_rekening(request):
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

def sp2d_gu_kepmen_ambil_spm(request):
	data 	= request.POST
	tahun 	= tahun_log(request)
	nospm 	= data.get('nospm').upper()
	skpd 	= data.get('skpd').split('.')
	kdunit 	= data.get('kdunit')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select nospm, tanggal, informasi, norekbank, bank, npwp, namayangberhak, triwulan\
			from penatausahaan.spm where tahun = %s and kodeurusan = %s and kodesuburusan = %s \
			and kodeorganisasi = %s and kodeunit = %s and nospm = %s",
			[tahun,skpd[0],skpd[1],skpd[2],kdunit,nospm])
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

def sp2d_gu_kepmen_ambil_sp2d(request):
	data 	= request.POST
	tahun 	= tahun_log(request)
	nosp2d 	= data.get('nosp2d').upper()
	skpd 	= data.get('skpd').split('.')
	akses 	= hakakses(request).upper()
	kodeunit = data.get('kodeunit')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select *,case when sumberdana is null then '|' else sumberdana end as sumdan \
			from penatausahaan.sp2d where tahun = %s and kodeurusan = %s \
			and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nosp2d = %s",
			[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nosp2d])
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
				"KODEUNIT" 		 : hsl["kodeunit"],
				"KUNCI" 		 : KUNCI,
				"LOCKED" 		 : hsl["locked"],
				"TANGGAL" 		 : tgl_indo(hsl["tanggal"]),
				"TGLSPM" 		 : tgl_indo(hsl["tglspm"]),
				"NOSPM" 		 : hsl["nospm"],
				"DESKRIPSISPM" 	 : hsl["deskripsispm"],
				"BANKASAL" 		 : hsl["bankasal"],
				"NOREKBANKASAL"  : hsl["norekbankasal"],
				"NAMAYANGBERHAK" : hsl["namayangberhak"],
				"SUMBERDANA" 	 : hsl["sumdan"],
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

def sp2d_gu_kepmen_potongan(request):
	data 	= request.POST

	if data.get('skpd') != "":
		skpd = data.get('skpd').split('.')
	else:
		skpd = '0.0.0.0'.split('.')

	tahun_x = tahun_log(request)
	nospm   = data.get('nospm').upper()
	nosp2d 	= data.get('nosp2d').upper()
	asal 	= data.get('asal').upper()
	kodeunit = data.get('kodeunit')

	arrJns = arrJns_potongan

	with connections[tahun_log(request)].cursor() as cursor:
		if asal == "SP2D":
			cursor.execute("select row_number() over() as nomor, s.idbiling,\
				s.rekeningpotongan,s.jumlah as jumlahpotongan,s.jenispotongan,''as keterangan,\
					(select kdrek from master.mpajak mp where mp.koderekening=s.rekeningpotongan) as kdrek,	\
				( select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun \
				and  r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||lpad(r.kodeobjek::text,2,'0')\
				||'.'||lpad(r.koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,3,'0')\
				=s.rekeningpotongan) from penatausahaan.sp2dpotongan s\
				where s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s\
				and s.kodeorganisasi = %s and s.kodeunit = %s and s.nosp2d = %s",
				[tahun_x, skpd[0], skpd[1], skpd[2], kodeunit, nosp2d])

		elif asal == "SPM":
			cursor.execute("select row_number() over() as nomor, s.idbiling,\
				s.rekeningpotongan,s.jumlah as jumlahpotongan,s.jenispotongan,''as keterangan,\
					(select kdrek from master.mpajak mp where mp.koderekening=s.rekeningpotongan) as kdrek,	\
				(select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun \
				and  r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||LPAD(r.kodeobjek::text,2,'0')\
				||'.'||LPAD(r.koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,3,'0')\
				=s.rekeningpotongan) from penatausahaan.spmpotongan s\
				where s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s\
				and s.kodeorganisasi = %s and s.kodeunit = %s and s.nospm = %s",
				[tahun_x, skpd[0], skpd[1], skpd[2], kodeunit, nospm])

		hasil = dictfetchall(cursor)

	arrOne = []
	for dt in hasil:
		dt['jumlahpotongan'] = format_rp(dt['jumlahpotongan'])
		arrOne.append(dt)

	ArrDT = {'potongan':hasil, 'jnsPot':arrJns}

	return render(request,'sp2d/tabel/sp2d_potongan.html',ArrDT)

def sp2d_gu_kepmen_mdl_cut(request):
	data 	= request.GET
	tahun_x = tahun_log(request)
	aidirow = data.get("i")

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0') \
			||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,3,'0') AS rekeningpotongan,urai \
			FROM master.master_rekening WHERE tahun = %s AND kodeakun = 2 AND kodekelompok = 1 \
			AND kodejenis IN (1) AND kodesubrincianobjek <> 0 ",[tahun_x])
		hasil = dictfetchall(cursor)

	ArrDT = {'aidirow':aidirow, 'hasil':hasil}
	return render(request,'sp2d/modal/sp2d_potongan.html',ArrDT)

def sp2d_gu_kepmen_frm_lap(request):

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		skpd 	= data.get('id_skpd').split('.')
		tahun 	= tahun_log(request)
		nosp2d 	= data.get('no_sp2d_lap').upper()
		aidi 	= data.get('id_pejabat')
		sumdana	= str(data.get('lap_sumberdana').replace("%",""))
		kodeunit = data.get('kodeunit')

		lapParm['report_type'] 		= 'pdf'
		lapParm['file'] 			= 'penatausahaan/sp2d/sp2d.fr3'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['nosp2d'] 			= "'"+nosp2d+"'"
		lapParm['kodeurusan'] 		= skpd[0]
		lapParm['kodesuburusan'] 	= skpd[1]
		lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
		lapParm['kodeunit'] 		= "'"+kodeunit+"'"
		lapParm['id'] 				= aidi
		lapParm['sumberdana'] 		= sumdana

		return HttpResponse(laplink(request, lapParm))

	else:
		list_pejabat = get_pejabat_pengesah(request)
		data = { 'ls_data':list_pejabat }

		return render(request,'sp2d/laporan/btlppkd.html',data)

def sp2d_gu_kepmen_simpan(request, jenis):
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
		tgl_saiki		= 'now()'
		# sumdana			= data.get('nm_sumberdana').replace("%","")
		sumdana			= data.get('frm_sumberdana_x')+'|'+data.get('frm_sumberdana')
		rincian 		= data.getlist('checkbox')
		norekbankasal 	= data.get('norek_bankasal').split('|')[1]
		duite 			= toAngkaDec(data.get('tot_sekarang'))
		enpewepe 		= data.get('npwp_bendahara')
		pot_kdrek 		= data.getlist('cut_kdrek')
		pot_jumlah 		= data.getlist('jml_pot')
		pot_jenis 		= data.getlist('jns_cut')
		pot_idbiling 	= data.getlist('idbiling')
		kegiatan 		= data.get('kegiatan').split('.')
		kd_bid 			= str(kegiatan[0]+"."+kegiatan[1])
		kd_prog 		= kegiatan[2]
		kd_keg 			= kegiatan[3]
		kodeunit 		= data.get('kodeunit')

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
								cursor.execute("INSERT INTO penatausahaan.sp2d(tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
								nosp2d,tanggal,tanggal_draft,norekbank,bank,npwp,nospm,tglspm,jumlahspm,\
								pemegangkas,namayangberhak,kodebidang,kodeprogram,kodekegiatan,triwulan,\
								lastupdate,jenissp2d,sumberdana,informasi,deskripsispm,perubahan,\
								rekeningpengeluaran,statuskeperluan,jumlahsp2d,norekbankasal,bankasal,uname) \
								values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d,tglsp2d,tglsp2d,data.get('norek_bendahara'),
								data.get('bank_bendahara'),npwp_x,data.get('no_spm'),tglspm,duite,
								data.get('bendahara'),data.get('bendahara'),'',0,0,data.get('inpt_triwulan'),
								tgl_saiki,'GU',sumdana,data.get('status_keperluan'),
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
			cek_lock = cek_isLocked(tahun,nosp2d_x,skpd[0],skpd[1],skpd[2],kodeunit)

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
						AND KODEUNIT = %s AND NOSP2D = %s",
						[nosp2d,tglsp2d,tglsp2d,data.get('no_spm'),tglspm,duite,duite,data.get('bendahara'),
						sumdana,data.get('bendahara'),data.get('inpt_triwulan'),tgl_saiki,data.get('status_keperluan'),
						data.get('status_keperluan'),data.get('inpt_perubahan'),data.get('status_keperluan'),
						data.get('bank_asal'),norekbankasal,data.get('norek_bendahara'),data.get('bank_bendahara'),
						npwp_x,tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d_x])

				isSimpan = 1
				pesan = 'Perubahan nomor SP2D : '+nosp2d_x+' berhasil disimpan !'

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN WHERE NO.SP2D
				cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN WHERE tahun = %s AND kodeurusan = %s \
					AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nosp2d = %s ",
					[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d])

				# HAPUS TABEL POTONGAN WHERE NO.SP2D
				cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN WHERE tahun = %s AND kodeurusan = %s \
					AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nosp2d = %s ",
					[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d])

				# INSERT INTO TABEL RINCIAN
				# print(rincian)
				for val in rincian:
					hasil  = val.split("|")
					objek0 = hasil[1].split("-")
					objek1 = objek0[0].split(".")
					objek2 = objek0[1].split(".")
					uange  = toAngkaDec(hasil[2])

					cursor.execute("INSERT INTO penatausahaan.SP2DRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,\
						KODEORGANISASI,KODEUNIT,NOSP2D,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,\
						KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK, \
						TANGGAL,JUMLAH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun,skpd[0],skpd[1],skpd[2],kodeunit,nosp2d,
						objek1[0]+"."+objek1[1],objek1[2],objek1[3]+"."+objek1[4],objek1[5],0,
						objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],objek2[5],tglsp2d,uange])

				for p in range(len(pot_kdrek)):
					if pot_kdrek[p] != "":
						cursor.execute("INSERT INTO penatausahaan.SP2DPOTONGAN (TAHUN,KODEURUSAN,KODESUBURUSAN,\
							KODEORGANISASI,KODEUNIT,NOSP2D,TANGGAL,REKENINGPOTONGAN,JUMLAH,JENISPOTONGAN,IDBILING) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,skpd[0],skpd[1],skpd[2],kodeunit,
							nosp2d,tglsp2d,pot_kdrek[p],toAngkaDec(pot_jumlah[p]),pot_jenis[p], pot_idbiling[p]])

			
# UNTUK DELETE ==============================================================================================
	else: 
		skpd 	= data.get('skpd').split('.')
		nosp2d 	= data.get('nosp2d').upper()

		cek_lock = cek_isLocked(tahun,nosp2d,skpd[0],skpd[1],skpd[2],skpd[3])

		if cek_lock == 'Y':
			isSimpan = -1
			pesan = 'SP2D Nomor : "'+nosp2d+'" telah di ACC oleh pimpinan. Anda tidak diperkenankan menghapus SP2D tersebut!'
		else:
			where 	= " WHERE tahun = %s AND kodeurusan = %s AND kodesuburusan = %s \
				AND kodeorganisasi = %s AND kodeunit = %s AND nosp2d = %s AND locked <> 'Y' "

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.SP2D"+where,[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nosp2d])
			## cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN"+where,[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nosp2d])
			## cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN"+where,[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nosp2d])

			isSimpan = 0
			pesan = 'Data SP2D Dengan Nomor : '+nosp2d+', berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)