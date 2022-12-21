from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from support.support_sipkd import *

def index(request):

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		tahun 	= tahun_log(request)
		pilih_skpd 	= data.get('is_skpd')
		pilih_tgl  	= data.get('pil_tanggal')

		if pilih_skpd == "oneskpd" and data.get('organisasi') != "":
			skpd = data.get('organisasi').split('.')

			lapParm['file'] 		= 'kasda/ben55/laporanBelanja2.fr3'
			lapParm['kodeurusan'] 		= "'"+skpd[0]+"'"
			lapParm['kodesuburusan'] 	= "'"+skpd[1]+"'"
			lapParm['kodeorganisasi'] 	= "'"+skpd[2]+"'"
			lapParm['kodeunit'] 		= "'"+skpd[3]+"'"
			lapParm['kodesatker'] 	= "'"+data.get('organisasi')+"'"
			lapParm['skpd'] 		= "'"+data.get('organisasi')+"'"
			lapParm['qry'] 			= " WHERE KODESATKER='"+data.get('organisasi')+"'"
		else: ### allskpd ===================================================================
			lapParm['file'] 		= 'kasda/ben55/laporanBelanja1.fr3'
			lapParm['kodesatker'] 	= ""
			lapParm['skpd'] 		= ""
			lapParm['qry'] 			= ""

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
		lapParm['bb'] 				= 'BUKU BESAR SP2D'
		lapParm['jb'] 				= "'SP2D'" 
		lapParm['id']				= "'"+data.get('id_pejabat')+"'"
		lapParm['nip'] 				= data.get('nip_pejabat')
		lapParm['nama'] 			= data.get('nama_pejabat')
		lapParm['jabatan'] 			= data.get('pangkat_pejabat')
		lapParm['tahun'] 			= "'"+tahun+"'"

		return HttpResponse(laplink(request, lapParm))

	else:
		list_pejabat = get_pejabat_pengesah(request)
		data = {'ls_data':list_pejabat}

		return render(request, 'kasda/kasda_lap_bukubesarsp2d.html', data)