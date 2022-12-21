"""

	TODO|UNTESTED. KARENA BELUM ADA DATA SAMA SEKALI. 20190701.

"""

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from .. import main
from ...anov import *
import re

isskpd = 0
jenisjenis = 'RK-PPKD'
bkurincian_cond_1_re = 'UP|GU|TU'
bkurincian_cond_2_re = 'LS|GJ'

def browse(rq):
	data = []
	
	try:
		jenis_bku = rq.GET['jenis_bku']
		jenis_sp2d = rq.GET['jenis_sp2d']
		if jenis_sp2d == 'UP': jenis_sp2d += '|GU'
		if jenis_sp2d == 'GU': jenis_sp2d += '|UP'
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			jenis_sp2d,
			jenis_bku,
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');
	
	if jenis_bku == jenisjenis:
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.*,
				a.nosts as bukti,
				a.uraian as urai,
				a.tglsts as tgl_bku,
				a.tglsts as tgl_bukti,
				a.jenissp2d as jenis_sp2d,
				coalesce(b.jumlah,0) AS jumlah
				FROM pertanggungjawaban.skpd_pengembalian a
				LEFT JOIN (SELECT b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
					b.nosts,SUM(b.jumlah) AS jumlah
					FROM pertanggungjawaban.skpd_rincian_pengembalian b
					GROUP BY b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodeunit,
					b.nosts
				) b ON (b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit AND b.nosts = a.nosts
				)
				WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
				AND a.jenissp2d SIMILAR TO %s
				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit AND b.jenis_bku = %s
					AND b.bukti = a.nosts
				)
				ORDER BY a.tahun, a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,a.kodeunit, a.tglsts,a.jenissp2d,a.nosts
			""", cond)
			qb.result_many(data);
	else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain');
	
	return JsonResponse(data, safe=False)
# 

def stsrincian(rq):
	data = {'rincian': []}
	try:
		jenis_bku = str(rq.GET['jenis_bku'])
		jenis_sp2d = str(rq.GET['jenis_sp2d'])
		cond = (
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['nosts'],
			rq.GET['tahun'],
		)

		cond2 = (
				rq.GET['tahun'],
				rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
				jenis_sp2d,
				rq.GET['nosts'],
				rq.GET['tahun'],
			)
		# cond_1 = ( *cond, rq.GET['nosts'], )
		cond_1 = ( *cond,)
		cond_2 = ( *cond2, )
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	if jenis_bku == jenisjenis:
		# $FLEX/sipkd_SPJSKPD/src/spjskpd/views/VInputRKPPKD.mxml:hasilPengembalian(nosts)
		with querybuilder() as qb:
			if re.search(bkurincian_cond_1_re, jenis_sp2d):
				qb.execute(
				"""
					SELECT a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek, a.kodesubrincianobjek, 
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
					AS kode_rekening,
					a.urai AS urai_rekening,
					0 AS penerimaan,
					(SELECT SUM(jumlah) FROM pertanggungjawaban.skpd_rincian_pengembalian b WHERE b.tahun=a.tahun and kodeurusan = %s and 
					kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nosts = %s) AS pengeluaran
					FROM master.master_rekening a WHERE a.tahun = %s
					AND a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 3 AND a.kodeobjek = 1 AND a.koderincianobjek = 1 AND a.kodesubrincianobjek = 1
				""",cond_1);

			elif re.search(bkurincian_cond_2_re, jenis_sp2d):
				qb.execute("""
					SELECT a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek, a.kodesubrincianobjek, 
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
					AS kode_rekening,
					a.urai AS urai_rekening,
					0 AS penerimaan,
					(SELECT SUM(jumlah) FROM pertanggungjawaban.skpd_view_rincianpengembalian(%s,%s,%s,%s,%s,%s,%s,%s) b
					WHERE b.isbold <> 0 AND b.jumlah <> 0) AS pengeluaran
					FROM master.master_rekening a WHERE a.tahun = %s
					AND a.kodeakun = 3 AND a.kodekelompok = 1 AND a.kodejenis = 3 AND a.kodeobjek = 1 AND a.koderincianobjek = 1 AND a.kodesubrincianobjek = 1
				""",cond_2)
			else: return HttpResponseServerError('unknown jenis_sp2d(%s)' % jenis_sp2d, content_type='text/plain')
			qb.result_many(data['rincian'])
	else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain')
	return JsonResponse(data, safe=False)
# 

def bkurincian(rq):
	data = {'rincian': []}
	try:
		jenis_bku = str(rq.GET['jenis_bku'])
		jenis_sp2d = str(rq.GET['jenis_sp2d'])
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
			isskpd,
			rq.GET['no_bku'],
		)
		cond_1 = ( *cond, )
		cond_2 = ( *cond, )
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	if jenis_bku == jenisjenis:
		# $FLEX/sipkd_SPJSKPD/src/spjskpd/views/VInputRKPPKD.mxml:ambilDataRincian(no_bku)
		
		with querybuilder() as qb:
			qb.execute(
				"""
					SELECT
					a.kodebidang,a.kodeprogram,a.kodekegiatan,
					a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek, a.kodesubrincianobjek, 
					(
						a.kodeurusan||'.'||
						LPAD(a.kodesuburusan::text,2,'0')||'.'||
						a.kodeorganisasi||'.0.0-'||
						a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
						LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
					) AS kode_rekening,b.urai AS urai_rekening,
					a.penerimaan,a.pengeluaran

					FROM pertanggungjawaban.skpd_bkurincian a
					LEFT JOIN master.master_rekening b ON (b.tahun = a.tahun
						AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
					)
					WHERE a.tahun = %s
					AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
					AND a.isskpd = %s
					AND a.no_bku = %s
					-- AND a.kodeakun = 3 AND a.kodekelompok = 4 AND a.kodejenis = 1 AND a.kodeobjek = 1 AND a.koderincianobjek = 1
				""",cond_1);
			# if re.search(bkurincian_cond_1_re, jenis_sp2d):
			# 	qb.execute(
			# 	"""
			# 		SELECT
			# 		a.kodebidang,a.kodeprogram,a.kodekegiatan,
			# 		a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek, a.kodesubrincianobjek, 
			# 		(
			# 			a.kodeurusan||'.'||
			# 			LPAD(a.kodesuburusan::text,2,'0')||'.'||
			# 			a.kodeorganisasi||'.0.0-'||
			# 			a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
			# 			LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
			# 		) AS kode_rekening,b.urai AS urai_rekening,
			# 		a.penerimaan,a.pengeluaran

			# 		FROM pertanggungjawaban.skpd_bkurincian a
			# 		LEFT JOIN master.master_rekening b ON (b.tahun = a.tahun
			# 			AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
			# 		)
			# 		WHERE a.tahun = %s
			# 		AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			# 		AND a.isskpd = %s
			# 		AND a.no_bku = %s
			# 		-- AND a.kodeakun = 3 AND a.kodekelompok = 4 AND a.kodejenis = 1 AND a.kodeobjek = 1 AND a.koderincianobjek = 1
			# 	""",cond_1);
			# elif re.search(bkurincian_cond_2_re, jenis_sp2d):
			# 	qb.execute("""
			# 		SELECT
			# 		a.kodebidang,a.kodeprogram,a.kodekegiatan,
			# 		a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek,
			# 		(
			# 			a.kodeurusan||'.'||
			# 			LPAD(a.kodesuburusan::text,2,'0')||'.'||
			# 			a.kodeorganisasi||'.0.0-'||
			# 			a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
			# 			LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			# 		) AS kode_rekening,b.urai AS urai_rekening,
			# 		0 AS penerimaan,a.pengeluaran

			# 		FROM pertanggungjawaban.skpd_bkurincian a
			# 		LEFT JOIN master.master_rekening b ON (b.tahun = a.tahun
			# 			AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			# 		)
			# 		WHERE a.tahun = %s
			# 		AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			# 		AND a.isskpd = %s
			# 		AND a.no_bku = %s
			# 	""",cond_2)
			# else: return HttpResponseServerError('unknown jenis_sp2d(%s)' % jenis_sp2d, content_type='text/plain')
			qb.result_many(data['rincian'])
	else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain')
	return JsonResponse(data, safe=False)
# 
