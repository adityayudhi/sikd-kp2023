import io
import os
import re
import time
import math
import urllib
import hashlib
import datetime
import configparser
from django.conf import settings
from django.urls import reverse
from django.http import (
	HttpResponse,
	JsonResponse,
	FileResponse,
	StreamingHttpResponse,
	HttpResponseRedirect,
	HttpResponseServerError,
)
from django.views.decorators.http import (
	require_GET,
	require_POST,
)
from sipkd import config as cfg
from ..anov import *
from sipkd.config import *

def report_href(request):
	report_href = cfg.laplink(request, {0:1}).replace('?0=1', '').replace('&', '?')
	return report_href

report_href_local = 'sipkd:spjskpd_main_report'

# # --- EXECUTE.SQL.START --- #
# if True:
# 	now = time.time()
# 	age = 300 if is_anov_host else math.inf # 604800 # 3600 # 5min|1w/1h/forever
# 	storedprocedures = [
# 		'99.sql',
# 		'01.sql',
# 		'05.sql',
# 		'07.sql',
# 		'06.sql',
# 		'08.sql','09.sql','10.sql','11.sql',
# 	]
# 	for storedprocedure in storedprocedures:
# 		path = os.path.join(os.path.dirname(__file__), '../storedprocedures/', storedprocedure)
# 		delta = now - os.path.getmtime(path)
# 		if delta <= age:
# 			print('# --- EXECUTE:', path, '; --- #')
# 			with open(path, 'r') as fs:
# 				with querybuilder() as qb:
# 					try: qb.execute(fs.read());
# 					except Exception as xcp: raise xcp;
# # --- EXECUTE.SQL.STOP --- #

isskpd = 0
jenissistem = 2
bulanbulan = {int(k):v for k,v in cfg.arrBulan.items()}
# form_token_name = 'csrfmiddlewaretoken'

bku_primarykeys = []; bkurincian_primarykeys = [];
bku_fields = {}; bkurincian_fields = {};
with querybuilder() as qb:
	qb.info_columns('pertanggungjawaban','skpd_bku', bku_fields)
	qb.info_columns('pertanggungjawaban','skpd_bkurincian', bkurincian_fields)
	qb.info_primarykeys('pertanggungjawaban', 'skpd_bku', bku_primarykeys)
	qb.info_primarykeys('pertanggungjawaban', 'skpd_bkurincian', bkurincian_primarykeys)

@require_GET
def potongan(rq):
	data = []
	cond = {
		'kodejenis': ('IN','(1,3)'),
		'kodeobjek': ('IS NOT NULL',''),
		'koderincianobjek': ('<>','0'),
		'kodesubrincianobjek': ('<>','0'),
	}
	for k in rq.GET:
		m = re.match('(\w+)\[\]', k)
		if m: cond[m.group(1)] = rq.GET.getlist(k)
		else: cond[k] = ('=', rq.GET[k])

	with querybuilder() as qb:
		qb.execute("""
			SELECT
			a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek,
			(
				a.kodeakun|| '.' ||a.kodekelompok|| '.' ||a.kodejenis|| '.' ||
				LPAD(a.kodeobjek::text,2,'0')||'.'||LPAD(a.koderincianobjek::text,2,'0')||'.'||LPAD(a.kodesubrincianobjek::text,4,'0')
			) AS kode_rekening,
			a.urai AS urai_rekening
			FROM master.master_rekening a WHERE a.tahun = %s
			AND a.kodeakun = 2 AND a.kodekelompok = 1
			AND a.kodejenis {kodejenis[0]} {kodejenis[1]}
			AND a.kodeobjek {kodeobjek[0]} {kodeobjek[1]}
			AND a.koderincianobjek {koderincianobjek[0]} {koderincianobjek[1]}
			AND a.kodesubrincianobjek {kodesubrincianobjek[0]} {kodesubrincianobjek[1]}
			ORDER BY a.kodeakun,a.kodekelompok,a.kodejenis,a.kodeobjek,a.koderincianobjek,a.kodesubrincianobjek
		""".format(**cond), (rq.GET['tahun'],))
		qb.result_many(data)

	return JsonResponse(data, safe=False)
# 

@require_GET
def pejabat(request):
	required = ['tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi']
	condition = {'jenissistem': jenissistem}
	result = []

	for k in required:
		try: condition[k] = request.GET[k]
		except Exception as err: return HttpResponseServerError(err, content_type='text/plain')

	with querybuilder('master.pejabat_skpd', **condition) as qb:
		qb.read_sort('tahun', 'kodeurusan', 'kodesuburusan', 'kodeorganisasi', 'id')
		qb.read()
		qb.result_many(result)

	return JsonResponse(result, safe=False)
#

@require_GET
def skpd(request):
	required = ['tahun','kodeurusan','kodesuburusan','kodeorganisasi','kodeunit','skpkd']
	condition = {'kodeorganisasi': ('<>', '',)}
	result = []

	for k,v in request.GET.items():
		if k in required:
			if k in condition:
				del condition[k]
			condition[k] = v

	with querybuilder('master.master_organisasi', **condition) as qb:
		qb.read_sort(*required[:-1])
		qb.read()
		qb.result_many(result)

	return JsonResponse(result, safe=False)
