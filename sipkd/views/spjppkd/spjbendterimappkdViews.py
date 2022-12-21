from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json
import time
kd_org_bendterima = ''
xbulan = ''

def spjbendterimappkd(request):
	data = {

	}
	return render(request, 'spjppkd/spjbendterimappkd.html', data)

def refreshdata_spjbendterimappkd(request):
	hasil_penerimaan = ''
	hasil_setor = ''
	kd_organisasi = request.POST.get('kode_organisasi')
	bulan = request.POST.get('xbulan')

	global kd_org_bendterima
	kd_org_bendterima = kd_organisasi
	
	global xbulan
	xbulan = bulan

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT NOBKU,TGLBKU,NOBUKTI,TGLBUKTI,URAIAN,CARABAYAR,STATUS,JUMLAH,0 as cek,xstatus FROM pertanggungjawaban.fc_SKPD_VIEW_PENERIMAAN(%s,%s,%s,%s,%s,%s) where x_bulan = %s",[tahun_log(request), kd_organisasi.split('.')[0], kd_organisasi.split('.')[1], kd_organisasi.split('.')[2], xbulan, 1 ,xbulan])
		hasil_penerimaan = dictfetchall(cursor)
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM pertanggungjawaban.fc_SKPD_VIEW_SETOR(%s,%s,%s,%s,%s,%s)",[tahun_log(request), kd_organisasi.split('.')[0], kd_organisasi.split('.')[1], kd_organisasi.split('.')[2], xbulan, 1])
		hasil_setor = dictfetchall(cursor)
	
	data = {
		'hasil_penerimaan':convert_tuple(hasil_penerimaan),
		'hasil_setor':convert_tuple(hasil_setor),
	}
	return JsonResponse(data)

def hapus_spjbendterimappkd(request):
	jenis = request.POST.get('jenis')
	pesan = ''
	no_bku_sts = []

	
	if jenis=='penerimaan':
		arr_penerima = json.loads(request.POST.get('arr_penerima'))
		for x in range(len(arr_penerima)):
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM pertanggungjawaban.skpd_penerimaan WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU = %s AND ISSKPD=1",[
					tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2],arr_penerima[x].split('^')[0]])
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU = %s AND ISSKPD=1",[
					tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2],arr_penerima[x].split('^')[0]])
	elif jenis=='setor':
		arr_setor_bendterima = json.loads(request.POST.get('arr_setor_bendterima'))
		
		for x in range(len(arr_setor_bendterima)):
			no_bku_sts.append(arr_setor_bendterima[x].split('^')[0])
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM pertanggungjawaban.skpd_penerimaan WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU = %s AND ISSKPD=1",[
					tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2],arr_setor_bendterima[x].split('^')[0]])
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU = %s AND ISSKPD=1",[
					tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2],arr_setor_bendterima[x].split('^')[0]])
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("UPDATE pertanggungjawaban.SKPD_PENERIMAAN SET LOCKED= 'T',BKU_STS=null WHERE BKU_STS in ("+','.join(no_bku_sts)+") AND TAHUN=%s\
			 AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND ISSKPD=1",[tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2]])
			
	return HttpResponse(pesan)

