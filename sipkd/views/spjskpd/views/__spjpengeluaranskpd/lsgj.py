from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

isskpd = 0
jenisjenis = {
	'SP2D-GJ': 'Penerimaan SP2D Gaji (SP2D-GJ)',
	'BAYAR-GJ': 'Pertanggung Jawaban SP2D Gaji (SPJ-GJ)',
}

sekarang_penerimaan_re = 'SP2D-GJ'

# OK
def rincian_sp2d(rq):
	data = {'rincian': [], 'potongan': []}

	cond_0 = (
		rq.GET['nosp2d'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
		rq.GET['kodeunit'],
	)

	cond_1 = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
		rq.GET['kodeunit'],
		rq.GET['nosp2d'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			-- a.kodeurusan, a.kodesuburusan, a.kodeorganisasi,
			a.kodebidang,a.kodeprogram,a.kodekegiatan,
			a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) AS kode_rekening,

			(
				select b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			) AS urai_rekening,

			a.jumlah_p AS anggaran,
			COALESCE((
				select b.jumlah FROM penatausahaan.sp2drincian b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit 
				AND b.kodebidang is not null AND b.kodekegiatan = 0 AND b.kodeprogram = 0
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.nosp2d = %s
			),0) AS penerimaan

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			AND a.kodeakun = 5 AND a.kodekelompok = 1 AND a.kodejenis = 1

			ORDER BY
			-- a.tahun,
			-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	with querybuilder() as qb:
		qb.execute("""
			SELECT
			CAST(split_part(a.rekeningpotongan, '.', 1) AS INTEGER) AS kodeakun,
			CAST(split_part(a.rekeningpotongan, '.', 2) AS INTEGER) AS kodekelompok,
			CAST(split_part(a.rekeningpotongan, '.', 3) AS INTEGER) AS kodejenis,
			CAST(split_part(a.rekeningpotongan, '.', 4) AS INTEGER) AS kodeobjek,
			CAST(split_part(a.rekeningpotongan, '.', 5) AS INTEGER) AS koderincianobjek,
			a.rekeningpotongan AS kode_rekening,
			(
				SELECT b.urai AS urai_rekening
				FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0') = a.rekeningpotongan
			),
			a.jumlah AS penerimaan
			FROM penatausahaan.sp2dpotongan a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			AND a.nosp2d = %s
			ORDER BY a.rekeningpotongan
		""", cond_1)
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
# 

def rincian_bayar(rq):
	data = {'rincian': [], 'potongan': []}

	cond_0 = (
		rq.GET['no_bku'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
		rq.GET['kodeunit'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT 
			-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'|| 
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) AS kode_rekening,
			(
				SELECT b.urai as urai_rekening FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			),

			a.jumlah_p AS anggaran,
			COALESCE((
				SELECT b.penerimaan FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun 
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit 
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.no_bku = %s
			),0) AS pengeluaran

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			AND a.kodeakun = 5 AND a.kodekelompok = 1 AND a.kodejenis = 1 

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	bkupotongan(rq, jenis_bku='SP2D-GJ', is_return=False, data=data['potongan'])
	for n in data['potongan']:
		n['pengeluaran'] = n['penerimaan']
		del n['penerimaan']

	return JsonResponse(data, safe=False)
# 

def bkupotongan(rq, jenis_bku=None, is_return=True, data=None):
	if data == None: data = []
	if jenis_bku == None: jenis_bku = rq.GET['jenis_bku']

	cond = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
		rq.GET['kodeunit'],
		rq.GET['no_bku'],
	)

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	with querybuilder() as qb:
		qb.execute("""
			SELECT 
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
			(
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) AS kode_rekening,
			(
				select b.urai as urai_rekening from master.master_rekening b where b.tahun = a.tahun
				and b.kodeakun = a.kodeakun and b.kodekelompok = a.kodekelompok and b.kodejenis = a.kodejenis and b.kodeobjek = a.kodeobjek and b.koderincianobjek = a.koderincianobjek
			),
			a.{}
			from pertanggungjawaban.skpd_bkurincian a where a.tahun = %s
			and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
			and a.no_bku = %s
			and a.kodeakun = 2
			order by a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""".format(sekarang), cond)
		qb.result_many(data)

	if is_return: return JsonResponse(data, safe=False)
# 

# OK
def bkurincian(rq):
	data = {'rincian': [], 'potongan': []}
	try:
		no_bku = rq.GET['no_bku']
		jenis_bku = rq.GET['jenis_bku']
		cond = (
			no_bku,
			rq.GET['tahun'],
			rq.GET['kodeurusan'],
			rq.GET['kodesuburusan'],
			rq.GET['kodeorganisasi'],
			rq.GET['kodeunit'],
		)
	except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			-- a.kodebidang,a.kodeprogram,a.kodekegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) as kode_rekening,
			(
				SELECT b.urai
				FROM master.master_rekening b WHERE b.tahun = a.tahun 
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			) AS urai_rekening,

			a.jumlah_p as anggaran,
			COALESCE((
				SELECT b.{0} FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit 
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.no_bku = %s
			),0) as {0}

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			AND a.kodeakun = 5 AND a.kodekelompok = 1 AND a.kodejenis = 1 
			ORDER BY 
			-- a.tahun,
			-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""".format(sekarang), cond)
		qb.result_many(data['rincian'])

	bkupotongan(rq, is_return=False, data=data['potongan'])

	return JsonResponse(data, safe=False)
# 

# OK
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
		return HttpResponseServerError('undefined %s' % err, content_type='text/plain');

	if jenis_bku == 'SP2D-GJ':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				-- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
				a.nosp2d, a.nosp2d as bukti,
				a.jenissp2d, a.jenissp2d as jenis_sp2d,
				a.tanggal, a.tanggal as tgl_bukti,
				a.tglkasda,
				a.namayangberhak,
				a.informasi, a.informasi as urai,
				a.nospm,
				a.tglspm,
				(
					SELECT COALESCE(SUM(b.jumlah),0) FROM penatausahaan.sp2drincian b where b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan and b.kodesuburusan = a.kodesuburusan and b.kodeorganisasi = a.kodeorganisasi and b.kodeunit = a.kodeunit 
					AND b.nosp2d = a.nosp2d
				) as jumlah
				from penatausahaan.sp2d a where a.tahun = %s
				and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
				and a.jenissp2d = 'GJ'
				and a.nosp2d NOT IN (
					SELECT b.bukti FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun 
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan 
					AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.jenis_bku = 'SP2D-GJ'
					AND b.jenis_sp2d = 'GJ'
				)
			""",
			cond)
			qb.result_many(data);

	elif jenis_bku == 'BAYAR-GJ':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				a.no_bku, a.tgl_bku,
				a.bukti, a.tgl_bukti, a.jenis_sp2d,
				a.simpananbank, a.is_pihak_ketiga,
				a.urai,
				(
					SELECT COALESCE(SUM(b.penerimaan),0) FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit
					AND b.no_bku = a.no_bku
					AND b.isskpd = a.isskpd
					AND b.kodeakun = 5 AND b.kodekelompok = 1 AND b.kodejenis = 1
				) AS jumlah
				FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
				AND a.isskpd = 0
				AND a.jenis_sp2d = 'GJ'
				AND a.bukti NOT IN (
					SELECT b.bukti FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit 
					AND b.jenis_bku = 'BAYAR-GJ' AND b.jenis_sp2d = 'GJ'
				)
			""",
			cond);
			qb.result_many(data);

	else: return HttpResponseServerError('jenis_bku ?? "%s"' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 
