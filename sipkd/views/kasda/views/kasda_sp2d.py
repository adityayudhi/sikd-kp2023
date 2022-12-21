from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
from django.views.decorators.http import require_http_methods

def index(request):
	sumberdana = ''
	request.session['nobukukas_{}'.format(encrypt(username(request)))] = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT urut,kodesumberdana,urai,rekening||' ('||namarekening||' )' as rekening,\
			rekening as norekeningbank \
			FROM kasda.KASDA_SUMBERDANAREKENING WHERE KODESUMBERDANA <> 99 ORDER BY KODESUMBERDANA")
		sumberdana = dictfetchall(cursor)

	data = { 'sumberdana':sumberdana, }
	return render(request, 'kasda/kasda_sp2d.html', data)

def list_transaksi_sp2dViews(request):
	data = { 'formasal':'SP2D' }
	return render(request, 'kasda/modal/mdl_list_transaksi_sp2d.html', data)

def list_transaksi_sp2d_srvsideViews(request):
	tahun_x = tahun_log(request)
	arrRinc = []

	# JIKA KOLOM PENCARIAN DIISI =======
	if request.GET.get('search[value]') != '':
		keyword = request.GET.get('search[value]')
		arg = f"where lower(nobukukas||tanggal||nobukti||skpd||deskripsi) like '%%{keyword.lower()}%%'"
	else:
		arg = ''

	# GET JUMLAH DATA =======
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(nobukti) FROM kasda.fc_kasda_transaksi(%s, %s) "+arg,
		[tahun_log(request), 'SP2D'])
		hasil_row = cursor.fetchone()[0]

	# GET DATA ============================================
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit as organisasi,\
			nobukukas,tanggal,nobukti,skpd,deskripsi,pengeluaran,kodesumberdana,jenissp2d,tglbukti \
			FROM kasda.fc_kasda_transaksi(%s, %s) "+arg+" ORDER BY nobukukas DESC LIMIT %s OFFSET %s",
			[tahun_log(request), 'SP2D', request.GET.get('length'), request.GET.get('start')])
		hasil = ArrayFormater(dictfetchall(cursor))

	for xs in hasil:
		arrRinc.append((xs['nobukukas'],xs['tanggal'],xs['nobukti'],xs['skpd'],xs['deskripsi'],
			0 if xs['pengeluaran'] is None else xs['pengeluaran'],str(xs['organisasi']),
			xs['kodesumberdana'],xs['jenissp2d'].upper(),xs['tglbukti']))

	data_query = [list(i) for i in arrRinc]

	data = {
		"recordsTotal": hasil_row,
	 	"recordsFiltered": hasil_row,
	 	"data": data_query
	}
	return JsonResponse(data)

def list_kasda_sp2dViews(request):
	data = {'formasal':'SP2D'}
	return render(request, 'kasda/modal/mdl_list_sp2d.html', data)

