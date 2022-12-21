from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

isskpd = 0
angg_kegiatan_fields = None
jenisjenis = {
	'SP2D': 'Penerimaan SP2D LS',
	'SPJ': 'Pertanggung Jawaban SPJ LS',
}
sekarang_penerimaan_re = 'SP2D'

rincian_re_match = '\w+\[\w+\]\[\]'
rincian_re_capture = '(\w+)\[(\w+)\]\[\]'
rincian_re_replace = '{}[{}][]'

# OK
def browse(request):
	must = ['tahun','kodeurusan','kodesuburusan','kodeorganisasi','jenis_bku']
	for n in must:
		try: request.GET[n]
		except Exception as err:
			return HttpResponseServerError(err, content_type='text/plain');

	jenis_bku = request.GET['jenis_bku'];
	data = []
	cond = (
		request.GET['tahun'],
		request.GET['kodeurusan'], request.GET['kodesuburusan'], request.GET['kodeorganisasi'],
	)

	if jenis_bku == 'SP2D':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				-- a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
				b.kodebidang,b.kodeprogram,b.kodekegiatan,
				b.kodebidang||'.'||b.kodeprogram||'.'||b.kodekegiatan as kegiatan_kode,
				c.urai as kegiatan_urai,
				a.nosp2d, a.nosp2d as bukti,
				a.jenissp2d, a.jenissp2d as jenis_sp2d,
				a.tanggal, a.tanggal as tgl_bukti,
				a.tglkasda, a.tglkasda as tgl_bku,
				a.namayangberhak,
				a.informasi, a.informasi as urai,
				a.nospm,
				a.tglspm,
				b.jumlah

				FROM penatausahaan.sp2d a
				RIGHT JOIN (SELECT b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,
					b.kodebidang,b.kodeprogram,b.kodekegiatan,
					b.nosp2d,
					COALESCE(SUM(b.jumlah),0) as jumlah
					FROM penatausahaan.sp2drincian b GROUP BY b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,
					b.kodebidang,b.kodeprogram,b.kodekegiatan,
					b.nosp2d
				) b ON (b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.nosp2d = a.nosp2d
				)
				LEFT JOIN apbd.angg_kegiatan c on (c.tahun = a.tahun
					AND c.kodeurusan = a.kodeurusan AND c.kodesuburusan = a.kodesuburusan AND c.kodeorganisasi = a.kodeorganisasi
					AND c.kodebidang = b.kodebidang AND c.kodeprogram = b.kodeprogram AND c.kodekegiatan = b.kodekegiatan
				)

				WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.jenissp2d = 'LS'

				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku z WHERE z.tahun = a.tahun
					AND z.kodeurusan = a.kodeurusan AND z.kodesuburusan = a.kodesuburusan AND z.kodeorganisasi = a.kodeorganisasi
					AND z.jenis_bku = 'SP2D' AND z.jenis_sp2d = 'LS'
					AND z.bukti = a.nosp2d
				)
			""", cond)
			qb.result_many(data);

	elif jenis_bku == 'SPJ':
		with querybuilder() as qb:
			qb.execute(
			"""SELECT
				b.kodebidang,b.kodeprogram,b.kodekegiatan,
				b.kodebidang||'.'||b.kodeprogram||'.'||b.kodekegiatan as kegiatan_kode, c.urai as kegiatan_urai,
				a.no_bku, a.tgl_bku,
				a.bukti, a.tgl_bukti, a.jenis_sp2d,
				a.is_pihak_ketiga, a.simpananbank,
				a.urai,
				COALESCE(b.penerimaan,0) AS jumlah

				FROM pertanggungjawaban.skpd_bku a
				RIGHT JOIN (SELECT b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodebidang,b.kodeprogram,b.kodekegiatan,
					b.no_bku,b.isskpd,
					SUM(b.penerimaan) AS penerimaan
					FROM pertanggungjawaban.skpd_bkurincian b WHERE b.kodeakun = 5 AND b.kodekelompok = 2 GROUP BY b.tahun,
					b.kodeurusan,b.kodesuburusan,b.kodeorganisasi,b.kodebidang,b.kodeprogram,b.kodekegiatan,
					b.no_bku,b.isskpd
				) b on (b.tahun = a.tahun
					AND b.kodeurusan=a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.no_bku = a.no_bku AND b.isskpd = a.isskpd
				)
				LEFT JOIN apbd.angg_kegiatan c on (c.tahun = a.tahun
					AND c.kodeurusan = a.kodeurusan AND c.kodesuburusan = a.kodesuburusan AND c.kodeorganisasi = a.kodeorganisasi
					AND c.kodebidang = b.kodebidang AND c.kodeprogram = b.kodeprogram AND c.kodekegiatan = b.kodekegiatan
				)

				WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.jenis_bku LIKE '%%SP2D%%' AND a.jenis_sp2d = 'LS'
				AND a.isskpd = %s

				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku z WHERE z.tahun = a.tahun
					AND z.kodeurusan = a.kodeurusan AND z.kodesuburusan = a.kodesuburusan AND z.kodeorganisasi = a.kodeorganisasi
					AND z.jenis_bku LIKE '%%SPJ%%' AND z.jenis_sp2d = 'LS'
					AND z.bukti = a.bukti
				)
			""", (*cond, isskpd));
			qb.result_many(data);

	else: return HttpResponseServerError('jenis_bku ?? "%s"' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 

# OK
def rincian_sp2d(rq):
	data = {'rincian': [], 'potongan': []}
	cond_0 = (
		rq.GET['nosp2d'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],
		rq.GET['kodebidang'],rq.GET['kodeprogram'],rq.GET['kodekegiatan'],
	)
	cond_1 = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],
		rq.GET['nosp2d'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			(
				a.kodebidang||'.'||
				a.kodeorganisasi||'.'||
				a.kodeprogram||'.'||a.kodekegiatan||'-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			) as urai_rekening,

			-- a.tahun,
			-- a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
			a.kodebidang,a.kodeprogram,a.kodekegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,

			a.jumlah_p AS anggaran,
			COALESCE((
				SELECT b.jumlah FROM penatausahaan.sp2drincian b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.nosp2d = %s
			),0) AS penerimaan

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodebidang = %s AND a.kodeprogram = %s AND a.kodekegiatan = %s

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	with querybuilder() as qb:
		qb.execute("""
			SELECT
			'' AS kodebidang, 0 AS kodeprogram, 0 AS kodekegiatan,
			b.kodeakun, b.kodekelompok, b.kodejenis, b.kodeobjek, b.koderincianobjek,
			a.rekeningpotongan AS kode_rekening,
			b.urai AS urai_rekening,
			a.jumlah AS penerimaan

			FROM penatausahaan.sp2dpotongan a
			JOIN master.master_rekening b on (b.tahun = a.tahun
				AND (
					b.kodeakun||'.'||b.kodekelompok||'.'||b.kodejenis||'.'||
					LPAD(b.kodeobjek::text,2,'0')||'.'||LPAD(b.koderincianobjek::text,2,'0')
				) = a.rekeningpotongan
			)

			WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.nosp2d = %s

			ORDER BY a.rekeningpotongan
		""", cond_1)
		qb.result_many(data['potongan'])

	return JsonResponse(data, safe=False)
# 

def rincian_spj(rq):
	data = {'rincian': [], 'potongan': []}

	cond_0 = (
		rq.GET['no_bku'],
		rq.GET['tahun'],
		rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],
		rq.GET['kodebidang'],rq.GET['kodeprogram'],rq.GET['kodekegiatan'],
	)

	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			a.kodebidang,a.kodeprogram,a.kodekegiatan,
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
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.no_bku = %s
			),0) AS pengeluaran

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodebidang = %s AND a.kodeprogram = %s AND a.kodekegiatan = %s

			order by a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""", cond_0)
		qb.result_many(data['rincian'])

	bkupotongan(rq, jenis_bku='SP2D', is_return=False, data=data['potongan'])
	for n in data['potongan']:
		n['pengeluaran'] = n['penerimaan']
		del n['penerimaan']

	return JsonResponse(data, safe=False)
