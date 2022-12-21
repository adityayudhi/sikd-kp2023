"""
menjalankan fastreport dari python secara standalone.
cara pake, pada "settings.py" buat "FASTREPORT_DIR",
yaitu ABSOLUTE_PATH yang mengarah ke direktori fastreport.

@reference https://git.gi.co.id/adityayudhi/sipkd1/blob/master/sipkd/views/spjskpd/views/main.py
@version 20190903,20191126193412,20191212
@author anovsiradj
"""

import io,os,re,urllib,hashlib,pathlib,datetime,platform,subprocess
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse,StreamingHttpResponse
from django.views import (View as CommonView)

# deteksi sistem operasi #
is_win = True if re.match('win|wow', platform.system().lower()) is not None else False
is_tux = False if is_win else True

# skrip untuk menampilkan fastreport #
class FastReportView(CommonView):
	report_type_default = 'PDF'
	report_type = {
		'TXT': 'text/plain',
		'PDF': 'application/pdf',
		'XLS': 'application/vnd.ms-excel',
		'XML': 'application/vnd.ms-excel',
	}

	# gawe koyo ngene supaya flexible, arep nggo GET opo POST terserah. #
	def get(self,request,*args,**kwargs):  return self.execute(request,*args,**kwargs)
	def post(self,request,*args,**kwargs): return self.execute(request,*args,**kwargs)

	def http_request_merge(self,request):
		result = {}
		for k,v in request.POST.items(): result[k] = v
		for k,v in request.GET.items(): result[k] = v
		return result

	def execute(self,request,*args,**kwargs):
		result = None

		params = self.http_request_merge(request)
		params_required = ['file','report_type','tahun']
		if any(params.get(i,None) == None for i in params_required):
			result = 'params: ' + str(params_required) + ' is required;'

		debug = True if ('debug' in params and params['debug'] == '1') else False

		report_type = params['report_type'].strip().upper()
		if report_type not in self.report_type:
			report_type = self.report_type_default
			result = 'undefined report_type: %s;' % params['report_type']
		report_type = 'TXT' if debug else report_type

		if result == None:
			result = generate(params)

			# urung reti carane konversi bytes dadi string secara literally #
			if debug: result = str(result.read1(-1)) # ASU #

		# le nampilke result kudu streaming supaya cepet #
		if result: return StreamingHttpResponse((result), content_type=self.report_type[report_type])
		return HttpResponse(None)
	# 
# 

# skrip untuk generate fastreport #
def generate(params):
	prefix = settings.FASTREPORT_DIR+'/'+params['tahun_console']

	params_name = hashlib.md5((str(datetime.datetime.now())).encode('utf-8')).hexdigest()
	params_name = str('fastreport.%s.tmp' % params_name)
	params_file = os.path.join(prefix, params_name)
	params_data = urllib.parse.urlencode(params)
	param_tahun_console = params['tahun_console']

	with open(params_file, 'w') as fs: fs.write(params_data)

	fastreport_commands = []
	if is_tux:
		fastreport_commands.append('env DISPLAY=:69') # STANDARD INTRUKSI PPR #
		fastreport_commands.append('env HOME=%s/html/sipkd' % pathlib.Path.home())
		fastreport_commands.append('env WINEDEBUG=-all')
		fastreport_commands.append('wine')
	fastreport_commands.append(f'/var/www/html/sikd-kp2023/report_sikd/{param_tahun_console}/ReportServerConsole.exe')
	commands = fastreport_commands[:]
	commands.append(params_name)
	command = ' '.join(commands)

	# https://en.wikipedia.org/wiki/Working_directory
	cwd = os.getcwd()

	os.chdir(prefix)
	result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	os.chdir(cwd)

	# concat stderr karo stdout supaya gampang le debug #
	result = result.stderr + result.stdout
	result = io.BytesIO(result)

	if os.path.exists(params_file): os.unlink(params_file)
	return result
# 
