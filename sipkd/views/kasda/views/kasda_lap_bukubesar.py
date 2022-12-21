from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from support.support_sipkd import *

def index(request):

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		tahun 	= tahun_log(request)
		jns_lap = int(data.get('jns_laporan'))
		pilih_skpd 	= data.get('is_skpd')
		pilih_tgl  	= data.get('pil_tanggal')
		jb = bb = jSP2D = ''

		if jns_lap == 0:
			jb = 'SP2D'
			bb = 'Perhitungan Fihak Ketiga'
			jSP2D = ''
		elif jns_lap == 1:
			jb = 'NOTA'
			bb = 'NOTA'
			jSP2D = ''
		elif jns_lap == 2:
			jb = 'STS'
			bb = 'Surat Tanda Setoran'
			jSP2D = ''
		elif jns_lap == 3:
			jb = 'CONTRAKEMARIN'
			bb = 'Setoran Sisa Kas Bendahara Tahun Kemarin'
			jSP2D = ''
		elif jns_lap == 4:
			jb = 'CONTRA'
			bb = 'Pengembalian UP/GU/TU Tahun Berjalan'
			jSP2D = 'UP'
		elif jns_lap == 5:
			jb = 'CONTRA'
			bb = 'Pengembalian LS Tahun Berjalan'
			jSP2D = 'LS'

		if jns_lap == 0 or jns_lap == 1 or jns_lap == 2 or jns_lap == 3 or jns_lap == 4 or jns_lap == 5:

			lapParm['bb'] 	 = bb
			lapParm['jb'] 	 = "'"+jb+"'" 
			lapParm['jsp2d'] = "'"+jSP2D+"'" 

			if pilih_skpd == "oneskpd" and data.get('organisasi') != "":
				skpd = data.get('organisasi').split('.')

				lapParm['file'] 		= 'kasda/ben55/laporanNonBelanja2.fr3'
				lapParm['kodeurusan'] 		= "'"+skpd[0]+"'"
				lapParm['kodesuburusan'] 	= "'"+skpd[1]+"'"
				lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
				lapParm['kodeunit'] 		= "'"+skpd[3]+"'"
				lapParm['kodesatker'] 	= "'"+data.get('organisasi')+"'"
				lapParm['skpd'] 		= "'"+data.get('organisasi')+"'"
				lapParm['qry'] 			= " WHERE KODESATKER='"+data.get('organisasi')+"'"
			else: ### allskpd ===================================================================
				lapParm['file'] 		= 'kasda/ben55/laporanNonBelanja1.fr3'
				lapParm['kodesatker'] 	= ""
				lapParm['skpd'] 		= ""
				lapParm['qry'] 			= ""

		elif jns_lap == 6:
			lapParm['file'] = 'kasda/ben55/RekapSTS.fr3'

			if data.get('organisasi') != "":
				skpd = data.get('organisasi').split('.')
				
				lapParm['skpd'] 			= "0"
				lapParm['kodeurusan'] 		= "'"+skpd[0]+"'"
				lapParm['kodesuburusan'] 	= "'"+skpd[1]+"'"
				lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
				lapParm['kodeunit'] 		= "'"+skpd[3]+"'"
			else:
				lapParm['skpd'] 			= "1"


		if pilih_tgl == "daritgl":
			lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_tglawal'))+"'"
			lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_tglakhir'))+"'"
			lapParm['periodeawal'] 	= data.get('periode_tglawal')
			lapParm['periodeakhir'] = data.get('periode_tglakhir')
		else: ### pertgl ====================================================================
			lapParm['tglawal'] 		= "'"+tgl_short(data.get('periode_pertgl'))+"'"
			lapParm['tglakhir'] 	= "'"+tgl_short(data.get('periode_pertgl'))+"'"
			lapParm['periodeawal'] 	= data.get('periode_pertgl')
			lapParm['periodeakhir'] = data.get('periode_pertgl')


		lapParm['report_type'] 		= 'pdf'
		lapParm['id']				= "'"+data.get('id_pejabat')+"'"
		lapParm['nip'] 				= data.get('nip_pejabat')
		lapParm['nama'] 			= data.get('nama_pejabat')
		lapParm['jabatan'] 			= data.get('pangkat_pejabat')
		lapParm['tahun'] 			= "'"+tahun+"'"

		return HttpResponse(laplink(request, lapParm))

	else:
		arrJnsLap = [ {'ID':0,'label':'SP2D ( PFK / Perhitungan Fihak Ketiga )'},
			{'ID':1,'label':'NOTA'}, {'ID':2,'label':'STS ( Pendapatan )'},
			{'ID':3,'label':'Pengembalian Tahun Lalu'}, {'ID':4,'label':'Pengembalian UP/GU/TU Tahun Berjalan'},
			{'ID':5,'label':'Pengembalian LS Tahun Berjalan'}, {'ID':6,'label':'Rekap STS ( Pendapatan )'} ]

		list_pejabat = get_pejabat_pengesah(request)
		data = {'arrJnsLap':arrJnsLap, 'ls_data':list_pejabat, }

		return render(request, 'kasda/kasda_lap_bukubesar.html', data)