from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from sipkd import config as cfg
from . import __spjpengeluaranskpd as pkg
from . import main
from ..anov import querybuilder
import json
import re

isskpd = 0
rincian_re_match = '\w+\[\w+\]\[\]'
rincian_re_capture = '(\w+)\[(\w+)\]\[\]'
rincian_re_replace = '{}[{}][]'

@require_GET
def index(rq):
	return render(rq, 'spjskpd/spjpengeluaranskpd/main.html', {
		'isskpd': 0,
		'username': rq.session['sipkd_username'],
		'hakakses': rq.session['sipkd_hakakses'],
		'bulanbulan': main.bulanbulan,
		'laporan_jenisjenis': pkg.laporan.jenisjenis,
		'laporan_jenisjenis_json': json.dumps({k['kode']:k for k in pkg.laporan.jenisjenis }),
		'laporan_href': (reverse_lazy(main.report_href_local) if main.is_anov_host else main.report_href(rq)),
		'pergeseran_jenisjenis': pkg.pergeseran.jenisjenis,
		'upgu_jenisjenis': pkg.upgu.jenisjenis,
		'lsgj_jenisjenis': pkg.lsgj.jenisjenis,
		'tu_jenisjenis': pkg.tu.jenisjenis,
		'rkppkd_jenisjenis': pkg.rkppkd.jenisjenis,
		'barjas_jenisjenis': pkg.barjas.jenisjenis,
		'panjar_jenisjenis': pkg.panjar.jenisjenis,
		'pajak_jenisjenis': pkg.pajak.jenisjenis,
	})
#

@require_GET
def data(rq):
	result = { 'tbody': [], 'tfoot': {} }

	try:
		cond_1 = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['bulan'],
			rq.session['sipkd_username'],
		)
		cond_2 = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],rq.GET['kodeunit'],
			rq.GET['bulan'], rq.GET['bulan'],
		)
	except Exception as err: return HttpResponseServerError('unknown %s' % err, content_type='text/plain')

	try:
		with querybuilder() as qb:
			qb.execute('SELECT * from pertanggungjawaban.anov_bku_skpd(%s, %s,%s,%s, %s, %s,%s)', cond_1)
			qb.result_many(result['tbody'])
			qb.execute('SELECT * FROM pertanggungjawaban.fc_report_bku_pengeluaran_footer(%s, %s,%s,%s, %s,%s,%s) LIMIT 1', cond_2)
			qb.result_one(result['tfoot'])
	except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	return JsonResponse(result, safe=False);
#

# [OK][FUTURE]
@require_POST
def rm(rq):
	data = {}

	for k in main.bku_primarykeys:
		try: data[k] = rq.POST[k]
		except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	no_bku = data['no_bku'].split(',');
	no_bku = list(filter(None, no_bku));

	for i in range(len(no_bku)):
		data['no_bku'] = no_bku[i]
		
		with querybuilder('pertanggungjawaban.skpd_bku', **data) as qb:
			try: qb.delete()
			except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	return HttpResponse('ok', content_type='text/plain')
#

# [OK][TODO][FUTURE]
@require_POST
def save(rq):
	bku_default = {
		'isskpd': isskpd,
		'simpananbank': 0, 'is_pihak_ketiga': 0,
		'is_bendahara_pembantu': rq.session['sipkd_is_bendahara_pembantu'],
		'uname': rq.session['sipkd_username'],
	}
	bkurincian_default = {
		'kodebidang': '', 'kodeprogram': 0, 'kodekegiatan': 0, 'kodesubkegiatan':0,
	}

	post = {}
	dump = {}
	for k in rq.POST:
		if re.search(rincian_re_match, k):
			match = re.match(rincian_re_capture, k)
			group = rq.POST.getlist(rincian_re_replace.format(match.group(1), match.group(2)))
			if match.group(1) not in dump: dump[match.group(1)] = {}
			for g,n in enumerate(group):
				if g not in dump[match.group(1)]: dump[match.group(1)][g] = {};
				if match.group(2) in main.bkurincian_fields: dump[match.group(1)][g][match.group(2)] = n;
		elif k in main.bku_fields: post[k] = rq.POST[k]

	__type__ = int(rq.POST['__type__'])
	jenis_bku = rq.POST['jenis_bku']
	jenis_sp2d = rq.POST['jenis_sp2d']
	print(rq.POST)

	for k in bku_default:
		if k in main.bku_fields and k not in post:
			post[k] = bku_default[k]
	for k in post:
		if k in main.bkurincian_fields and k not in bkurincian_default:
			bkurincian_default[k] = post[k]

	try:
		if __type__ == 0:
			with querybuilder('pertanggungjawaban.skpd_bku', **post) as qb: qb.create();
		elif __type__ == 1:
			with querybuilder('pertanggungjawaban.skpd_bku', *main.bku_primarykeys, **post) as qb: qb.update();
		else:
			return HttpResponseServerError('unknown __type__(%s)' % __type__, content_type='text/plain')
	except Exception as xcp: return HttpResponseServerError(xcp, content_type='text/plain');

	# delete bkurincian
	with querybuilder('pertanggungjawaban.skpd_bkurincian') as qb:
		rm = {}
		for a in main.bku_primarykeys:
			if a in main.bkurincian_fields and a in post:
				rm[a] = post[a]
		qb.delete(**rm)
	# 

	# """
	# create bkurincian
	with querybuilder('pertanggungjawaban.skpd_bkurincian') as qb:
		for t in dump:
			for e in dump[t]:
				for a in bkurincian_default:
					if a in main.bkurincian_fields and a not in dump[t][e]:
						dump[t][e][a] = bkurincian_default[a]
				qb.create(**dump[t][e])
	#	#	#
	# """

	# return HttpResponse('ok', content_type='text/plain')
	return JsonResponse({
		'jenis_sp2d': rq.POST['jenis_sp2d'],
		'rm': rm,
		'post': post,
		'dump': dump,
		'data': rq.POST,
	}, safe=False)
#