def list_kasda_sp2d_srvsideViews(request):
	tahun_x = tahun_log(request)
	arrRinc = []

	# JIKA KOLOM PENCARIAN DIISI =======
	if request.GET.get('search[value]') != '':
		keyword = request.GET.get('search[value]')
		arg0 = f"and lower(s.nosp2d||s.tanggal||s.statuskeperluan||s.jenissp2d||s.informasi||\
			s.norekbankasal||s.kodeurusan||s.kodesuburusan||s.kodeorganisasi||s.kodeunit||\
			(select urai from master.master_organisasi where tahun=s.tahun and kodeurusan=s.kodeurusan \
			and kodesuburusan=s.kodesuburusan and kodeorganisasi=s.kodeorganisasi and kodeunit=s.kodeunit)) \
			like '%%{keyword.lower()}%%'"

		arg1 = f"and lower(s.nosp2d||s.tanggal||mo.urai||s.statuskeperluan||s.jenissp2d||s.informasi||s.norekbankasal||\
			s.kodeurusan||s.kodesuburusan||s.kodeorganisasi||s.kodeunit) like '%%{keyword.lower()}%%'"
	else:
		arg0 = arg1 = ''

	# GET JUMLAH DATA =======
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(tahun) FROM penatausahaan.sp2d s where s.tahun=%s and s.locked='Y' \
		and s.tglkasda is null and s.jenissp2d not in ('GU_NIHIL','TU_NIHIL') "+arg0,
		[tahun_log(request)])
		hasil_row = cursor.fetchone()[0]

	# GET DATA =======================
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT s.nosp2d,s.tanggal,mo.urai as skpd,s.statuskeperluan,\
		(select sum(jumlah) from penatausahaan.sp2drincian where tahun=s.tahun and kodeurusan=s.kodeurusan \
		and kodesuburusan=s.kodesuburusan and kodeorganisasi=s.kodeorganisasi and nosp2d=s.nosp2d) as jumlah,\
		s.jenissp2d,s.informasi,s.norekbankasal,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit\
		from penatausahaan.sp2d s left join master.master_organisasi mo on mo.tahun=s.tahun and mo.kodeurusan=s.kodeurusan\
		and mo.kodesuburusan=s.kodesuburusan and mo.kodeorganisasi=s.kodeorganisasi and mo.kodeunit=s.kodeunit\
		where s.tahun=%s and s.locked='Y' and s.tglkasda is null \
		and s.jenissp2d not in ('GU_NIHIL','TU_NIHIL') \
		"+arg1+" ORDER BY s.tanggal,s.nosp2d DESC LIMIT %s OFFSET %s", 
		[tahun_log(request), request.GET.get('length'), request.GET.get('start')])
		hasil = ArrayFormater(dictfetchall(cursor))

	for xs in hasil:
		arrRinc.append((xs['nosp2d'],xs['tanggal'],xs['skpd'],xs['statuskeperluan'],
			0 if xs['jumlah'] is None else xs['jumlah'],
			str(xs['kodeurusan'])+"."+str(xs['kodesuburusan'])+"."+str(xs['kodeorganisasi'])+"."+str(xs['kodeunit']),
			xs['jenissp2d'].upper(),xs['norekbankasal']))

	data_query = [list(i) for i in arrRinc]

	data = {
		"recordsTotal": hasil_row,
	 	"recordsFiltered": hasil_row,
	 	"data": data_query
	}
	return JsonResponse(data)

def render_afektasi_sp2dViews(request):
	kodeskpd = request.POST.get('skpd')
	kodeurusan = kodeskpd.split('.')[0]
	kodesuburusan = kodeskpd.split('.')[1]
	kodeorganisasi = kodeskpd.split('.')[2]
	kodeunit = kodeskpd.split('.')[3]
	nomor = request.POST.get('nomor')
	jenis = request.POST.get('jenis')
	
	some_variabel = ''
	
	with connections[tahun_log(request)].cursor() as cursor:
		if jenis == 'sp2d':
			request.session['nobukukas_{}'.format(encrypt(username(request)))] = ''
			cursor.execute("SELECT koderekening, urai, penerimaan, pengeluaran FROM kasda.fc_kasda_afektasi_sp2d(%s, %s, %s, %s, %s, %s)", [tahun_log(request),
				kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, nomor])
		else:
			request.session['nobukukas_{}'.format(encrypt(username(request)))] = nomor
			cursor.execute(""" 
				SELECT d.kodebidang||'.'||d.kodeorganisasi||'.'||d.kodeprogram||'.'||d.kodekegiatan||'.'||d.kodesubkegiatan
				||'-'||d.kodeakun||'.'||d.kodekelompok||'.'||d.kodejenis||'.'||lpad(d.kodeobjek::text,2,'0')||'.'||lpad(d.koderincianobjek::text,2,'0')||'.'||lpad(d.kodesubrincianobjek::text,4,'0') AS KODEREKENING,
				t.*,r.urai as urai,d.* from kasda.kasda_transaksi t join  kasda.KASDA_TRANSAKSI_DETIL d on d.nobukukas=t.nobukukas
				and d.tahun=t.tahun left join master.master_rekening r on r.kodeakun=d.kodeakun and r.kodekelompok=d.kodekelompok and r.kodejenis=d.kodejenis 
				and r.kodeobjek=d.kodeobjek and r.koderincianobjek=d.koderincianobjek and r.kodesubrincianobjek=d.kodesubrincianobjek and r.tahun=d.tahun 
				where t.tahun=%s
				and t.nobukukas=%s and t.kodeurusan = %s and t.kodesuburusan = %s and t.kodeorganisasi = %s and t.kodeunit = %s 
				order by d.kodeakun,d.kodekelompok,d.kodejenis,d.kodeobjek,d.koderincianobjek,d.kodesubrincianobjek
				""", [tahun_log(request), nomor,kodeurusan, kodesuburusan, kodeorganisasi, kodeunit])
		some_variabel = dictfetchall(cursor)
	data = {
		"render_table":convert_datatable(some_variabel, ['koderekening','urai', 'penerimaan', 'pengeluaran']),
	}
	return JsonResponse(data)

