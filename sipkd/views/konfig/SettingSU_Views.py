from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

def setting_hakakses(request):
	if request.method == 'POST':
		post 	= request.POST
		akses 	= post.get("jns_hakakses")
		x = post.getlist("modulelist",0)
		y = post.getlist("listpilih",0)
		z = post.getlist("listsub",0)

		if(x != 0):
			moduls 	= "''"+"'',''".join(map(str,x))+"''"
		else: moduls = "''0''"
		if(y != 0): 
			menuls   = "''"+"'',''".join(map(str,y))+"''"
			fil_menu = ", listpilih = ""'"+menuls+"'"""
		else: fil_menu = ", listpilih = '''0.0'''"
		if(z != 0): 
			listsub = "''"+"'',''".join(map(str,z))+"''"
			fil_sub = ", listsub = ""'"+listsub+"'"""
		else: fil_sub = ", listsub = '''0.0.0.0'''"

		sqlku = "UPDATE PENATAUSAHAAN.HAKAKSES SET modulelist = ""'"+moduls+"'"" "+fil_menu+fil_sub+" "\
			"WHERE hakakses = %s "

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute(sqlku,[akses])

		return HttpResponse("Perubahan data Hak Akses berhasil disimpan.")

	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT DISTINCT(hakakses),* FROM PENATAUSAHAAN.HAKAKSES ORDER BY hakakses ASC")
			dt_akses = dictfetchall(cursor)

			# SELECT ROW_NUMBER () OVER (ORDER BY hakakses) as nomor,* FROM PENATAUSAHAAN.HAKAKSES "\
			# 	"ORDER BY hakakses ASC

		data = {'page':'akses','judpage':'HAK AKSES','dt_akses':dt_akses}
		return render(request, 'konfig/setting_sup_us.html',data)

def tabel_setting_hakakses(request):

	gets = request.GET.get("id")

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM PENATAUSAHAAN.HAKAKSES WHERE hakakses = %s ",[gets])
		ls_aks = dictfetchall(cursor)

		for dat in ls_aks:
			modulelist = dat["modulelist"]
			listpilih  = dat["listpilih"]
			listsub    = dat["listsub"]

		cursor.execute("SELECT ROW_NUMBER () OVER (ORDER BY id_modul,id_menu,id_menu_sub) as nomor, id_modul,id_menu,id_menu_sub, "\
			"(case when id_menu = 0 and id_menu_sub = 0 then id_modul::varchar "\
			"when id_menu <> 0 and id_menu_sub = 0 then id_modul||'.'||id_menu "\
			"else id_modul||'.'||id_menu||'.'||id_menu_sub end ) as kode, "\
			"(case when id_menu = 0 and id_menu_sub = 0 then 'modulelist' "\
			"when id_menu <> 0 and id_menu_sub = 0 then 'listpilih' else 'listsub' end ) as jenis, "\
			"(case when id_menu = 0 and id_menu_sub = 0 and id_modul in ("+modulelist+") then 'checked=\"checked\"' "\
			"when id_menu <> 0 and id_menu_sub = 0 and id_modul||'.'||id_menu in ("+listpilih+") then 'checked=\"checked\"' "\
			"when id_menu_sub <> 0 and id_modul||'.'||id_menu||'.'||id_menu_sub in ("+listsub+") then 'checked=\"checked\"' "\
			"else '' end) as sts_chk, "\
			"(case when status is true then 'check-square' else 'times-circle' end) as mdl_chk, "\
			"(case when status is true then 'green' else 'red' end) as mdl_clr, "\
			"(case when status is true then 'Enable' else 'Disable' end) as mdl_sts, "\
			"uraian, class FROM PENATAUSAHAAN.SET_MENU "\
			"ORDER BY id_modul,id_menu,id_menu_sub,kode ASC")
		dt_akses = dictfetchall(cursor)

	data = {'page':'akses','dt_akses':dt_akses}
	return render(request, 'konfig/tabel/menu_akses.html',data)

def setting_menu(request):
	if request.method == 'POST':
		post = request.POST
		kode = post.get("kode_menu").split(".")
		arre = post.get("kode_menu").split(".")
		arre.insert(0,post.get("vale_menu"))
		jml  = len(kode)

		if(jml == 1):
			filtering = "WHERE id_modul = %s "
		elif(jml == 2):
			filtering = "WHERE id_modul = %s AND id_menu = %s "
		elif(jml == 3):
			filtering = "WHERE id_modul = %s AND id_menu = %s AND id_menu_sub = %s "

		if(post.get("aksi_menu") == 'sts'): 
			aksi = "Menu"
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE PENATAUSAHAAN.SET_MENU SET status = %s "+filtering, arre)

		elif(post.get("aksi_menu") == 'div'): 
			aksi = "Divider"
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE PENATAUSAHAAN.SET_MENU SET is_divider = %s "+filtering, arre)

		return HttpResponse("Perubahan data "+aksi+" telah disimpan.")

	else:
		data = {'page':'menus','judpage':'MENU'}
		return render(request, 'konfig/setting_sup_us.html',data)

def tabel_setting_menu(request):

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT (case when id_menu = 0 and id_menu_sub = 0 then id_modul::varchar "\
			"when id_menu <> 0 and id_menu_sub = 0 then id_modul||'.'||id_menu "\
			"else id_modul||'.'||id_menu||'.'||id_menu_sub end ) as kode, "\
			"id_modul||'.'||id_menu||'.'||id_menu_sub as kd_full, "\
			"(case when status is true then 'checked=\"checked\"' else '' end) as sts_chk, "\
			"(case when is_modal is true then 'check-square' else 'times-circle' end) as mdl_chk, "\
			"(case when is_modal is true then 'green' else 'red' end) as mdl_clr, "\
			"(case when is_modal is true then 'YES' else 'NO' end) as mdl_tit, "\
			"(case when is_divider is true then 'checked=\"checked\"' else '' end) as div_chk, "\
			"(case when is_divider is true then 'YES' else 'NO' end) as div_tit, "\
			"* FROM PENATAUSAHAAN.SET_MENU "\
			"ORDER BY id_modul,id_menu,id_menu_sub,kode ASC")
		dt_menu = dictfetchall(cursor)

	data = {'page':'menus','dt_menu':dt_menu}
	return render(request, 'konfig/tabel/menu_akses.html',data)

def modal_setting_menu(request):

	gets = request.GET.get("k",1)
	jml  = len(gets.split("."))

	if(jml == 1):
		filtering = "id_modul "
	elif(jml == 2):
		filtering = "id_modul||'.'||id_menu "
	elif(jml == 3):
		filtering = "id_modul||'.'||id_menu||'.'||id_menu_sub "

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from PENATAUSAHAAN.set_menu where "+filtering+" in (%s)",[gets])
		dt_menu = dictfetchall(cursor)

	# [{'id_modul': 5, 'id_menu': 5, 'id_menu_sub': 0, 'uraian': 'Persetujuan RKA', 'status': True, 
	# 'class': 'fa-check-square-o', 'modul': 'skpd', 'link_page': 'persetujuanrka', 'onclick': '-', 
	# 'is_modal': False, 'is_divider': True}]

	data = {'page':'modal', 'gets':dt_menu}
	return render(request, 'konfig/tabel/menu_akses.html',data)

def aweso_setting_menu(request):

	faikon = read_file_fa(request)

	data = {'page':'awesome', 'faikon':faikon}
	return render(request, 'konfig/tabel/menu_akses.html',data)