from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

jenisjenis = {
	'SP2D': 'Penerimaan SP2D UP/GU',
	'SPJ': 'Pertanggung Jawaban SPJ UP/GU',
}
sekarang_penerimaan_re = 'SP2D'

isskpd = 0
bku_fields = main.bku_fields
bku_primarykeys = main.bku_primarykeys
bkurincian_primarykeys = main.bkurincian_primarykeys
bkurincian_fields = main.bkurincian_fields

def browse(request):
	rq = request
	data = []

	try:
		jenis_bku = rq.GET['jenis_bku']; 
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		)
	except Exception as err:
		return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	if jenis_bku == 'SP2D':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				a.nosp2d, a.nosp2d as bukti,
				a.jenissp2d, a.jenissp2d as jenis_sp2d,
				a.tanggal, a.tanggal as tgl_bukti,
				a.tglkasda, a.tglkasda as tgl_bku,
				a.namayangberhak,
				a.informasi, a.informasi as urai,
				a.nospm, a.tglspm,
				(
					SELECT COALESCE(SUM(b.jumlah),0) FROM penatausahaan.sp2drincian b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND TRIM(b.kodeorganisasi) = TRIM(a.kodeorganisasi)
					AND b.kodeunit = a.kodeunit AND b.nosp2d = a.nosp2d
				) AS jumlah

				FROM penatausahaan.sp2d a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.jenissp2d in ('UP','GU')
				
				AND a.nosp2d NOT IN (
					SELECT b.bukti FROM pertanggungjawaban.SKPD_BKU b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit AND b.jenis_bku = 'SP2D'
					AND b.jenis_sp2d IN ('UP','GU')
				)
			""", cond)
			qb.result_many(data);

	elif jenis_bku == 'SPJ':
		with querybuilder() as qb:
			# qb.execute(
			# """
			# 	SELECT
			# 	-- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			# 	a.nospj, a.nospj as bukti,
			# 	a.tglspj, a.tglspj as tgl_bukti,
			# 	a.keperluan, a.keperluan as urai,
			# 	a.jenis, a.jenis as jenis_sp2d,
			# 	(
			# 		SELECT COALESCE(SUM(b.jumlah),0) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE b.tahun = a.tahun
			# 		AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
			# 		AND b.nospj = a.nospj
			# 	) AS jumlah
			# 	FROM penatausahaan.spj_skpd a WHERE a.tahun = %s
			# 	AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			# 	AND a.jenis in ('UP','GU')
			# 	AND a.nospj NOT IN (
			# 		SELECT b.bukti FROM pertanggungjawaban.skpd_bku b WHERE b.TAHUN = a.tahun
			# 		AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan  AND b.kodeorganisasi = a.kodeorganisasi
			# 		AND b.jenis_bku = 'SPJ'
			# 		AND b.jenis_sp2d in ('UP','GU')
			# 	)
			# """, cond);

			qb.execute(
			"""
				SELECT
				-- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,a.kodeunit,
				a.nospj||'::'||a.nobukti as nospj, a.nospj||'::'||a.nobukti as bukti,
				a.tglbukti as  tglspj, a.tglbukti as tgl_bukti,
				b.keperluan, b.keperluan as urai,
				b.jenis, b.jenis as jenis_sp2d,
				sum(a.jumlah) as jumlah   
				FROM penatausahaan.spj_skpd_rinc_sub1 a join penatausahaan.spj_skpd b on
			    (a.tahun=b.tahun and a.kodeurusan=b.kodeurusan and a.kodesuburusan=b.kodesuburusan and a.kodeorganisasi=b.kodeorganisasi 
			    and a.kodeunit=b.kodeunit and a.nospj=b.nospj ) 	
			    WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND b.jenis in ('UP','GU')
				AND a.nospj||'::'||a.nobukti NOT IN (
					SELECT b.bukti FROM pertanggungjawaban.skpd_bku b WHERE b.TAHUN = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan  AND b.kodeorganisasi = a.kodeorganisasi
					and a.kodeunit=b.kodeunit AND b.jenis_bku = 'SPJ'
					AND b.jenis_sp2d in ('UP','GU')
				)
				group by a.nospj,a.nobukti,a.nospj,a.tglbukti,b.keperluan,b.jenis 
				order by a.tglbukti,a.nospj 
			""", cond);
			
			qb.result_many(data);

	else: return HttpResponseServerError('jenis_bku ?? "%s"' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 

def sp2drincian(rq):
	data = {'rincian': [], 'potongan': []}
	try:
		jenissp2d = rq.GET['jenissp2d']
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['nosp2d'],
		)
	except Exception as err:
		return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	if jenissp2d == 'UP':
		with querybuilder() as qb:
			qb.execute("""
				SELECT DISTINCT
				(
					a.kodeurusan||'.'||LPAD(a.kodesuburusan::text,2,'0')||'.'||a.kodeorganisasi||'.'||a.kodeunit||
					'.0.0-'||
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
				) AS kode_rekening,
				-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
				(
					CASE
						WHEN TRIM(a.kodebidang) = '' THEN a.kodeurusan||'.'||LPAD(a.kodesuburusan::text,2,'0')
						ELSE TRIM(a.kodebidang)
					END
				) AS kodebidang,
				-- a.kodebidang,
				a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
				a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
				(
					SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
					AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS urai_rekening,
				a.jumlah AS anggaran,
				a.jumlah AS penerimaan
				FROM penatausahaan.sp2drincian a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
				AND a.kodeakun = 1
				AND a.nosp2d = %s
			""", cond)
			qb.result_many(data['rincian'])

	elif jenissp2d == 'GU':
		# print(cond)
		with querybuilder() as qb:
			qb.execute("""
				SELECT DISTINCT
				(
					a.kodebidang||'.'||
					a.kodeprogram||'.'||
					a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
				) AS kode_rekening,
				-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
				a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
				a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
				(
					SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
					AND b.kodeakun = a.kodeakun  AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS urai_rekening,
				(
					SELECT COALESCE(SUM(b.jumlah_p),0) FROM penatausahaan.belanja b
					WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan 
					AND b.kodeakun = a.kodeakun  AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS anggaran,
				a.jumlah AS penerimaan
				FROM (
					SELECT a.* FROM penatausahaan.sp2drincian a ORDER BY a.tahun,
					a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,a.kodeunit,
					a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan, 
					a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
				) a
				where a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
				AND a.kodeakun = 5
				AND a.nosp2d = %s
			""", cond)
			qb.result_many(data['rincian'])

	else:
		return HttpResponseServerError('unknown jenissp2d(%s)' % jenissp2d, content_type='text/plain');

	# FLEX:/sipkd_SPJSKPD/src/spjskpd/views/VinputUPGU.mxml:ambilPajak()
	with querybuilder() as qb:
		qb.execute("""
			SELECT
			CAST(split_part(a.rekeningpotongan, '.', 1) AS INTEGER) AS kodeakun,
			CAST(split_part(a.rekeningpotongan, '.', 2) AS INTEGER) AS kodekelompok,
			CAST(split_part(a.rekeningpotongan, '.', 3) AS INTEGER) AS kodejenis,
			CAST(split_part(a.rekeningpotongan, '.', 4) AS INTEGER) AS kodeobjek,
			CAST(split_part(a.rekeningpotongan, '.', 5) AS INTEGER) AS koderincianobjek,
			CAST(split_part(a.rekeningpotongan, '.', 6) AS INTEGER) AS kodesubrincianobjek,
			a.rekeningpotongan AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND (
					b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||
					LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0')||'.'||
					LPAD(b.kodesubrincianobjek::text,3,'0')
				) = a.rekeningpotongan
			) AS urai_rekening,
			a.jumlah AS penerimaan
			FROM penatausahaan.sp2dpotongan a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			AND a.nosp2d = %s
			order by a.rekeningpotongan
		""", cond)
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
#

