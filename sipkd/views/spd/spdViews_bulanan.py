from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def spd_bul(request):
	return render(request,'spd/spd_bulanan.html')

# def ambil_bendahara(request):
# 	dataBendahara = ''
# 	kode_organisasi = request.POST.get('kode_organisasi','')
# 	if kode_organisasi!='':
# 		kd_urusan = kode_organisasi.split('.')[0] 
# 		kd_suburusan = kode_organisasi.split('.')[1]
# 		kd_organisasi = kode_organisasi.split('.')[2]
# 		with connections[tahun_log(request)].cursor() as cursor:
# 			cursor.execute('SELECT * FROM master.pejabat_skpd \
# 							WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and trim(kodeorganisasi) = %s and jenissistem = 2\
# 									and jabatan LIKE \'Bendahara Pengeluaran SKPD\'',[tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi])
# 			dataBendahara = dictfetchall(cursor)
# 	return HttpResponse(json.dumps(dataBendahara))

def rinci_spd_bul(request):
	hasil = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')
	
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and nospd != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
				and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s',
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])
			hasil = dictfetchall(cursor)

	data = { 'hasil':hasil, }
	return JsonResponse(data)

def link_tabel_rinci_spd_bul(request):
	data_rincian = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')
	bln_awal = request.POST.get('bln_awal','')
	bln_akhir = request.POST.get('bln_akhir','')
	triwulan = int(request.POST.get('triwulan',''))
	jenisdpa = request.POST.get('jenisdpa','')
	
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and triwulan != '' and jenisdpa != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT row_number() over() as nomor,\
				nodpa, uraian, anggaran, lalu, sekarang, jumlah, sisa \
				FROM penatausahaan.fc_view_spd_rincian_bulanan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,bln_awal,bln_akhir,jenisdpa,triwulan])
			data_rincian = dictfetchall(cursor)
		
	data = { 'data_rincian':ArrayFormater(data_rincian), }
	
	return render(request, 'spd/tabel/tabel_spd_edit_rinci.html',data)

def cek_data_bul(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa,jenis=False):
	jumlah = ''
	if jenisdpa=='DPA-SKPD' or jenisdpa=='DPPA-SKPD':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(*) as jumlah, nospd  FROM penatausahaan.spd \
				WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
				and jenisdpa in ('DPA-SKPD','DPPA-SKPD') and  BULAN_AWAL=%s \
				GROUP BY nospd",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
			jumlah = cursor.fetchone()
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(*) as jumlah,nospd  FROM penatausahaan.spd \
				WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
				and jenisdpa in ('DPA-PPKD','DPPA-PPKD') and  BULAN_AWAL=%s \
				GROUP BY nospd",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
			jumlah = cursor.fetchone()

	return '0' if jumlah==None else jumlah

def cek_data_spd_bul(request, nospd):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(*) as jumlah FROM penatausahaan.spd \
			WHERE tahun=%s and nospd=%s",[tahun_log(request),nospd])
		jumlah = cursor.fetchone()
	return '0' if jumlah==None else jumlah

