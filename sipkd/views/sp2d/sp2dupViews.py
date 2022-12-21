from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def up(request):
	no_rekening = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT rekening,bank,kodesumberdana, urai from kasda.kasda_sumberdanarekening \
			where kodesumberdana <99 order by kodesumberdana")
		no_rekening = dictfetchall(cursor)
	
	data = { 'no_rekening':no_rekening, }

	return render(request, 'sp2d/up.html', data)

def cekdataUP(request):
	kd_org = request.POST.get('kd_org','')
	hasil = ''

	if kd_org != '':
		kd_urusan = kd_org.split('.')[0]
		kd_suburusan = kd_org.split('.')[1]
		kd_organisasi = kd_org.split('.')[2]
		kd_unit = kd_org.split('.')[3]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT COUNT(*) as jumlah from penatausahaan.sp2d where tahun=%s \
				and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and jenissp2d='UP'",
				[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit])
			hasil = dictfetchall(cursor)

	data = { 'hasil':hasil, }

	return JsonResponse(data)

def cekdataSKUP(request):
	kd_org = request.POST.get('kd_org','')
	hasil = ''

	if kd_org != '':
		kd_urusan = kd_org.split('.')[0]
		kd_suburusan = kd_org.split('.')[1]
		kd_organisasi = kd_org.split('.')[2]
		kd_unit = kd_org.split('.')[3]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.sk_up where tahun=%s and kodeurusan=%s \
				and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s",
				[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit])
			hasil = dictfetchall(cursor)

	data = { 'hasil':hasil, }

	return JsonResponse(data)

def ambilUP(request):
	kd_org = request.POST.get('kd_org','')
	ket = request.POST.get('ket','')
	nosp2d = request.POST.get('nosp2d','')
	hasil = ''
	hasilnya = ''

	if kd_org != '':
		if ket == 'new':
			kd_urusan = kd_org.split('.')[0]
			kd_suburusan = kd_org.split('.')[1]
			kd_organisasi = kd_org.split('.')[2]
			kd_unit = kd_org.split('.')[3]

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nosp2d \
					FROM penatausahaan.sp2d where tahun=%s and kodeurusan=%s \
					and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and jenissp2d='UP'",
					[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit])
				hasil = dictfetchall(cursor)

			for x in range(len(hasil)):
				hasilnya = ambilDataSp2d(request, hasil[x]['kodeurusan'], hasil[x]['kodesuburusan'], hasil[x]['kodeorganisasi'], hasil[x]['kodeunit'], hasil[x]['nosp2d'])
		
		elif ket == 'not_new':
			kd_urusan = kd_org.split('.')[0]
			kd_suburusan = kd_org.split('.')[1]
			kd_organisasi = kd_org.split('.')[2]
			kd_unit = kd_org.split('.')[3]

			hasilnya = ambilDataSp2d(request, kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d)

	data = { 'hasil':hasilnya, }

	return JsonResponse(data)

def ambilDataSp2d(request, kd_urusan, kd_suburusan, kd_organisasi , kd_unit, nosp2d):
	hasil = ''
	
	if kd_urusan!= '' and kd_suburusan != '' and kd_organisasi != '' and kd_unit != '' and nosp2d != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.sp2d where tahun =%s and kodeurusan=%s \
				and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nosp2d=%s",
				[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d])
			hasil = dictfetchall(cursor)

		hasil[0]['kodesumberdana'] = get_kodesumdan(request, hasil[0]['norekbankasal'])
	return hasil

def ambil_spm(request):
	hasil = ''
	no_spm = request.POST.get('no_spm', '')
	kd_org = request.POST.get('kd_org','')

	if no_spm!='' and kd_org!='':
		kd_urusan = kd_org.split('.')[0] 
		kd_suburusan = kd_org.split('.')[1]
		kd_organisasi = kd_org.split('.')[2]
		kd_unit = kd_org.split('.')[3].split('-')[0]
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.spm where tahun=%s and kodeurusan = %s \
				and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospm = %s", 
				[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, no_spm])
			hasil = dictfetchall(cursor)

	data = {
		'hasil':hasil,
	}
	return JsonResponse(data)

