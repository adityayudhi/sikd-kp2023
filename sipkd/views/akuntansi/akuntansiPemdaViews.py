from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *

#laporan lra bulanan
def laporan_realisasi_pemda(request):
	tahun 	= tahun_log(request)
	arrBln  = []

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}		
		bulan_lap = int(data.get("bulan_lap"))
		realisasi = int(data.get("realisasi"))
		versi_lap = int(data.get("versi_laporan"))
		nip_pejabat	  = data.get('nip_pejabat')
		perubahan = int(data.get("status"))

		if realisasi== 0:
			jenisreal = 'SP2D'
		else:
			jenisreal = 'SPJ'

		if versi_lap== 0:
			versi_laporan = 'penatausahaan/AKUNTANSIPEMDA/Lra_bulanan_sap.fr3'
		else:
			versi_laporan = 'penatausahaan/AKUNTANSIPEMDA/Lra_bulanan.fr3'

		if nip_pejabat == '':
			nip = nip_pejabat
		else:
			nip = 'NIP : '+nip_pejabat	

		if perubahan == 1:
			status = '0'
		else:
			status = '1'


		lapParm['report_type'] 	= 'pdf'
		lapParm['tahun'] 		= "'"+tahun+"'"
		lapParm['id'] 			= data.get("id_pejabat")
		lapParm['nip'] 			= "'"+nip+"'"
		lapParm['nama'] 		= data.get("nama_pejabat")
		lapParm['pangkat'] 		= data.get("pangkat_pejabat")
		lapParm['jabatan'] 		= data.get("jabatan")
		lapParm['bulan']		= data.get("bulan_lap")
		lapParm['status'] 		= "'"+status+"'"
		lapParm['jenisReal'] 	= "'"+jenisreal+"'"
		lapParm['file'] 		= versi_laporan
		lapParm['TGLCETAK'] 	= data.get("tgl_cetak_lap")

		if (bulan_lap == 1): lapParm['xbulan'] = 'JANUARI'
		elif (bulan_lap == 2): lapParm['xbulan'] = 'FEBRUARI'
		elif (bulan_lap == 3): lapParm['xbulan'] = 'MARET'
		elif (bulan_lap == 4): lapParm['xbulan'] = 'APRIL'
		elif (bulan_lap == 5): lapParm['xbulan'] = 'MEI'
		elif (bulan_lap == 6): lapParm['xbulan'] = 'JUNI'
		elif (bulan_lap == 7): lapParm['xbulan'] = 'JULI'
		elif (bulan_lap == 8): lapParm['xbulan'] = 'AGUSTUS'
		elif (bulan_lap == 9): lapParm['xbulan'] = 'SEPTEMBER'
		elif (bulan_lap == 10): lapParm['xbulan'] = 'OKTOBER'
		elif (bulan_lap == 11): lapParm['xbulan'] = 'NOVEMBER'
		elif (bulan_lap == 12): lapParm['xbulan'] = 'DESEMBER'

		return HttpResponse(laplink(request, lapParm))
	else:
		pjbt  = get_pejabat_pengesah(request)

		aidi_bln = 1
		for i in monthList: # monthList -> array from config.py
			arrBln.append({'id':aidi_bln, 'kode':i, 'nama':monthList[i], 'tahun':tahun})
			aidi_bln += 1		

		arrData = {'bulan_lap':arrBln, 'ls_data':pjbt
		}

		return render(request,'akuntansi/laporan/lap_lra_bulanan.html', arrData)

