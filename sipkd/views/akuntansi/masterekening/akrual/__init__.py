from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from sipkd import config as cfg
from sipkd.views.spjskpd.anov import *
from ..main import *
import json

kode_separator = '.'
kode_fields = [
	'kodeakun',
	'kodekelompok',
	'kodejenis',
	'kodeobjek',
	'koderincianobjek',
];

@require_GET
def index(rq):
	return render(rq, 'akuntansi/masterekening/main.html', {
		'masterekening_header_title': 'Setting Kode Rekening Akrual',
		'akuntansi_masterekening_is_crud': True,
		'href_report': cfg.laplink(rq, {
			'file': 'AKUNTANSIPEMDA/masterrekening64.fr3',
			'tahun': rq.session['sipkd_tahun'],
			'report_type': 'pdf',
		}),
		'href_browse': reverse_lazy('sipkd:akuntansi_masterekening_akrual_browse'),
		'href_save': reverse_lazy('sipkd:akuntansi_masterekening_akrual_save'),
		'href_rm': reverse_lazy('sipkd:akuntansi_masterekening_akrual_rm'),
		'kode_separator': kode_separator,
		'kode_fields': kode_fields,
		'kode_fields_json': json.dumps(kode_fields),
	})
#

def browse(rq):
	first = True
	tahun = rq.session['sipkd_tahun']
	cond = {k:0 for k in kode_fields}
	entry_ext = {}
	data = []
	try:
		kode0 = rq.GET['node']
		kode1 = kode0.split(kode_separator)
	except Exception as err:
		kode0 = '0{0}'.format(kode_separator) * len(kode_fields)
		kode1 = [0] * len(kode_fields)
		entry_ext['__first__'] = 1

	if '__first__' in entry_ext and entry_ext['__first__'] == 1:
		cond[kode_fields[0]] = ('<>', 999)
	else:
		for i in range(len(kode_fields)):
			if i > 0 and first and int(kode1[i]) == 0:
				cond[kode_fields[i]] = ('<>', kode1[i]);
				first = False
			else:
				cond[kode_fields[i]] = kode1[i]

			if i == len(kode_fields)-1:
				if cond[kode_fields[i]].__class__.__name__ == 'tuple':
					entry_ext['__last__'] = 1

	with querybuilder('akuntansi.akrual_master_rekening', **cond) as qb:
		qb.read_sort(*kode_fields)
		qb.read(tahun=tahun)
		qb.result_many(data)

	for entry in data:
		entry['urai_rekening'] = entry['urai']
		entry['kode_rekening'] = kode_separator.join([str(entry[i]) for i in kode_fields])
		for e in entry_ext:
			entry[e] = entry_ext[e]

	return JsonResponse(data, safe=False)
	return JsonResponse([
		kode0,kode1,
		cond,
	], safe=False)
# 

@require_POST
def save(rq):
	primarykeys = ['tahun', *kode_fields,]

	try:
		__type__ = int(rq.POST['__type__'])

		data = {
			'tahun': rq.session['sipkd_tahun'],
		}
		for p in rq.POST:
			if p in masterekeningakrual_fields and p not in data:
				data[p] = rq.POST[p]
	except Exception as err:
		return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	try:
		if __type__ == 0:
			with querybuilder('akuntansi.akrual_master_rekening', **data) as qb:
				qb.create()
		elif __type__ == 1:
			with querybuilder('akuntansi.akrual_master_rekening', *primarykeys, **data) as qb:
				qb.update()
		else:
			return HttpResponseServerError('unknown __type__(%s)' % __type__, content_type='text/plain')
	except Exception as err:
		return HttpResponseServerError(err, content_type='text/plain')

	return HttpResponse('ok', content_type='text/plain')
	return JsonResponse([
		data,
	], safe=False)
# 

@require_POST
def rm(rq):
	try:
		cond = {
			'tahun': rq.session['sipkd_tahun'],
		}
		for i in range(len(kode_fields)):
			if i > 0 and int(rq.POST[kode_fields[i]]) == 0: break
			cond[kode_fields[i]] = rq.POST[kode_fields[i]]

	except Exception as err:
		return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	with querybuilder('akuntansi.akrual_master_rekening', **cond) as qb:
		qb.delete()

	return HttpResponse('ok', content_type='text/plain')
# 
