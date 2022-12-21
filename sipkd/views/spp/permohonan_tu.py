from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import pprint

def mohon_spptu(request):
	skpd = set_organisasi(request)
	is_perubahan = perubahan(request)
	namabank = set_nama_bank(request)        
	path = ''    
	if skpd["kode"] == '': kode = 0
	else: kode = skpd["kode"]

	dataAsal = 'array'
	if dataAsal == 'db':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM master.master_metode_pengadaan ORDER BY id")
			list_pengadaan = dictfetchall(cursor)
	else:
		list_pengadaan = [{'id': 1, 'uraian': 'LS Bendahara'},{'id': 2, 'uraian': 'LS Pihak Ketiga'}]

	data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"], 'pengadaan':list_pengadaan, 
		'asaldtpengadaan':dataAsal, 'is_perubahan':is_perubahan,'namabank':namabank['list_bank']}
		
	return render(request, 'spp/sppTU_mohon.html',data)


def mohon_spptu_simpan(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			dtx = request.POST
			aksi = dtx.get('aksi')
			jenis = dtx.get('jenis').upper()
			org = dtx.get('organisasi').split('.')
			kd_unit = dtx.get('kode_unit')
			no_spp = dtx.get('no_spp')
			no_spp_lama = dtx.get('no_spp_lama')
			tanggal_spp = tgl_short(dtx.get('tanggal_spp'))
			bendahara = dtx.get('bendahara')
			norek_bendahara = dtx.get('norek_bendahara')
			nama_bank = dtx.get('nama_bank')
			npwp_bendahara = dtx.get('npwp_bendahara')
			nm_pemilik_rekening = dtx.get('nama_rekening_bank')
			status_keperluan = dtx.get('status_keperluan')            
			total = dtx.get('total_spp')
			triwulan = dtx.get('st_triwulan')
			perubahan = dtx.get('st_perubahan')
			rincian = dtx.getlist('afektasispp')
			tanggal = dtx.get('tanggal_spp').split(' ')
			tw = int(arrMonth[tanggal[1]])
			tgldpa = 'NOW()'
			jenispengadaan = 0
			kode_sumberdana = dtx.get('kode_sumberdana') 
			tgl_pelaksanaan = tgl_short(dtx.get('tanggal_pelaksanaan'))

			nospj = jenisdpa = nomordpa = namaperusahaan = bentukperusahaan = alamatperusahaan = ''
			pimpinan = npwp_perusahaan = bank_perusahaan = rekperusahaan = nomerkontrak = pelaksanaan = ''
			pemilik_rekening_perusahaan = ''
		
			if tw <= 3:
				triwulan = 1
			elif tw <= 6:
				triwulan = 2
			elif tw <= 9:
				triwulan = 3
			else:
				triwulan = 4  
		   
			if no_spp != "":
				if aksi == "true":
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO PENATAUSAHAAN.SPP_PERMOHONAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,TGLSPP,TGLSPP_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"\
							" DESKRIPSISPP,NOSPD,TGLSPD,SISADANASPD,JMLSPD,JUMLAHSPP,BENDAHARAPENGELUARAN,NOREKENINGBENDAHARA,JENISSPP,jenisdpa,tgldpa,nodpa,namabank,"\
							" namaperusahaan,bentukperusahaan,alamatperusahaan,namapimpinanperusahaan,norekperusahaan,nokontrak,namabankperusahaan,npwpperusahaan,"\
							" npwp,deskripsipekerjaan,triwulan,perubahan,nospj,waktupelaksanaan,namarekeningbank,uname,jenispengadaan,pemilikrekeningperusahaan,kode_sumberdana,tgl_pelaksanaan)"\
							" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun_log(request),org[0],org[1],org[2],kd_unit,no_spp.upper(),tanggal_spp,tanggal_spp,'',0,0,status_keperluan,'','NOW()',0,0,total,
							bendahara,norek_bendahara,jenis,jenisdpa,tgldpa,nomordpa,nama_bank,namaperusahaan,bentukperusahaan,alamatperusahaan,
							pimpinan,rekperusahaan,nomerkontrak,bank_perusahaan,npwp_perusahaan,npwp_bendahara,status_keperluan,
							triwulan,perubahan,nospj,pelaksanaan,nm_pemilik_rekening,username(request),jenispengadaan,pemilik_rekening_perusahaan,kode_sumberdana,tgl_pelaksanaan])
						hasil = ""
						   
				elif aksi == "false":
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE PENATAUSAHAAN.SPP_PERMOHONAN SET NOSPP=%s, TGLSPP=%s, TGLSPP_DRAFT=%s, DESKRIPSISPP=%s,"
							"JUMLAHSPP=%s, BENDAHARAPENGELUARAN=%s, NOREKENINGBENDAHARA=%s, namarekeningbank=%s, jenisdpa=%s, tgldpa=%s, nodpa=%s, "
							"namabank=%s, namaperusahaan=%s, bentukperusahaan=%s, alamatperusahaan=%s, namapimpinanperusahaan=%s, "
							"norekperusahaan=%s, nokontrak=%s, npwp=%s, deskripsipekerjaan=%s, namabankperusahaan=%s, npwpperusahaan=%s, " 
							"PERUBAHAN=%s, TRIWULAN=%s, NOSPJ=%s, waktupelaksanaan=%s, jenispengadaan=%s, pemilikrekeningperusahaan=%s, kode_sumberdana=%s, tgl_pelaksanaan=%s"
							"WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s and NOSPP=%s ",
							[no_spp.upper(),tanggal_spp,tanggal_spp,status_keperluan,total,bendahara,norek_bendahara,nm_pemilik_rekening,jenisdpa,tgldpa,nomordpa,
							nama_bank,namaperusahaan,bentukperusahaan,alamatperusahaan,pimpinan,rekperusahaan,nomerkontrak, npwp_bendahara, status_keperluan,
							bank_perusahaan,npwp_perusahaan,perubahan,triwulan,nospj,pelaksanaan,jenispengadaan,pemilik_rekening_perusahaan,kode_sumberdana,tgl_pelaksanaan,
							tahun_log(request),org[0],org[1],org[2],kd_unit,no_spp_lama.upper()])
						hasil = ""

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM PENATAUSAHAAN.SPP_PERMOHONAN_RINCIAN WHERE tahun=%s and KODEURUSAN=%s "
						"and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s  and NOSPP=%s",
						[tahun_log(request),org[0],org[1],org[2],kd_unit,no_spp.upper()])
				
				for i in range(0,len(rincian)):
					obj = rincian[i].split("|")
					if len(obj[0].split('.')) != 5:
						obj1 = obj[0].split("-") #rekening
						obj2 = toAngkaDec(obj[1]) #jumlah
						objek1 = obj1[0].split(".") #kodeorganisasi bidang
						objek2 = obj1[1].split(".") #koderekening

						if obj2!='0.00':
							with connections[tahun_log(request)].cursor() as cursor:
								 cursor.execute("INSERT INTO PENATAUSAHAAN.SPP_PERMOHONAN_RINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,"
									"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
									"KODERINCIANOBJEK,KODESUBRINCIANOBJEK,KODESUB1,KODESUB2,KODESUB3,TANGGAL,JUMLAH)"
									" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
									[tahun_log(request),org[0],org[1],org[2],kd_unit,no_spp.upper(),objek1[0]+"."+objek1[1],objek1[2],objek1[3]+"."+objek1[4],objek1[5],0,
									objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],objek2[5],0,0,0,tanggal_spp,obj2])                                     
							hasil = "Data berhasil disimpan!"

			return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')

