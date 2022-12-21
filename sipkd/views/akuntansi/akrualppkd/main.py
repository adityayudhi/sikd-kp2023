from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
import json
import re

from sipkd import config as cfg
from ...spjskpd.views import main
from ...spjskpd.anov import *

from . import laporan

isskpd = 1;
tahun = None; jenisjenis = None; skpd_ppkd = None;
norefauto_length = 5; norefauto_prefix = 0;

rincian_re_match = '\w+\[\w+\]\[\]'
rincian_re_capture = '(\w+)\[(\w+)\]\[\]'
rincian_re_replace = '{}[{}][]'

jurnal_primarykeys = {}; jurnalrincian_primarykeys = {};
jurnal_fields = {}; jurnalrincian_fields = {};

with querybuilder() as qb:
	qb.info_columns('akuntansi','akrual_buku_jurnal', jurnal_fields)
	qb.info_columns('akuntansi','akrual_jurnal_rincian', jurnalrincian_fields)
	qb.info_primarykeys('akuntansi','akrual_buku_jurnal', jurnal_primarykeys)
	qb.info_primarykeys('akuntansi','akrual_jurnal_rincian', jurnalrincian_primarykeys)
# 

# [DONE] #
@require_GET
def index(rq):
	global tahun, jenisjenis, skpd_ppkd
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if jenisjenis is None: jenisjenis_load(rq);
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	laporan_pejabat = laporan.pejabat(tahun);

	return render(rq, 'akuntansi/akrualppkd/main.html', {
		'isskpd': isskpd,
		'username': rq.session['sipkd_username'],
		'hakakses': rq.session['sipkd_hakakses'],
		'skpkd': skpd_ppkd,
		'skpkd_json': json.dumps(skpd_ppkd),
		'bulanbulan': main.bulanbulan,
		'jenisjenis': jenisjenis,
		'jenisjenis_json': json.dumps({ e['id']:e for e in jenisjenis }),
		'laporan_href': (reverse_lazy(main.report_href_local) if main.is_anov_host else main.report_href(rq)),
		'laporan_pejabat': laporan_pejabat,
		'laporan_jenisakun': laporan.jenisakun(tahun),
		'laporan_jenisjenis': laporan.jenisjenis,
		'laporan_pejabat_json': json.dumps({ e['id']:e for e in laporan_pejabat }),
		'laporan_jenisjenis_json': json.dumps(laporan.jenisjenis),
	});
# 

