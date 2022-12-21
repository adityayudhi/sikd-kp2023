from django.http import HttpResponse, JsonResponse
from support.support_sipkd import *

def autonobukas(request):
	hasil = cek_kasda_autoNoKas(request) ### dari support_sipkd
	data = {'hasilnya':hasil}

	return JsonResponse(data)

def mdl_afektasi(request,jenis):
	tahun_x = tahun_log(request)
	data 	= request.GET
	aidirow = data.get("i")
	skpd 	= data.get("d")
	frmFrom = jenis.lower()

	formMdl = 'none'
	hasil 	= ''
	arrjns_akun = ''
	
	## ambil data menggunakan ServerSide (mdl_afektasi_srvside)
	if frmFrom == "sts" or frmFrom == "contrakemarin" or frmFrom == "awal":
		formMdl = 'mdl_afektasi_sts' ### nama form

	if frmFrom == "nota":
		formMdl = 'mdl_afektasi_nota' ### nama form

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun as kode, urai as nama FROM master.master_rekening "
			"WHERE tahun = %s AND kodekelompok = 0 ORDER BY kodeakun",[tahun_x])
			arrjns_akun = dictfetchall(cursor)

	data = { 'formasal':frmFrom, 'aidirow':aidirow, 'hasil':hasil,
		'arrjns_akun':arrjns_akun, 'eskapede':skpd }

	return render(request, 'kasda/modal/'+formMdl+'.html', data)

def mdl_afektasi_srvside(request,jenis,jenis1):
	tahun_x = tahun_log(request)
	frmFrom = jenis.lower()
	skpd = jenis1.split(".")
	arrRinc = []

	######### STS, CONTRAKEMARIN, AWAL ==================================================================
	if frmFrom == "sts" or frmFrom == "contrakemarin" or frmFrom == "awal":
		if frmFrom == "sts":
			fungsipgsql = 'fc_browse_rek_sts'
		elif frmFrom == "contrakemarin":
			fungsipgsql = 'fc_browse_rek_pengembalian_kemarin'
		elif frmFrom == "awal":
			fungsipgsql = 'fc_browse_rek_awal'

		# JIKA KOLOM PENCARIAN DIISI =======
		if request.GET.get('search[value]') != '':
			keyword = request.GET.get('search[value]')
			arg = f"WHERE lower(koderekening||uraian) like '%%{keyword.lower()}%%'"
		else:
			arg = ''

		# GET JUMLAH DATA =======
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(koderekening) FROM kasda."+fungsipgsql+" (%s,%s,%s,%s,%s,%s) "+arg,
				[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],0])
			hasil_row = cursor.fetchone()[0]

		# GET DATA ===============
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT koderekening,uraian,anggaran_p as pagu \
				FROM kasda."+fungsipgsql+"(%s,%s,%s,%s,%s,%s) "+arg+" ORDER BY koderekening ASC LIMIT %s OFFSET %s",
				[tahun_x,skpd[0],skpd[1],skpd[2],skpd[3],0,request.GET.get('length'),request.GET.get('start')])
			hasil = ArrayFormater(dictfetchall(cursor))

		for xs in hasil:
			arrRinc.append((xs['koderekening'],xs['uraian'],xs['pagu']))


	######### NOTA ======================================================================================
	elif frmFrom == "nota":
		kodeakun = int(request.GET.get('k'))

		# JIKA KOLOM PENCARIAN DIISI =======
		if request.GET.get('search[value]') != '':
			keyword = request.GET.get('search[value]')
			arg = f"AND lower(urai||kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0') \
				||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,4,'0')) \
				like '%%{keyword.lower()}%%'"
		else:
			arg = ''

		# GET JUMLAH DATA =======
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(kodeakun) FROM master.master_rekening \
				WHERE tahun=%s and kodeakun=%s and koderincianobjek<>0 and kodesubrincianobjek<>0 "+arg,
				[tahun_x,kodeakun])
			hasil_row = cursor.fetchone()[0]

		# GET DATA ===============
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0') \
				||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,4,'0') as koderekening, \
				urai, kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek \
				FROM master.master_rekening WHERE tahun=%s and kodeakun=%s and koderincianobjek<>0 and kodesubrincianobjek<>0 \
				"+arg+" ORDER BY kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek \
				LIMIT %s OFFSET %s",
				[tahun_x,kodeakun, request.GET.get('length'), request.GET.get('start')])
			hasil = ArrayFormater(dictfetchall(cursor))

		for xs in hasil:
			arrRinc.append((xs['koderekening'],xs['urai']))

	######### END NOTA ===================================================================================		

	data_query = [list(i) for i in arrRinc]
	data = {
		"recordsTotal": hasil_row,
	 	"recordsFiltered": hasil_row,
	 	"data": data_query
	}
	return JsonResponse(data)