def mohon_spptu_load(request, jenis):
	org = request.GET.get('id').split('.') 
	tanggal_spp = ''
	jenis_spp = 'tu'
	jenis = jenis.lower()
	fromx = 'tu_mohon'

	print('bajindul')

	if jenis == 'tu_mohon':
		is_locked = ''
	else:
		is_locked = "and s.locked = 'Y'"
		
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT s.kodeunit,s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai "
			"from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan "
			"and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.deskripsispp as keperluan,"
			"(select sum (jumlah) from penatausahaan.spp_permohonan_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
			"and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp ) as jumlah,"
			"(select kodebidang from penatausahaan.spp_permohonan_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
			"and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp limit 1 ) as kodebidang,"
			"(select kodeprogram from penatausahaan.spp_permohonan_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
			"and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodeprogram,"
			"(select kodekegiatan from penatausahaan.spp_permohonan_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
			"and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodekegiatan,"
			"(select kodesubkegiatan from penatausahaan.spp_permohonan_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
			"and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodesubkegiatan,"
			"s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit FROM penatausahaan.spp_permohonan s  where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s "
			"and s.kodeorganisasi=%s and kodeunit=%s and s.jenisspp=%s "+is_locked+" and ((s.no_spp_tu is null) or (s.no_spp_tu not in (select nospp from penatausahaan.spp w where w.tahun=%s and w.kodeurusan=%s and w.kodesuburusan=%s and w.kodeorganisasi=%s and w.kodeunit=%s and w.jenisspp=%s)))",
			[tahun_log(request),org[0],org[1],org[2],org[3],jenis_spp.upper(), tahun_log(request),org[0],org[1],org[2],org[3],jenis_spp.upper()])
		list_spp = dictfetchall(cursor)

	objek = []
	for arr in list_spp:
		objek.append({'nospp':arr['nospp'],'organisasi':arr['organisasi'],'keperluan':arr['keperluan'],
			'jumlah':arr['jumlah'],'tanggal':tgl_indo(arr['tanggal']),'kodebidang':arr['kodebidang'],'kodeunit':arr['kodeunit'],
			'kodeprogram':arr['kodeprogram'],'kodekegiatan':arr['kodekegiatan'],'kodesubkegiatan':arr['kodesubkegiatan']})

	data = {'list_spp':objek, 'fromx':fromx}
	return render(request, 'spp/modal/modal_spp.html', data)

