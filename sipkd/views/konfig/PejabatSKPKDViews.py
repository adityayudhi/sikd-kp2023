from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..config import *
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

# list pejabat skpkd
def pejabatskpkd(request):
	# pejabat skpkd	
	tahun = tahun_log(request)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from master.PEJABAT_SKPKD where tahun= %s and jenissistem=2 ORDER BY id ASC", [tahun])
		pejabat_skpkd = dictfetchall(cursor)

	# master jabatan
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from master.MASTERJABATAN where isskpd=1 and jenissistem=2 order by urut")
		master_jabatan = dictfetchall(cursor)		

	data = {'pejabat_skpkd': pejabat_skpkd, 'master_jabatan':master_jabatan}
	return render(request, 'konfig/pejabatskpkd.html', data)
	

# combo pejabat skpkd
def combopejabatskpkd(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("select urai from master.masterjabatan where isskpd=1 and jenissistem = 2 order by urut")
        ms_jbtn = dictfetchall(cursor)

    aidi = request.GET.get('id', None)
    urai_jbtn = ""
    for result in ms_jbtn:
        urai_jbtn += "<option value='" + result['urai'] + "'>" + result['urai'] + "</option>"

    combo = "<select class='dropdown-in-table' id='jabatan_" + aidi + "' name='jabatan'>"\
       "<option value='0'>-- Silahkan Pilih --</option>" + urai_jbtn + "</select>"

    return HttpResponse(combo)

# tambah pejabat skpkd
def addpejabatskpkd(request):
	action = request.GET.get('act')
	idpejabat = request.GET.get('id')
	namapejabat = nip = pangkat = jabatan =''
	tahun = tahun_log(request)
	
	# master jabatan
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from master.MASTERJABATAN where isskpd=1 and jenissistem=2 order by urut")
		master_jabatan = dictfetchall(cursor)

	if action == 'edit'	:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from master.PEJABAT_SKPKD where tahun= %s and jenissistem=2 and id=%s", [tahun,idpejabat])
			hasil = dictfetchall(cursor)
			for result in hasil:
				idpejabat = result['id']
				namapejabat = result['nama']
				nip = result['nip']
				pangkat = result['pangkat']
				jabatan = result['jabatan']	

	data = {
		'idpejabat': idpejabat, 
		'master_jabatan':master_jabatan,
		'action' : action,
		'namapejabat' : namapejabat,
		'nip' : nip,
		'pangkat' : pangkat,
		'jabatan' : jabatan
	}
	return render(request, 'konfig/modal/pejabatskpkd.html', data)

# simpan
def saveskpkd(request):	
	# post method
	if request.method == 'POST':	
		action = request.POST.get('action')	
		tahun = tahun_log(request)
		aidi = request.POST.get('id')
		nama = request.POST.get('namapejabat')
		nip = request.POST.get('nip')
		pangkat = request.POST.get('pangkat')
		jabatan = request.POST.get('jabatan')	

		if(nama!=""):
			if action == 'add':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO master.PEJABAT_SKPKD (TAHUN,NAMA,PANGKAT,JABATAN,NIP,jenissistem)"\
						"VALUES (%s,%s,%s,%s,%s,%s)",[tahun, nama, pangkat, jabatan, nip, '2'])
				# notif success
				messages.success(request, "Data berhasil disimpan!")
			elif action == 'edit':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("UPDATE master.PEJABAT_SKPKD set tahun=%s, nama=%s, pangkat=%s, jabatan=%s, nip=%s where id=%s",
					[tahun, nama, pangkat, jabatan, nip, aidi])
				# notif success
				messages.success(request, "Data berhasil diubah!")
		return HttpResponseRedirect(reverse('sipkd:pejabatskpkd'))

# hapus pejabatskpkd
def deletepejabatskpkd(request):
	# get id
	aidi = request.GET.get('id')
	tahun = tahun_log(request)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM master.PEJABAT_SKPKD where tahun=%s and id=%s",[tahun,aidi])
	messages.success(request, "Data berhasil dihapus!")
	return HttpResponseRedirect(reverse('sipkd:pejabatskpkd'))