# 


# ?!
def kegiatan_browse(rq):
	global angg_kegiatan_fields
	if angg_kegiatan_fields == None:
		with querybuilder() as qb:
			angg_kegiatan_fields = {}
			qb.tablecolumns('apbd','angg_kegiatan', angg_kegiatan_fields)

	data = []
	cond = {
		'tahun': rq.GET['tahun'],
		'kodeorganisasi': rq.GET['kodeorganisasi'],
		'kodekegiatan': rq.GET['kodekegiatan'],
	}

	for k in rq.GET:
		if k in angg_kegiatan_fields:
			cond[k] = rq.GET[k]

	with querybuilder('apbd.angg_kegiatan', **cond) as qb: qb.read().result_many(data)

	return JsonResponse(data, safe=False)
	pass
# 

def bkurincian(rq):
	data = {'rincian': [], 'potongan': [], 'entry': {}}
	try:
		no_bku = rq.GET['no_bku']
		jenis_bku = rq.GET['jenis_bku']
		cond = (
			no_bku,
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],
		)
	except Exception as err: return HttpResponseServerError('%s is unknown' % err, content_type='text/plain')

	with querybuilder() as qb:
		qb.execute("""SELECT
			a.kodebidang, a.kodeprogram, a.kodekegiatan,
			a.kodebidang||'.'||a.kodeprogram||'.'||a.kodekegiatan as kegiatan_kode,
			(
				SELECT b.urai as kegiatan_urai FROM apbd.angg_kegiatan b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan
			)
			FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.no_bku = %s AND a.kodeakun = 5 AND a.isskpd = %s
		""", (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],
			no_bku,
			isskpd,
		))
		qb.result_one(data['entry'])

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	cond = (
		*cond,
		data['entry']['kodebidang'],
		data['entry']['kodeprogram'],
		data['entry']['kodekegiatan'],
	)
	with querybuilder() as qb:
		qb.execute("""
			SELECT DISTINCT
			a.kodebidang,a.kodeprogram,a.kodekegiatan,
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,
			(
				a.kodeurusan||'.'||
				LPAD(a.kodesuburusan::text,2,'0')||'.'||
				a.kodeorganisasi||'.0.0-'||
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')
			) as kode_rekening,
			(
				SELECT b.urai as urai_rekening
				FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
			),

			a.jumlah_p as anggaran,
			(
				SELECT b.{} FROM pertanggungjawaban.skpd_bkurincian b WHERE b.tahun = a.tahun
				AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
				AND b.kodebidang = a.kodebidang AND b.kodeprogram = a.kodeprogram AND b.kodekegiatan = a.kodekegiatan
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek
				AND b.no_bku = %s
			)

			FROM apbd.angg_belanja a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodebidang = %s AND a.kodeprogram = %s AND a.kodekegiatan = %s

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""".format(sekarang), cond)
		qb.result_many(data['rincian'])

	bkupotongan(rq, is_return=False, data=data['potongan'])

	return JsonResponse(data, safe=False)
# 

# OK
def bkupotongan(rq, jenis_bku=None, is_return=True, data=None):
	if data == None: data = []
	if jenis_bku == None: jenis_bku = rq.GET['jenis_bku']

	cond = (
		rq.GET['tahun'],
		rq.GET['kodeurusan'],
		rq.GET['kodesuburusan'],
		rq.GET['kodeorganisasi'],
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
				SELECT b.urai AS urai_rekening FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis and b.kodeobjek = a.kodeobjek and b.koderincianobjek = a.koderincianobjek
			),
			a.{0}

			FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
			AND a.kodeakun = 2
			AND a.no_bku = %s

			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek
		""".format(sekarang), cond)
		qb.result_many(data)

	if is_return: return JsonResponse(data, safe=False)
# 
