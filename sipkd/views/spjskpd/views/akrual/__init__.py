from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from sipkd import config as cfg
from .. import main
from ...anov import querybuilder
import json
import re

isskpd = main.isskpd
jenisjenis = None

@require_GET
def index(rq):
	if jenisjenis == None: jenisjenis_load()

	return render(rq, 'spjskpd/akrual/main.html', {
		'isskpd': isskpd,
		'username': rq.session['sipkd_username'],
		'hakakses': rq.session['sipkd_hakakses'],
		'bulanbulan': main.bulanbulan,
		'jenisjenis': jenisjenis,
		'jenisjenis_json': json.dumps({ k['id']:k for k in jenisjenis }),
	})
#

def data(rq):
	result = []

	try:
		cond = (
			rq.GET['tahun'],
			rq.GET['kodeurusan'], rq.GET['kodesuburusan'], rq.GET['kodeorganisasi'],
			rq.GET['bulan'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	try:
		with querybuilder() as qb:
			qb.execute('SELECT * from akuntansi.anov_jurnal_skpd(%s, %s,%s,%s, %s)', cond)
			qb.result_many(result)
	except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	return JsonResponse(result, safe=False);
#


@require_POST
def save(rq):
	return HttpResponse(None)
# 

def jenisjenis_load():
	global jenisjenis
	jenisjenis = []
	with querybuilder('akuntansi.akrual_jenis_jurnal', isskpd=isskpd) as qb:
		qb.read_sort('id')
		qb.read()
		qb.result_many(jenisjenis)

		"""
		20190704
		karena saya males,
		"jenis_transaksi" saya ambil singkatan dari teks pada jenisjurnal,
		jadi saya tidak perlu hardcoded "jenis_transaksi" pada *.py maupun *.js.
		"""
		for i in range(len(jenisjenis)):
			pk = re.findall('\((\w+)\)', jenisjenis[i]['uraian'])
			jenisjenis[i]['pk'] = pk[0] if len(pk) > 0 else None;
# 

def defaults():
	pass
# 