@require_http_methods(["POST"])
def simpan_kasda_sp2dViews(request):
	status = False
	insert_status  = False
	nomor = request.POST.get('no_bukukas')
	no_sp2d = request.POST.get('no_sp2d')
	tgl_sp2d = request.POST.get('tgl_sp2d')
	organisasi = request.POST.get('organisasi')
	sumberdana = request.POST.get('sumber_dana')
	tgl_kasda = request.POST.get('tgl_transaksi')
	deskripsi = request.POST.get('deskripsi')
	jenis_sp2d = request.POST.get('jenis_sp2d')
	afektasi = ''
	sumdan_sp2d = request.POST.get('frm_sumberdana')

	kodeurusan = organisasi.split('.')[0]
	kodesuburusan = organisasi.split('.')[1]
	kodeorganisasi = organisasi.split('.')[2]
	kodeunit = organisasi.split('.')[3]

	timeout = 0

	while True:
		if timeout == 20:
			insert_status = False
			break
		else:
			try:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute('''
									SELECT count(nobukti) from kasda.kasda_transaksi WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and 
									nobukti = %s and jenissp2d = %s

						''', [tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_sp2d, jenis_sp2d])
					cek_existensi = cursor.fetchone()[0]
				
				if cek_existensi == 0:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute('''
										INSERT INTO kasda.kasda_transaksi(tahun,nobukukas,nobukti,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,
										deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi, username,locked,
										jenissp2d,sumberdana) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
									   ''',[tahun_log(request), nomor, no_sp2d, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, 
									   		deskripsi, '0', tgl_to_db(tgl_kasda), tgl_to_db(tgl_sp2d), sumberdana, 'SP2D', username(request), 'T', jenis_sp2d, sumdan_sp2d])

					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("""
									UPDATE penatausahaan.sp2d set tglkasda=%s where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s 
								and kodeunit = %s and nosp2d= %s
							""", [tgl_to_db(tgl_kasda), tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_sp2d])
					insert_status = True
					timeout = 0
					break
				else:
					insert_status = False
					timeout+=1
					break
			except Exception as e:
				print('error insert', e)
				nomor = cek_kasda_autoNoKas(request)[0]
				insert_status = False
				timeout+=1
	
	if insert_status:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s and nobukukas = %s", [tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT koderekening, urai, penerimaan, pengeluaran FROM kasda.fc_kasda_afektasi_sp2d(%s, %s, %s, %s, %s, %s)", [tahun_log(request),
				kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_sp2d])
			afektasi = dictfetchall(cursor)
		
			
		try:
			for x in afektasi:
				if jenis_sp2d != 'UP':
					kodebidang = x['koderekening'].split('-')[0].split('.')[0]+'.'+x['koderekening'].split('-')[0].split('.')[1]
					kodeprogram = x['koderekening'].split('-')[0].split('.')[3]
					kodekegiatan = x['koderekening'].split('-')[0].split('.')[4]+'.'+x['koderekening'].split('-')[0].split('.')[5]
					kodesubkegiatan = x['koderekening'].split('-')[0].split('.')[6]
				else:
					kodebidang = ''
					kodeprogram = 0
					kodekegiatan = '0'
					kodesubkegiatan = 0
				
				kodeakun = x['koderekening'].split('-')[1].split('.')[0]
				kodekelompok = x['koderekening'].split('-')[1].split('.')[1]
				kodejenis = x['koderekening'].split('-')[1].split('.')[2]
				kodeobjek = x['koderekening'].split('-')[1].split('.')[3]
				koderincianobjek = x['koderekening'].split('-')[1].split('.')[4]
				kodesubrincianobjek = x['koderekening'].split('-')[1].split('.')[5]

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("""
									INSERT INTO kasda.KASDA_TRANSAKSI_DETIL(TAHUN,NOBUKUKAS,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
									KODEBIDANG,KODEPROGRAM,KODEKEGIATAN, KODESUBKEGIATAN, kodesubkeluaran,  KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,
									KODESUBRINCIANOBJEK,PENERIMAAN,PENGELUARAN)
									VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
								   """,[tahun_log(request), nomor, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, 
								   kodesubkegiatan, 0, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, x['penerimaan'], x['pengeluaran']])
				status = True
		except Exception as e:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s and nobukukas = %s", [tahun_log(request), nomor])
			
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE FROM kasda.kasda_transaksi WHERE tahun = %s and nobukukas = %s and kodeurusan = %s and kodesuburusan = %s \
								and kodeorganisasi = %s and kodeunit = %s", [tahun_log(request), nomor, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit])
			print('Error insert afektasi, ', e)
			status = False

	data = {
		'status':status,
		'is_save':True,
	}
	return JsonResponse(data)