def tambah_spjbendterimappkd_terima(request,jenisnya,no_bku,nobukti,jenisterima):
	nomor_oto = [None]
	rekening = ''
	no_bku_db = no_bku
	nobukti_db1 = nobukti.replace("^**^", " ").split('_')
	nobukti_db = '/'.join(nobukti_db1)
	hasil = [{'dummy': ''}]
	rincian_rekening = ''
	hilang = ''
	lbl_wajar = 'Wajib Bayar'
	isSimpan = True
	lbl_tbp = 'TBP'
	
	if jenisnya == 'add':
		isSimpan = True
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT MAX(NO_BKU+1) as NOBKU FROM pertanggungjawaban.SKPD_PENERIMAAN WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and isskpd = 1',[tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2]])
			nomor_oto = cursor.fetchone()
		if jenisterima=='setor':
			hilang = 'hilang'
			lbl_wajar = 'Penyetor'
			lbl_tbp = 'STS'
	else:
		isSimpan = False
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM pertanggungjawaban.skpd_penerimaan WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and no_bku = %s and replace(nobukti, ' ', '') = %s and isskpd=1", [tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2], no_bku_db, nobukti_db.replace(' ', '')])
			hasil = dictfetchall_format(cursor)
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM pertanggungjawaban.fc_skpd_view_penerimaan_rekening(%s,%s,%s,%s,%s,%s)",[tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2], no_bku_db, 0])
			rincian_rekening = convert_tuple(dictfetchall(cursor))
		if jenisterima == 'pungut':
			lbl_wajar = 'Wajib Bayar'
		elif jenisterima=='setor':
			lbl_tbp = 'STS'
			hilang = 'hilang'
			lbl_wajar = 'Penyetor'
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from kasda.kasda_sumberdanarekening where kodesumberdana<=99")
		rekening = dictfetchall(cursor)

	data = {
		'nomor_oto':'1' if nomor_oto[0] == None else nomor_oto[0],
		'rekening':rekening,
		'hasil':hasil,
		'jenisnya':jenisnya,
		'rincian_rekening':json.dumps({'rr':rincian_rekening}),
		'hilang':hilang,
		'jenisterima':jenisterima,
		'lbl_wajar':lbl_wajar,
		'lbl_tbp':lbl_tbp,
		'hasil_pungutan':json.dumps({'hasil_pungutan':convert_tuple(ambilPungutanppkd(request,isSimpan,no_bku_db))}),
	}
	return render(request, 'spjppkd/modal/input_edit_spjbendterima_ppkd.html', data)

def ambilPungutanppkd(request,isSimpan,no_bku):
	hasil_pungutan = ''

	if isSimpan == True:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM pertanggungjawaban.fc_SKPD_VIEW_PENERIMAAN(%s,%s,%s,%s,%s,%s) WHERE XSTATUS = 'T'",[
				tahun_log(request), kd_org_bendterima.split('.')[0],kd_org_bendterima.split('.')[1],kd_org_bendterima.split('.')[2],
				xbulan,1])
			hasil_pungutan = dictfetchall(cursor)
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM pertanggungjawaban.fc_SKPD_EDIT_SETOR(%s,%s,%s,%s,%s,%s,%s) WHERE BKU_STS = %s or BKU_STS is NULL or BKU_STS = 0",[
				tahun_log(request), kd_org_bendterima.split('.')[0],kd_org_bendterima.split('.')[1],kd_org_bendterima.split('.')[2],1,int(xbulan),no_bku,no_bku])
			hasil_pungutan  = dictfetchall(cursor)
	
	return hasil_pungutan

