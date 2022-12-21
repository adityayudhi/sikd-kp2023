from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import pprint

def getnew_nopspj(request,jenis):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')              

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT hasil FROM penatausahaan.fc_otomatis_bkp(%s,%s,%s,lpad(%s,2,'0'),%s,%s)",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],jenis])
			no_lpj = dictfetchall(cursor)

		data = {}
		for arr in no_lpj:
			data = {'nopspj':arr['hasil']}

		return JsonResponse(data)
	else:
		return redirect('sipkd:index')

def bkp_index(request,jenis):
	path = '' 
	skpd = set_organisasi(request)   
	jns_bkp = jenis.upper()

	if skpd["kode"] == '': kode = 0
	else: kode = skpd["kode"]

	if jns_bkp == 'GU':
		path = 'bkp_UPGU.html'
	# elif jns_bkp == 'TU':
	# 	path = 'bkp_TU.html'
	else:
		return redirect('sipkd:index')

	data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"],}
	return render(request, 'spp/'+path+'',data)

def bkp_list(request,jenis):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd',None)
		jenis = jenis.upper() 
		path = '' 


		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')                        
		
		if jenis == 'GU':
			path = 'bkp_tabel_upgu.html'
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("""SELECT DISTINCT a.nopspj,a.tglpspj,b.nospj,d.tglspj,a.keperluan, 0 as cek, a.jenis,
					(select sum(c.jumlah) from penatausahaan.bkp_skpd_rinc_sub1 c 
					    where c.tahun = a.tahun and c.kodeurusan = a.kodeurusan
					    and c.kodesuburusan = a.kodesuburusan and c.kodeorganisasi = a.kodeorganisasi
					    and c.kodeunit = a.kodeunit and c.nopspj = a.nopspj) as jumlah
					FROM penatausahaan.bkp_skpd a
						LEFT JOIN penatausahaan.spj_skpd_rinc b ON b.tahun = a.tahun and b.kodeurusan = a.kodeurusan
							and b.kodesuburusan = a.kodesuburusan and b.kodeorganisasi = a.kodeorganisasi
							and b.kodeunit = a.kodeunit and b.nopspj = a.nopspj
						LEFT JOIN penatausahaan.spj_skpd d ON d.tahun = b.tahun and d.kodeurusan = b.kodeurusan
							and d.kodesuburusan = b.kodesuburusan and d.kodeorganisasi = b.kodeorganisasi
							and d.kodeunit = b.kodeunit and d.nospj = b.nospj and d.jenis = a.jenis
					WHERE a.tahun = %s and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s 
					and a.kodeunit = %s and a.jenis = %s
					ORDER BY a.tglpspj,a.nopspj DESC""",
					[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'GU'])
				list_lpj = dictfetchall(cursor)
				
		# elif jenis=='TU':        
		#     path = 'bkp_tabel_tu.html'
		#     with connections[tahun_log(request)].cursor() as cursor:
		#         cursor.execute("SELECT * ,0 as cek, to_char( tglspj, 'dd/mm/yyyy') as tanggal, "
		#             "(CASE WHEN jumlahsp2d is NULL THEN 0.00 ELSE jumlahsp2d END) as jumlahsp2d, "
		#             "(CASE WHEN jumlahsetor is NULL THEN 0.00 ELSE jumlahsetor END) as jumlahsetor, "
		#             "(CASE WHEN sisasp2d is NULL THEN 0.00 ELSE sisasp2d END) as sisasp2d "
		#             "FROM penatausahaan.fc_skpd_view_spj(%s,%s,%s,lpad(%s,2,'0'),%s) "
		#             "WHERE jenis=%s order by tglspj,nospj ",
		#             [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'TU'])
		#         list_lpj = dictfetchall(cursor) 
		else:
			return redirect('sipkd:index')

		data = {'list_lpj' : ArrayFormater(list_lpj)}
		return render(request, 'spp/tabel/'+path+'', data)

	else:
		return redirect('sipkd:index')

