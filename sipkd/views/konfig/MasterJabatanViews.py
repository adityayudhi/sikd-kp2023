from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from ..config import *
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from support.support_sipkd import *

def masterjabatan(request):
	jenissistem = request.GET.get('jenissistem', None)
	urut = request.GET.get('urut', None)
	urai = request.GET.get('urai', None)


	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT * FROM master.masterjabatan where jenissistem='2' and isskpd='0' order by urut asc")
	jabatan_list = dictfetchall(cursor)
	data = {
	'jenissistem': jenissistem,
	'urut': urut,
	'urai': urai,
	'jabatan_list':jabatan_list
	}
	return render(request, 'konfig/masterjabatan.html', data)

def get_listJabatan(request):
	isskpd = request.GET.get('idnya', None)
	id_table = ''
	if isskpd=='0':
		id_table = '0'
	elif isskpd=='1':
		id_table = '1'
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM master.masterjabatan where jenissistem='2' and isskpd=%s order by urut asc",[isskpd])
		jabatan_list = dictfetchall(cursor)

	data = {
	'jabatan_list':jabatan_list,
	'id_table':id_table
	}
	return render(request, 'konfig/tabel/Jabatan.html', data)


def save_jabatan(request):
	if request.method == 'POST':	
		
		action = request.POST['act']		
		if action == 'add':
			namajabatan = request.POST['nmjabatan']
			kodejabatan = request.POST['kdjabatan']
			if request.POST['jns_pejabat2'] == 'PEJABAT SKPD':
				jenis = 0
			elif request.POST['jns_pejabat2'] == 'PEJABAT SKPKD':
				jenis = 1
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO MASTER.MASTERJABATAN (jenissistem,isskpd,urut,urai)"\
					" VALUES (%s,%s,%s,%s)",['2', jenis, kodejabatan,namajabatan])
			messages.success(request, "Data Jabatan Berhasil Disimpan")
		elif action == 'edit':
			kodejabatan = request.POST['kdjab']
			namajabatan = request.POST['nmjabatan']
			if request.POST['jenis'] == 'PEJABAT SKPD':
				jenis = 0
			elif request.POST['jenis'] == 'PEJABAT SKPKD':
				jenis = 1	
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE MASTER.MASTERJABATAN SET urai=%s WHERE isskpd=%s and urut=%s and jenissistem=2",[str(namajabatan),jenis,kodejabatan])
			messages.success(request, 'Data Jabatan Berhasil Diubah')

	return HttpResponseRedirect(reverse('sipkd:masterjabatan'))

def updatejabatan(request):
	kodejabatan = request.GET.get('jabatan',None)	
	isskpd =  request.GET.get('isskpd',None)	
	# print(isskpd)
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT * FROM master.masterjabatan where jenissistem='2' and urut=%s and isskpd=%s order by urut asc",[kodejabatan,isskpd])
	list_jabatan = dictfetchall(cursor)
	data = {'list_jabatan':list_jabatan}
	# print(list_jabatan)
	return JsonResponse(data)

def hapus_jabatan(request):
    urut = request.GET.get('id')
    isskpd = request.GET.get('jenis')
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM master.masterjabatan WHERE urut=%s and isskpd=%s and jenissistem='2'", [urut,isskpd])
        messages.success(request, 'Jabatan Berhasil di hapus')
    return redirect('sipkd:masterjabatan')


def jabatanmodal(request):
	action = request.GET.get('act', None)
	id_jabatan = request.GET.get('id', None)
	tahun = tahun_log(request)

	if action == 'add':
		if id_jabatan == '0':
			id_jabatan = select_jabatan_skpd('master.masterjabatan','urut','jenissistem','isskpd',tahun)
			if id_jabatan == None:
				id_jabatan = 1
			else:
				id_jabatan = id_jabatan+1
		elif id_jabatan == '1':

			id_jabatan = select_jabatan_skpkd('master.masterjabatan','urut','jenissistem','isskpd',tahun)
			if id_jabatan == None:
				id_jabatan = 1
			else:
				id_jabatan = id_jabatan+1
	data = {
		'action':action,
		'id_jabatan':id_jabatan,
	}

	return render(request, 'konfig/modal/jabatan.html', data)