def cek_nobukti(request):
	hasil = cek_noBukti(tahun_log(request), request.POST['kode']) ### dari support_sipkd
	data = {'hasilnya':hasil}

	return JsonResponse(data)

def tbl_afektasi(request):
	tahun_x = tahun_log(request)
	hasil = jenissp2d = aksi = ""
	psdt = request.POST
	formTabel = 'none'
	frmAsal = psdt['asal'].lower()
	skpd = psdt['skpd'].split('.')
	nobukas = psdt['nobkas']
	nobukti = psdt['no_bukti']
	jenissp2d = psdt['jenissp2d']
	aksi = psdt['aksi']

	if frmAsal == "sts" or frmAsal == "contrakemarin":
		formTabel = 'tbl_kasda_sts'

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over() as nomor, kodeurusan||'.'||lpad(kodesuburusan::text,2,'0')||'.'||kodeorganisasi::text ||'.0.0-'||\
				kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0')\
				||'.'||lpad(koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,4,'0') as koderekening,\
				(select urai from master.master_rekening mr where mr.tahun=a.tahun and mr.kodeakun=a.kodeakun \
				and mr.kodekelompok=a.kodekelompok and mr.kodejenis=a.kodejenis and mr.kodeobjek=a.kodeobjek \
				and mr.koderincianobjek=a.koderincianobjek and mr.kodesubrincianobjek=a.kodesubrincianobjek) as uraian,\
				penerimaan as jumlahpenerimaan, pengeluaran as jumlahpengeluaran FROM kasda.kasda_transaksi_detil a\
				WHERE tahun = %s AND nobukukas = %s \
				ORDER BY kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek",
				[tahun_x,nobukas])
			hasil = ArrayFormater(dictfetchall(cursor))

	if frmAsal == "nota":
		formTabel = 'tbl_kasda_nota'

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT d.kodebidang||'.'||d.kodeorganisasi||'.'||d.kodeprogram||'.'||d.kodekegiatan||'.'||d.kodesubkegiatan||'-' \
				||d.KodeAkun||'.'||d.KodeKelompok||'.'||d.KodeJenis||'.'||lpad(d.kodeobjek::text,2,'0')|| \
				'.'||lpad(d.koderincianobjek::text,2,'0')||'.'||lpad(d.kodesubrincianobjek::text,4,'0') AS KODEREKENING, \
				t.*,r.urai,d.* from kasda.kasda_transaksi t join  kasda.KASDA_TRANSAKSI_DETIL d \
				on d.nobukukas=t.nobukukas and d.tahun=t.tahun left join master.master_rekening r on \
				r.kodeakun=d.kodeakun and r.kodekelompok=d.kodekelompok and r.kodejenis=d.kodejenis \
				and r.kodeobjek=d.kodeobjek and r.koderincianobjek=d.koderincianobjek and r.kodesubrincianobjek=d.kodesubrincianobjek and r.tahun=d.tahun \
				where t.tahun=%s \
				and t.nobukukas=%s \
				and t.jenistransaksi='NOTA'\
				order by d.kodeakun,d.kodekelompok,d.kodejenis,d.kodeobjek,d.koderincianobjek, r.kodesubrincianobjek=d.kodesubrincianobjek",
				[tahun_x,nobukas])
			hasil = ArrayFormater(dictfetchall(cursor))

	if frmAsal == "awal":
		formTabel = 'tbl_kasda_sts'

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over() as nomor, d.kodebidang||'.'||d.kodeorganisasi||'.'||d.kodeprogram||'.'||d.kodekegiatan||'.'||d.kodesubkegiatan||'-'||d.KodeAkun||'.'||d.KodeKelompok||'.'||\
				d.KodeJenis||'.'||lpad(d.kodeobjek::text,2,'0')||'.'||lpad(d.koderincianobjek::text,2,'0')||'.'||lpad(d.kodesubrincianobjek::text,4,'0') AS KODEREKENING,t.*,r.urai as uraian,d.*,d.penerimaan as jumlahpenerimaan, d.pengeluaran as jumlahpengeluaran\
				from kasda.kasda_transaksi t join  kasda.KASDA_TRANSAKSI_DETIL d on d.nobukukas=t.nobukukas \
				and d.tahun=t.tahun left join master.master_rekening r on \
				r.kodeakun=d.kodeakun and r.kodekelompok=d.kodekelompok and r.kodejenis=d.kodejenis and r.kodeobjek=d.kodeobjek and r.koderincianobjek=d.koderincianobjek and r.kodesubrincianobjek=d.kodesubrincianobjek and r.tahun=d.tahun \
				where t.tahun=%s\
				and t.nobukukas=%s\
				and t.jenistransaksi='AWAL'\
				order by d.kodeakun,d.kodekelompok,d.kodejenis,d.kodeobjek,d.koderincianobjek,d.kodesubrincianobjek",
				[tahun_x,nobukas])
			hasil = ArrayFormater(dictfetchall(cursor))
	
	if frmAsal == "contra":
		if psdt['skpd']=='':
			formTabel = 'tbl_kasda_contra'
			hasil=''
			
		else:
			if jenissp2d == 'UP' or jenissp2d == 'GU' or jenissp2d == 'TU' or jenissp2d=='':
				formTabel = 'tbl_kasda_contra'
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT PENERIMAAN,PENGELUARAN \
						FROM kasda.KASDA_TRANSAKSI_DETIL D JOIN kasda.KASDA_TRANSAKSI T ON \
						T.TAHUN=D.TAHUN AND T.KODEURUSAN=D.KODEURUSAN AND T.KODESUBURUSAN=D.KODESUBURUSAN AND T.KODEORGANISASI=D.KODEORGANISASI AND T.KODEUNIT=D.KODEUNIT AND \
						T.NOBUKUKAS=D.NOBUKUKAS AND T.JENISSP2D=%s \
						WHERE D.TAHUN=%s \
						AND D.KODEURUSAN=%s AND D.KODESUBURUSAN=%s AND D.KODEORGANISASI=%s AND D.KODEUNIT=%s \
						AND D.KODEPROGRAM=0 AND D.KODEKEGIATAN='0' AND D.KODESUBKEGIATAN=0 AND D.NOBUKUKAS=%s",
							[jenissp2d, tahun_x, skpd[0], skpd[1], skpd[2], skpd[3], nobukas,])
					hasil = ArrayFormater(dictfetchall(cursor))

			elif jenissp2d == 'LS':
				# AMBIL REKENING
				if psdt['ambilRekeningLS'] == 'true':
					formTabel = 'tbl_kasda_contra_ls_rekening'
					# INSERT
					if aksi=='true':
						kegiatan = psdt['arr'].split('.')
						kodebidang = f"{kegiatan[0]}.{kegiatan[1]}"
						kodeprogram = kegiatan[2]
						kodekegiatan = f"{kegiatan[3]}.{kegiatan[4]}"
						kodesubkegiatan = kegiatan[5]
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("SELECT distinct sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan as kode, \
								0,0,0,0,0, urai as uraian,0 as penerimaan,0 as pengeluaran,3 as pilih \
								from penatausahaan.kegiatan sr \
								where sr.tahun=%s and \
								sr.kodebidang=%s and \
								sr.kodeprogram=%s and \
								sr.kodekegiatan=%s and \
								sr.kodesubkegiatan=%s \
								and sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s  \
								UNION \
								select distinct sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan||'-'\
								||sr.kodeakun||'.'||sr.kodekelompok||'.'||sr.kodejenis||'.'||lpad(sr.kodeobjek::text,2,'0')||'.'||lpad(sr.koderincianobjek::text,2,'0')||'.'||lpad(sr.kodesubrincianobjek::text,4,'0') as kode,\
								sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek,\
								(SELECT urai from master.master_rekening where tahun=sr.tahun and kodeakun=sr.kodeakun and kodekelompok=sr.kodekelompok and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek and kodesubrincianobjek=sr.kodesubrincianobjek) as uraian,\
								0 as penerimaan,0 as pengeluaran,0 as pilih \
								from penatausahaan.belanja sr where sr.tahun=%s and \
								sr.kodebidang=%s and \
								sr.kodeprogram=%s  and \
								sr.kodekegiatan=%s and \
								sr.kodesubkegiatan=%s \
								and sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s",
								[tahun_x, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, skpd[0],skpd[1],skpd[2],skpd[3], 
								tahun_x, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, skpd[0],skpd[1],skpd[2],skpd[3],])
							hasil = ArrayFormater(dictfetchall(cursor))

					# UPDATE
					else:
						kegiatan = psdt['arr'].split('.')
						kodebidang = f"{kegiatan[0]}.{kegiatan[1]}"
						kodeprogram = kegiatan[2]
						kodekegiatan = f"{kegiatan[3]}.{kegiatan[4]}"
						kodesubkegiatan = kegiatan[5]
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("SELECT distinct sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan as kode, 0,0,0,0,0, \
								urai as uraian,0 as penerimaan,0 as pengeluaran,3 as pilih \
								from penatausahaan.kegiatan sr \
								where sr.tahun=%s and sr.kodebidang=%s and sr.kodeprogram=%s  and sr.kodekegiatan=%s and sr.kodesubkegiatan=%s \
								and sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s  \
								UNION \
								select distinct sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan||'-' \
								||sr.kodeakun||'.'||sr.kodekelompok||'.'||sr.kodejenis||'.'||lpad(sr.kodeobjek::text,2,'0')||'.'||lpad(sr.koderincianobjek::text,2,'0')||'.'||lpad(sr.kodesubrincianobjek::text,2,'0') as kode, \
								sr.kodeakun,sr.kodekelompok,sr.kodejenis,sr.kodeobjek,sr.koderincianobjek, \
								(SELECT urai from master.master_rekening where tahun=sr.tahun and kodeakun=sr.kodeakun and kodekelompok=sr.kodekelompok \
								and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek and kodesubrincianobjek=sr.kodesubrincianobjek) as uraian, \
								(select penerimaan from kasda.kasda_transaksi_detil where tahun=sr.tahun and kodeurusan=sr.kodeurusan and kodesuburusan=sr.kodesuburusan \
								and kodeorganisasi=sr.kodeorganisasi and kodeunit=sr.kodeunit and nobukukas=%s and kodebidang=sr.kodebidang \
								and kodeprogram=sr.kodeprogram and kodekegiatan=sr.kodekegiatan and kodesubkegiatan=sr.kodesubkegiatan and kodeakun=sr.kodeakun \
								and kodekelompok=sr.kodekelompok and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek and kodesubrincianobjek=sr.kodesubrincianobjek) as penerimaan,\
								(select pengeluaran from kasda.kasda_transaksi_detil where tahun=sr.tahun and kodeurusan=sr.kodeurusan and kodesuburusan=sr.kodesuburusan \
								and kodeorganisasi=sr.kodeorganisasi and kodeunit=sr.kodeunit and nobukukas=%s and kodebidang=sr.kodebidang \
								and kodeprogram=sr.kodeprogram and kodekegiatan=sr.kodekegiatan and kodesubkegiatan=sr.kodesubkegiatan and kodeakun=sr.kodeakun \
								and kodekelompok=sr.kodekelompok and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek \
								and kodesubrincianobjek=sr.kodesubrincianobjek) as pengeluaran, \
								case when (select penerimaan from kasda.kasda_transaksi_detil where tahun=sr.tahun and kodeurusan=sr.kodeurusan and kodesuburusan=sr.kodesuburusan \
								and kodeorganisasi=sr.kodeorganisasi and kodeunit=sr.kodeunit and nobukukas=%s and kodebidang=sr.kodebidang \
								and kodeprogram=sr.kodeprogram and kodekegiatan=sr.kodekegiatan and kodesubkegiatan=sr.kodesubkegiatan and kodeakun=sr.kodeakun \
								and kodekelompok=sr.kodekelompok and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek and kodesubrincianobjek=sr.kodesubrincianobjek) > 0 then 1 else 0 end as pilih \
								from penatausahaan.belanja sr \
								where sr.tahun=%s and sr.kodebidang=%s and sr.kodeprogram=%s  and sr.kodekegiatan=%s and sr.kodesubkegiatan=%s and \
								sr.kodeurusan=%s and sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s",
								[tahun_x, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, skpd[0],skpd[1],skpd[2],skpd[3], nobukas, nobukas, nobukas, 
								tahun_x, kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, skpd[0],skpd[1],skpd[2],skpd[3],])
							hasil = ArrayFormater(dictfetchall(cursor))
				
				# AMBIL KEGIATAN
				else:
					formTabel = 'tbl_kasda_contra_ls'
					# INSERT
					if aksi=='true':
						print("kegiatan insert")
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("SELECT  distinct sr.kodebidang||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan as koderekening, \
								(select urai from penatausahaan.kegiatan where tahun=sr.tahun and kodeurusan=sr.kodeurusan and kodesuburusan=sr.kodesuburusan and \
								kodeorganisasi=sr.kodeorganisasi and kodeunit=sr.kodeunit and kodebidang=sr.kodebidang and kodeprogram=sr.kodeprogram and kodekegiatan=sr.kodekegiatan and kodesubkegiatan=sr.kodesubkegiatan), \
								sr.kodeprogram,sr.kodekegiatan, sr.kodesubkegiatan,0 as pilih, 0.00 as penerimaan, 0.00 as pengeluaran \
								from penatausahaan.sp2drincian sr join penatausahaan.sp2d s on (sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
								sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nosp2d=s.nosp2d ) \
								where sr.tahun=%s and sr.kodeurusan=%s  and \
								sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s and \
								s.jenissp2d='LS' order by sr.kodeprogram,sr.kodekegiatan",
								[tahun_x, skpd[0], skpd[1], skpd[2], skpd[3]])
							hasil = ArrayFormater(dictfetchall(cursor))
					# UPDATE
					else:
						print("kegiatan update")
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("SELECT o_koderekening as koderekening, o_urai as urai, o_kodebidang as kodebidang,\
								o_kodeprogram as kodeprogram, o_kodekegiatan as kodekegiatan, o_kodesubkegiatan as kodesubkegiatan,\
								o_penerimaan as penerimaan, o_pengeluaran as pengeluaran, o_pilih as pilih \
								FROM kasda.fc_kasda_contra_ls(%s, %s, %s, %s, %s, %s, %s)",
								[tahun_x, skpd[0], skpd[1], skpd[2], skpd[3], nobukas, "LS"])
							hasil = ArrayFormater(dictfetchall(cursor))

	data = {'asal':frmAsal, 'list_dt':hasil}
	return render(request, 'kasda/tabel/'+formTabel+'.html', data)