"""
jadi begini, ada yang aneh.
kalo parameter ${data} dibuat list|array, result ${data} bisa duplicated.
tapi kalo dibuat none|null, lalu dijadikan list|array secara lazy, tidak.
"""
def spjrincian(rq, is_return=True, nospj=None, data=None):
	if data == None: data = {'rincian': [], 'potongan': []};

	if nospj == None:
		if 'nospj' in rq.GET: nospj = rq.GET['nospj']
		elif 'bukti' in rq.GET: nospj = rq.GET['bukti']
		else:
			if is_return: return HttpResponseServerError('nospj ?? "%s"' % (nospj,), content_type='text/plain');
			else: raise Exception('nospj ?? "%s"' % (nospj,))


	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			(
				a.kodebidang||'.'||
				a.kodeprogram||'.'||
				a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
			) AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun 
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
			) AS urai_rekening,
			(
				SELECT CASE WHEN SUM(b.jumlah_p) is NULL THEN 0 ELSE SUM(b.jumlah_p) END FROM penatausahaan.belanja b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
			) AS anggaran,
			(
				SELECT SUM(b.jumlah) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
				AND b.nospj||'::'||b.nobukti = a.nospj||'::'||a.nobukti
			) AS pengeluaran,
			-- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek

			FROM penatausahaan.spj_skpd_rinc_sub1 a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s and a.kodeunit = %s
			AND trim(a.nobukti)  = trim(%s)
		""", (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],
			rq.GET['kodesuburusan'],
			rq.GET['kodeorganisasi'],
			rq.GET['kodeunit'],
			nospj
		))

		
		 
		qb.result_many(data['rincian']);


	cond_1 = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		nospj,
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT
		    '' AS kodebidang, 0 AS kodeprogram, 0 AS kodekegiatan, 0 AS kodesubkegiatan,
		    b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, b.kodesubrincianobjek,
		    a.rekeningpotongan AS kode_rekening,
		    b.urai AS urai_rekening,
		    SUM(a.jumlah) AS pengeluaran

		    FROM penatausahaan.spj_skpd_potongan a
		    JOIN master.master_rekening b on (b.tahun = a.tahun
		       AND (
		            b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||
		            LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0')
		            ||'.'||LPAD(b.kodesubrincianobjek::text,3,'0')
		        ) = a.rekeningpotongan
		    )

		    WHERE a.tahun = %s
		    AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
		    AND trim(a.nobukti)  = trim(%s)

		    GROUP BY 
		    b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, 
		    b.kodesubrincianobjek, 
		    a.rekeningpotongan
		    , b.urai
		    ORDER BY a.rekeningpotongan
		""", cond_1)
		qb.result_many(data['potongan'])
	

	if is_return: return JsonResponse(data, safe=False)