def simpan_sp2d(request):
	hasil = 'SP2D berhasil disimpan.'
	no_spm = request.POST.get('no_spm', '')
	kd_org = request.POST.get('kd_org','')
	isSimpan = request.POST.get('isSimpan', '')
	nosp2d = request.POST.get('nosp2d','')
	tanggal = request.POST.get('tanggal','')
	tanggal_draft = request.POST.get('tanggal_draft','')
	tglspm = request.POST.get('tglspm','')
	jumlahspm = request.POST.get('jumlahspm','')
	pemegangkas = request.POST.get('pemegangkas','')
	namayangberhak = request.POST.get('namayangberhak','')
	triwulan = request.POST.get('triwulan','')
	sumberdana = request.POST.get('sumberdana','')
	lastupdate = request.POST.get('lastupdate','')
	informasi = request.POST.get('informasi','')
	deskripsispm = request.POST.get('deskripsispm','')
	perubahan = request.POST.get('perubahan','')
	statuskeperluan = request.POST.get('statuskeperluan','')
	jumlahsp2d = request.POST.get('jumlahsp2d','')
	bankasal = request.POST.get('bankasal','')
	norekbank = request.POST.get('norekbank','')
	norekbankasal = request.POST.get('norekbankasal').split('|')[1]
	bank = request.POST.get('bank','')
	npwp = request.POST.get('npwp','')
	nosp2d_asli = request.POST.get('nosp2d_asli','')
	oke = False

	org = request.POST.get('kd_org', None).split('.') 

	if no_spm!='' and kd_org!='' and isSimpan != '':
		kd_urusan = kd_org.split('.')[0] 
		kd_suburusan = kd_org.split('.')[1]
		kd_organisasi = kd_org.split('.')[2].split('-')[0]
		
		print(isSimpan)
		if isSimpan == 'false':
			if check_locked_sp2d(request, kd_org, nosp2d_asli.upper())=='T':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("update penatausahaan.sp2d set\
								nosp2d=%s\
								,tanggal=%s\
								,tanggal_draft=%s\
								,nospm=%s\
								,tglspm=%s\
								,jumlahspm=%s\
							    ,pemegangkas=%s\
							    ,namayangberhak=%s\
							    ,triwulan=%s\
							    ,sumberdana=%s\
							    ,lastupdate=%s\
							    ,informasi=%s\
							    ,deskripsispm=%s\
							    ,perubahan=%s\
							    ,statuskeperluan=%s\
							    ,jumlahsp2d=%s\
							    ,bankasal=%s\
							    ,norekbank=%s\
							    ,norekbankasal=%s\
							    ,bank=%s\
								,npwp=%s\
								WHERE tahun=%s\
								AND kodeurusan=%s\
								AND kodesuburusan=%s\
								AND kodeorganisasi=%s\
								AND kodeunit=%s\
								AND nosp2d=%s",[nosp2d.upper(),tgl_to_db(tanggal),tgl_to_db(tanggal_draft),no_spm,tgl_to_db(tglspm),jumlahspm,pemegangkas,namayangberhak,triwulan,sumberdana,lastupdate,informasi,deskripsispm,perubahan,statuskeperluan,jumlahsp2d,bankasal,norekbank,norekbankasal,bank,npwp,tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi,org[3],nosp2d_asli.upper()])
					hasil = 'SP2D berhasil diubah.'
					oke = True
					
		elif isSimpan == 'true':
			if(check_before_insert(request,kd_org)[0]==0):
				with connections[tahun_log(request)].cursor() as cursor:
					try:
						cursor.execute("insert into penatausahaan.sp2d(tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nosp2d,tanggal,tanggal_draft,norekbank,\
								bank,npwp,nospm,tglspm,jumlahspm,pemegangkas,namayangberhak,kodebidang,kodeprogram,kodekegiatan,triwulan,\
								lastupdate,jenissp2d,informasi,deskripsispm,sumberdana,perubahan,rekeningpengeluaran,statuskeperluan,jumlahsp2d,norekbankasal,bankasal,uname ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun_log(request),org[0],org[1],org[2],org[3],nosp2d.upper(),tgl_to_db(tanggal),tgl_to_db(tanggal_draft),norekbank,bank,npwp,no_spm,tgl_to_db(tglspm),jumlahspm,pemegangkas,namayangberhak,'', 0,0,triwulan,lastupdate,'UP',informasi,deskripsispm,sumberdana,perubahan,'1.1.1.01.0 - Kas Daerah',statuskeperluan,jumlahsp2d,norekbankasal,bankasal,username(request)])
						
						hasil = 'SP2D berhasil disimpan.'
						oke = True				
					except IntegrityError as e:
						hasil = 'Nomor SP2D sudah ada !'
						oke = False
			else:
				hasil = 'SP2D sudah dibuat, UP hanya sekali dalam satu tahun'
				oke = False

		if oke == True:
			with connections[tahun_log(request)].cursor() as cursor2:
				cursor2.execute("delete from penatausahaan.sp2drincian where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nosp2d=%s",[tahun_log(request),org[0], org[1],org[2],org[3], nosp2d.upper()])
			with connections[tahun_log(request)].cursor() as cursor3:	
				cursor3.execute("insert into penatausahaan.sp2drincian (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nosp2d,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodesubkeluaran,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,tanggal,jumlah) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request), org[0],org[1],org[2],org[3], nosp2d.upper(), '', 0,'0',0,0,1,1,1,3,1,1,tgl_to_db(tanggal),jumlahsp2d])
				#print ("insert into penatausahaan.sp2drincian (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nosp2d,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodesubkeluaran,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,tanggal,jumlah) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request), org[0],org[1],org[2],org[3], nosp2d.upper(), '', 0,'0',0,0,1,1,1,3,1,1,tgl_to_db(tanggal),jumlahsp2d])
	return HttpResponse(hasil)

def render_cetak_sp2dup(request):
	pejabat = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1 \
			from master.pejabat_skpkd where tahun=%s and jenissistem=2", [tahun_log(request)])
		pejabat = dictfetchall(cursor)

	data = {
		'pejabat':pejabat,
	}
	return render(request, 'sp2d/modal/laporan_up.html', data)

def cetak_sp2dup(request):
	post 	= request.POST
	lapParm = {}
	skpd 	= post.get('skpd').split('.')
	no_sp2d = post.get('no_sp2d')
	tgl_sp2d = post.get('tgl_sp2d')
	nama = post.get('nama')
	nip = post.get('nip')
	pangkat = post.get('pangkat')
	id_jabatan = post.get('id_jabatan')

	lapParm['file'] = 'penatausahaan/sp2d/sp2d.fr3'	
	lapParm['tahun'] = "'"+tahun_log(request)+"'"
	lapParm['nosp2d'] ="'"+no_sp2d+"'"
	lapParm['kodeurusan'] = "'"+skpd[0]+"'"
	lapParm['kodesuburusan'] = "'"+skpd[1]+"'"
	lapParm['kodeorganisasi'] = "'"+skpd[2]+"'"
	lapParm['kodeunit'] = "'"+skpd[3]+"'"
	lapParm['id'] = "'"+id_jabatan+"'"
	lapParm['sumberdana'] = "'"+get_sumdan_laporan(request,no_sp2d)+"'"
	lapParm['report_type'] = 'pdf'

	# http://localhost/sipkd_deiyai/report/?tahun=2016&file=spd/SPD.fr3&report_type=pdf&KodeUrusan='1'&KodeSubUrusan='1'&KodeOrganisasi='01'&NOMER='0001/SPD/1/2016'&ID=3

	return HttpResponse(laplink(request, lapParm))

def hapus_sp2d(request):
	hasil = ''
	kd_org = request.POST.get('kd_org','')
	nosp2d = request.POST.get('nosp2d','')
	

	if hakakses(request)!='BELANJA':
		if kd_org!='' and nosp2d!='':
			org = request.POST.get('kd_org', None).split('.') 

			if check_locked_sp2d(request, kd_org, nosp2d)=='T':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.sp2d WHERE tahun = %s and kodeurusan = %s \
						and kodesuburusan = %s and kodeorganisasi = %s and kodeunit=%s and nosp2d = %s",
						[tahun_log(request), org[0], org[1], org[2],org[3], nosp2d])
					hasil = 'Berhasil dihapus'
	return HttpResponse(hasil)

def ambilbankData(request):
	hasil_bank = ''
	norek = request.POST.get('norek','')
	if norek!='':
		kodesumberdana = norek.split('|')[3]
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * from kasda.kasda_sumberdanarekening where kodesumberdana = %s",
				[kodesumberdana])
			hasil_bank = dictfetchall(cursor)
	data = {
		'hasil_bank':hasil_bank,
	}
	return JsonResponse(data)

def check_before_insert(request, skpd):
	if skpd != '':
		with connections[tahun_log(request)].cursor() as cursor:
			kd_urusan = skpd.split('.')[0]
			kd_suburusan = skpd.split('.')[1]
			kd_organisasi = skpd.split('.')[2]
			kd_unit = skpd.split('.')[3]
			org = request.POST.get('kd_org', None).split('.') 

			cursor.execute("SELECT count(tahun) as jumlah_pertahun FROM penatausahaan.sp2d WHERE tahun = %s \
				and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s \
				and jenissp2d= 'UP'",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit])
			hasil = cursor.fetchone()
	return hasil