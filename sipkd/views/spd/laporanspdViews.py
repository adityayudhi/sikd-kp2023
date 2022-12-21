from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def laporanspd(request):
	jns_lap = []
	if hakakses(request) == 'ANGGARAN':
		jns_lap = 	[{'label' : "Kartu Pengawas - Realisasi Anggaran"},
		  			{'label' : "Register SPD"},
		  			{'label' : "Kartu Kendali Anggaran"},
		  			{'label' : "Realisasi SP2D"},
		  			{'label' : "Kartu Kontrol SPD"},
		  			{'label' : "Realisasi Per SKPD Per Rekening"},
		  			{'label' : "Rekapitulasi Anggaran SKPD"},
		  			{'label' : "Rekapitulasi Realisasi Anggaran Per Rekening"}]
	else:
		jns_lap =  [{'label' : "Kartu Pengawas - Realisasi Anggaran"},
		  			{'label' : "Register SPD"},
		  			{'label' : "Kartu Kendali Anggaran"},
		  			{'label' : "Realisasi SP2D"},
		  			{'label' : "Kartu Kontrol SPD"},
		  			{'label' : "Realisasi Per SKPD Per Rekening"},
		  			{'label' : "Rekapitulasi Anggaran SKPD"},
		  			{'label' : "Rekapitulasi Realisasi Anggaran Per Rekening"},
		  			# {'label' : "Rekap Belanja PPKD"}
		  			]
	
	data = {
		'jns_lap':jns_lap,
	}
	return render(request, 'spd/laporanspd.html', data)