@require_http_methods(["POST"])
def edit_kasda_sp2dViews(request):
	status = False
	nomor = request.session.get('nobukukas_{}'.format(encrypt(username(request))))
	nomor_x = request.POST.get('no_bukukas')
	no_sp2d = request.POST.get('no_sp2d')
	tgl_sp2d = request.POST.get('tgl_sp2d')
	organisasi = request.POST.get('organisasi')
	sumberdana = request.POST.get('sumber_dana')
	tgl_kasda = request.POST.get('tgl_transaksi')
	deskripsi = request.POST.get('deskripsi')
	jenis_sp2d = request.POST.get('jenis_sp2d')
	
	afektasi = ''

	kodeurusan = organisasi.split('.')[0]
	kodesuburusan = organisasi.split('.')[1]
	kodeorganisasi = organisasi.split('.')[2]
	kodeunit = organisasi.split('.')[3]

	timeout = 0
	if nomor_x == '':
		data = {
			'status':status,
			'is_save':True,
		}
		return JsonResponse(data)

	try:
		int(nomor_x)
	except Exception as e:
		data = {
			'status':status,
			'is_save':True,
		}
		return JsonResponse(data)
		
	while True:
		if timeout == 20:
			insert_status = False
			break
		else:
			try:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute('''
					UPDATE kasda.kasda_transaksi SET nobukukas = %s,nobukti = %s ,kodeurusan = %s ,kodesuburusan = %s ,kodeorganisasi = %s ,kodeunit = %s ,
					deskripsi = %s ,kdlokasi = %s ,tanggal = %s ,tglbukti = %s ,kodesumberdana = %s ,jenistransaksi = %s , username = %s ,
					jenissp2d = %s  WHERE tahun = %s and nobukukas = %s
				   	''',[nomor_x, no_sp2d, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, 
				   	deskripsi, '0', tgl_to_db(tgl_kasda), tgl_to_db(tgl_sp2d), sumberdana, 'SP2D', username(request), jenis_sp2d, 
				   	tahun_log(request), nomor])
				insert_status = True
				timeout = 0
				break
			except Exception as e:
				print('error insert', e)
				nomor = cek_kasda_autoNoKas(request)[0]
				insert_status = False
				timeout+=1
	
	if insert_status:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s and nobukukas = %s", [tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT koderekening, urai, penerimaan, pengeluaran FROM kasda.fc_kasda_afektasi_sp2d(%s, %s, %s, %s, %s, %s)", [tahun_log(request),
				kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_sp2d])
			afektasi = dictfetchall(cursor)
			
		try:
			for x in afektasi:
				if jenis_sp2d != 'UP':
					kodebidang = x['koderekening'].split('-')[0].split('.')[0]+'.'+x['koderekening'].split('-')[0].split('.')[1]
					kodeprogram = x['koderekening'].split('-')[0].split('.')[3]
					kodekegiatan = x['koderekening'].split('-')[0].split('.')[4]+'.'+x['koderekening'].split('-')[0].split('.')[5]
					kodesubkegiatan = x['koderekening'].split('-')[0].split('.')[6]
				else:
					kodebidang = ''
					kodeprogram = 0
					kodekegiatan = '0'
					kodesubkegiatan = 0
				
				kodeakun = x['koderekening'].split('-')[1].split('.')[0]
				kodekelompok = x['koderekening'].split('-')[1].split('.')[1]
				kodejenis = x['koderekening'].split('-')[1].split('.')[2]
				kodeobjek = x['koderekening'].split('-')[1].split('.')[3]
				koderincianobjek = x['koderekening'].split('-')[1].split('.')[4]
				kodesubrincianobjek = x['koderekening'].split('-')[1].split('.')[5]

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("""
					INSERT INTO kasda.KASDA_TRANSAKSI_DETIL(TAHUN,NOBUKUKAS,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
					KODEBIDANG,KODEPROGRAM,KODEKEGIATAN, KODESUBKEGIATAN, kodesubkeluaran,  KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,
					KODESUBRINCIANOBJEK,PENERIMAAN,PENGELUARAN)
					VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
				   	""",[tahun_log(request), nomor_x, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, kodebidang, kodeprogram, kodekegiatan, 
				   	kodesubkegiatan, 0, kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, kodesubrincianobjek, x['penerimaan'], x['pengeluaran']])
				status = True
		except Exception as e:
			print('Error insert afektasi, ', e)
			# with connections[tahun_log(request)].cursor() as cursor:
			# 	cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s and nobukukas = %s", [tahun_log(request), nomor])
			
			# with connections[tahun_log(request)].cursor() as cursor:
			# 	cursor.execute("DELETE FROM kasda.kasda_transaksi WHERE tahun = %s and nobukukas = %s and kodeurusan = %s and kodesuburusan = %s \
			# 					and kodeorganisasi = %s and kodeunit = %s", [tahun_log(request), nomor, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit])
			status = False
	data = {
		'status':status,
		'is_save':False,
	}
	return JsonResponse(data)

