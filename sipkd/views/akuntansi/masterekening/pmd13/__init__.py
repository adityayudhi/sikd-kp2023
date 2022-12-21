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
		'masterekening_header_title': 'Setting Kode Rekening PMD 13',
		'akuntansi_masterekening_is_crud': False,
		'href_report': cfg.laplink(rq, {
			'file': 'AKUNTANSIPEMDA/masterrekening13.fr3',
			'tahun': rq.session['sipkd_tahun'],
			'report_type': 'pdf',
		}),
		'href_browse': reverse_lazy('sipkd:akuntansi_masterekening_pmd13_browse'),
		'href_save': None,
		'href_rm': None,
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

	with querybuilder('master.master_rekening', **cond) as qb:
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
