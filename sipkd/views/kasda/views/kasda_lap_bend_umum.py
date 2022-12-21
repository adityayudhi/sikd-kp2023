from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from support.support_sipkd import *
from datetime import datetime, timedelta

def index(request):

	if request.method == 'POST':
		data 		= request.POST
		lapParm 	= {}
		tahun 		= tahun_log(request)
		jns_lap 	= int(data.get('jns_laporan'))
		pilih_tgl  	= data.get('pil_tanggal')
		sumdana 	= data.get('sumdana')
		bulanxx 	= data.get('periode')

		if pilih_tgl == "pertgl": ### cari tanggal kemarin =================================
			ubahtglx  = tgl_to_db_original(data.get('periode_pertgl')).replace('/','')
			datenowx  = datetime.strptime(ubahtglx, '%d%m%Y').date()
			yesterday = datenowx - timedelta(days=1)

		if jns_lap == 0:
			lapParm['kodesumberdana'] 	= '-1'
			if pilih_tgl == "daritgl":
				lapParm['file'] 	= 'kasda/ben55/RekapPosisiKas.fr3'
				lapParm['periode'] 	= data.get('periode_tglakhir')
				lapParm['tglawal'] 			= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 		= "'"+tgl_short(data.get('periode_tglakhir'))+"'"

			else: ### pertgl ====================================================================
				lapParm['file'] 	= 'kasda/ben55/RekapPosisiKas2.fr3'
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['tanggal'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['kemarin'] 	= "'"+tgl_to_db(tgl_indo(yesterday))+"'"

		elif jns_lap == 1:
			lapParm['kodesumberdana'] 	= '-1'
			if pilih_tgl == "daritgl":
				lapParm['file'] 	= 'kasda/ben55/BukuKasTerimaKeluar.fr3'
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['tglawal'] 			= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 		= "'"+tgl_short(data.get('periode_tglakhir'))+"'"

			else: ### pertgl ====================================================================
				lapParm['file'] 	= 'kasda/ben55/BukuKasTerimaKeluar2.fr3'
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['tanggal'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"

		elif jns_lap == 2:
			lapParm['kodesumberdana'] 	= '-1'
			if pilih_tgl == "daritgl":
				lapParm['file'] 	= 'kasda/ben55/LPKH.fr3'
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['tglawal'] 			= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 		= "'"+tgl_short(data.get('periode_tglakhir'))+"'"

			else: ### pertgl ====================================================================
				lapParm['file'] 	= 'kasda/ben55/LPKH2.fr3'
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['tanggal'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"

		elif jns_lap == 3:
			sumdan_pch = sumdana.split("|")
			lapParm['kodesumberdana'] 	= "'"+sumdan_pch[0]+"'"
			lapParm['sumberdana'] 		= sumdan_pch[1]

			if pilih_tgl == "daritgl":
				lapParm['file'] 	= 'kasda/ben55/BKUPerSumberDana.fr3'
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['tglawal'] 	= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] = "'"+tgl_short(data.get('periode_tglakhir'))+"'"

			else: ### pertgl ====================================================================
				lapParm['file'] 	= 'kasda/ben55/BKUPerSumberDana2.fr3'
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['tanggal'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['kemarin'] 	= "'"+tgl_to_db(tgl_indo(yesterday))+"'"
				

		elif jns_lap == 4:
			lapParm['file'] = 'kasda/ben55/SP2DNotCair.fr3'

			if pilih_tgl == "daritgl":
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['periodeakhir'] = data.get('periode_tglakhir')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_tglakhir'))+"'"
				lapParm['tglcetak'] 	= data.get('periode_tglakhir')

			else: ### pertgl ====================================================================
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['periodeakhir'] = data.get('periode_pertgl')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['tglcetak'] 	= data.get('periode_pertgl')

		elif jns_lap == 5:
			sumdan_pch = sumdana.split("|")
			lapParm['kodesumberdana'] 	= "'"+sumdan_pch[0]+"'"
			lapParm['sumberdana'] 		= sumdan_pch[1]

			if pilih_tgl == "daritgl":
				lapParm['file'] 	= 'kasda/ben55/modelRC.fr3'
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['periodeakhir'] = data.get('periode_tglakhir')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_tglakhir'))+"'"

			else: ### pertgl ====================================================================
				lapParm['file'] 	= 'kasda/ben55/modelRC.fr3'
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['periodeakhir'] = data.get('periode_pertgl')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				

		elif jns_lap == 6:
			cbBulan = bulanxx.split("|")
			lapParm['file'] = 'kasda/ben55/rekappenerbitansp2d.fr3'
			lapParm['bulan'] = cbBulan[0]
			lapParm['periodebulan'] = cbBulan[1] 

		elif jns_lap == 7:
			lapParm['file'] = 'kasda/ben55/SP2DNotCairv2.fr3'

			if pilih_tgl == "daritgl":
				lapParm['periode'] 	= data.get('periode_tglawal')
				lapParm['periodeakhir'] = data.get('periode_tglakhir')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_tglawal'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_tglakhir'))+"'"
				lapParm['tglcetak'] 	= data.get('periode_tglakhir')

			else: ### pertgl ====================================================================
				lapParm['periode'] 	= data.get('periode_pertgl')
				lapParm['periodeakhir'] = data.get('periode_pertgl')
				lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
				lapParm['tglcetak'] 	= data.get('periode_pertgl')


		lapParm['report_type'] 		= 'pdf'
		lapParm['id']				= "'"+data.get('id_pejabat')+"'"
		lapParm['nip'] 				= data.get('nip_pejabat')
		lapParm['nama'] 			= data.get('nama_pejabat')
		lapParm['jabatan'] 			= data.get('pangkat_pejabat')
		lapParm['tahun'] 			= "'"+tahun+"'"

		return HttpResponse(laplink(request, lapParm))

	else:

		arrJnsLap = [
			{'ID':0,'label':'Rekapitulasi Posisi Kas BUD'},
			{'ID':1,'label':'Buku Kas Penerimaan dan Pengeluaran'},
			{'ID':2,'label':'Laporan Posisi Kas Harian (LPKH)'},
			{'ID':3,'label':'BKU Penerimaan Pengeluaran Per Sumber Dana'},
			{'ID':4,'label':'SP2D yang belum cair'},
			# {'ID':5,'label':'Model RC Bank'},
			{'ID':6,'label':'Rekapitulasi Penerbitan SP2D dan Pencairan'},
			# {'ID':7,'label':'SP2D yang belum cair Per Sumber Dana'} 
		]

		arrBulanx = [
			{'ID':'1','label':'Januari'},{'ID':'2','label':'Februari'},
			{'ID':'3','label':'Maret'},{'ID':'4','label':'April'},
			{'ID':'5','label':'Mei'},{'ID':'6','label':'Juni'},
			{'ID':'7','label':'Juli'},{'ID':'8','label':'Agustus'},
			{'ID':'9','label':'September'},{'ID':'10','label':'Oktober'},
			{'ID':'11','label':'November'},{'ID':'12','label':'Desember'} ]

		list_pejabat = get_pejabat_pengesah(request)
		dt_sumberdana = put_kasda_sumberdana(request)

		data = {'arrJnsLap':arrJnsLap, 'arrBulanx':arrBulanx, 'ls_data':list_pejabat, 'dt_sumdan':dt_sumberdana}

		return render(request, 'kasda/kasda_lap_bend_umum.html', data)