#

def bkurincian(rq):
	must = ['tahun','kodeurusan','kodesuburusan','kodeorganisasi','no_bku','jenis_bku','jenis_sp2d','bukti']
	data = {'rincian': [], 'potongan': []}


	for n in must:
		try: rq.GET[n]
		except Exception as err:
			return HttpResponseServerError(err, content_type='text/plain');

	jenis_bku = rq.GET['jenis_bku']
	jenis_sp2d = rq.GET['jenis_sp2d']

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	if jenis_bku == 'SP2D':
		if jenis_sp2d == 'UP':
			with querybuilder() as qb:
				qb.execute("""
					SELECT DISTINCT
					(
						a.kodebidang||'.'||
						a.kodeprogram||'.'||
						a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
						a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
					) AS kode_rekening,
					-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
					a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
					a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
					(
						SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS urai_rekening,
					(
						SELECT COALESCE(SUM(b.penerimaan),0) FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
						AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
						AND b.no_bku = a.no_bku
						AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS anggaran,
					(
						SELECT COALESCE(SUM(b.penerimaan),0) FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
						AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
						AND b.no_bku = a.no_bku
						AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS penerimaan
					FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
					AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
					AND a.kodeakun = 1
					AND a.no_bku = %s
				""", (
					rq.GET['tahun'],
					rq.GET['kodeurusan'],
					rq.GET['kodesuburusan'],
					rq.GET['kodeorganisasi'],
					rq.GET['kodeunit'],
					rq.GET['no_bku'],
				))
				qb.result_many(data['rincian'])
		elif jenis_sp2d == 'GU':
			with querybuilder() as qb:
				qb.execute("""
					SELECT DISTINCT
					(
						a.kodebidang||'.'||
						a.kodeprogram||'.'||
						a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
						a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
					) AS kode_rekening,
					-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
					a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
					a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
					(
						SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS urai_rekening,
					(
						SELECT COALESCE(SUM(b.jumlah_p),0) FROM apbd.rka_belanja b WHERE b.tahun = a.tahun 
						AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
						AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS anggaran,
					(
						SELECT COALESCE(SUM(b.penerimaan),0) FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
						AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
						AND b.no_bku = a.no_bku
						AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					) AS penerimaan
					FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
					AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 

					-- karena, yg sekarang, UP selalu disimpan menggunakan GU.
					AND a.kodeakun IN (1,5)

					AND a.no_bku = %s
				""", (
					rq.GET['tahun'],
					rq.GET['kodeurusan'],
					rq.GET['kodesuburusan'],
					rq.GET['kodeorganisasi'],
					rq.GET['kodeunit'],
					rq.GET['no_bku'],
				))
				qb.result_many(data['rincian'])
		else: return HttpResponseServerError('jenis_sp2d ?? "%s"' % jenis_sp2d, content_type='text/plain')
	elif jenis_bku == 'SPJ' and jenis_sp2d == 'GU':
		spjrincian(rq, is_return=False, data=data)
	else: return HttpResponseServerError('jenis_bku/jenis_sp2d ?? "%s"/"%s"' % (jenis_bku,jenis_sp2d,), content_type='text/plain');		

	return JsonResponse(data, safe=False)
#