def input_tambah_penerimaanppkd(request,jenisnya):
	arr_fix = json.loads(request.POST.get('arr_fix'))
	arr_setor = json.loads(request.POST.get('arr_setor'))
	jenis_pungutValue = request.POST.get('jenis_pungutValue','')
	no_bkuValue = request.POST.get('no_bkuValue','')
	tgl_bkuValue = request.POST.get('tgl_bkuValue','')
	no_buktiValue = request.POST.get('no_buktiValue','')
	tgl_buktiValue = request.POST.get('tgl_buktiValue','')
	cara_bayarValue = request.POST.get('cara_bayarValue','')
	uraianValue = request.POST.get('uraianValue','')
	wajib_bayarValue = request.POST.get('wajib_bayarValue','')
	alamatValue = request.POST.get('alamatValue','')
	npwpdValue = request.POST.get('npwpdValue','')
	jenistransaksiValue = request.POST.get('jenistransaksiValue','')
	no_ketetapanValue = request.POST.get('no_ketetapanValue','')
	rekeningbankValue = request.POST.get('rekeningbankValue','')
	locked = 'T'
	total = 0
	total_setor = 0
	no_bku_setor = []

	isSimpan = request.POST.get('isSimpan','')
	kd_urusan = kd_org_bendterima.split('.')[0]
	kd_suburusan = kd_org_bendterima.split('.')[1]
	kd_organisasi = kd_org_bendterima.split('.')[2]

	hasil_select_setor = ''

	for x in range(len(arr_fix)):
		total += float(arr_fix[x].split('^')[1])

	for x in range(len(arr_setor)):
		total_setor += float(arr_setor[x].split('^')[2])
		no_bku_setor.append(arr_setor[x].split('^')[0])

	cek_tgl = time.strptime(tgl_to_db(tgl_bkuValue), "%m/%d/%Y")>=time.strptime(tgl_to_db(tgl_buktiValue), "%m/%d/%Y")
	
	if isSimpan != '':
		if no_bkuValue != '' and no_buktiValue != '' and uraianValue != '' and  cek_tgl == True:
			if jenisnya == 'pungut':
				if isSimpan == 'false':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE pertanggungjawaban.SKPD_PENERIMAAN SET \
										TGL_BKU= %s\
										,TGL_BUKTI=%s\
										,URAI=%s\
										,JUMLAH=%s\
										,CARABAYAR=%s\
										,JENIS_TRANSAKSI=%s\
										,ISSKP=%s\
										,LOCKED=%s\
										,SK1=%s\
										,PENYETOR=%s\
										,ALAMAT=%s\
										,NPWPD=%s\
										 WHERE TAHUN=%s\
										 AND KODEURUSAN = %s\
										 AND KODESUBURUSAN=%s\
										 AND KODEORGANISASI=%s\
										 AND NO_BKU=%s\
										 AND ISSKPD=1",[tgl_to_db(tgl_bkuValue), tgl_to_db(tgl_buktiValue), uraianValue, 
										 total, cara_bayarValue.title(), jenistransaksiValue, jenis_pungutValue, locked, no_ketetapanValue, wajib_bayarValue, alamatValue, npwpdValue,
										 tahun_log(request), kd_urusan,kd_suburusan,kd_organisasi,no_bkuValue])
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO pertanggungjawaban.SKPD_PENERIMAAN(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NO_BKU,ID_STS,TGL_BKU,NOBUKTI,TGL_BUKTI,URAI,CARABAYAR,JUMLAH,LOCKED,ISSKP,JENIS_TRANSAKSI,SK1,PENYETOR,ALAMAT,NPWPD,REKENINGBANK,ISSKPD) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi,no_bkuValue,no_bkuValue,tgl_to_db(tgl_bkuValue),no_buktiValue,tgl_to_db(tgl_buktiValue),uraianValue,cara_bayarValue.title(),total,locked,jenis_pungutValue,jenistransaksiValue,no_ketetapanValue,wajib_bayarValue,alamatValue,npwpdValue,'',1])		

				if cara_bayarValue != 'LEWAT REKENING KAS UMUM DAERAH':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s and kodeurusan = %s\
										and kodesuburusan = %s and kodeorganisasi = %s and no_bku = %s and isskpd = 1",[
										tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, no_bkuValue])	
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("select no_bku from pertanggungjawaban.skpd_penerimaan WHERE TAHUN= %s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI= %s AND ISSKPD=1 and jenis_transaksi='SETOR' and nobukti=%s",[
							tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi,no_buktiValue])
						no_bku_setor = cursor.fetchone()

					if no_bku_setor == None:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU= %s AND ISSKPD=1",[
								tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi,no_bkuValue])
					else:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND NO_BKU in (%s,%s) AND ISSKPD=1",[
								tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi,no_bkuValue,no_bku_setor[0]])


				for x in range(len(arr_fix)):
					if float(arr_fix[x].split('^')[1]) > 0:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("INSERT INTO pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN(TAHUN,KODEURUSAN,KODESUBURUSAN,\
								KODEORGANISASI,NO_BKU,ID_STS,JUMLAH,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,ISSKPD)\
								VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi,
								no_bkuValue, no_bkuValue, float(arr_fix[x].split('^')[1]), arr_fix[x].split('^')[0].split('.')[0],
								arr_fix[x].split('^')[0].split('.')[1],arr_fix[x].split('^')[0].split('.')[2],arr_fix[x].split('^')[0].split('.')[3],
								arr_fix[x].split('^')[0].split('.')[4],1])
			elif jenisnya == 'setor':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("select kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,sum(jumlah) as jumlah \
						from pertanggungjawaban.skpd_rincian_penerimaan where tahun=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s and KODEORGANISASI=%s\
						and isskpd=1 and  no_bku in ("+','.join(no_bku_setor)+") group by  kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek",[
						tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi])
					hasil_select_setor = dictfetchall(cursor)

				if isSimpan == 'false':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE pertanggungjawaban.skpd_penerimaan SET tgl_bku = %s\
							,NOBUKTI=%s\
							,TGL_BUKTI=%s\
							,URAI=%s\
							,CARABAYAR=%s\
							,JENIS_TRANSAKSI=%s\
							,ISSKP=%s\
							,SK1=%s\
							,PENYETOR=%s\
							,ALAMAT=%s\
							,REKENINGBANK=%s\
							 WHERE TAHUN=%s AND KODEURUSAN=%s\
		               		 AND KODESUBURUSAN=%s AND KODEORGANISASI=%s\
		               		 AND NO_BKU=%s\
		               		 AND ISSKPD=1",[tgl_to_db(tgl_bkuValue),no_buktiValue,tgl_to_db(tgl_buktiValue),uraianValue,cara_bayarValue.title(),
		               		 jenistransaksiValue, '0',no_ketetapanValue, wajib_bayarValue, alamatValue,rekeningbankValue,
		               		 tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, no_bkuValue])
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO pertanggungjawaban.SKPD_PENERIMAAN(TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,\
							NO_BKU,ID_STS,TGL_BKU,NOBUKTI,TGL_BUKTI,URAI,CARABAYAR,JUMLAH,LOCKED,ISSKP,JENIS_TRANSAKSI,SK1,PENYETOR,\
							ALAMAT,REKENINGBANK,ISSKPD) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[
							tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, no_bkuValue, no_bkuValue, tgl_to_db(tgl_bkuValue),
							no_buktiValue, tgl_to_db(tgl_buktiValue), uraianValue, '', total, 'T', 0, jenistransaksiValue, no_ketetapanValue,
							wajib_bayarValue, alamatValue, rekeningbankValue, 1])

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN WHERE TAHUN=%s and \
						kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and no_bku = %s and isskpd = 1",[
						tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, no_bkuValue])

				for x in range(len(hasil_select_setor)):
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO pertanggungjawaban.SKPD_RINCIAN_PENERIMAAN(TAHUN,KODEURUSAN,\
							KODESUBURUSAN,KODEORGANISASI,NO_BKU,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,\
							JUMLAH,ID_STS,isskpd) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[
							tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi,no_bkuValue,
							hasil_select_setor[x]['kodeakun'],hasil_select_setor[x]['kodekelompok'],hasil_select_setor[x]['kodejenis'],hasil_select_setor[x]['kodeobjek'],
							hasil_select_setor[x]['koderincianobjek'],hasil_select_setor[x]['jumlah'],no_bkuValue,1])
				
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE pertanggungjawaban.SKPD_PENERIMAAN SET LOCKED= 'T',BKU_STS=null WHERE BKU_STS = %s AND NO_BKU NOT IN("+','.join(no_bku_setor)+") AND TAHUN=%s\
					 AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND ISSKPD=1",[no_bkuValue, tahun_log(request), kd_org_bendterima.split('.')[0], kd_org_bendterima.split('.')[1], kd_org_bendterima.split('.')[2]])

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE pertanggungjawaban.SKPD_PENERIMAAN SET LOCKED = 'Y', \
						BKU_STS=%s WHERE NO_BKU IN ("+','.join(no_bku_setor)+")\
						AND TAHUN=%s AND KODEURUSAN=%s\
			    	    AND KODESUBURUSAN=%s AND isskpd=1 and \
			    	    KODEORGANISASI=%s",[no_bkuValue,tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi])
	return HttpResponse('ssdd')

