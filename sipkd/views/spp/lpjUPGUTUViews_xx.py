from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
import base64
from support.support_sipkd import ArrayFormater

def getnewnospj(request,jenis):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')		         

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT hasil FROM penatausahaan.fc_otomatis_lpj(%s,%s,%s,lpad(%s,2,'0'),%s)",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],jenis])
			no_lpj = dictfetchall(cursor)

		data = {}
		for arr in no_lpj:
			data = {'nospj':arr['hasil']}

		return JsonResponse(data)
	else:
		return redirect('sipkd:index')

def getnolpj(request):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')	
		jenis = request.POST.get('jenis')	         

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(*) as hasil FROM pertanggungjawaban.SKPD_PENGEMBALIAN WHERE tahun=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and jenissp2d=%s ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],jenis])
			no_lpj = dictfetchall(cursor)

		data = {}
		for arr in no_lpj:
			nomer = arr['hasil']+1
			nospj = f'{nomer:03}'+'/STS-'+jenis+'/'+gets+'/'+tahun_log(request)			
			data = {'nospj':nospj}

		return JsonResponse(data)
	else:
		return redirect('sipkd:index')

def loadlpjsts(request):
	org = request.GET.get('skpd').split('.')     

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT nosp2d,nolpj,keperluan,sisasp2d FROM penatausahaan.fc_skpd_view_lpj (%s,%s,%s,lpad(%s,2,'0')) "
			"WHERE jenis='TU' ",
			[tahun_log(request),org[0],org[1],org[2]])
		list_lpj = dictfetchall(cursor)

	data = {'list_lpj' : list_lpj}
	return render(request,'spp/modal/modal_lpj_sts.html',data)

def listkegiatanlpj(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nospj = request.POST.get('nospj')		
		kondisi = ''
		
		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		

		# rincian kegiatan
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select DISTINCT(sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan) as kegiatan, "
				"sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,sr.kodesubkegiatan,sr.nospj,sr.kodeorganisasi, sr.kodeunit,"
				"(select urai from master.master_organisasi morg WHERE morg.tahun = sr.tahun and morg.kodeurusan=sr.kodeurusan and morg.kodesuburusan=sr.kodesuburusan and"
				" morg.kodeorganisasi=sr.kodeorganisasi and morg.kodeunit=sr.kodeunit) as urai_skpd,"
				"(select urai from penatausahaan.kegiatan k where k.tahun=sr.tahun and k.kodeurusan=sr.kodeurusan and k.kodesuburusan=sr.kodesuburusan "
				"and k.kodeorganisasi=sr.kodeorganisasi and k.kodeunit=sr.kodeunit and k.kodebidang=sr.kodebidang and k.kodeprogram=sr.kodeprogram and k.kodekegiatan=sr.kodekegiatan and k.kodesubkegiatan=sr.kodesubkegiatan and k.kodesubkeluaran = 0) as uraikegiatan,"
				"(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) from penatausahaan.spj_skpd_rinc_sub1 sj where sj.tahun=sr.tahun and sj.kodeurusan=sr.kodeurusan and sj.kodesuburusan=sr.kodesuburusan "
				"and sj.kodeorganisasi=sr.kodeorganisasi and sj.kodeunit=sr.kodeunit and sj.nospj=sr.nospj and sj.kodebidang=sr.kodebidang and sj.kodeprogram=sr.kodeprogram "
				"and sj.kodekegiatan=sr.kodekegiatan and sj.kodesubkegiatan=sr.kodesubkegiatan) as jumlah from penatausahaan.spj_skpd_rinc sr join penatausahaan.spj_skpd s "
				"ON(sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospj=s.nospj) "
				"where sr.tahun=%s and sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=lpad(%s,2,'0') "
				"and s.jenis in ('UP','GU') and s.nospj =%s order BY sr.nospj,sr.kodeprogram,sr.kodekegiatan ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nospj])
			list_keg = dictfetchall(cursor)	

		for arr in list_keg:
			kondisi += ','+arr['kegiatan']

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) AS sp2dup,(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) as jumlah from penatausahaan.spj_skpd_rinc_sub1 where tahun=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and nospj=%s) FROM penatausahaan.SP2DRINCIAN WHERE TAHUN=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeakun=1 and kodekelompok=1 and kodejenis=1 and kodeobjek=3 and koderincianobjek=1",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nospj,tahun_log(request),aidi[0],aidi[1],aidi[2]]) 
			list_foot = dictfetchall(cursor)
		print(list_foot)
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
		return render(request, 'spp/tabel/tabel_kegiatan.html', data)

	else:
		return redirect('sipkd:index')

