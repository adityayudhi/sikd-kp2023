"""
[anovedit][20190516][UNTESTED]

$ browse():SPJ:querybuilder
$ bkurincian():SPJ:spjrincian()
$ spjrincian()

karena tidak ada data spj_skpd:spj:tu yang bisa dijadikan dummy.
"""

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

isskpd = 0
jenisjenis = {
	'SP2D': 'Penerimaan SP2D TU',
	'SPJ': 'Pertanggung Jawaban SP2D TU',
}
sekarang_penerimaan_re = 'SP2D'

# 50%
def browse(rq):
	data = []
	try:
		jenis_bku = rq.GET['jenis_bku'];
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

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
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.nosp2d = a.nosp2d
				) AS jumlah

				FROM penatausahaan.sp2d a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.jenissp2d ='TU'
				AND a.locked = 'Y'

				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.jenis_bku LIKE '%%SP2D%%'
					AND b.jenis_sp2d = a.jenissp2d
					AND b.bukti = a.nosp2d
				)
			""",
			cond)
			qb.result_many(data);

	elif jenis_bku == 'SPJ':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				a.nospj, a.nospj as bukti,
				a.tglspj, a.tglspj as tgl_bukti,
				a.keperluan, a.keperluan as urai,
				a.jenis, a.jenis as jenis_sp2d,
				COALESCE((
					SELECT SUM(b.jumlah) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan
					AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit
					AND b.nospj = a.nospj
				),0) AS jumlah
				FROM penatausahaan.spj_skpd a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.jenis = 'TU'
				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku b WHERE b.TAHUN = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan
					AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit
					AND b.jenis_bku LIKE '%%SPJ%%' AND b.bukti = a.nospj AND b.jenis_sp2d = a.jenis
				)
			""",
			cond);
			qb.result_many(data);

	else: return HttpResponseServerError('%s is unknown' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 

def sp2drincian(rq):
	data = {'rincian': [], 'potongan': []}
	try:
		jenissp2d = rq.GET['jenissp2d']
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],
			rq.GET['kodesuburusan'],
			rq.GET['kodeorganisasi'],
			rq.GET['kodeunit'],
			rq.GET['nosp2d'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	if jenissp2d == 'TU':
		with querybuilder() as qb:
			qb.execute("""
				SELECT DISTINCT
				(
					a.kodebidang||'.'||
					a.kodeorganisasi||'.'||
					a.kodeprogram||'.'||a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')
					||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
				) AS kode_rekening,
				(
					SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
					AND b.kodeakun = a.kodeakun  AND b.kodekelompok = a.kodekelompok 
					AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
					AND b.koderincianobjek = a.koderincianobjek
					AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS urai_rekening,

				a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
				a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,

				(
					SELECT COALESCE(SUM(b.jumlah_p),0) FROM penatausahaan.belanja b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
					AND b.kodekegiatan = a.kodekegiatan
					AND b.kodesubkegiatan = a.kodesubkegiatan
					AND b.kodeakun = a.kodeakun  AND b.kodekelompok = a.kodekelompok 
					AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
					AND b.koderincianobjek = a.koderincianobjek
					AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS anggaran,

				a.jumlah AS penerimaan

				FROM penatausahaan.sp2drincian a where a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.kodeakun = 5
				AND a.nosp2d = %s

				ORDER BY
				a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
				a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
			""", cond)
			qb.result_many(data['rincian'])
	else: return HttpResponseServerError('unknown "%s" jenissp2d' % jenissp2d, content_type='text/plain');

	with querybuilder() as qb:
		qb.execute("""
			SELECT
			'' AS kodebidang, 0 AS kodeprogram, 0 AS kodekegiatan, 0 AS kodesubkegiatan,
			b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, b.kodesubrincianobjek,
			a.rekeningpotongan AS kode_rekening, b.urai AS urai_rekening,
			SUM(a.jumlah) AS penerimaan

			FROM penatausahaan.sp2dpotongan a
			JOIN master.master_rekening b on (b.tahun = a.tahun
				AND (
					b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||
					LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0')
					||'.'||LPAD(b.kodesubrincianobjek::text,3,'0')
				) = a.rekeningpotongan
			)

			WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodeunit = %s AND a.nosp2d = %s

			GROUP BY b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek, 
		    b.kodesubrincianobjek, a.rekeningpotongan, b.urai
			ORDER BY a.rekeningpotongan
		""", (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['nosp2d'],
		))
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
#

# 66%
def bkurincian(rq):
	data = {'rincian': [], 'potongan': []}

	try:
		jenis_bku = rq.GET['jenis_bku']
		jenis_sp2d = rq.GET['jenis_sp2d']
		no_spj = rq.GET['nospj']
		cond_0 = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
			rq.GET['no_bku'],
		)
		cond_1 = ( *cond_0, )
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	if jenis_bku == 'SP2D' and jenis_sp2d == 'TU':
		with querybuilder() as qb:
			qb.execute("""
				SELECT DISTINCT
				(
					a.kodebidang||'.'||
					a.kodeorganisasi||'.'||
					a.kodeprogram||'.'||a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
					a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||LPAD(a.kodeobjek::text,2,'0')
					||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
				) AS kode_rekening,
				(
					SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
					AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis
					AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
					AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS urai_rekening,

				a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
				a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
				(
					SELECT COALESCE(SUM(b.jumlah_p),0) FROM penatausahaan.belanja b WHERE b.tahun = a.tahun 
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
					AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
					AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok 
					AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
					AND b.koderincianobjek = a.koderincianobjek
					AND b.kodesubrincianobjek = a.kodesubrincianobjek
				) AS anggaran,
				(
					SELECT COALESCE(SUM(b.penerimaan),0) FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
					AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
					AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok 
					AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
					AND b.koderincianobjek = a.koderincianobjek
					AND b.kodesubrincianobjek = a.kodesubrincianobjek
					AND b.no_bku = a.no_bku
				) AS penerimaan
				FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.kodeakun IN (1,5)
				AND a.no_bku = %s
			""", cond_0)
			qb.result_many(data['rincian'])
	elif jenis_bku == 'SPJ' and jenis_sp2d == 'TU':
		spjrincian(rq, is_return=False, nospj=None, data=data['rincian'])
	else:
		return HttpResponseServerError('unknown "%s"/"%s" jenis_bku/jenis_sp2d' % (jenis_bku,jenis_sp2d,), content_type='text/plain');

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
			(
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
				||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
			) AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok 
				AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
				AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
			) as urai_rekening,
			a.{0}

			FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodeunit = %s AND a.kodeakun = 2 AND a.no_bku = %s
			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""".format(sekarang), cond_1)
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
#

def spjrincian(rq, is_return=True, nospj=None, data=None):
	if data == None: data = []
	cond = ()

	if nospj == None:
		if 'nospj' in rq.GET: nospj = rq.GET['nospj']
		elif 'bukti' in rq.GET: nospj = rq.GET['bukti']
		else:
			err = 'nospj undefined'
			if is_return: return HttpResponseServerError(err, content_type='text/plain')
			else: raise Exception(err)

		try:
			cond = (
				rq.GET['tahun'],
				rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
				nospj,
			)

		except Exception as err: raise Exception(err)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			(
				a.kodebidang||'.'||
				a.kodeorganisasi||'.'||
				a.kodeprogram||'.'||a.kodekegiatan||'.'||a.kodesubkegiatan||'-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
				||'.'||LPAD(a.kodesubrincianobjek::text,3,'0')
			) AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun 
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
			) AS urai_rekening,
			(
				SELECT SUM(b.jumlah_p) FROM penatausahaan.belanja b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
				AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
				AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
			) AS anggaran,
			(
				SELECT SUM(b.jumlah) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
				AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram 
				AND b.kodekegiatan = a.kodekegiatan AND b.kodesubkegiatan = a.kodesubkegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok 
				AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek 
				AND b.koderincianobjek = a.koderincianobjek
				AND b.kodesubrincianobjek = a.kodesubrincianobjek
				AND b.nospj = a.nospj
			) AS pengeluaran,
			a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek

			FROM penatausahaan.spj_skpd_rinc_sub1 a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodeunit = %s AND a.nospj = %s
		""", cond)
		qb.result_many(data);

	if is_return: return JsonResponse(data, safe=False)
#