def mohon_spptu_delete(request):
	tahun = tahun_log(request)
	nospp = request.POST.get('nospp')
	gets  = request.POST.get('org') 
	kdunit = request.POST.get('kdunit')
	hasil = ''
	
	if gets != '0':
		orgs = gets.split('.')
		skpd = orgs[0]+"."+orgs[1]+"."+orgs[2]+"."+orgs[3]
	else:
		skpd = '0.0.0.0'
		

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM PENATAUSAHAAN.SPP_PERMOHONAN where tahun = %s and nospp = %s and \
			kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit = %s ",
			[tahun,nospp,skpd])
		hasil = ""
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM PENATAUSAHAAN.SPP_PERMOHONAN_RINCIAN where tahun = %s and nospp = %s and \
			kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit = %s",
			[tahun,nospp,skpd])
		hasil = "Data berhasil dihapus!"

	return HttpResponse(hasil)


def mohon_spptu_setujui(request):
	skpd = set_organisasi(request)
	if skpd["kode"] == '': kode = 0
	else: kode = skpd["kode"]
	
	data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"],}
	return render(request, 'spp/sppTU_mohon_validasi.html',data)

def mohon_spptu_setujui_list(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd', None) 
		isppkd = request.POST.get('isppkd', None)  
		
		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')        

		total_spp = 0
		total_setuju = 0
		if(isppkd=='1'):
			jenis = " AND JENISSPP IN ('LS_PPKD','NON ANGG')"            
		else:
			jenis = " AND JENISSPP NOT IN ('LS_PPKD','NON ANGG')" 
				  
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT NOSPP,JENISSPP,TANGGAL as TGLSPP,KEPERLUAN,dasarspd,kegiatan,kodeunit,\
				JUMLAH,0 as CEK,idspp \
				FROM penatausahaan.fc_lihat_spp_skpd_mohon(%s,%s,%s,%s,%s) \
				WHERE locked='T' "+jenis+"",
				[tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
		   
			list_spp = dictfetchall(cursor)  

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT NOSPP,JENISSPP,TANGGAL as TGLSPP,\
				(case when NOSPM is null then '-' else NOSPM end)as NOSPM,\
				KEPERLUAN,dasarspd,kegiatan,kodeunit,JUMLAH,tanggal,0 as CEK,idspp \
				FROM penatausahaan.fc_lihat_spp_skpd_mohon(%s,%s,%s,%s,%s) \
				WHERE locked='Y' "+jenis+"",
				[tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
			list_setuju = dictfetchall(cursor)      

		objek = []
		for arr in list_setuju:
			total_setuju += arr['jumlah']
			objek.append({'nospp':arr['nospp'], 'jenisspp':arr['jenisspp'], 'tglspp':arr['tglspp'], 'nospm':arr['nospm'],
				'keperluan':arr['keperluan'], 'dasarspd':arr['dasarspd'],'idspp':arr['idspp'],'kodeunit':arr['kodeunit'],
				'kegiatan':arr['kegiatan'], 'jumlah':arr['jumlah'], 'cek':arr['cek'],'tanggal':tgl_indo(arr['tanggal'])})

		for total in list_spp:
			total_spp += total['jumlah']

		if total_spp == 0:
			total_spp = '0,00'
		if total_setuju == 0:
			total_setuju = '0,00'

		data = {'list_spp' : ArrayFormater(list_spp), 'list_setuju' : ArrayFormater(objek),'total_spp' : total_spp,'total_setuju':total_setuju}
		return render(request, 'spp/sppTU_mohon_validasi_list.html', data)

	else:
		return redirect('sipkd:index')

def mohon_spptu_setujui_action(request, jenis):
    hasil = ''
    lock = jenis.lower()
    
    if request.method == 'POST':
        tahun = tahun_log(request)
        gets = request.POST.get('skpd', None)    
        kdunit = request.POST.get('kdunit')

        if(lock == 'lock'):
            locked = 'Y'
            chkspp = request.POST.getlist('cek_draft')
            nomor = request.POST.getlist('nomer_draft')
        else:
            locked = 'T'  
            chkspp = request.POST.getlist('cek_spp')
            nomor = request.POST.getlist('nomer_spp')

        skpd = '0.0.0.0'
        if gets=='0':                        
            aidi = skpd.split('.')  
        else:
            aidi = gets.split('.') 

        
        for i in range(0,len(chkspp)):
            cek = chkspp[i]            
            nomer_spp = nomor[i]
            spp = cek+':'+nomer_spp  
            split_spp = spp.split(':')

            if(split_spp[0]=='1'):
                nospp = split_spp[1] 
        
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.spp_permohonan set locked=%s where tahun=%s"
                        " and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and KODEUNIT=%s"
                        " and NOSPP in (%s)",[locked,tahun,aidi[0],aidi[1],aidi[2],aidi[3],nospp])
                if(locked == "Y"):
                    hasil = "SPP Telah di Setujui"
                else:
                    hasil = "SPP Telah di Unlock"
    return HttpResponse(hasil)