# fed

@require_GET
def nobkuauto(request, is_return=True, result=None):
	if result == None: result = 1;
	with querybuilder() as qb:
		qb.execute("""
			SELECT coalesce(max(a.no_bku),0)+1
			FROM pertanggungjawaban.skpd_bku a WHERE a.tahun = %s
			and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
			and a.isskpd = %s
		""", (
			request.GET['tahun'],
			request.GET['kodeurusan'],request.GET['kodesuburusan'],request.GET['kodeorganisasi'],request.GET['kodeunit'],
			request.GET['isskpd'],
		))
		result = qb.context.fetchone()[0];

	if is_return: return HttpResponse(result, content_type="text/plain");
	else: return result;
# fed

report_prefix = None
report_config = None
report_arguments = None

def report_init(rq):
	global report_prefix, report_config, report_arguments

	report_prefix = os.path.join(
		os.path.dirname(__file__),
		'../../../../../..',
		'mbamad-20190410-report/reportsvc_sipkd',
	)
	report_prefix = '/var/www/sikd-django/mbamad-20190410-report/reportsvc_sipkd/'
	report_prefix = os.path.abspath(report_prefix)
	report_config = os.path.join(report_prefix,'konfig.ini')
	report_arguments = [
		# 'export',
		'HOME=/var/www/winereportservice/py',
		'LANG=en_US',
		'WINEARCH=win32',
		'WINEDEBUG=-all',
		# kalo pake WINEDLLOVERRIDES, wine ndak bisa baca exe nya.
		# 'WINEDLLOVERRIDES="winemenubuilder.exe=d"'
		# 'WINEDLLOVERRIDES="winemenubuilder.exe=d,mscoree,mshtml="'
		# ';', # export;
		# 'xvfb-run -a',
		'wine',
		# os.path.join(report_prefix,'ReportServerConsole.exe'),
		'ReportServerConsole.exe',
	]

	db = settings.DATABASES['default']
	report_config_ = 'ReportServer'
	report_config_0 = configparser.ConfigParser()
	report_config_0[report_config_] = {
		'AutoStartServer': 'Y',
		'databaseName': db['NAME'],
		'uName': db['USER'],
		'pwd': db['PASSWORD'],
		'port': db['PORT'],
		'server': db['HOST'],
		'driver': db['ENGINE'].split('.')[-1]
	}
	report_config_1 = configparser.ConfigParser()

	if os.path.exists(report_config):
		# ubah konfig, jika konfigurasi database report tidak-sama-dengan aplikasi
		report_config_1.read(report_config)
		hmm = False
		for n in report_config_0[report_config_]:
			if report_config_1[report_config_][n] != report_config_0[report_config_][n]:
				hmm = True
				report_config_1[report_config_][n] = report_config_0[report_config_][n]
		if hmm:
			with open(report_config, 'w') as fs:
				report_config_1.write(fs)
	else:
		# buat konfig
		with open(report_config, 'w') as fs:
			report_config_0.write(fs)
	# 
# 

"""
from sipkd.views.spjskpd.views import main
main.report(None)
"""

import subprocess

def report(rq, is_save=None):
	report_init(rq)

	report_type_origin = None
	report_type_active = None
	report_type = {
		# 'TXT': 'text/plain',
		'PDF': 'application/pdf',
		'XLS': 'application/vnd.ms-excel',
		'XML': 'application/vnd.ms-excel',
	}
	if rq and 'report_type' in rq.GET:
		report_type_origin = ('%s' % rq.GET['report_type']).strip().upper()
		if report_type_origin in report_type:
			report_type_active = report_type_origin

	arguments = report_arguments[:]
	parameters_file = hashlib.md5(('%s' % datetime.datetime.now()).encode('utf-8')).hexdigest()
	parameters_file = 'report.%s.txt' % parameters_file
	parameters_path = os.path.join(report_prefix, parameters_file)
	parameters = urllib.parse.urlencode(rq.GET) if rq else ''

	# buat file parameter report #
	with open(parameters_path, 'w') as fs: fs.write(parameters)

	arguments.append('%s' % parameters_path)
	arguments_str = ' '.join(arguments)

	os.chdir(report_prefix) # ubah CWD (current working directory) ke lokasi *.exe

	result = dick(stderr='', stdout='',)
	result = subprocess.run(arguments_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,) # eksekusi dan tangkap std*nya #
	# subprocess.call(' '.join(arguments), shell=True) # eksekusi stream/background/langsung dari cmd #

	# hapus file parameter report #
	if os.path.exists(parameters_path): os.unlink(parameters_path)

	fb0 = result.stderr + result.stdout
	fb1 = io.BytesIO(fb0) # konversi bytes mentah menjadi io-bytes #

	# simpan dalam bentuk file #
	if is_save: 
		with open('%s.%s' % (parameters_path, str(report_type_origin).lower(),), 'wb') as fs:
			fs.write(fb0)

	"""
	ingat
	StreamingHttpResponse harus eksekusi secara langsung,
	tidak boleh lewat variable.
	"""
	if rq:
		if report_type_active: return StreamingHttpResponse(fb1, content_type=report_type[report_type_active],)
		else: return StreamingHttpResponse(fb1,)
#