def laporan_kpra(request):
	post 	= request.POST
	lapParm = {}
	skpd 	= post.get('kd_org').split(' - ')
	kd_org  = skpd[0].split('.')
	jenis_laporan = post.get('jenis_laporan')
	id_pejabat = post.get('id_pejabat')
	nm_pejabat = post.get('nm_pejabat')
	nip_pejabat = post.get('nip_pejabat')
	pangkat_pejabat = post.get('pangkat_pejabat')
	tgl_laporan = post.get('tgl_laporan')
	isppkd = post.get('isppkd')
	
	triwulan = post.get('triwulan')
	periode1  = post.get('periode1')
	periode2 = post.get('periode2')
	jenis = post.get('jenis')

	if post.get('kegiatan') :
		keg = post.get('kegiatan').split(' - ')
		kegiatan = keg[0]
		urai_keg = keg[1]
		kode_keg = kegiatan.split('.')

		kd_bidang = kode_keg[0]+"."+kode_keg[1]
		kd_program = kode_keg[2]
		kd_kegiatan = kode_keg[3]+"."+kode_keg[4]
		kd_subkegiatan = kode_keg[5]
		
	if post.get('rekening') :
		rek = post.get('rekening').split(' - ')
		rekening = rek[0]
		urai_rek = rek[1]
		kode_rek = rekening.split('.')

		kd_akun = kode_rek[0]
		kd_kelompok = kode_rek[1]
		kd_jenis = kode_rek[2]
		kd_objek = kode_rek[3]
		kd_rincianobjek = kode_rek[4]
		kd_subrincianobjek = kode_rek[5]

	if jenis_laporan == 'Kartu Pengawas - Realisasi Anggaran':
		lapParm['file'] = 'penatausahaan/AKUNTANSI/KartuPengawasanRealisasiAnggaran.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""
		
		lapParm['id']= "'"+id_pejabat+"'"

	elif jenis_laporan == 'Register SPD':
		lapParm['file'] = 'penatausahaan/SPD/Register_SPD.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""

		lapParm['isppkd'] = ""+isppkd+""
		lapParm['id']= "'"+id_pejabat+"'"

	elif jenis_laporan == 'Kartu Kendali Anggaran':
		lapParm['file'] = 'penatausahaan/SPD/KartuKendaliAnggaran.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""

		lapParm['KODEBIDANG'] = "'"+kd_bidang+"'"
		lapParm['KODEPROGRAM'] = ""+kd_program+""
		lapParm['KODEKEGIATAN'] = "'"+kd_kegiatan+"'"
		lapParm['KODESUBKEGIATAN'] = ""+kd_subkegiatan+""
		lapParm['KODEBIDANG2'] = ""+kd_bidang+""
		lapParm['KEGIATAN'] = ""+urai_keg+""

		lapParm['tglawal'] = "'"+tgl_to_laporan(periode1)+"'"
		lapParm['tglakhir'] = "'"+tgl_to_laporan(periode2)+"'"
		lapParm['periode'] = periode1+" s/d "+periode2

		lapParm['isppkd'] = ""+isppkd+""
		lapParm['id']= "'"+id_pejabat+"'"

	elif jenis_laporan == 'Realisasi SP2D':
		lapParm['file'] = 'penatausahaan/SPD/KartuRealisasiSP2D.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""

		lapParm['KODEBIDANG'] = "'"+kd_bidang+"'"
		lapParm['KODEPROGRAM'] = ""+kd_program+""
		lapParm['KODEKEGIATAN'] = "'"+kd_kegiatan+"'"
		lapParm['KODESUBKEGIATAN'] = ""+kd_subkegiatan+""
		lapParm['KODEBIDANG2'] = ""+kd_bidang+""
		lapParm['KEGIATAN'] = ""+urai_keg+""
		
		lapParm['KODE'] = "'"+rekening+"'"
		lapParm['KODEAKUN'] = "'"+kd_akun+"'"		
		lapParm['KODEKELOMPOK'] = "'"+kd_kelompok+"'"
		lapParm['KODEJENIS'] = "'"+kd_jenis+"'"
		lapParm['KODEOBJEK'] = "'"+kd_objek+"'"
		lapParm['KODERINCIANOBJEK'] = "'"+kd_rincianobjek+"'"
		lapParm['KODESUBRINCIANOBJEK'] = "'"+kd_subrincianobjek+"'"
		lapParm['URAIREKENING'] = "'"+urai_rek+"'"
		lapParm['id']= "'"+id_pejabat+"'"

	elif jenis_laporan == 'Kartu Kontrol SPD':
		lapParm['file'] = 'penatausahaan/SPD/KontrolSPD.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""
		lapParm['xtriwulan'] = ""+triwulan.split('-')[0]+""
		lapParm['triwulan'] = "'"+triwulan.split('-')[1]+"'"
		lapParm['id']= "'"+id_pejabat+"'"

	elif jenis_laporan == 'Realisasi Per SKPD Per Rekening':
		lapParm['file'] = 'penatausahaan/SPD/RekapRealisasiRekening.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['KODEURUSAN'] = ""+kd_org[0]+""
		lapParm['KODESUBURUSAN'] = ""+kd_org[1]+""
		lapParm['KODEORGANISASI'] = "'"+kd_org[2]+"'"
		lapParm['KODEORGANISASI2'] = ""+kd_org[2]+""
		lapParm['KODEUNIT'] = "'"+kd_org[3]+"'"
		lapParm['ORGANISASI'] = ""+skpd[1]+""
		lapParm['idjenis'] = ""+jenis+""
		lapParm['id']= "'"+id_pejabat+"'"
		lapParm['tglawal'] = "'"+tgl_to_laporan(periode1)+"'"
		lapParm['tglakhir'] = "'"+tgl_to_laporan(periode2)+"'"
		lapParm['periodeawal'] = ""+periode1+""
		lapParm['periodeakhir'] = ""+periode2+""
		lapParm['periode'] = periode1+" s/d "+periode2
		lapParm['isppkd'] = ""+isppkd+""
		
	elif jenis_laporan == 'Rekapitulasi Anggaran SKPD':
		lapParm['file'] = 'penatausahaan/SPD/RekapPaguSKPD.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['id']= "'"+id_pejabat+"'"
		lapParm['tglawal'] = "'"+tgl_to_laporan(periode1)+"'"
		lapParm['tglakhir'] = "'"+tgl_to_laporan(periode2)+"'"
		lapParm['periode'] = periode1+" s/d "+periode2

	elif jenis_laporan == 'Rekapitulasi Realisasi Anggaran Per Rekening':
		if jenis == '0':
			lapParm['file'] = 'penatausahaan/SPD/RekapRealisasiRekeningBtl.fr3'
		else:
			lapParm['file'] = 'penatausahaan/SPD/RekapRealisasiRekeningBl.fr3'
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['id']= "'"+id_pejabat+"'"
		lapParm['tglawal'] = "'"+tgl_to_laporan(periode1)+"'"
		lapParm['tglakhir'] = "'"+tgl_to_laporan(periode2)+"'"
		lapParm['periodeawal'] = ""+periode1+""
		lapParm['periodeakhir'] = ""+periode2+""

	elif jenis_laporan == 'Rekap Belanja PPKD':
		lapParm['file'] = 'penatausahaan/SPD/RekapBelanjaPPKDBupatiVersion.fr3';
		lapParm['tahun'] = "'"+tahun_log(request)+"'"
		lapParm['id']= "'"+id_pejabat+"'"
		lapParm['tglawal'] = "'"+tgl_to_laporan(periode1)+"'"
		lapParm['tglakhir'] = "'"+tgl_to_laporan(periode2)+"'"
		lapParm['periodeawal'] = ""+periode1+""
		lapParm['periodeakhir'] = ""+periode2+""

		lapParm['KODEURUSAN'] = ""+get_PPKD(request)[0]['kode'].split('.')[0]+""
		lapParm['KODESUBURUSAN'] = ""+get_PPKD(request)[0]['kode'].split('.')[1]+""
		lapParm['KODEORGANISASI'] = "'"+get_PPKD(request)[0]['kode'].split('.')[2]+"'"
		lapParm['ORGANISASI'] = ""+get_PPKD(request)[0]['urai']+""
	
	lapParm['tglto'] = "'"+tgl_to_laporan(periode2)+"'"
	lapParm['tglfrom'] = "'"+tgl_to_laporan(periode1)+"'"
	lapParm['TGLCETAK'] = ""+tgl_laporan+""	
	lapParm['report_type'] = 'pdf'
	return HttpResponse(laplink(request, lapParm))