def cetak_bendterimappkd(request):
	pejabat = ''
	jns_lap = 	[{'label' : "==== Pilih Jenis Laporan ===="},
	  			{'label' : "Buku Kas Umum Penerimaan"},
	  			{'label' : "Rekap Penerimaan Per Rincian Objek"},
	  			{'label' : "Buku Penerimaan dan Penyetoran"},
	  			{'label' : "Register STS"},
	  			{'label' : "Laporan Pertanggung Jawaban Penutupan Kas"},
	  			{'label' : "Rekapitulasi Pertanggung Jawaban"}]
	bulan = [{'label':'Januari'},{'label':'Februari'},{'label':'Maret'},{'label':'April'},{'label':'Mei'},{'label':'Juni'},{'label':'Juli'},{'label':'Agustus'},
			{'label':'September'},{'label':'Oktober'},{'label':'November'},{'label':'Desember'}]

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM master.pejabat_skpd WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s",[
			tahun_log(request),kd_org_bendterima.split('.')[0],kd_org_bendterima.split('.')[1],kd_org_bendterima.split('.')[2]])
		pejabat = dictfetchall(cursor)

	data = {
		'jns_lap':jns_lap,
		'bulan':bulan,
		'pejabat':pejabat,
	}
	return render(request, 'spjppkd/modal/cetak_spjbendterima_ppkd.html', data)

