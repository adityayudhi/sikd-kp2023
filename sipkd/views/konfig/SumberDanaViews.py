from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages
from support.support_function import *

def sumberdana(request):
	list_dana = ''
	no = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM master.sumberdanarekening order by kodesumberdana ASC")
		list_dana = dictfetchall(cursor)
		for x in range(len(list_dana)):
			list_dana[x].update({"no": x})
	data = {'list_dana':list_dana,'no':no}
	return render(request, 'konfig/sumberdana.html', data)

def savesumberdana(request):
	idnya = request.GET.get('id', None)
	act = request.GET.get('act', None)

	if act == 'del':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM master.master_sumberdana WHERE kodesumberdana=%s",[idnya])
		messages.success(request, "Data Sumberdana berhasil dihapus!")

	if request.method == 'POST':
		action = request.POST.get('action',None)
		uraian_dana = request.POST.get('sumberdana',None)
		id_dana = request.POST.get('kode_sumberdana',None)
		if action=='add':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO master.master_sumberdana (kodesumberdana,urai) VALUES (%s,%s)",[id_dana,uraian_dana])
			messages.success(request, "Data Sumberdana berhasil Disimpan!")
		elif action=='edit':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE master.master_sumberdana SET urai=%s WHERE kodesumberdana=%s",[uraian_dana,id_dana])
			messages.success(request, "Data Sumber dana berhasil Diubah!")
	return HttpResponseRedirect(reverse('sipkd:sumberdana'))

def sumberdanamodal(request):
	action = request.GET.get('act', None)
	id_dana = request.GET.get('id', None)
	uraian_dana = ''

	if action == 'add':
		id_dana = select_max_dana('master.master_sumberdana','kodesumberdana')
		if id_dana == None:
			id_dana = 1
		else:
			id_dana = id_dana+1
	elif action == 'edit':
		uraian_dana = get_data_with_dana('master.master_sumberdana','kodesumberdana',id_dana)[1]
		
	data = {
		'action':action,
		'id_dana':id_dana,
		'uraian_dana':uraian_dana
	}
	return render(request, 'konfig/modal/sumberdana.html',data)