def getlistrinciansts(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		jenis = request.POST.get('jenis')
		nosts = request.POST.get('nosts')
		sp2d = request.POST.get('sp2d')
		kdrek = request.POST.get('kdrek')
		arr = request.POST.get('arr')		
		action = request.POST.get('action')
		# kodekegiatan = "'"+arr+"'"
		
		if action == 'true':
			sisasp2d = 'SISASP2D'
		else:
			sisasp2d = 'STS AS SISASP2D'

		if ',' in arr:
			keg_split = arr.split(',')
			kegiatan = "','".join(keg_split)
			kodekegiatan = "'"+kegiatan+"'"
		else:
			kodekegiatan = "'"+arr+"'"		

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		

		# rincian kegiatan
		if jenis == 'UP':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT DISTINCT kodeurusan||'.'||lpad(kodesuburusan::text,2,'0')||'.'||trim(kodeorganisasi)||'.0.0 - 3.4.1.01.01' as koderekening,'0,00' as sisasp2d,"
					"(select urai from master.master_rekening where tahun=%s and kodeakun=3 and kodekelompok=4 and kodejenis=1 and kodeobjek=1 and koderincianobjek=1),ROW_NUMBER () OVER () as nomor "
					"from penatausahaan.belanja where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') group by koderekening,sisasp2d,urai ",
					[tahun_log(request),tahun_log(request),aidi[0],aidi[1],aidi[2]])
				list_rincian = dictfetchall(cursor)
		elif jenis == 'GJ':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT KODEREKENING,URAI,jumlah as sisasp2d,ROW_NUMBER () OVER () as nomor FROM pertanggungjawaban.skpd_view_rincianpengembalian (%s,%s,%s,lpad(%s,2,'01'),'GJ',%s) "
					"WHERE isbold=0 ",
					[tahun_log(request),aidi[0],aidi[1],aidi[2],nosts])
				list_rincian = dictfetchall(cursor)
		elif jenis == 'LS':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT KODEREKENING,URAI,jumlah as sisasp2d,cek as PILIH,ROW_NUMBER () OVER () as nomor FROM pertanggungjawaban.skpd_view_rincianpengembalian (%s,%s,%s,lpad(%s,2,'01'),'LS',%s) "
					"WHERE isbold=1 and kodekegiatan1 in ("+kodekegiatan+") ",
					[tahun_log(request),aidi[0],aidi[1],aidi[2],nosts])
				list_rincian = dictfetchall(cursor)
		elif jenis == 'TU':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT KODEREKENING,URAIAN AS URAI,"+sisasp2d+",ROW_NUMBER () OVER () as nomor FROM penatausahaan.fc_view_lpj_tu_rinc (%s,%s,%s,lpad(%s,2,'01'),%s,%s)",
					[tahun_log(request),aidi[0],aidi[1],aidi[2],sp2d,''])
				list_rincian = dictfetchall(cursor)
		else:
			list_rincian = ''
		
		data = {'list_rincian' : list_rincian}
		return render(request, 'spp/tabel/tabel_rincian_sts.html', data)

	else:
		return redirect('sipkd:index')