def printout_bendterimappkd(request):
	lapParm = {}
	jenis_laporan = request.POST.get('jenis_laporan','')
	bulan = request.POST.get('bulan','')
	tgl_cetak = request.POST.get('tgl_cetak','')
	id_pengguna = request.POST.get('id_pengguna','')
	id_bendahara = request.POST.get('id_bendahara','')
	radio_tanggung = request.POST.get('radio_tanggung')

	if jenis_laporan != '' and bulan != '' and tgl_cetak != '' and id_pengguna != '' and id_bendahara:
		if jenis_laporan == 'Buku Kas Umum Penerimaan': 
				lapParm['file'] = 'spjppkdPENERIMAAN/BKU_Penerimaan.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""						
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""			
				
		elif jenis_laporan == 'Rekap Penerimaan Per Rincian Objek':
				
				lapParm['file'] = 'spjppkdPENERIMAAN/BKU_Penerimaan_Per_Rincian_Objek.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""						
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""
		elif jenis_laporan == 'Buku Penerimaan dan Penyetoran':
				
				lapParm['file'] = 'spjppkdPENERIMAAN/Buku_Penerimaan_dan_Penyetoran.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""						
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""
		elif jenis_laporan == 'Register STS':
				lapParm['file'] = 'spjppkdPENERIMAAN/Regisskter_STS.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""						
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""
		elif jenis_laporan == 'Laporan Pertanggung Jawaban Penutupan Kas':
				lapParm['file'] = 'spjppkdPENERIMAAN/Lpj_penerimaan.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""	
				
				lapParm['idspj'] =""+radio_tanggung+""					
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""
		elif jenis_laporan == 'Rekapitulasi Pertanggung Jawaban':
				
				lapParm['file'] = 'spjppkdPENERIMAAN/SPJ_penerimaan.fr3'
				lapParm['tahun'] = ""+tahun_log(request)+""
				lapParm['bulan'] = ""+bulan+""	
				lapParm['idspj'] = ""+radio_tanggung+""			
				lapParm['id']= ""+id_bendahara+""
				lapParm['idpa']= ""+id_pengguna+""

		lapParm['KODEURUSAN'] = ""+kd_org_bendterima.split('.')[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org_bendterima.split('.')[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org_bendterima.split('.')[2]+"'"
		lapParm['TGLCETAK'] = ""+tgl_cetak+""	
		lapParm['isskpd'] = ""+1+""
		lapParm['report_type'] = 'pdf'
	return HttpResponse(laplink(request, lapParm))