def del_transactViews(request):
	status = False
	nomor = request.session.get('nobukukas_{}'.format(encrypt(username(request))))
	organisasi = request.POST.get('organisasi')
	print(organisasi)
	if organisasi != '':
		kodeurusan = organisasi.split('.')[0]
		kodesuburusan = organisasi.split('.')[1]
		kodeorganisasi = organisasi.split('.')[2]
		kodeunit = organisasi.split('.')[3]
		no_sp2d = request.POST.get('no_sp2d')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""
				INSERT into kasda.kasda_transaksi_del(tahun,nobukukas,nobukti,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,
				deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi,lastupdate,username,locked,username_del,jenissp2d)
				select tahun,nobukukas,nobukti,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,deskripsi,kdlokasi,tanggal,tglbukti,
				kodesumberdana,jenistransaksi,lastupdate,username,locked,%s,jenissp2d
				from kasda.kasda_transaksi where tahun=%s
				and nobukukas=%s
				""",[username(request), tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""
				INSERT into kasda.kasda_transaksi_detil_del(tahun,nobukukas,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,
				kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,
				kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,
				penerimaan,pengeluaran,username_del)
				select tahun,nobukukas,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,
				kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,
				kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,
				penerimaan,pengeluaran,%s from kasda.kasda_transaksi_detil 
				where tahun=%s and nobukukas=%s
				""",[username(request), tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM kasda.kasda_transaksi_detil where tahun=%s and nobukukas=%s",
				[tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM kasda.kasda_transaksi where tahun=%s and nobukukas=%s",
				[tahun_log(request), nomor])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("UPDATE penatausahaan.sp2d set tglkasda=null \
				where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s \
				and kodeunit = %s and nosp2d= %s",
				[tahun_log(request), kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, no_sp2d])
		status = True

	data = {
		'status':status,
	}
	return JsonResponse(data)