def getlistrincianstsls(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		jenis = request.POST.get('jenis')
		nosts = request.POST.get('nosts')
		sp2d = request.POST.get('sp2d')
		kdrek = request.POST.get('kdrek')
		arr = request.POST.get('arr')
		action = request.POST.get('action')

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		

		# rincian kegiatan		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT KODEKEGIATAN1,URAI,jumlah as sisasp2d,cek as PILIH FROM pertanggungjawaban.skpd_view_rincianpengembalian (%s,%s,%s,lpad(%s,2,'01'),'LS',%s) "
				"WHERE isbold=0 ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nosts])
			list_kegiatan = dictfetchall(cursor)		
		
		data = {'list_kegiatan' : list_kegiatan}
		return render(request, 'spp/tabel/tabel_rincian_sts_ls.html', data)

	else:
		return redirect('sipkd:index')


def addkegiatanlpj(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nospj = request.POST.get('nospj')	

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		

		if hakakses_sipkd(request) in ['BPP']:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT kegiatan FROM penatausahaan.pengguna WHERE tahun = %s and UNAME = %s and hakakses = %s",[tahun_log(request), username(request), 
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
				"(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sp2dsisa "
				"from penatausahaan.fc_view_kegiatan_lpj (%s,%s,%s,lpad(%s,2,'0')) "+clause_in+"",
				[tahun_log(request),aidi[0],aidi[1],aidi[2]])
			add_kegiatan = dictfetchall(cursor)	    

		data = {'add_kegiatan' : add_kegiatan}
		return render(request, 'spp/tabel/tabel_tambah_kegiatan.html', data)

	else:
		return redirect('sipkd:index')

def simpankegiatanlpj(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			nospj = request.POST.get('no_lpj')
			tgl = tgl_short(request.POST.get('tgl_lpj'))
			keperluan = request.POST.get('uraian')
			nosp2d = request.POST.get('edNoSP2D')
			rincian = request.POST.getlist('daftarkegiatan')
			aksi = request.POST.get('aksi')	
			
			if nospj!='':				
				if aksi=='true':
					pass
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SPJ_SKPD SET nospj=%s, KEPERLUAN=%s, TGLSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') AND KODEUNIT = %s AND NOSPJ=%s",
							[nospj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],org[3],nospj])
						hasil = ''

				for i in range(0,len(rincian)):
					obj = rincian[i].split('|')
					obj1 = obj[1].split('.') #koderekening
					kodebidang = obj1[0]+'.'+obj1[1]
					kodeprogram = obj1[3]
					kodekegiatan = obj1[4]+'.'+obj1[5]
					kodesubkegiatan = obj1[6]

					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("INSERT INTO penatausahaan.SPJ_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit"
								",NOSPJ,TGLSPJ,KEPERLUAN,STATUS,USERNAME,JENIS,NOSP2D) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
								[tahun_log(request),org[0],org[1],org[2],obj[7],nospj,tgl,keperluan,'0',username(request),'GU',nosp2d])
							hasil = ''
					except Exception as e:
						print('Duplikasi Primary Key', e)
						pass

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND KODEUNIT=%s AND NOSPJ=%s "
							"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s AND KODESUBKEGIATAN = %s AND KODESUBKELUARAN = 0 AND KODEAKUN=%s "
							"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s",
							[tahun_log(request),org[0],org[1],org[2],obj[7],nospj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,0,0,0,0,0])
						hasil = ''

					try:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("INSERT INTO penatausahaan.SPJ_SKPD_RINC (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPJ,"
								"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
								"KODERINCIANOBJEK,kodesubrincianobjek) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
								[tahun_log(request),org[0],org[1],org[2],obj[7],nospj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,0,0,0,0,0,0])
							hasil = ''
					except Exception as e:
						print('Duplikasi Primary Key 2',e)
						pass

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')

def listrekeninglpj(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nospj = request.POST.get('nolpj')
		arr = request.POST.get('arr')			
		kegiatan = arr.split('|')		
		objek = kegiatan[0].split('.')
		kodebidang = objek[0]+'.'+objek[1]
		kodeprogram = objek[3]
		kodekegiatan = objek[4]+'.'+objek[5]
		kodesubkegiatan = objek[6]
		urai_kegiatan = kegiatan[0]+'-'+kegiatan[2]

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select kodeunit,koderekening,anggaran,uraian ,sekarang as jumlahspj,lalu,jumlah as totalspj,sisa as sisapagu "
				"from penatausahaan.fc_rekening_spj_skpd (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],kegiatan[3],kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,nospj])
			list_rekening = dictfetchall(cursor)	    

		data = {'list_rekening' : list_rekening,'urai_kegiatan':urai_kegiatan}
		return render(request, 'spp/tabel/tabel_rekening.html', data)

	else:
		return redirect('sipkd:index')

def getdatalpjtu(request):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')	
		nospj = request.POST.get('nospj')		         

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select NOSP2D,NOSPJ,KEPERLUAN,TGLSPJ FROM penatausahaan.SPJ_SKPD "
				"WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') "
				"and nospj=%s",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nospj])
			data_lpj = dictfetchall(cursor)

		data = {}
		for arr in data_lpj:
			data = {'nosp2d':arr['nosp2d'],'nospj':arr['nospj'],'keperluan':arr['keperluan'],
				'tglspj':tgl_indo(arr['tglspj'])}

		return JsonResponse(data)
	else:
		return redirect('sipkd:index')