# [DONE] #
def data(rq):
	global tahun, skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load();
	result = []

	try:
		cond = (
			tahun,
			rq.GET['bulan'],
			skpd_ppkd['kodeurusan'], skpd_ppkd['kodesuburusan'], skpd_ppkd['kodeorganisasi'], skpd_ppkd['kodeunit'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	try:
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.*, case when posting > 0 then 'hijau' else 'kuning' end as warna 
				from akuntansi.anov_jurnal_ppkd(%s,%s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			""", cond)
			qb.result_many(result)
	except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	return JsonResponse(result, safe=False);
# 

# [DONE] #
@require_GET
def rincian_update(rq):
	global tahun, skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	result = []

	try:
		cond = (
			tahun,
			skpd_ppkd['kodeurusan'],skpd_ppkd['kodesuburusan'],skpd_ppkd['kodeorganisasi'],skpd_ppkd['kodeunit'],
			rq.GET['noref'],
			isskpd,
		)
	except Exception as xcp: return HttpResponseServerError('%s undefined' % xcp, content_type='text/plain')

	with querybuilder() as qb:
		qb.execute("""
			SELECT a.*, b.kode_rekening, b.urai_rekening
			FROM akuntansi.akrual_buku_jurnal z
			JOIN akuntansi.akrual_jurnal_rincian a on (a.tahun = z.tahun
				AND a.kodeurusan = z.kodeurusan AND a.kodesuburusan = z.kodesuburusan 
				AND a.kodeorganisasi = z.kodeorganisasi AND a.kodeunit = z.kodeunit
				AND a.noref = z.noref AND a.isskpd = z.isskpd
			)
			JOIN akuntansi.anov_jurnal_rekening(a.tahun,a.kodeurusan,a.kodesuburusan,a.kodeorganisasi,
				a.kodeunit,a.kodebidang,a.kodeprogram,a.kodekegiatan,a.kodesubkegiatan) b on (
				b.kodeakun = a.kodeakun AND b.kodekelompok = a.kodekelompok AND b.kodejenis = a.kodejenis 
				AND b.kodeobjek = a.kodeobjek AND b.koderincianobjek = a.koderincianobjek AND b.kodesubrincianobjek = a.kodesubrincianobjek
			)
			WHERE a.tahun = %s
			AND z.kodeurusan = %s AND z.kodesuburusan = %s AND z.kodeorganisasi = %s
			AND z.kodeunit = %s AND z.noref = %s AND z.isskpd = %s
			ORDER BY a.tahun, a.urut
		""", cond)
		qb.result_many(result)

	return JsonResponse(result, safe=False)
#

# [TODO] #
@require_GET
def rincian_create(rq):
	global tahun,skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load(rq);


	try:
		result = [];

		nobukukas = rq.GET['nobukukas']
		nosp2d = rq.GET['nosp2d']

		jenis_bku = rq.GET['jenis_transaksi']
		jenissp2d = rq.GET['jenissp2d']

		cond = (
			tahun,
			skpd_ppkd['kodeurusan'],skpd_ppkd['kodesuburusan'],skpd_ppkd['kodeorganisasi'],skpd_ppkd['kodeunit'],
		);
		cond_1 = (tahun,jenis_bku,nosp2d,*cond[1:5])
		cond_2 = (tahun,jenis_bku,nobukukas,*cond[1:5])
	except Exception as xcp: return HttpResponseServerError('%s undefined' % xcp, content_type='text/plain')

	if jenis_bku == 'TIDAKCAIR':
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.* from akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian(%s, %s, %s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			""", cond_1)
			qb.result_many(result)
	else:
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.* from akuntansi.anov_akrual_to_jurnal_ppkd_ju_rincian(%s, %s, %s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			""", cond_2)
			qb.result_many(result)

	return JsonResponse(result, safe=False)
# 

# [DONE] #
@require_GET
def browse(rq):
	global tahun,skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	result = [];
	try:
		jenis_id = rq.GET['jenis_id'];
		jenis_pk = rq.GET['jenis_pk'];
		cond = (
			tahun,
			skpd_ppkd['kodeurusan'],skpd_ppkd['kodesuburusan'],skpd_ppkd['kodeorganisasi'],skpd_ppkd['kodeunit'],
		);
		cond_1 = (cond[0], rq.GET['bulan'], *cond[1:5])
	except Exception as xcp: return HttpResponseServerError('%s undefined' % xcp, content_type='text/plain')

	if jenis_pk == 'JU':
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.* from akuntansi.anov_jurnal_ppkd_ju_browse(%s,%s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s
				AND a.kodeunit = %s
			""", cond_1)
			qb.result_many(result)
	else: return HttpResponseServerError('unknown jenis_pk(%s)' % jenis_pk, content_type='text/plain')

	return JsonResponse(result, safe=False)
# 

# [DONE] #
@require_GET
def rekening_default(rq):
	global tahun,skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	result = [];
	try:
		jenis_id = rq.GET['jenis_id'];
		jenis_pk = rq.GET['jenis_pk'];
		cond = (
			tahun,
			skpd_ppkd['kodeurusan'],skpd_ppkd['kodesuburusan'],skpd_ppkd['kodeorganisasi'],skpd_ppkd['kodeunit'],
		);
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	if jenis_pk == 'JPLRA':
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.* from akuntansi.anov_jurnal_ppkd_penutup_lra(%s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			""", cond)
			qb.result_many(result)

	elif jenis_pk == 'JPLO':
		with querybuilder() as qb:
			qb.execute("""
				SELECT a.* from akuntansi.anov_jurnal_ppkd_penutup_lo(%s) a
				WHERE a.kodeurusan = %s AND a.kodesuburusan = %s AND a.kodeorganisasi = %s AND a.kodeunit = %s
			""", cond)
			qb.result_many(result)

	else: return HttpResponseServerError('unknown jenis_pk(%s)' % jenis_pk, content_type='text/plain')

	return JsonResponse(result, safe=False)
# 

# [DONE] #
@require_GET
def rekening(rq,is_return=True,result=None):
	global tahun,skpd_ppkd;
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if skpd_ppkd is None: skpd_ppkd_load();

	if result is None: result = [];
	try:
		cond = (
			tahun,
			skpd_ppkd['kodeurusan'], skpd_ppkd['kodesuburusan'], skpd_ppkd['kodeorganisasi'], skpd_ppkd['kodeunit'],
		)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	with querybuilder() as qb:
		qb.execute("""SELECT a.* FROM akuntansi.anov_jurnal_rekening(%s,%s,%s,%s,%s) a""", cond)
		qb.result_many(result);

	# print(result)

	if is_return: return JsonResponse(result, safe=False);
	else: return result;
# 

# [DONE] #
@require_POST
def save(rq):
	global tahun, jenisjenis, skpd_ppkd
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if jenisjenis is None: jenisjenis_load(rq);
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	default = {
		'tahun': rq.session['sipkd_tahun'],
		'username': rq.session['sipkd_username'],
		'isskpd': isskpd,
		'kodeurusan': skpd_ppkd['kodeurusan'],
		'kodesuburusan': skpd_ppkd['kodesuburusan'],
		'kodeorganisasi': skpd_ppkd['kodeorganisasi'],
		'kodeunit': skpd_ppkd['kodeunit'],
		'kodebidang': '{0}.{1}'.format(skpd_ppkd['kodeurusan'],str(skpd_ppkd['kodesuburusan']).zfill(2),),
		'kodeprogram': 0,
		'kodekegiatan': 0,
		'kodesubkegiatan': 0,
		'ispihakketiga': 0,
		'posting': 0,
	};

	try:
		__type__ = int(rq.POST['__type__'])
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	# parse post parameters #
	entry_item = {};
	entry_list = {};
	for k in rq.POST:
		if re.search(rincian_re_match, k):
			match = re.match(rincian_re_capture, k)
			group = rq.POST.getlist(rincian_re_replace.format(match.group(1), match.group(2)))

			if match.group(1) not in entry_list: entry_list[match.group(1)] = {}
			for g,n in enumerate(group):
				if g not in entry_list[match.group(1)]: entry_list[match.group(1)][g] = {}
				entry_list[match.group(1)][g][match.group(2)] = n

		elif k in jurnal_fields: entry_item[k] = rq.POST[k]
	# 

	for k in default:
		if k in jurnal_fields:
			if (k not in entry_item) or (k in entry_item and entry_item[k] == ''):
				entry_item[k] = default[k]
	# 

	try:
		with querybuilder('akuntansi.akrual_buku_jurnal') as qb:
			if __type__ == 0: qb.create(**entry_item);
			elif __type__ == 1: qb.update(*jurnal_primarykeys.keys(), **entry_item);
			else: return HttpResponseServerError('unknown __type__(%s)' % __type__, content_type='text/plain')

			if qb.context.rowcount < 1: return HttpResponseServerError('__type__(%s): tidak bisa simpan jurnal;' % __type__, content_type='text/plain')
	except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	# delete rincian
	with querybuilder('akuntansi.akrual_jurnal_rincian') as qb:
		rm = {}
		yn = True
		for a in jurnal_primarykeys.keys():
			if a in jurnalrincian_fields:
				rm[a] = entry_item[a]
			else: yn = False;
		if yn: qb.delete(**rm)
	# 

	# create rincian
	with querybuilder('akuntansi.akrual_jurnal_rincian') as qb:
		for t in entry_list:
			for e in entry_list[t]:
				auto = 'urut'; # seharusnya menjadi tanggungjawab database #
				if auto in jurnalrincian_fields and auto not in entry_list[t][e]:
					entry_list[t][e][auto] = int(e) + 1;

				# copas item
				for a in entry_item:
					if a in jurnalrincian_fields and a not in entry_list[t][e]:
						entry_list[t][e][a] = entry_item[a]

				# copas default
				for a in default:
					if a in jurnalrincian_fields:
						if (a not in entry_list[t][e]) or (a in entry_list[t][e] and entry_list[t][e][a] == ''):
							entry_list[t][e][a] = default[a]

				qb.create(**entry_list[t][e])
	#	#	#

	return HttpResponse(None)
# 

# [TODO] #
@require_POST
def posting(rq):
	global tahun, jenisjenis, skpd_ppkd
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if jenisjenis is None: jenisjenis_load(rq);
	if skpd_ppkd is None: skpd_ppkd_load(rq);
	try:
		cond = { 'tahun': tahun, 'isskpd': isskpd, 'posting': rq.POST['posting'], }

		for pk in jurnal_primarykeys.keys():
			if pk not in cond:
				cond[pk] = rq.POST[pk]

		noref = cond['noref'].split(',');
		noref = list(filter(None, noref));
	except Exception as xcp: return HttpResponseServerError('%s undefined' % xcp, content_type='text/plain')

	for i in range(len(noref)):
		cond['noref'] = noref[i]
		try:
			with querybuilder('akuntansi.akrual_buku_jurnal', *jurnal_primarykeys.keys(), **cond) as qb: qb.update()
			with querybuilder('akuntansi.akrual_jurnal_rincian', *jurnal_primarykeys.keys(), **cond) as qb: qb.update()
		except Exception as xcp: return HttpResponseServerError(xcp, content_type='text/plain')

	return HttpResponse('ok', content_type='text/plain')
#

# [DONE] #
@require_POST
def destroy(rq):
	global tahun, jenisjenis, skpd_ppkd
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	if jenisjenis is None: jenisjenis_load(rq);
	if skpd_ppkd is None: skpd_ppkd_load(rq);

	cond = {
		'tahun': tahun,
		'isskpd': isskpd,
	}

	try:
		for pk in jurnal_primarykeys.keys():
			if pk not in cond: cond[pk] = rq.POST[pk]

		noref = cond['noref'].split(',');
		noref = list(filter(None, noref));
	except Exception as xcp: return HttpResponseServerError('%s undefined' % xcp, content_type='text/plain')

	for i in range(len(noref)):
		cond['noref'] = noref[i]
		try:
			with querybuilder('akuntansi.akrual_buku_jurnal', **cond) as qb: qb.delete()
		except Exception as xcp: return HttpResponseServerError(xcp, content_type='text/plain')

	return HttpResponse('ok', content_type='text/plain')
#

# [DONE] #
@require_GET
def norefauto(rq, is_return=True, result=None):
	global tahun;
	if tahun is None: tahun = rq.session['sipkd_tahun'];

	try: cond = (tahun, isskpd,)
	except Exception as err: return HttpResponseServerError('%s undefined' % err, content_type='text/plain')

	with querybuilder() as qb:
		qb.execute("""
			SELECT 
			LPAD(
				(COALESCE(MAX( SUBSTRING(a.noref, '[0-9]+')::INTEGER ), 0) + 1)::VARCHAR,
				'{0}'::INTEGER,
				'{1}'::VARCHAR
			)
			FROM akuntansi.akrual_buku_jurnal a WHERE a.tahun = %s AND a.isskpd = %s
		""".format(norefauto_length, norefauto_prefix,), cond)
		result = qb.context.fetchone()[0];

	if is_return: return HttpResponse(result, content_type='text/plain');
	else: return result;
# 

# [DONE] #
def jenisjenis_load(rq=None):
	global jenisjenis
	jenisjenis = []

	"""
	(20190708) karena "akuntansi.akrual_jenis_jurnal" hanya sebagai opsi saja,
	jadi tidak mengacu pada "isskpd".
	"""
	with querybuilder('akuntansi.akrual_jenis_jurnal', isskpd=('IS NOT', None,)) as qb:
		qb.read_sort('id').read().result_many(jenisjenis)

		"""
		(20190704) karena saya males,
		"jenis_transaksi" saya ambil singkatan dari teks pada jenisjurnal,
		jadi saya tidak perlu hardcoded "jenis_transaksi" pada skrip py maupun js.
		"""
		for i in range(len(jenisjenis)):
			if 'isskpd' in jenisjenis[i]: del jenisjenis[i]['isskpd']
			pk = re.findall('\((\w+)\)', jenisjenis[i]['uraian'])
			jenisjenis[i]['pk'] = pk[0] if len(pk) > 0 else None;
# 

# [DONE] #
def skpd_ppkd_load(rq=None):
	global tahun, skpd_ppkd
	if tahun is None: tahun = rq.session['sipkd_tahun'];
	skpd_ppkd = {}

	with querybuilder('master.master_organisasi') as qb:
		qb.read(tahun=tahun, kodeorganisasi=('<>', ''), skpkd=isskpd).result_one(skpd_ppkd)
	# print(skpd_ppkd) 
# 