def list_kasda(request, jenis):
	tahun_x = tahun_log(request)
	jenis_x = jenis.upper()

	data = { 'formasal':jenis_x}
	return render(request, 'kasda/modal/mdl_list_kasda.html', data)

def list_kasda_srvside(request, jenis):
	tahun_x = tahun_log(request)
	jenis_x = jenis.upper()
	arrRinc = []

	if request.GET.get('search[value]') != '':
		keyword = request.GET.get('search[value]')
		arg = f"where lower((nobukukas||nobukti||skpd||deskripsi)) \
			like '%%{keyword.lower()}%%'"
	else:
		arg = ''

	# GET JUMLAH DATA =======
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(nobukukas) FROM kasda.fc_kasda_transaksi(%s,%s) "+arg, [tahun_x, jenis_x])
		hasil_row = cursor.fetchone()[0]

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT nobukukas,tanggal,nobukti,skpd,deskripsi,penerimaan,pengeluaran, \
			kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit as organisasi \
			FROM kasda.fc_kasda_transaksi(%s,%s) "+arg+" ORDER BY nobukukas DESC LIMIT %s OFFSET %s",
			[tahun_x, jenis_x, request.GET.get('length'), request.GET.get('start')])
		hasil = ArrayFormater(dictfetchall(cursor))

	for xs in hasil:
		arrRinc.append((xs['nobukukas'],xs['tanggal'],xs['nobukti'],xs['skpd'],xs['deskripsi'],
			0 if xs['penerimaan'] is None else xs['penerimaan'],
			0 if xs['pengeluaran'] is None else xs['pengeluaran'],xs['organisasi']))

	data_query = [list(i) for i in arrRinc]

	data = {
		"recordsTotal": hasil_row,
	 	"recordsFiltered": hasil_row,
	 	"data": data_query
	}

	return JsonResponse(data)