def listrekeninglpjtu(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		sp2d = request.POST.get('sp2d')	
		nolpj = request.POST.get('nolpj')

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		

		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select s.koderekening,s.uraian,"
				"(CASE WHEN s.jumlahsp2d is NULL THEN 0.00 ELSE s.jumlahsp2d END) as jumlahsp2d,"
				"(CASE WHEN s.jumlahspj is NULL THEN 0.00 ELSE s.jumlahspj END) as jumlahspj,"
				"(CASE WHEN s.jumlahsetor is NULL THEN 0.00 ELSE s.jumlahsetor END) as jumlahsetor,"
				"(CASE WHEN s.sisasp2d is NULL THEN 0.00 ELSE s.sisasp2d END) as sisasp2d,s.isbold,s.kodebidang,s.kodeprogram,s.kodekegiatan, "
				"(select urai from apbd.angg_kegiatan k where k.tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s "
				"and k.kodebidang=s.kodebidang and k.kodeprogram=s.kodeprogram and  k.kodekegiatan=s.kodekegiatan ) as uraikegiatan,0 as pilih "
				"from penatausahaan.fc_view_kegiatan_lpj_tu (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s) s ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],tahun_log(request),aidi[0],aidi[1],aidi[2],'SPJ',sp2d,nolpj])
			list_rekening = dictfetchall(cursor)	    

		data = {'list_rekening' : list_rekening}
		return render(request, 'spp/tabel/tabel_rekening_tu.html', data)

	else:
		return redirect('sipkd:index')

def deletelpj(request):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('organisasi').split('.')
		arr = request.POST.getlist('draftchk')
		jenis = request.POST.get('jenis')		
		hasil = ''

		for i in range(0,len(arr)):
			obj = arr[i].split('|')
			
			if jenis == 'PENGEMBALIAN':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM pertanggungjawaban.SKPD_PENGEMBALIAN WHERE TAHUN=%s and KODEURUSAN=%s and"\
						" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and NOSTS=%s ",
						[tahun_log(request),skpd[0],skpd[1],skpd[2],obj])
				hasil = ""

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM pertanggungjawaban.SKPD_RINCIAN_PENGEMBALIAN WHERE TAHUN=%s and KODEURUSAN=%s and"\
						" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and NOSTS=%s ",
						[tahun_log(request),skpd[0],skpd[1],skpd[2],obj])
				hasil = "Data berhasil dihapus!"
			else:
				
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD WHERE TAHUN=%s and KODEURUSAN=%s and"\
						" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOSPJ=%s ",
						[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[1],obj[0]])
				hasil = ""

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC WHERE TAHUN=%s and KODEURUSAN=%s and"\
						" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOSPJ=%s ",
						[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[1],obj[0]])
				hasil = ""

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC_SUB1 WHERE TAHUN=%s and KODEURUSAN=%s and"\
						" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOSPJ=%s ",
						[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[1],obj[0]])
				hasil = "Data berhasil dihapus!"

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')

def deletekegiatanlpj(request):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('skpd').split('.')
		nolpj = request.POST.get('x_nolpj')
		arr = request.POST.getlist('kegiatan')		
		hasil = ''		

		for i in range(0,len(arr)):
			obj = arr[i].split('|')	
			
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC WHERE TAHUN=%s and KODEURUSAN=%s and"\
					" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOSPJ=%s "\
					"AND KODEBIDANG||'.'||KODEORGANISASI||'.'||KODEPROGRAM||'.'||KODEKEGIATAN||'.'||kodesubkegiatan=%s and kodesubkeluaran=0",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[3],nolpj,obj[0]])
			hasil = ""

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC_SUB1 WHERE TAHUN=%s and KODEURUSAN=%s and"\
					" KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s and NOSPJ=%s "\
					"AND KODEBIDANG||'.'||KODEORGANISASI||'.'||KODEPROGRAM||'.'||KODEKEGIATAN||'.'||kodesubkegiatan=%s and kodesubkeluaran=0 ",
					[tahun_log(request),skpd[0],skpd[1],skpd[2],obj[3],nolpj,obj[0]])
			hasil = "Data berhasil dihapus!"

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')