def bkp_kegiatan(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nopspj = request.POST.get('nopspj')       
		kondisi = ''
		
		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')      

		# rincian kegiatan
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT DISTINCT(sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan) as kegiatan, "
				"sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.nopspj,sr.kodeorganisasi, sr.kodeunit,"
				"(select urai from master.master_organisasi morg WHERE morg.tahun = sr.tahun and morg.kodeurusan=sr.kodeurusan and morg.kodesuburusan=sr.kodesuburusan and"
				" morg.kodeorganisasi=sr.kodeorganisasi and morg.kodeunit=sr.kodeunit) as urai_skpd,"
				"(select urai from penatausahaan.kegiatan k where k.tahun=sr.tahun and k.kodeurusan=sr.kodeurusan and k.kodesuburusan=sr.kodesuburusan "
				"and k.kodeorganisasi=sr.kodeorganisasi and k.kodeunit=sr.kodeunit and k.kodebidang=sr.kodebidang and k.kodeprogram=sr.kodeprogram and k.kodekegiatan=sr.kodekegiatan and k.kodesubkegiatan=sr.kodesubkegiatan and k.kodesubkeluaran = 0) as uraikegiatan,"
				"(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) from penatausahaan.bkp_skpd_rinc_sub1 sj where sj.tahun=sr.tahun and sj.kodeurusan=sr.kodeurusan and sj.kodesuburusan=sr.kodesuburusan "
				"and sj.kodeorganisasi=sr.kodeorganisasi and sj.kodeunit=sr.kodeunit and sj.nopspj=sr.nopspj and sj.kodebidang=sr.kodebidang and sj.kodeprogram=sr.kodeprogram "
				"and sj.kodekegiatan=sr.kodekegiatan and sj.kodesubkegiatan=sr.kodesubkegiatan) as jumlah from penatausahaan.bkp_skpd_rinc sr join penatausahaan.bkp_skpd s "
				"ON(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nopspj=s.nopspj) "
				"where sr.tahun=%s and sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=lpad(%s,2,'0') and sr.kodeunit=%s"
				"and s.jenis in ('UP','GU') and s.nopspj =%s order BY sr.nopspj,sr.kodeprogram,sr.kodekegiatan ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],nopspj])
			list_keg = dictfetchall(cursor) 

		for arr in list_keg:
			kondisi += ','+arr['kegiatan']

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) AS sp2dup,(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) as jumlah from penatausahaan.bkp_skpd_rinc_sub1 where tahun=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nopspj=%s) FROM penatausahaan.SP2DRINCIAN WHERE TAHUN=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and kodeakun=1 and kodekelompok=1 and kodejenis=1 and kodeobjek=3 and koderincianobjek=1",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],nopspj,tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3]]) 
			list_foot = dictfetchall(cursor)
		
		for ar in list_foot:
			sp2dup = ar['sp2dup']
			jumlahlpj = ar['jumlah']
			sisaup = ar['sp2dup']-ar['jumlah']

		if hakakses_sipkd(request) in ['BPP']:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT pengeluaran FROM pertanggungjawaban.skpd_bku WHERE tahun = %s and UNAME_BANTU = %s \
					and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s",
					[tahun_log(request), username(request), aidi[0],aidi[1],aidi[2],aidi[3]])
				up_bpp = cursor.fetchone()
			sp2dup = up_bpp[0]
			sisaup = sp2dup-jumlahlpj
		
		data = {'list_keg' : list_keg,'kondisi':kondisi[1:],
			'sp2dup':sp2dup, 'jumlahlpj':jumlahlpj, 'sisaup':sisaup}
		return render(request, 'spp/tabel/bkp_tabel_kegiatan.html', data)

	else:
		return redirect('sipkd:index')

def bkp_kegiatan_add(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nopspj = request.POST.get('nopspj')       
		kondisi = ''

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')      

		if hakakses_sipkd(request) in ['BPP']:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT kegiatan FROM penatausahaan.pengguna WHERE tahun = %s \
					and UNAME = %s and hakakses = %s",[tahun_log(request), username(request), 
					hakakses_sipkd(request)])
				kegiatan = dictfetchall(cursor)
			clause_in = "WHERE kodeunit||'|'||koderekening in ("+"'{0}'".format("', '".join(kegiatan[0]['kegiatan'].replace('-','.').split('~')))+")"
		else:
			clause_in = ''
		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select *, ROW_NUMBER () OVER () as nomor, "
				"(CASE WHEN CEK is NULL THEN 0 ELSE CEK END) as pilih, "
				"(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as pagu, "
				"(CASE WHEN ls is NULL THEN 0.00 ELSE ls END) as sp2dls, "
				"(CASE WHEN upgu is NULL THEN 0.00 ELSE upgu END) as sp2dupgu, "
				"(CASE WHEN tu is NULL THEN 0.00 ELSE tu END) as sp2dtu, "
				"(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sp2dsisa, "
				"COALESCE(array_length(string_to_array(sumberdana, '|'),1),0) as jumsumdan, "
				"string_to_array(sumberdana, '|') as sumdan "
				"from penatausahaan.fc_view_kegiatan_bkp (%s,%s,%s,lpad(%s,2,'0'),%s) "+clause_in+"",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3]])
			add_kegiatan = dictfetchall(cursor)     

		# print(add_kegiatan['uraian'])

		data = {'add_kegiatan' : ArrayFormater(add_kegiatan)}
		return render(request, 'spp/tabel/bkp_tabel_tambah_kegiatan.html', data)

	else:
		return redirect('sipkd:index')

