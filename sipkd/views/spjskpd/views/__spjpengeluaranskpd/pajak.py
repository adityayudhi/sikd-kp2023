from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from ...anov import *
from .. import main
import re

isskpd = 0
jenisjenis = {
	'PUNGUT-PAJAK': 'Pungutan Pajak',
	'SETOR-PAJAK': 'Setoran Pajak',
}
sekarang_penerimaan_re = 'PUNGUT'

# OK
@require_GET
def noauto(rq):
	data = {}

	if 'nobkuauto' in rq.GET and int(rq.GET['nobkuauto']) == 1:
		data['nobkuauto'] = main.nobkuauto(rq, is_return=False);

	if 'nosspauto' in rq.GET and int(rq.GET['nosspauto']) == 1:
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['jenis_bku'],
			rq.GET['bulan'],
		)
		with querybuilder() as qb:
			qb.execute("""
				SELECT COALESCE(COUNT(a.tahun),0)+1 FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan= %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND jenis_bku = %s AND EXTRACT(MONTH FROM a.tgl_bku) = %s
			""", cond)
			data['nosspauto'] = qb.context.fetchone()[0]

	return JsonResponse(data)
# 

# OK
def bkurincian(rq):
	data = {'potongan': []}
	keluar_eq_terima = (int(rq.GET['keluar_eq_terima']) == 1) if 'keluar_eq_terima' in rq.GET else False;

	try:
		jenis_bku = rq.GET['jenis_bku']
		jenis_sp2d = rq.GET['jenis_sp2d']
		cond_0 = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
			rq.GET['no_bku'],
		)
		cond_1 = ( *cond_0, )
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	sekarang = 'pengeluaran';
	if re.search(sekarang_penerimaan_re, jenis_bku): sekarang = 'penerimaan'

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek, 
			(
				a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
			) AS kode_rekening,
			(
				SELECT b.urai FROM master.master_rekening b WHERE b.tahun = a.tahun
				AND b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek  
			) as urai_rekening,
			a.penerimaan,
			a.pengeluaran

			FROM pertanggungjawaban.skpd_bkurincian a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s 
			AND a.kodeakun = 2
			AND a.no_bku = %s
			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""", cond_1)
		qb.result_many(data['potongan'])

		for d in data['potongan']:
			# digunakan untuk isi form setoran (yg diambil dari pungutan)
			if keluar_eq_terima: d['pengeluaran'] = d['penerimaan']

			if sekarang == 'penerimaan': del d['pengeluaran']
			if sekarang == 'pengeluaran': del d['penerimaan']

	return JsonResponse(data, safe=False)
#

# OK
def browse(rq):
	data = []
	try:
		jenis_bku = rq.GET['jenis_bku'];
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			isskpd,
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	if jenis_bku == 'SETOR-PAJAK':
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
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit AND b.no_bku = a.no_bku
					AND b.isskpd = a.isskpd
				) AS jumlah
				FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s AND a.isskpd = %s
				AND a.jenis_bku = 'PUNGUT-PAJAK'
				AND NOT EXISTS (
					SELECT b.bukti FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi
					AND b.kodeunit = a.kodeunit AND b.isskpd = a.isskpd
					AND b.bukti = a.bukti
					AND b.jenis_bku = 'SETOR-PAJAK'
				)
			""", cond);
			qb.result_many(data);
	else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 