def listlpjupgu(request,jenis):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd')         
		nolpj = request.POST.get('nolpj')
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

		if jenis == 'GU':
			pagu = kegiatan[2]
			total = kegiatan[5]
			sisa = kegiatan[6]
		else:
			pagu = kegiatan[2]
			total = kegiatan[3]
			sisa = kegiatan[5]

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')		
		
		# rincian kegiatan
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select sr.kodeunit, sr.kodesub1 as pilih,sr.uraian,sr.tglbukti,sr.jumlah as spjsekarang,sr.nobukti "
				"from penatausahaan.spj_skpd_rinc_sub1 sr where sr.tahun=%s and sr.kodeurusan=%s and sr.kodesuburusan=%s "
				"and sr.kodeorganisasi=%s and sr.kodeunit=%s and sr.kodebidang=%s and sr.kodeprogram=%s and sr.kodekegiatan=%s and sr.kodesubkegiatan=%s and sr.kodesubkeluaran=0"
				"and sr.kodeakun=%s and sr.kodekelompok=%s and sr.kodejenis=%s and sr.kodeobjek=%s and sr.koderincianobjek=%s and sr.kodesubrincianobjek=%s"
				"and sr.nospj=%s ",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],kegiatan[7],kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,objek3[0],
				objek3[1],objek3[2],objek3[3],objek3[4],objek3[5],nolpj])
			list_rincian = dictfetchall(cursor)	

		objek = []
		for arr in list_rincian:					
			objek.append({'kodeunit':arr['kodeunit'],'pilih':arr['pilih'],'uraian':arr['uraian'],'tglbukti':tgl_indo(arr['tglbukti']),
				'spjsekarang':arr['spjsekarang'],'nobukti':arr['nobukti'],'idInp':(int(arr['pilih'])+1)})

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) AS sp2dup,(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) as jumlah from penatausahaan.spj_skpd_rinc_sub1 where tahun=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and nospj=%s) FROM penatausahaan.SP2DRINCIAN WHERE TAHUN=%s "
				"and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeakun=1 and kodekelompok=1 and kodejenis=1 and kodeobjek=3 and koderincianobjek=1",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nolpj,tahun_log(request),aidi[0],aidi[1],aidi[2]]) 
			list_foot = dictfetchall(cursor)
		print('nolpj', nolpj)
		for ar in list_foot:
			sp2dup = ar['sp2dup']
			jumlahlpj = ar['jumlah']
			sisaup = ar['sp2dup']-ar['jumlah']

		if hakakses_sipkd(request) in ['BPP']:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT pengeluaran FROM pertanggungjawaban.skpd_bku WHERE tahun = %s and UNAME_BANTU = %s and kodeurusan = %s \
					and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s",
					[tahun_log(request), username(request), aidi[0],aidi[1],aidi[2],aidi[3]])
				up_bpp = cursor.fetchone()
			sp2dup = up_bpp[0]
			sisaup = sp2dup-jumlahlpj

		data = {'list_rincian' : objek,
			'urai_kegiatan':urai_kegiatan,
			'urai_rekening':urai_rekening,
			'pagu':pagu,
			'total':total,
			'sisa':sisa,
			'sisaup':sisaup,
			}
		
		return render(request, 'spp/tabel/tabel_rincianlpj.html', data)

	else:
		return redirect('sipkd:index')

def cek_no_spd(request):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')
		nospj = request.POST.get('nospj','|').split('|')    
		
		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')   

		# ambil spj
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select NOSP2D,NOSPJ,KEPERLUAN,TGLSPJ FROM penatausahaan.SPJ_SKPD where tahun=%s"
				" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit = %s and nospj=%s",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nospj[1],nospj[0]])
			list_spj = dictfetchall(cursor)

		data = {}
		for arr in list_spj:  
		    data = {'nosp2d':arr['nosp2d'], 'nospj':arr['nospj'],'keperluan':arr['keperluan'],'tglspj':tgl_indo(arr['tglspj'])}

	return JsonResponse(data)