def bkp_cek_nospd(request):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')
		nopspj = request.POST.get('nopspj','|').split('|')    
		
		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')   

		# ambil spj
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select NOSP2D,nopspj,KEPERLUAN,TGLPSPJ FROM penatausahaan.BKP_SKPD where tahun=%s"
				" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit = %s and nopspj=%s",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],nopspj[0]])
			list_spj = dictfetchall(cursor)

		data = {}
		for arr in list_spj:  
			data = {'nosp2d':arr['nosp2d'], 'nopspj':arr['nopspj'],'keperluan':arr['keperluan'],'tglpspj':tgl_indo(arr['tglpspj'])}

	return JsonResponse(data)

def bkp_kegiatan_save(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			nopspj = request.POST.get('no_pspj')
			nopspj_old = request.POST.get('no_pspj_old')
			tgl = tgl_short(request.POST.get('tgl_pspj'))
			keperluan = request.POST.get('uraian')
			nosp2d = request.POST.get('edNoSP2D')
			rincian = request.POST.getlist('daftarkegiatan')
			aksi = request.POST.get('aksi') 
			
			if nopspj!='':               
				if aksi=='true':
					# pass
					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("INSERT INTO penatausahaan.BKP_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit"
								",nopspj,TGLPSPJ,KEPERLUAN,STATUS,USERNAME,JENIS,NOSP2D) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
								[tahun_log(request),org[0],org[1],org[2],org[3],nopspj,tgl,keperluan,'0',username(request),'GU',nosp2d])
							hasil = ''
					except Exception as e:
						print('Duplikasi Primary Key', e)
						pass
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BKP_SKPD SET nopspj=%s, KEPERLUAN=%s, TGLPSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') AND KODEUNIT = %s AND nopspj=%s",
							[nopspj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],org[3],nopspj_old])
						hasil = ''

				for i in range(0,len(rincian)):
					obj = rincian[i].split('|')
					obj1 = obj[1].split('.') #koderekening
					kodebidang = obj1[0]+'.'+obj1[1]
					kodeprogram = obj1[3]
					kodekegiatan = obj1[4]+'.'+obj1[5]
					kodesubkegiatan = obj1[6]

					# try:
					# 	with connections[tahun_log(request)].cursor() as cursor:
					# 		cursor.execute("INSERT INTO penatausahaan.BKP_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit"
					# 			",nopspj,TGLPSPJ,KEPERLUAN,STATUS,USERNAME,JENIS,NOSP2D) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
					# 			[tahun_log(request),org[0],org[1],org[2],obj[7],nopspj,tgl,keperluan,'0',username(request),'GU',nosp2d])
					# 		hasil = ''
					# except Exception as e:
					# 	print('Duplikasi Primary Key', e)
					# 	pass

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND KODEUNIT=%s AND nopspj=%s "
							"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s AND KODESUBKEGIATAN = %s AND KODESUBKELUARAN = 0 AND KODEAKUN=%s "
							"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s",
							[tahun_log(request),org[0],org[1],org[2],obj[7],nopspj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,0,0,0,0,0])
						hasil = ''

					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("INSERT INTO penatausahaan.BKP_SKPD_RINC (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,nopspj,"
								"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
								"KODERINCIANOBJEK,kodesubrincianobjek) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
								[tahun_log(request),org[0],org[1],org[2],obj[7],nopspj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,0,0,0,0,0,0])
							hasil = ''
					except Exception as e:
						print('Duplikasi Primary Key 2',e)
						pass

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')