def load_data(request):
	tahun = tahun_log(request)
	psdt = request.POST
	skpd = psdt['skpd'].split('.')
	nobukas = psdt['nobkas']
	nobukti = psdt['no_bukti']

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * from kasda.kasda_transaksi where tahun = %s and kodeurusan = %s \
			and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nobukukas = %s and nobukti = %s",
			[tahun,skpd[0],skpd[1],skpd[2],skpd[3],nobukas,nobukti])
		
		hasil = dictfetchall(cursor)

	if(hasil):
		for hsl in hasil:
			if(hsl['locked'] == 'T'):
				PESAN 	= ''
			else:
				PESAN 	= 'Nomor Buku Kas: '+hsl['nobukukas']+', tidak bisa diedit atau dihapus karena sudah disetujui/diproses!'
			
			ArrDT = {
				"TGLTRANS" 		 : tgl_indo(hsl["tanggal"]),
				"TGLBUKTI" 		 : tgl_indo(hsl["tglbukti"]),
				"KDSUMDAN" 		 : hsl["kodesumberdana"],
				"DESKRIPSI" 	 : hsl["deskripsi"], 
				"LOCKED" 		 : hsl["locked"],
				"NOBUKAS_X"		 : hsl['nobukukas'],
				"JENISSP2D"		 : hsl['jenissp2d'],
				"PESAN" 		 : PESAN,
			}
	else:
		ArrDT = {'PESAN':'Data Transaksi tidak ditemukan!'}

	return JsonResponse(ArrDT)