def simpanlpjrincian(request,jenis):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			nospj = request.POST.get('no_lpj')
			tgl = tgl_short(request.POST.get('tgl_lpj'))
			keperluan = request.POST.get('uraian')
			nosp2d = request.POST.get('edNoSP2D')
			nomer = request.POST.getlist('nomer')
			no_bukti = request.POST.getlist('no_bukti')
			tgl_bukti = request.POST.getlist('tgl_bukti')
			uraian = request.POST.getlist('urai_belanja')
			pengeluaran = request.POST.getlist('pengeluaran')
			aksi = request.POST.get('aksi')	
			urai_rek = request.POST.get('urai_rekening')
			rekening = urai_rek.split('-')
			objek = rekening[0].split('.')
			kodebidang = objek[0]+'.'+objek[1]
			kodeprogram = objek[3]
			kodekegiatan = objek[4]+'.'+objek[5]
			kodesubkegiatan = objek[6]
			objek2 = rekening[1].split('.')
			kodeunit = request.POST.get('kegiatan').split('|')[3]
			
			# if jenis=='GU':
			# 	kodeakun = 0
			# 	kodekelompok = 0
			# 	kodejenis = 0
			# 	kodeobjek = 0
			# 	koderincianobjek = 0
			# else:
			kodeakun = objek2[0]
			kodekelompok = objek2[1]
			kodejenis = objek2[2]
			kodeobjek = objek2[3]
			koderincianobjek = objek2[4]
			kodesubrincianobjek = objek2[5]
					
			if nospj!='':
				if aksi=='true':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO penatausahaan.SPJ_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit"
							",NOSPJ,TGLSPJ,KEPERLUAN,STATUS,USERNAME,JENIS,NOSP2D) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nospj,tgl,keperluan,'0',username(request),jenis,nosp2d])
						hasil = ''
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SPJ_SKPD SET nospj=%s, KEPERLUAN=%s, TGLSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') and kodeunit = %s AND NOSPJ=%s",
							[nospj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],kodeunit,nospj])
						hasil = ''

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC WHERE TAHUN=%s "
						"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND kodeunit = %s AND NOSPJ=%s "
						"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s AND kodesubkegiatan = %s and kodesubkeluaran = 0 AND KODEAKUN=%s "
						"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s",
						[tahun_log(request),org[0],org[1],org[2],kodeunit,nospj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek, kodesubrincianobjek])
					hasil = ''

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.SPJ_SKPD_RINC (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPJ,"
						"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan,kodesubkeluaran,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
						"KODERINCIANOBJEK,kodesubrincianobjek) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
						[tahun_log(request),org[0],org[1],org[2],kodeunit,nospj,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,0,kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek])
					hasil = ''

				for i in range(0,len(nomer)):
					kodesub1 = nomer[i]	
					tglbukti = tgl_short(tgl_bukti[i])			
					# jumlah = toAngkaDec(pengeluaran[i])
					jumlah = pengeluaran[i].replace(',','')
					nobukti	= no_bukti[i]
					urai = uraian[i]

					with connections[tahun_log(request)].cursor() as cursor:						
						cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC_SUB1 WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s and kodeunit = %s AND NOSPJ=%s "
							"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s and kodesubkegiatan = %s and kodesubkeluaran = 0 AND KODEAKUN=%s "
							"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek = %s AND KODESUB1=%s ",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nospj,kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,
							int(kodeakun),int(kodekelompok),int(kodejenis),int(kodeobjek),int(koderincianobjek),kodesubrincianobjek,int(kodesub1)])
						hasil = ''

					with connections[tahun_log(request)].cursor() as cursor:	
						cursor.execute("INSERT INTO penatausahaan.SPJ_SKPD_RINC_SUB1 (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPJ,"
							"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan,kodesubkeluaran,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
							"KODERINCIANOBJEK,kodesubrincianobjek,KODESUB1,JUMLAH,NOBUKTI,TGLBUKTI,URAIAN) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun_log(request),org[0],org[1],org[2],kodeunit,nospj,kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,0,
							int(kodeakun),int(kodekelompok),int(kodejenis),int(kodeobjek),int(koderincianobjek),kodesubrincianobjek,int(kodesub1),jumlah,nobukti,
							tglbukti,urai])					
						hasil = 'Data telah berhasil disimpan' 

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')

def deleterincianlpj(request):
	if 'sipkd_username' in request.session:
		skpd = request.POST.get('skpd').split('.')
		nospj = request.POST.get('nolpj')
		kodeunit = request.POST.get('unit')
		urai_rek = request.POST.get('rekening')
		kodesub1 = request.POST.get('id')
		rekening = urai_rek.split('-')
		objek = rekening[0].split('.')
		kodebidang = objek[0]+'.'+objek[1]
		kodeprogram = objek[3]
		kodekegiatan = objek[4]+'.'+objek[5]
		kodesubkegiatan = objek[5]
		objek2 = rekening[1].split('.')
		hasil = ''
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.SPJ_SKPD_RINC_SUB1 WHERE TAHUN=%s "
				"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s and kodeunit = %s AND NOSPJ=%s "
				"AND KODEBIDANG=%s AND KODEPROGRAM =%s AND KODEKEGIATAN=%s and kodesubkegiatan = %s and kodesubkeluaran=0 AND KODEAKUN=%s "
				"AND KODEKELOMPOK=%s AND KODEJENIS=%s AND KODEOBJEK=%s AND KODERINCIANOBJEK=%s and kodesubrincianobjek =%s AND KODESUB1=%s ",
				[tahun_log(request),skpd[0],skpd[1],skpd[2],kodeunit,nospj,kodebidang,int(kodeprogram),kodekegiatan,kodesubkegiatan,
				int(objek2[0]),int(objek2[1]),int(objek2[2]),int(objek2[3]),int(objek2[4]),objek2[5],int(kodesub1)])
			hasil = "Data berhasil dihapus!"

		return HttpResponse(hasil)
	else:
		return redirect('sipkd:index')