def bkp_rekening_list(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nopspj = request.POST.get('nopspj')
		arr = request.POST.get('arr')           
		kegiatan = arr.split('|')       
		objek = kegiatan[0].split('.')
		kodebidang = objek[0]+'.'+objek[1]
		kodeprogram = objek[3]
		kodekegiatan = objek[4]+'.'+objek[5]
		kodesubkegiatan = objek[6]
		urai_kegiatan = kegiatan[0]+'-'+kegiatan[2]

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select kodeunit,koderekening,anggaran,uraian ,sekarang as jumlahspj,lalu,jumlah as totalspj,sisa as sisapagu "
				"from penatausahaan.fc_rekening_bkp_skpd (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],kegiatan[3],kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,nopspj])
			list_rekening = dictfetchall(cursor)        

		data = {'list_rekening' : ArrayFormater(list_rekening),'urai_kegiatan':urai_kegiatan}
		return render(request, 'spp/tabel/bkp_tabel_rekening.html', data)

	else:
		return redirect('sipkd:index')


def bkp_rincian_list(request,jenis):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nopspj = request.POST.get('nopspj')
		urai_kegiatan = request.POST.get('kegiatan')
		arr = request.POST.get('arr')

		kegiatan = arr.split('|')
		
		urai_rekening = kegiatan[0]+' - '+kegiatan[1]       
		objek = kegiatan[0].split('-')
		objek2 = objek[0].split('.') # program kegiatan
		objek3 = objek[1].split('.') # koderekening
		kodebidang = objek2[0]+'.'+objek2[1]
		kodeprogram = objek2[3]
		kodekegiatan = objek2[4]+'.'+objek2[5]
		kodesubkegiatan = objek2[6]
		spj_lalu = '0,00'
		jml_lpj_lalu = 0
		jumlah_lpj_terbit = 0

		if jenis == 'GU':
			pagu = kegiatan[2]
			spj_lalu = kegiatan[3]
			# total = kegiatan[5]
			total = kegiatan[4]
			sisa = kegiatan[6]
			kodeunit = kegiatan[7]
		else:
			pagu = kegiatan[2]
			total = kegiatan[3]
			sisa = kegiatan[5]
			kodeunit = kegiatan[6]

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')      
		
		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT sr.kodeunit, sr.kodesub1 as pilih,sr.uraian,sr.tglbukti, sr.jenisbayar, \
				sr.jumlah as spjsekarang,sr.nobukti,sr.sumberdana,\
				(select count(tahun) from penatausahaan.bkp_skpd_potongan b where b.tahun=sr.tahun and b.kodeurusan=sr.kodeurusan \
				and b.kodesuburusan=sr.kodesuburusan and b.kodeorganisasi=sr.kodeorganisasi and b.kodeunit=sr.kodeunit \
				and b.nopspj=sr.nopspj and b.nobukti = sr.nobukti) as jml_pot,\
				case when sr.nobukti is not null then 'true' else 'false' end as status \
				from penatausahaan.bkp_skpd_rinc_sub1 sr where sr.tahun=%s and sr.kodeurusan=%s and sr.kodesuburusan=%s \
				and sr.kodeorganisasi=%s and sr.kodeunit=%s and sr.kodebidang=%s and sr.kodeprogram=%s \
				and sr.kodekegiatan=%s and sr.kodesubkegiatan=%s and sr.kodesubkeluaran=0 \
				and sr.kodeakun=%s and sr.kodekelompok=%s and sr.kodejenis=%s and sr.kodeobjek=%s \
				and sr.koderincianobjek=%s and sr.kodesubrincianobjek=%s and sr.nopspj=%s ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],kodeunit,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,
				int(objek3[0]),int(objek3[1]),int(objek3[2]),int(objek3[3]),int(objek3[4]),int(objek3[5]),nopspj])
			
			list_rincian = dictfetchall(cursor) 

		objek = [] 
		tot_pot = 0
		for arr in list_rincian:     
			# rek_pot = '-' if arr['rekpot'] == None else arr['rekpot']
			# jum_pot = '0.00' if arr['jumlahpotongan'] == 0 else arr['jumlahpotongan'] 
			# tot_pot = tot_pot + arr['jumlahpotongan']

			objek.append({'kodeunit':arr['kodeunit'],'pilih':arr['pilih'],'uraian':arr['uraian'],'tglbukti':tgl_indo(arr['tglbukti']),
				'spjsekarang':arr['spjsekarang'],'nobukti':arr['nobukti'],'idInp':(int(arr['pilih'])),
				'rekeningpotongan':arr['jml_pot'],'status':arr['status'], 'jenisbayar':arr['jenisbayar'],'sumberdana':arr['sumberdana']})


		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) AS sp2dup,"
				"(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) as jumlah "
				"from penatausahaan.bkp_skpd_rinc_sub1 where tahun=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nopspj=%s) "
				"FROM penatausahaan.SP2DRINCIAN WHERE TAHUN=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s "
				"and kodeakun=1 and kodekelompok=1 and kodejenis=1 and kodeobjek=3 and koderincianobjek=1",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],nopspj,
				tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3]]) 
			list_foot = dictfetchall(cursor)

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""SELECT (CASE WHEN sum(a.jumlah) is NULL THEN 0.00 ELSE sum(a.jumlah) END) AS lpj_lalu
				FROM penatausahaan.bkp_skpd_rinc_sub1 a WHERE a.tahun = %s and a.kodeurusan = %s \
				and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
				and a.nopspj in (SELECT b.nopspj FROM penatausahaan.bkp_skpd b WHERE b.tahun = a.tahun \
				and b.kodeurusan = a.kodeurusan and b.kodesuburusan = a.kodesuburusan \
				and b.kodeorganisasi = a.kodeorganisasi and b.kodeunit = a.kodeunit and b.jenis = 'GU')
				""",[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3]])
			jml_lpj_lalu = cursor.fetchone()
		
		for ar in list_foot:
			sp2dup = ar['sp2dup']
			jumlahlpj = ar['jumlah']
			sisaup = ar['sp2dup']-ar['jumlah']

		if hakakses_sipkd(request) in ['BPP']:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT pengeluaran FROM pertanggungjawaban.skpd_bku WHERE tahun = %s \
					and UNAME_BANTU = %s and kodeurusan = %s \
					and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s",
					[tahun_log(request), username(request), aidi[0],aidi[1],aidi[2],aidi[3]])
				up_bpp = cursor.fetchone()
			sp2dup = up_bpp[0]
			sisaup = sp2dup-jumlahlpj

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute(""" SELECT case when  sum(sr.jumlah) is null then 0 else sum(sr.jumlah) end as jumlahsp2dup 
				FROM penatausahaan.sp2drincian sr join penatausahaan.sp2d s on
				(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan \
				and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nosp2d=s.nosp2d )
				WHERE sr.tahun = %s and sr.kodeurusan = %s and sr.kodesuburusan = %s and sr.kodeorganisasi = %s 
				and sr.kodeunit = %s and s.jenissp2d in ('UP','GU')
				""", [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3]])
			jumlah_lpj_terbit = cursor.fetchone()

		sisaup = jumlah_lpj_terbit[0] - jml_lpj_lalu[0]
		
		data = {'list_rincian' : objek,
			'urai_kegiatan':urai_kegiatan,
			'urai_rekening':urai_rekening,
			'pagu':pagu,
			'total':total,
			'sisa':sisa,
			'sisaup':sisaup,
			'spj_lalu':spj_lalu,
			'total_pot':'0.00' if tot_pot == 0 else tot_pot,
			'jenis':jenis,
			'sp2dup':sp2dup,
			}
		
		# print(data)

		return render(request, 'spp/tabel/bkp_tabel_rincian.html', data)

	else:
		return redirect('sipkd:index')


def bkp_rincian_save(request,jenis):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':			
			aksi = request.POST.get('aksi') 
			org = request.POST.get('skpd').split('.')
			nopspj = request.POST.get('no_pspj')
			nopspj_old = request.POST.get('no_pspj_old')
			tgl = tgl_short(request.POST.get('tgl_pspj'))
			keperluan = request.POST.get('uraian')	
			urai_rek = request.POST.get('urai_rekening')

			nomer = request.POST.getlist('nomer')
			sumberdana = request.POST.getlist('sumberdana')
			no_bukti = request.POST.getlist('no_bukti')
			tgl_bukti = request.POST.getlist('tgl_bukti')
			uraian = request.POST.getlist('urai_belanja')
			pengeluaran = request.POST.getlist('pengeluaran')
			jenisbayar = request.POST.getlist('jns_bayar')

			rekening = urai_rek.split('-')
			objek = rekening[0].split('.')
			kodebidang = objek[0]+'.'+objek[1]
			kodeprogram = objek[3]
			kodekegiatan = objek[4]+'.'+objek[5]
			kodesubkegiatan = objek[6]

			objek2 = rekening[1].split('.')
			kodeakun = objek2[0]
			kodekelompok = objek2[1]
			kodejenis = objek2[2]
			kodeobjek = objek2[3]
			koderincianobjek = objek2[4]
			kodesubrincianobjek = objek2[5]

			if jenis == 'TU':
				nosp2d = request.POST.get('no_sp2d')
				kodeunit = request.POST.get('skpd').split('.')[3]
			else:
				nosp2d = request.POST.get('edNoSP2D')
				kodeunit = request.POST.get('kegiatan').split('|')[3]   
				

			# REKENING POTONGAN =========================================
			rek_potongan = request.POST.getlist('cut_kdrek')
			jml_potongan = request.POST.getlist('jml_potongan')
					
			if nopspj != '':
				if aksi=='true':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO penatausahaan.BKP_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit"
							",nopspj,TGLPSPJ,KEPERLUAN,STATUS,USERNAME,JENIS,NOSP2D) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj,tgl,keperluan,'0',username(request),jenis,nosp2d])
						hasil = ''
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BKP_SKPD SET nopspj=%s, KEPERLUAN=%s, TGLPSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s AND nopspj=%s",
							[nopspj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj])
						hasil = ''

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC WHERE TAHUN=%s "
						"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND kodeunit = %s AND nopspj=%s "
						"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s AND kodesubkegiatan = %s and kodesubkeluaran = 0 AND KODEAKUN=%s "
						"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s",
						[tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek, kodesubrincianobjek])
					hasil = ''

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.BKP_SKPD_RINC (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,nopspj,"
						"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan,kodesubkeluaran,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
						"KODERINCIANOBJEK,kodesubrincianobjek) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
						[tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek])
					hasil = ''

				for i in range(0,len(nomer)):
					kodesub1 = nomer[i] 
					tglbukti = tgl_short(tgl_bukti[i])          
					# jumlah = toAngkaDec(pengeluaran[i])
					jumlah = pengeluaran[i].replace(',','')
					nobukti = no_bukti[i]
					urai = uraian[i]
					jenis_pembayaran = jenisbayar[i]
					sumberdana_lpj = sumberdana[i]

					# rek_pot = rek_potongan[i].split(' - ')[0]
					# jml_pot = jml_potongan[i].replace(',','')
					rek_pot = '0'
					jml_pot = 0

					with connections[tahun_log(request)].cursor() as cursor:                     
						cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC_SUB1 WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s and kodeunit = %s AND nopspj=%s "
							"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s and kodesubkegiatan = %s and kodesubkeluaran = 0 AND KODEAKUN=%s "
							"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s AND KODESUB1=%s ",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj,kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,
							int(kodeakun),int(kodekelompok),int(kodejenis),int(kodeobjek),int(koderincianobjek),kodesubrincianobjek,int(kodesub1)])
						hasil = ''

					with connections[tahun_log(request)].cursor() as cursor: 
						cursor.execute("INSERT INTO penatausahaan.BKP_SKPD_RINC_SUB1 (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,nopspj,"
							"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan,kodesubkeluaran,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
							"KODERINCIANOBJEK,kodesubrincianobjek,KODESUB1,JUMLAH,NOBUKTI,TGLBUKTI,URAIAN,rekeningpotongan,jumlahpotongan, jenisbayar,sumberdana) "
							"VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nopspj,kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,0,
							int(kodeakun),int(kodekelompok),int(kodejenis),int(kodeobjek),int(koderincianobjek),kodesubrincianobjek,int(kodesub1),jumlah,nobukti,
							tglbukti,urai,rek_pot,jml_pot, jenis_pembayaran,sumberdana_lpj])                 
						hasil = 'Data telah berhasil disimpan' 

		return HttpResponse(hasil) 

	else:
		return redirect('sipkd:index')

def bkp_list_delete(request):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('organisasi').split('.')
		arr = request.POST.getlist('draftchk')
		jenis = request.POST.get('jenis')       
		hasil = ''

		# print(request.POST)
		# <QueryDict: {'jenis': ['GU'], 'organisasi': ['1.2.01.0001'], 'draftchk': ['00001/PSPJ/GU/1.2.01.0001/2022|']}>

		for i in range(0,len(arr)):
			obj = arr[i].split('|')

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.BKP_SKPD WHERE TAHUN=%s and KODEURUSAN=%s and"\
					" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOPSPJ=%s ",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]])
			hasil = ""

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC WHERE TAHUN=%s and KODEURUSAN=%s and"\
					" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOPSPJ=%s ",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]])
			hasil = ""

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC_SUB1 WHERE TAHUN=%s and KODEURUSAN=%s and"\
					" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOPSPJ=%s ",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]])
			hasil = "Data berhasil dihapus!"

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')


## ADD JOEL ======================================================================== 
def bkp_modal_potongan(request):
	tahun_x = tahun_log(request)

	# # JIKA REKUWES POST - KLIK TOMBOL SIMPAN ============================================================================
	if request.method == 'POST':
		data    = request.POST
		eskapde = data.get("eskapde")
		no_pspj  = data.get("no_pspj")
		tgl_pspj = tgl_short(data.get("tgl_pspj"))
		nobukti = data.get("nobukti")
		pesan_x = 'Data Berhasil Disimpan'

		if eskapde != '0' or eskapde != '':
			aidi = eskapde.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		pot_kdrek   = data.getlist('cut_kdrek')
		pot_jumlah  = data.getlist('jml_pot')
		pot_jenis   = data.getlist('jns_cut')
		pot_idbiling  = data.getlist('idbiling')
		pot_ntpn = data.getlist('ntpn')

		## HAPUS TABEL POTONGAN ============================================================================
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.bkp_skpd_potongan WHERE tahun = %s AND kodeurusan = %s \
				AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s AND nopspj = %s AND nobukti = %s",
				[tahun_x,aidi[0],aidi[1],aidi[2],aidi[3],no_pspj,nobukti])

		## INSERT TABEL POTONGAN ===========================================================================
		for p in range(len(pot_kdrek)):
			if pot_kdrek[p] != "" and nobukti != "":
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.bkp_skpd_potongan (tahun,\
						kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nopspj,\
						rekeningpotongan,jumlah,jenispotongan,tanggal,nobukti, idbiling,ntpn) \
						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun_x,aidi[0],aidi[1],aidi[2],aidi[3],no_pspj,pot_kdrek[p],toAngkaDec(pot_jumlah[p]),
						pot_jenis[p],tgl_pspj,nobukti, pot_idbiling[p],pot_ntpn[p]])

				pesan_x = 'Data Potongan Berhasil Disimpan'

		data = {'pesan_x':pesan_x}
		return JsonResponse(data)
	
	# # JIKA REKUWES GET - LOAD MODAL ============================================================================
	else:
		data    = request.GET
		hasil   = ''
		aidirow = data.get("i")
		nobukti = data.get("b").replace('^','/')
		eskapde = data.get("s")
		no_pspj  = data.get("n").replace('^','/')
		tgl_pspj = data.get("t").replace('_',' ')

		arrJns = arrJns_potongan

		if eskapde != '0' or eskapde != '':
			aidi = eskapde.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')  


		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over() as nomor, idbiling,ntpn, \
				rekeningpotongan, urai, jenispotongan, jumlah as jumlahpotongan,\
					(select kdrek from master.mpajak mp where mp.koderekening=a.rekeningpotongan) as kdrek \
				from penatausahaan.bkp_skpd_potongan a \
				left join master.master_rekening b on b.tahun=a.tahun and b.kodeakun||'.'||b.kodekelompok\
				||'.'||b.kodejenis||'.'||lpad(b.kodeobjek::text,2,'0')||'.'||lpad(b.koderincianobjek::text,2,'0')\
				||'.'||lpad(b.kodesubrincianobjek::text,3,'0') = a.rekeningpotongan \
				where a.tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s \
				and kodeunit = %s and nopspj = %s and nobukti = %s",
				[tahun_x,aidi[0],aidi[1],aidi[2],aidi[3],no_pspj,nobukti])
			hasil = ArrayFormater(dictfetchall(cursor))

		ArrDT = {'aidirow':aidirow, 'hasil':hasil, 'jnsPot':arrJns, 'nobukti':nobukti, 
			'eskapde':eskapde, 'no_pspj':no_pspj, 'tgl_pspj':tgl_pspj}
		return render(request,'spp/modal/bkp_potongan_lihat.html',ArrDT)


def bkp_modal_kwitansi(request):    
	# IF KLIK CETAK================================================================
	if request.method == 'POST':
		post    = request.POST
		lapParm = {}       
		
		organisasi  = post.get('skpd').split('.')
		no_pspj = post.get('no_pspj')
		
		if ',' in no_pspj:
			no_pspj_split = post.get('no_pspj').split(',')
			no_pspj = "','".join(no_pspj_split)
		else:
			no_pspj = post.get('no_pspj').split('|')[0]
		
		lapParm['file']     = 'penatausahaan/spjskpd/kwitansi.fr3'

		lapParm['NOSPJ']        = "'"+no_pspj+"'"

	 
		lapParm['tahun']            = "'"+tahun_log(request)+"'" 
		lapParm['report_type']      = 'pdf'
		lapParm['kodeurusan']       = organisasi[0]
		lapParm['kodesuburusan']    = organisasi[1]
		lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
		lapParm['kodeunit']         = "'"+organisasi[3]+"'"
		lapParm['id']               = "'"+post.get('id')+"'"
		lapParm['idpa']             = "'"+post.get('idpa')+"'" 
		lapParm['noKwitansi']       = "'"+post.get('bukti')+"'" 
		lapParm['kepada']           = "'"+post.get('kepada')+"'" 

		return HttpResponse(laplink(request, lapParm))

	# IF PERTAMA LOAD MODAL LAPORAN KWITANSI ======================================
	else:
		base = request.GET.get('base') 
		deskrip = base64.b64decode(base).decode('utf-8')
		explode = deskrip.split('|')
		nobukti = explode[0]
		tglbukti = explode[1]
		uraian = explode[2]
		gets = explode[3]
		no_pspj = explode[4]

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')  

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
				" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and jenissistem=%s order by id ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],2])
			pejabat = dictfetchall(cursor) 

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from penatausahaan.bkp_skpd_rinc_sub1 where tahun=%s"
				" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and nopspj=%s and nobukti=%s ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],no_pspj,nobukti])
			penerima = dictfetchall(cursor) 

		for arr in penerima:
			penerima = arr['kepada']
			tglkwitansi = tgl_indo(arr['tglbukti'])
			if penerima==None:
				penerima=''

		data = {        
			'pejabat' : pejabat,
			'nobukti': nobukti,
			'tglbukti' : tglbukti,
			'uraian':uraian,
			'penerima':penerima,
			'tglkwitansi':tglkwitansi,
			'aidi':gets,
			'no_pspj':no_pspj,
		}
		return render(request,'spp/modal/bkp_modal_kwitansi.html',data)

def bkp_rincian_delete(request, jenis):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('skpd').split('.')
		nopspj = request.POST.get('no_pspj')
		kodeunit = request.POST.get('unit')
		urai_rek = request.POST.get('rekening')
		kodesub1 = request.POST.get('id')
		rekening = urai_rek.split('-')
		objek = rekening[0].split('.')
		kodebidang = objek[0]+'.'+objek[1]
		kodeprogram = objek[3]
		kodekegiatan = objek[4]+'.'+objek[5]
		kodesubkegiatan = objek[6]
		objek2 = rekening[1].split('.')
		hasil = ''

		nobukti = request.POST.get('nobukti')
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.BKP_SKPD_RINC_SUB1 WHERE TAHUN=%s \
				AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s and kodeunit = %s AND NOpSPJ=%s \
				AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s \
				and kodesubkegiatan = %s and kodesubkeluaran=0 \
				AND KODEAKUN=%s AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s \
				AND KODERINCIANOBJEK=%s and kodesubrincianobjek =%s AND KODESUB1=%s ",
				[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],nopspj,
				kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,
				int(objek2[0]),int(objek2[1]),int(objek2[2]),int(objek2[3]),
				int(objek2[4]),int(objek2[5]),int(kodesub1)])
			hasil = "Data berhasil dihapus!"

		### HAPUS TABEL POTONGAN LPJ ------
		if hasil != '':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.bkp_skpd_potongan \
					where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s \
					and kodeunit=%s and nopspj=%s and nobukti=%s ",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],nopspj,nobukti])

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')


def bkp_kegiatan_update(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			no_pspj = request.POST.get('no_pspj')
			no_pspj_old = request.POST.get('no_pspj_old')
			tgl = tgl_short(request.POST.get('tgl_pspj'))
			keperluan = request.POST.get('uraian')          
			aksi = request.POST.get('aksi') 

			if no_pspj!='':               
				if aksi=='false':                   
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BKP_SKPD SET NOPSPJ=%s, KEPERLUAN=%s, TGLPSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') AND NOPSPJ=%s",
							[no_pspj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],no_pspj_old])
						hasil = ''              

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BKP_SKPD_RINC SET NOPSPJ=%s "
							"WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') "
							"AND NOPSPJ=%s ",
							[no_pspj,tahun_log(request),org[0],org[1],org[2],no_pspj_old])
						hasil = ''

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BKP_SKPD_RINC_SUB1 SET NOPSPJ=%s "
							"WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') "
							"AND NOPSPJ=%s ",
							[no_pspj,tahun_log(request),org[0],org[1],org[2],no_pspj_old])
						hasil = 'Data telah berhasil disimpan' 

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')


def bkp_kegiatan_delete(request):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('skpd').split('.')
		no_pspj_old = request.POST.get('no_pspj_old')
		arr = request.POST.getlist('kegiatan')      
		hasil = ''      

		for i in range(0,len(arr)):
			obj = arr[i].split('|') 
			
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("""DELETE FROM penatausahaan.BKP_SKPD_RINC WHERE TAHUN=%s and KODEURUSAN=%s 
					and KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOPSPJ=%s 
					AND KODEBIDANG||'.'||KODEORGANISASI||'.'||KODEPROGRAM||'.'||KODEKEGIATAN||'.'||kodesubkegiatan=%s 
					and kodesubkeluaran=0""",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[3],no_pspj_old,obj[0]])
			hasil = ""

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("""DELETE FROM penatausahaan.BKP_SKPD_RINC_SUB1 WHERE TAHUN=%s and KODEURUSAN=%s 
					and KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOPSPJ=%s 
					AND KODEBIDANG||'.'||KODEORGANISASI||'.'||KODEPROGRAM||'.'||KODEKEGIATAN||'.'||kodesubkegiatan=%s 
					and kodesubkeluaran=0 """,
					[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[3],no_pspj_old,obj[0]])
			hasil = "Data berhasil dihapus!"

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')

def bkp_laporan(request,jenis):

	if request.method == 'POST':
		post    = request.POST
		lapParm = {}

		organisasi  = post.get('org').split('.')
		nopspj = post.get('nopspj') 
		jenisctk = post.get('jenisctk')
		
		if ',' in nopspj:
			nopspj_split = post.get('nopspj').split(',')
			nopspj = "','".join(nopspj_split)
		else:
			nopspj = post.get('nopspj').split('|')[0]
		
		if jenisctk == '0':
			if jenis == 'GU':
				lapParm['file']     = 'penatausahaan/spjskpd/lpjup.fr3'
			else :
				lapParm['file']     = 'penatausahaan/spjskpd/lpjtu.fr3'
			lapParm['nolpj']        = "'"+nopspj+"'"

	 
		lapParm['tahun']            = "'"+tahun_log(request)+"'" 
		lapParm['report_type']      = 'pdf'
		lapParm['kodeurusan']       = organisasi[0]
		lapParm['kodesuburusan']    = organisasi[1]
		lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
		lapParm['kodeunit']         = "'"+organisasi[3]+"'"
		lapParm['id']               = "'"+post.get('id_mengajukan')+"'"
		lapParm['idpa']             = "'"+post.get('id_otorisasi')+"'" 

		return HttpResponse(laplink(request, lapParm))
	# ##===========================================================================================
	else:
		gets = str(request.GET.get('skpd'))
		jenisctk = request.GET.get('jnsct')
		nopspj = request.GET.get('nopspj')
		jenis = jenis.upper()        

		if gets != '0' or gets != '':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')  
	   
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
				" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and jenissistem=%s order by id ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],2])
			bendahara = dictfetchall(cursor)    

		data = {        
			'bendahara' : bendahara,                    
			'jenis' : jenis,
			'jenisctk' : jenisctk,
			'nopspj' : nopspj       
		}
		return render(request,'spp/modal/bkp_modal_laporan.html',data)