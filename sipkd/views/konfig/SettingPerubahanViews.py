from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..config import *
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from django.urls import reverse

# setting perubahan
def settingperubahan(request):
	# list perubahan
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select perubahansipkd from master.SETTINGTAHUN where tahun=%s",[tahun_log(request)])
		list_perubahan = dictfetchall(cursor)
	data = {'list_perubahan': list_perubahan}		
	return render(request,'konfig/settingperubahan.html',data)
	

# simpan perubahan
def editperubahan(request):	
	# method post		
	if request.method == 'POST':
		prbhn = request.POST.get('perubahan')
		if prbhn != '':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("update master.SETTINGTAHUN set perubahansipkd =%s where tahun=%s",
					[prbhn, tahun_log(request)])
		# redirect logout
		# messages.success(request, "Data berhasil disimpan!")
		return HttpResponseRedirect(reverse('sipkd:logout'))
	