def updatelpjtu(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			nospj = request.POST.get('x_nolpj')
			nolpj = request.POST.get('no_lpj')
			tgl = tgl_short(request.POST.get('tgl_lpj'))
			keperluan = request.POST.get('uraian')			
			aksi = request.POST.get('aksi')	

			if nospj!='':				
				if aksi=='false':					
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SPJ_SKPD SET nospj=%s, KEPERLUAN=%s, TGLSPJ=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') AND NOSPJ=%s",
							[nolpj,keperluan,tgl,tahun_log(request),org[0],org[1],org[2],nospj])
						hasil = ''				

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SPJ_SKPD_RINC SET NOSPJ=%s "
							"WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') "
							"AND NOSPJ=%s ",
							[nolpj,tahun_log(request),org[0],org[1],org[2],nospj])
						hasil = ''

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SPJ_SKPD_RINC_SUB1 SET NOSPJ=%s "
							"WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN=%s and KODEORGANISASI=lpad(%s,2,'0') "
							"AND NOSPJ=%s ",
							[nolpj,tahun_log(request),org[0],org[1],org[2],nospj])
						hasil = 'Data telah berhasil disimpan' 

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')

def getdatapengembalian(request):
	if 'sipkd_username' in request.session:
		gets = request.POST.get('skpd')	
		nosts = request.POST.get('nosts')		         

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select nosts,uraian,tglsts,nolpj,nosp2d,rekeningbank,jenissp2d FROM pertanggungjawaban.skpd_pengembalian "
				"WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') "
				"and nosts=%s",
				[tahun_log(request),aidi[0],aidi[1],aidi[2],nosts])
			data_lpj = dictfetchall(cursor)

		data = {}
		for arr in data_lpj:
			data = {'nosts':arr['nosts'],'uraian':arr['uraian'],'nolpj':arr['nolpj'],
				'nosp2d':arr['nosp2d'],'rekening':arr['rekeningbank'],'jenis':arr['jenissp2d'],
				'tglsts':tgl_indo(arr['tglsts'])}

		return JsonResponse(data)
	else:
		return redirect('sipkd:index')

def simpanpengembaliansts(request):
	hasil = ''
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			org = request.POST.get('skpd').split('.')
			nosts = request.POST.get('no_sts')
			tgl = tgl_short(request.POST.get('tgl_sts'))
			keperluan = request.POST.get('uraian')
			nosp2d = request.POST.get('no_sp2d')
			jenissp2d = request.POST.get('myRadios')
			no_lpj = request.POST.get('no_lpj')
			rekening_bank = request.POST.get('rek_bank').split('|')	
			rekeningbank = rekening_bank[3]
			aksi = request.POST.get('aksi')	
			urai_rek = request.POST.getlist('urai_rekening')

			if nosts!='':
				if aksi=='true':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO pertanggungjawaban.SKPD_PENGEMBALIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI"
							",NOSTS,TGLSTS,URAIAN,NOSP2D,JENISSP2D,UNAME,NOLPJ,REKENINGBANK) VALUES(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
							[tahun_log(request),org[0],org[1],org[2],nosts,tgl,keperluan,nosp2d,jenissp2d,username(request),no_lpj,str(rekeningbank)])
						hasil = ''
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE pertanggungjawaban.SKPD_PENGEMBALIAN SET TGLSTS=%s, JENISSP2D=%s, REKENINGBANK=%s, URAIAN=%s WHERE TAHUN=%s "
							"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0') AND nosts=%s",
							[tgl,jenissp2d,str(rekeningbank),keperluan,tahun_log(request),org[0],org[1],org[2],nosts])
						hasil = ''

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM pertanggungjawaban.skpd_rincian_pengembalian WHERE TAHUN=%s "
						"AND KODEURUSAN=%s AND KODESUBURUSAN=%s AND KODEORGANISASI=%s AND nosts=%s ",
						[tahun_log(request),org[0],org[1],org[2],nosts])
					hasil = ''

				for i in range(0,len(urai_rek)):									
					rekening = urai_rek[i].split('|')

					if rekening[1] != '0,00':
						koderekening = rekening[0].split('-')					
						objek = koderekening[0].split('.')						
						kodebidang = objek[0]+'.'+objek[1]
						kodeprogram = objek[3]
						kodekegiatan = objek[4]
						objek2 = koderekening[1].split('.')	
						jumlah = toAngkaDec(rekening[1])															

						with connections[tahun_log(request)].cursor() as cursor:	
							cursor.execute("INSERT INTO pertanggungjawaban.SKPD_RINCIAN_PENGEMBALIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSTS,"
								"KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
								"KODERINCIANOBJEK,JUMLAH) VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun_log(request),org[0],org[1],org[2],nosts,kodebidang,int(kodeprogram),int(kodekegiatan),
								objek2[0],objek2[1],objek2[2],int(objek2[3]),int(objek2[4]),jumlah])					
							hasil = 'Data telah berhasil disimpan' 

		return HttpResponse(hasil)

	else:
		return redirect('sipkd:index')