def simpan_spd_bul(request):
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','').upper()
	no_spdold = request.POST.get('no_spdold','').upper()
	bulan = request.POST.get('bulan','')
	bln_awal = request.POST.get('bln_awal','')
	bln_akhir = request.POST.get('bln_akhir','')
	jenisdpa = request.POST.get('jenisdpa','')
	jumlah_total = request.POST.get('jumlah_total','')
	tanggal_draft =  request.POST.get('tanggal_draft','') 
	bendahara = request.POST.get('bendahara','')
	isSimpan = request.POST.get('isSimpan','')
	spd_rincian = json.loads(request.POST.get('spd_rincian'))

	jumlah = ''
	hasil = ''
	if_bener = False

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
		with connections[tahun_log(request)].cursor() as cursor:
			# Kalau buat SPD baru
			if isSimpan=='true':

				if int(cek_data_bul(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bln_awal,jenisdpa)[0])!=0:
					hasil = 'SPD pada bulan ini sudah pernah dibuat !'
					if_bener = False
				else:
					if nospd!='' or jenisdpa!='' or bendahara!='':
						if int(cek_data_spd_bul(request, nospd)[0])!=0:
							hasil = 'Nomor SPD sudah ada !'
							if_bener = False
						else:
							try:
								cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,\
									kodeorganisasi,kodeunit,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,\
									bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname) \
									values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
									[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,
									tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),
									bendahara,bln_awal,bln_akhir,jenisdpa,jumlah_total,username(request)])
								hasil = 'Simpan SPD berhasil !'
								if_bener = True

							except IntegrityError as e:
								hasil = 'Nomor SPD sudah ada, silahkan hubungi administrator!'
								if_bener = False
					else:
						hasil = 'Lengkapi data terlebih dahulu !'
						if_bener = False
			# Kalau update data SPD
			else:
				# print('awal akhir',bln_awal, bln_akhir, jumlah_total)
				if int(cek_data_bul(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bln_awal,jenisdpa,True)[0])!=0:
					try:
						cursor.execute('UPDATE penatausahaan.spd set nospd=%s, tanggal_draft=%s, tanggal=%s, \
							tgldpa=%s, bendaharapengeluaran=%s, jenisdpa=%s, jumlahspd=%s, uname = %s, \
							bulan_awal = %s, bulan_akhir = %s WHERE tahun = %s and kodeurusan = %s \
							and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s',
							[nospd, tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft), 
							bendahara, jenisdpa, jumlah_total,username(request),bln_awal,bln_akhir,tahun_log(request), 
							kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spdold])

						hasil = 'Simpan SPD berhasil !'
						if_bener = True
						# print(cursor.query)
					except IntegrityError as e:
						hasil = 'Nomor SPD sudah ada !'
						if_bener = False
				else:
					pass
					# if nospd!='' or jenisdpa!='' or bendahara!='':
					# 	if int(cek_data_spd_bul(request, nospd)[0])!=0:
					# 		hasil = 'Nomor SPD sudah ada !'
					# 	else:
					# 		try:
					# 			cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft), bendahara, bln_awal,bln_akhir,jenisdpa, jumlah_total,username(request)])
					# 			hasil = 'Simpan SPD berhasil !'
					# 		except IntegrityError as e:
					# 			hasil = 'Nomor SPD sudah ada !'

			
			if if_bener == True:
				# HAPUS RINCIAN DULU
				cursor.execute("DELETE FROM penatausahaan.spdrincian WHERE tahun=%s and kodeurursan=%s "
	                "and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nospd=%s",
	                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])

				# SIMPAN RINCIAN
				try:
					for i in range(0,len(spd_rincian)):
						kode = spd_rincian[i]['kode'].split(".") # ['1', '1', '01', '0003', '1', '01', '2', '2', '01', '11']
						uang = toAngkaDec(spd_rincian[i]['uang'])

						kdurusan = kode[0]
						kdsuburusan = kode[1]
						kdorganisasi = kode[2]
						kdunit = kode[3]
						kdbidang = kode[4]+"."+kode[5]
						kdprogram = kode[6]
						kdkegiatan = kode[7]+"."+kode[8]
						kdsubkegiatan = kode[9]

						cursor.execute("INSERT INTO penatausahaan.spdrincian (tahun,kodeurursan,kodesuburusan,kodeorganisasi,kodeunit,\
							nospd,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodesubkeluaran,jumlah) \
		                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
		                    [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,uang])                                     
		                	
						hasil = "Data berhasil disimpan!"
				except Exception as e:
					hasil = "Input Rincian Gagal"

	return HttpResponse(hasil)

def hapus_spd_bul(request):
	hasil = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')
	
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT LOCKED FROM penatausahaan.spd WHERE tahun = %s \
				and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
			jumlah = cursor.fetchone()

			if jumlah[0]=='Y':
				hasil = 'SPD sudah di lock !'
			else:
				cursor.execute("DELETE FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
					and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
					[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
				hasil = 'Data SPD berhasil dihapus !'

	return HttpResponse(hasil)

def render_cetak_spd_bul(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1  \
			FROM master.pejabat_skpkd where jenissistem=2 and tahun=%s and upper(jabatan) LIKE '%%BENDAHARA UMUM%%'",
			[tahun_log(request)])
		pejabat = dictfetchall(cursor)
	
	data = {
		'pejabat':pejabat,
	}
	return render(request, 'spd/modal/modal_cetak_spd.html',data)

def cetak_spd_bul(request):

	post 	= request.POST
	lapParm = {}
	skpd 	= post.get('skpd').split('.')
	no_spd = post.get('no_spd')
	id_jabatan = post.get('id_jabatan')

	lapParm['file'] 		= 'penatausahaan/spd/SPD.fr3'
	lapParm['NOMER'] = "'"+no_spd+"'"
	lapParm['tahun'] = "'"+tahun_log(request)+"'"
	lapParm['ID'] = "'"+id_jabatan+"'"				
	lapParm['KodeUrusan'] = "'"+skpd[0]+"'"
	lapParm['KodeSubUrusan'] = "'"+skpd[1]+"'"
	lapParm['KodeOrganisasi'] = "'"+skpd[2]+"'"
	lapParm['report_type'] = 'pdf'

	# http://localhost/sipkd_deiyai/report/?tahun=2016&file=spd/SPD.fr3&report_type=pdf&KodeUrusan='1'&KodeSubUrusan='1'&KodeOrganisasi='01'&NOMER='0001/SPD/1/2016'&ID=3

	return HttpResponse(laplink(request, lapParm))