# laporan verifikasi
def laporan_verifikasi(request):
	tahun 	= tahun_log(request)
	arrBln  = []

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		kd_uru  = kd_subur = kd_org = jspj_ky = jspj_kd = ''

		if data.get('organisasi') != "":
			skpd 	 = data.get('organisasi').split('.')
			kd_uru   = skpd[0]
			kd_subur = skpd[1]
			kd_org 	 = skpd[2]

		if data.get('jenis_spj') != "":
			jns_spj  = data.get('jenis_spj').split("|")
			jspj_ky  = jns_spj[1]
			jspj_kd  = jns_spj[0]

		jenisLap = int(data.get('jsn_lap'))

		lapParm['report_type'] 		= 'pdf'
		lapParm['tahun'] 			= "'"+tahun+"'"
		lapParm['id'] 				= data.get("id_pejabat")		
		lapParm['TGLCETAK'] 		= data.get("tgl_cetak_lap")

		if jenisLap == 0:
			lapParm['file'] 		= 'penatausahaan/AKUNTANSI/KartuPengawasanUP.fr3'

		elif jenisLap == 1:
			lapParm['file']			= 'penatausahaan/AKUNTANSI/KartuPengawasanTU.fr3'

		elif jenisLap == 2:
			lapParm['file']				= 'penatausahaan/AKUNTANSI/KartuPengawasanRealisasiAnggaran.fr3'
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['KODEORGANISASI2'] 	= kd_org
			lapParm['ORGANISASI'] 		= data.get("org_urai")

		elif jenisLap == 3:
			lapParm['file']				= 'penatausahaan/AKUNTANSI/RegisterSP2D.fr3'
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['KODEORGANISASI2'] 	= kd_org
			lapParm['ORGANISASI'] 		= data.get("org_urai")
			lapParm['PERIODE'] 			= data.get("bulan_dari")+" - "+data.get("bulan_sampai")
			lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 4:
			lapParm['file']				= 'penatausahaan/AKUNTANSI/RegisterSP2DRincian.fr3'
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['KODEORGANISASI2'] 	= kd_org
			lapParm['ORGANISASI'] 		= data.get("org_urai")
			lapParm['PERIODE'] 			= data.get("bulan_dari")+" - "+data.get("bulan_sampai")
			lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 5:
			lapParm['file']				= 'penatausahaan/AKUNTANSI/RegisterSPJ.fr3'
			lapParm['jenis'] 			= jspj_ky
			lapParm['jenis1'] 			= jspj_kd
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['KODEORGANISASI2'] 	= kd_org
			lapParm['ORGANISASI'] 		= data.get("org_urai")
			lapParm['PERIODE'] 			= data.get("bulan_dari")+" - "+data.get("bulan_sampai")
			lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 6:
			lapParm['qry'] 				= "where kodeurusan='"+kd_uru+"' and kodesuburusan='"+kd_subur+"' \
				and kodeorganisasi='"+kd_org+"' and jumlahspj=0 and tglkasda is not null"
			lapParm['file']				= 'penatausahaan/AKUNTANSI/RekapSP2dTUNonSPJ.fr3'
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 7:
			lapParm['qry'] 				= "where kodeurusan='"+kd_uru+"' and kodesuburusan='"+kd_subur+"' \
				and kodeorganisasi='"+kd_org+"' and jumlahspj=0 and tglkasda is not null"
			lapParm['file']				= 'penatausahaan/AKUNTANSI/RekapSP2dTUNonSPJ.fr3'
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 8:
			if int(data.get("is_skpkd")) == 0 and int(data.get("radiobaten")) == 0:
				lapParm['file'] 		= 'penatausahaan/AKUNTANSI/SuratPengesahanSPJ.fr3'
			elif int(data.get("radiobaten")) == 1:
				lapParm['file'] 		= 'penatausahaan/AKUNTANSI/SuratPengesahanSPJPenerimaanSKPD.fr3'
			elif int(data.get("is_skpkd")) == 1 and int(data.get("radiobaten")) == 1:
				lapParm['file'] 		= 'penatausahaan/AKUNTANSI/SuratPengesahanSPJPPKD.fr3'
			lapParm['bulan']			= data.get("bulan_lap")	
			lapParm['KODEURUSAN'] 		= kd_uru
			lapParm['KODESUBURUSAN'] 	= kd_subur
			lapParm['KODEORGANISASI'] 	= "'"+kd_org+"'"
			lapParm['KODEORGANISASI2'] 	= kd_org
			lapParm['ORGANISASI'] 		= data.get("org_urai")
			lapParm['PERIODE'] 			= data.get("bulan_dari")+" - "+data.get("bulan_sampai")
			lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['isppkd'] 			= data.get("is_skpkd")

		elif jenisLap == 9:
			lapParm['file']				= 'penatausahaan/AKUNTANSI/lap_spj_sp2d.fr3'
			lapParm['tglfrom'] 			= "'"+tgl_short(data.get("bulan_dari"))+"'"
			lapParm['tglto'] 			= "'"+tgl_short(data.get("bulan_sampai"))+"'"
			lapParm['jenis'] 			= jspj_ky

		elif jenisLap == 10:
			lapParm['file']				= 'penatausahaan/AAKUNTANSI/KertasKerjaVerifikasi.fr3'
			

		return HttpResponse(laplink(request, lapParm))
	else:
		arrjns_spj = [{'key':'0','kode':'UP-GU / TU','nama':'Semua ( UP-GU / TU )'},
			{'key':'1','kode':'GU ( Ganti Uang Persediaan )','nama':'UP-GU'},
			{'key':'2','kode':'TU ( Tambahan Uang Persediaan )','nama':'TU'},
		]
		arrjns_lap = [{'kode':'0','nama':'Kartu Pengawas - Uang Persediaan'}, #0 
			{'kode':'1','nama':'Kartu Pengawas - Tambahan Uang Persediaan'}, #1
			{'kode':'2','nama':'Kartu Pengawas - Realisasi Anggaran'}, #2
			{'kode':'3','nama':'Register SP2D'}, #3
			{'kode':'4','nama':'Register SP2D Per Rincian'}, #4
			{'kode':'5','nama':'Register SPJ'}, #5
			{'kode':'6','nama':'Rekap SP2D TU Yang Belum di LPJ-kan'}, #6
			{'kode':'7','nama':'Rekap Sisa SP2D TU Yang di LPJ-kan'}, #7
			{'kode':'8','nama':'LPJ Fungsional Versi Akuntansi'}, #8
			{'kode':'9','nama':'Laporan SPJ SP2D'}, #9
			{'kode':'10','nama':'Kertas Kerja'}, #10			
		]

		pjbt  = get_pejabat_pengesah(request)

		aidi_bln = 1
		for i in monthList: # monthList -> array from config.py
			arrBln.append({'id':aidi_bln, 'kode':i, 'nama':monthList[i], 'tahun':tahun})
			aidi_bln += 1	

		arrData = {'jns_spj':arrjns_spj, 'jns_lap':arrjns_lap,
				'ls_data':pjbt,'bulan_lap':arrBln,
		}

		return render(request,'akuntansi/laporan/lap_verifikasi.html',arrData)