def loadlaporanlpj(request,jenis):
    gets = str(request.GET.get('skpd'))
    jenisctk = request.GET.get('jnsct')
    nolpj = request.GET.get('nolpj')
    jenis = jenis.upper()        

    if gets != '0':
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
        'nolpj' : nolpj       
    }
    return render(request,'spp/modal/modal_laporan_lpj.html',data)

def loadmodalsp2d(request):
	gets = str(request.GET.get('skpd'))    
    
	if gets != '0':
		aidi = gets.split('.')
	else:
		skpd = '0.0.0.0'
		aidi = skpd.split('.')  
   
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT nosp2d,tanggal,jenissp2d,informasi,(CASE WHEN jumlahsp2d is NULL THEN 0.00 ELSE jumlahsp2d END) as jumlahsp2d FROM PENATAUSAHAAN.SP2D WHERE tahun=%s"
			" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') AND TGLKASDA IS NOT NULL AND JENISSP2D='TU' AND LOCKED='Y' "
			" AND NOSP2D NOT IN (SELECT NOSP2D FROM PENATAUSAHAAN.SPJ_SKPD WHERE TAHUN =%s AND KODEURUSAN =%s AND KODESUBURUSAN=%s AND KODEORGANISASI=lpad(%s,2,'0')) ORDER BY NOSP2D",
			[tahun_log(request),aidi[0],aidi[1],aidi[2],tahun_log(request),aidi[0],aidi[1],aidi[2]])
		list_sp2d = dictfetchall(cursor)

	objek = []
	for arr in list_sp2d:		
		objek.append({'nosp2d':arr['nosp2d'],'jenissp2d':arr['jenissp2d'],'informasi':arr['informasi'],
			'tanggal':tgl_indo(arr['tanggal']),'jumlahsp2d':arr['jumlahsp2d']}) 

	data = {'list_sp2d' : objek} 

	return render(request,'spp/modal/modal_load_sp2d.html',data)

def getkwitansi(request):	 
	base = request.GET.get('base') 
	deskrip = base64.b64decode(base).decode('utf-8')
	explode = deskrip.split('|')
	nobukti = explode[0]
	tglbukti = explode[1]
	uraian = explode[2]
	gets = explode[3]
	nolpj = explode[4]

	if gets != '0':
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
		cursor.execute("select * from penatausahaan.spj_skpd_rinc_sub1 where tahun=%s"
			" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and nospj=%s and nobukti=%s ",
			[tahun_log(request),aidi[0],aidi[1],aidi[2],nolpj,nobukti])
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
		'tglkwitansi':tglkwitansi
	}
	return render(request,'spp/modal/modal_kwitansi.html',data)

def cetaklaporanlpj(request,jenis):
    post    = request.POST
    lapParm = {}    
    jenis = jenis.upper()       
    
    organisasi  = post.get('org').split('.')
    nolpj = post.get('nolpj') 
    jenisctk = post.get('jenisctk')
    
    if ',' in nolpj:
    	nolpj_split = post.get('nolpj').split(',')
    	nolpj = "','".join(nolpj_split)
    else:
    	nolpj = post.get('nolpj').split('|')[0]
    
    if jenisctk == '0':
    	if jenis == 'GU':
    		lapParm['file']		= 'penatausahaan/spjskpd/lpjup.fr3'
    	else :
    		lapParm['file']     = 'penatausahaan/spjskpd/lpjtu.fr3'

    	lapParm['nolpj']		= "'"+nolpj+"'"
    else:
    	lapParm['file']         = 'penatausahaan/spjskpd/stspengembalian.fr3'
    	lapParm['nosts'] 		= "'"+nolpj+"'"

 
    lapParm['tahun']            = "'"+tahun_log(request)+"'" 
    lapParm['report_type']      = 'pdf'
    lapParm['kodeurusan']       = organisasi[0]
    lapParm['kodesuburusan']    = organisasi[1]
    lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
    lapParm['kodeunit']   		= "'"+organisasi[3]+"'"
    lapParm['id']           	= "'"+post.get('id_mengajukan')+"'"
    lapParm['idpa']         	= "'"+post.get('id_otorisasi')+"'" 

    return HttpResponse(laplink(request, lapParm))