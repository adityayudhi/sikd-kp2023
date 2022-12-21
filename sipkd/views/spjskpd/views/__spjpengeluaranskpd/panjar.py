from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from .. import main
from ...anov import *

# CUSTOM #
jenisjenis = {
	'KELUAR': 'Pemberian Panjar',
	'TERIMA': 'Pertanggung jawaban Panjar',
}

isskpd = 0
sekarang_penerimaan_re = 'TERIMA'

def load(rq):
	data = {'entry': {}, 'rincian': [], 'potongan': [],}
	try:
		jenis_bku = rq.GET['jenis_bku']
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'], rq.GET['kodeunit'],
			isskpd,
			rq.GET['no_bku'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.* FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
			AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			AND a.isskpd = %s
			AND a.no_bku = %s
			AND a.jenis_bku = 'PANJAR'
		""", cond)
		qb.result_one(data['entry']);

	if jenis_bku == 'TERIMA':
		jumlah = data['entry']['penerimaan']
		data['entry']['penerimaan'] = data['entry']['pengeluaran']
		data['entry']['pengeluaran'] = jumlah

		del data['entry']['no_bku']
		del data['entry']['jenis_bku']

	return JsonResponse(data, safe=False)
# 

def browse(rq):
	data = []
	try:
		jenis_bku = rq.GET['jenis_bku'];
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'],rq.GET['kodesuburusan'],rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			jenis_bku,
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain');

	if jenis_bku == 'PANJAR':
		with querybuilder() as qb:
			qb.execute(
			"""
				SELECT
				a.no_bku, a.tgl_bku,
				a.bukti, a.tgl_bukti,
				a.urai,
				a.pengeluaran AS jumlah,
				a.simpananbank, a.is_pihak_ketiga
				FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
				AND a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
				AND a.jenis_bku = %s
				AND NOT EXISTS (
					SELECT 1 FROM pertanggungjawaban.skpd_bku b WHERE b.tahun = a.tahun
					AND b.kodeurusan = a.kodeurusan AND b.kodesuburusan = a.kodesuburusan AND b.kodeorganisasi = a.kodeorganisasi AND b.kodeunit = a.kodeunit 
					AND b.jenis_bku = a.jenis_bku
					AND b.bukti = a.bukti
					AND b.penerimaan <> 0
				)
			""", cond)
			qb.result_many(data)

	else: return HttpResponseServerError('unknown jenis_bku(%s)' % jenis_bku, content_type='text/plain');

	return JsonResponse(data, safe=False)
# 
