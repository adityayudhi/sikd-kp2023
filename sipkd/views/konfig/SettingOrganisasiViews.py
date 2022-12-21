from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages
from support.support_function import *
import json

def settingorganisasi(request):
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT KODEURUSAN, URAI FROM MASTER.MASTER_ORGANISASI WHERE TAHUN =%s AND KODESUBURUSAN='0' ORDER BY KODEURUSAN",[tahun_log(request)])
	masterorganisasi = dictfetchall(cursor)
	data = {'masterorganisasi': masterorganisasi}
	return render(request, 'konfig/settingorganisasi.html', data)

def listurusan(request):
	kodeurusan = request.GET.get('jnsurusan', None)
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT * FROM MASTER.MASTER_ORGANISASI where TAHUN =%s and kodeurusan =%s and kodesuburusan <>'0' and kodeorganisasi ='' order by kodeurusan asc",[tahun_log(request),kodeurusan])
	list_urusan = dictfetchall(cursor)
	data = {'list_urusan':list_urusan, 'kode_urusan':kodeurusan}
	return render(request, 'konfig/tabel/Suburusan.html', data)

def listsuburusan(request):
	kodesuburusan = request.GET.get('jnssuburusan', None)
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT * FROM MASTER.MASTER_ORGANISASI where TAHUN =%s and kodeurusan =%s and kodesuburusan <>'0' and kodeorganisasi ='' order by kodeurusan asc",[tahun_log(request),kodesuburusan])
	list_suburusan = dictfetchall(cursor)
	option = '<option value="0">-- PILIH ORGANISASI --</option>'
	for hasil in list_suburusan:
		option+='<option value="'+str(hasil['kodesuburusan'])+'">'+str(hasil['kodesuburusan'])+' - '+hasil['urai']+'</option>'
	data = {'list_suburusan':list_suburusan}
	return HttpResponse(option)

def listorganisasi(request):
	kodeorganisasi = request.GET.get('jnsorganisasi', None)
	kodeurusan = request.GET.get('jnsurusan', None)
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi, kodeunit, urai, alamat, notelp, nofax, email FROM master.master_organisasi where TAHUN =%s and kodesuburusan=%s and kodeurusan = %s and (kodeorganisasi<>'0' and kodeorganisasi<>'') order by kodesuburusan asc",[tahun_log(request),kodeorganisasi,kodeurusan])
	list_organisasi = dictfetchall(cursor)
	data = {'list_organisasi':list_organisasi}
	return render(request, 'konfig/tabel/Organisasi.html',data)

def listfungsi(request):

	action = request.GET.get('act')
	kodeurusan = request.GET.get('kodeurusan');
	# kodesuburusan = 1

	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT kodefungsi, urai FROM master.master_fungsi WHERE tahun =%s ORDER BY kodefungsi",[tahun_log(request)])
	list_fungsi = dictfetchall(cursor)

	if action == 'add':
		cursor.execute("select max(kodesuburusan) from master.master_organisasi where tahun=%s and kodeurusan=%s AND kodeorganisasi=''",[tahun_log(request), kodeurusan])
		kodeurusan_terakhir = cursor.fetchone()[0]
		kodeurusan = kodeurusan_terakhir + 1

	# cursor.execute("select max(kodeurusan) from master.master_organisasi where tahun=%s and kodeurusan=%s AND kodesuburusan=%s AND kodeorganisasi=''",[tahun_log(request), kodeurusan, kodesuburusan])

	data = {
		'list_fungsi':list_fungsi,
		'id_suburusan':kodeurusan,
	}
	
	return  render(request, 'konfig/modal/suburusan.html',data)
	
def urusanmodal(request):
	action = request.GET.get('act', None)
	id_urusan = request.POST.get('id', None)
	if action == 'add':
		id_urusan = select_max_id('master.master_organisasi','kodeurusan',tahun_log(request))
		if id_urusan == None:
			id_urusan = 1
		else:
			id_urusan = id_urusan+1
	elif action == 'edit':
		id_urusan = id_urusan

	data = {
		'action':action,
		'id_urusan':id_urusan,
	}
	return render(request, 'konfig/modal/urusan.html', data)

def suburusanmodal(request):
	return render(request, 'konfig/modal/suburusan.html')

def cek_urusan(request):
	kodeurusan = request.GET.get('kodeurusan', None)
	status = False
	message = ''
	with connections[tahun_log(request)].cursor() as cursor:
		try:
			cursor.execute("SELECT COUNT(*) FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN='0'", [tahun_log(request),kodeurusan])
			hasil = cursor.fetchone()[0]

			if(hasil ==0):
				message = 'Kode bisa digunakan'
				status = True
			else:
				message = 'Kode Urusan sudah ada'

		except:
			message = 'Terjadi kesalahan, silakan coba kembali'

	data = {
		'status' : status,
		'message' : message
	}
	return JsonResponse(data)

def cek_suburusan(request):
	kodeurusan = request.GET.get('kodeurusan', None)
	kodesuburusan =  request.GET.get('kodesuburusan',None)
	status = False
	message = ''
	with connections[tahun_log(request)].cursor() as cursor:
		try:
			cursor.execute("SELECT COUNT(*) FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s AND KODEURUSAN=%s and KODESUBURUSAN<>'0' AND KODEORGANISASI='' AND KODESUBURUSAN=%s", [tahun_log(request),kodeurusan, kodesuburusan])
			hasil = cursor.fetchone()[0]

			if(hasil ==0):
				message = 'Kode bisa digunakan'
				status = True
			else:
				message = 'Kode Suburusan sudah ada'

		except:
			message = 'Terjadi kesalahan, silakan coba kembali'

	data = {
		'status' : status,
		'message' : message
	}
	return JsonResponse(data)

def cek_organisasi(request):
	kodeurusan = request.GET.get('kodeurusan', None)
	kodesuburusan =  request.GET.get('kodesuburusan',None)
	kodeorganisasi = request.GET.get('kodeorganisasi', None)
	status = False
	message = ''
	with connections[tahun_log(request)].cursor() as cursor:
		try:
			cursor.execute("SELECT COUNT(*) FROM master.master_organisasi WHERE tahun=%s and kodeurusan =%s and kodesuburusan =%s and kodeorganisasi <>'0' and kodeorganisasi =%s",[tahun_log(request),kodeurusan,kodesuburusan,kodeorganisasi])
			hasil = cursor.fetchone()[0]

			if(hasil ==0):
				message = 'Kode bisa digunakan'
				status = True
			else:
				message = 'Kode Organisasi sudah ada'

		except:
			message = 'Terjadi kesalahan, silakan coba kembali'
	data = {
		'status' : status,
		'message' : message
	}
	return JsonResponse(data)

def organisasimodal(request):
	return render(request, 'konfig/modal/organisasi.html')
    
def getorganisasi(request):
	action = request.GET.get('act')
	kodeurusan = request.GET.get('kodeurusan');
	kodesuburusan = request.GET.get('kodesuburusan');
	with connections[tahun_log(request)].cursor() as cursor:
		# cursor.execute("SELECT * FROM sipkd.fc_angg_view_cek_organisasi('2018',1,1,'1') ORDER BY kodebidang")
		cursor.execute("SELECT * FROM MASTER.MASTER_BIDANG WHERE TAHUN = %s ORDER BY KODEBIDANG",[tahun_log(request)])
		list_bidang = dictfetchall(cursor)
		if action == 'add':
			cursor.execute("select max(kodeorganisasi) from master.master_organisasi where tahun=%s and kodeurusan=%s AND kodesuburusan=%s AND kodeorganisasi<>'0'",[tahun_log(request), kodeurusan,kodesuburusan])
			kodeorganisasi_terakhir = cursor.fetchone()[0]
			try:
				kodeorganisasi = int(kodeorganisasi_terakhir) + 1
			except:
				kodeorganisasi = 1
		elif action == 'edit':
			# koding untuk edit, silakan
			kodeorganisasi = request.GET.get('kodeorganisasi')

		data = {
    		'list_bidang':list_bidang,
    		'id_organisasi':kodeorganisasi,
    	}
	return render(request, 'konfig/modal/organisasi.html',data)

def simpanurusan(request):
	if request.method == 'POST':
		
		namaurusan = request.POST['nmurusan']
		action = request.POST['act']

		if action == 'add':
			kodeurusan = request.POST['kdurusan']
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO MASTER.MASTER_ORGANISASI (tahun,kodeurusan,kodesuburusan,kodeorganisasi,urai)"\
					" VALUES (%s,%s,%s,%s,%s)",[tahun_log(request),kodeurusan, '0', '', namaurusan])
			messages.success(request, "Data Urusan Berhasil Disimpan")
		elif action == 'edit':
			kodeurusan = request.POST['kdurusan_lama2']
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE MASTER.MASTER_ORGANISASI SET urai=%s WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s",
					[namaurusan,tahun_log(request),kodeurusan, '0', ''])
			messages.success(request, 'Data Urusan Berhasil Diubah')

	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def simpansuburusan(request):
	if request.method == 'POST':
		kdurusan = request.POST['kdurusan']
		
		namasub = request.POST['nmsuburusan']
		jenis = request.POST['jnsfungsi']
		action = request.POST['act']
		
		if action == 'add':
			kodesuburusan = request.POST['kdsuburusan']
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO MASTER.MASTER_ORGANISASI (tahun,kodeurusan,kodesuburusan,kodeorganisasi,urai,fungsi)"\
					" VALUES (%s,%s,%s,%s,%s,%s)",[tahun_log(request), kdurusan, kodesuburusan, '', namasub,jenis])
			messages.success(request, "Data Sub Urusan Berhasil Disimpan")
		elif action == 'edit':
			kodesuburusan = request.POST['kdsub']
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute(
                    "UPDATE MASTER.MASTER_ORGANISASI SET urai=%s, fungsi=%s WHERE tahun=%s and kodeurusan=%s and kodeorganisasi=%s and kodesuburusan=%s",
                    [namasub, jenis, tahun_log(request), kdurusan, '', kodesuburusan])
			messages.success(request, 'Data Sub Urusan Berhasil Diubah')

	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def simpanorganisasi(request):
	if request.method == 'POST':
		kode_uru = request.POST['kduru']
		kode_sub = request.POST['kdsub']
		
		nama_org = request.POST['nmorg']
		alamat = request.POST['alamat']
		notelp = request.POST['notelp']
		nofax = request.POST['nofax']
		email = request.POST['email']
		skpkd = request.POST.get('skpkd', 0)
		act = request.POST['act']

		if act =='add':
			kode_org = request.POST['kdorg']
			kode_bid = request.POST.getlist('kode_bidang')
			
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO MASTER.MASTER_ORGANISASI (tahun,kodeurusan,kodesuburusan,kodeorganisasi,urai,alamat,notelp,nofax,email,skpkd)"\
					" VALUES (%s,%s,%s,lpad(trim(%s)::text,2,'0'),%s,%s,%s,%s,%s,%s)",[tahun_log(request), kode_uru, kode_sub, kode_org, nama_org, alamat, notelp, nofax, email, skpkd])
				cursor.execute("DELETE FROM APBD.ANGG_BIDANG_ORGANISASI WHERE tahun =%s AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi =lpad(trim(%s)::text,2,'0')",[tahun_log(request),kode_uru,kode_sub,kode_org])
			for x in range(len(kode_bid)):
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO APBD.ANGG_BIDANG_ORGANISASI (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEBIDANG) VALUES (%s,%s,%s,lpad(trim(%s)::text,2,'0'),%s) ",[tahun_log(request),kode_uru, kode_sub, kode_org, kode_bid[x]])
			messages.success(request, "Data Organisasi Berhasil Disimpan")
	

		elif act == 'edit':
			kode_org = request.POST['kd_org']
			kode_bid = request.POST.getlist('kode_bidang')
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE MASTER.MASTER_ORGANISASI SET urai=%s, alamat=%s, notelp=%s, nofax=%s, "\
					"email=%s, skpkd=%s WHERE tahun=%s AND kodeurusan=%s AND kodesuburusan=%s "\
					"AND kodeorganisasi= lpad(trim(%s)::text,2,'0')",
                    [nama_org, alamat, notelp, notelp, email, skpkd, tahun_log(request), kode_uru, kode_sub, kode_org])
				cursor.execute("DELETE FROM APBD.ANGG_BIDANG_ORGANISASI WHERE tahun =%s AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi =%s",[tahun_log(request),kode_uru,kode_sub,kode_org])
			for y in range(len(kode_bid)):
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO APBD.ANGG_BIDANG_ORGANISASI (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEBIDANG) "\
						"VALUES (%s,%s,%s,lpad(trim(%s)::text,2,'0'),%s)",[tahun_log(request),kode_uru, kode_sub, kode_org, kode_bid[y]])
			messages.success(request, "Data Organisasi Berhasil Diubah")
			
	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def hapusurusan(request):
	kdurusan = request.GET.get('id', None)
	act = request.GET.get('act', None)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s and kodeurusan = %s ",[tahun_log(request),kdurusan])
		messages.success(request, 'Data Urusan Berhasil Dihapus')
	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def hapussuburusan(request):
	kdsuburusan = request.GET.get('idsub', None)
	kdurusan = request.GET.get('iduru', None)
	act = request.GET.get('act', None)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s and kodeurusan = %s "\
			"and kodesuburusan = %s",[tahun_log(request),kdurusan,kdsuburusan])
		messages.success(request, 'Data Sub Urusan Berhasil Dihapus')
	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def hapusorganisasi(request):
	kdorganisasi = request.GET.get('idorg', None)
	kdsuburusan = request.GET.get('idsub', None)
	kdurusan = request.GET.get('iduru', None)
	act = request.GET.get('act', None)

	if(int(kdorganisasi) < 10):
		# kd_org[awal:akhir]
		kdorganisasi=kdorganisasi[1:2]
		
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("DELETE FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s and kodeorganisasi = lpad(trim(%s)::text,2,'0') "\
		"and kodesuburusan = %s and kodeurusan =%s",[tahun_log(request),kdorganisasi,kdsuburusan,kdurusan])
		messages.success(request, 'Data Organisasi Berhasil Dihapus')
	return HttpResponseRedirect(reverse('sipkd:settingorganisasi'))

def updateurusan(request):
	kodeurusan = request.GET.get('id', None)
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT KODEURUSAN, URAI FROM MASTER.MASTER_ORGANISASI WHERE TAHUN=%s AND KODEURUSAN=%s AND KODESUBURUSAN='0' ORDER BY KODEURUSAN",[tahun_log(request),kodeurusan])
	list_urusan = dictfetchall(cursor)
	data = {'list_urusan':list_urusan}
	return JsonResponse(data)

def updatesuburusan(request):
	kodeurusan = request.GET.get('id', None)
	suburusan =  request.GET.get('suburusan',None)	
	cursor = connections[tahun_log(request)].cursor()
	cursor.execute("SELECT * FROM MASTER.MASTER_ORGANISASI where tahun=%s AND kodeurusan =%s and kodesuburusan <>'0' and kodeorganisasi ='' and kodesuburusan = %s order by kodeurusan asc",[tahun_log(request),kodeurusan,suburusan])
	list_urusan = dictfetchall(cursor)
	data = {'list_urusan':list_urusan}
	return JsonResponse(data)

def updateorganisasi(request):
	kd_uru = request.GET.get('id_uru', None)
	kd_sub = request.GET.get('id_sub', None)
	kd_org = request.GET.get('id_org', None)

	if(int(kd_org) < 10):
		# kd_org[awal:akhir]
		kd_org=kd_org[1:2]

	kd_bid = request.GET.getlist('id_get', None)
	
	list_organisasi = ''
	list_bidang = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM MASTER.MASTER_ORGANISASI where tahun=%s and kodeurusan =%s and kodesuburusan =%s "\
			"and kodeorganisasi <>'0' and kodeorganisasi = lpad(trim(%s)::text,2,'0') order by kodesuburusan asc",[tahun_log(request),kd_uru,kd_sub,kd_org])
		list_organisasi = dictfetchall(cursor)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM APBD.ANGG_BIDANG_ORGANISASI where tahun=%s and kodeurusan =%s and kodesuburusan =%s "\
			"and kodeorganisasi = lpad(trim(%s)::text,2,'0') order by kodeorganisasi asc",[tahun_log(request),kd_uru,kd_sub,kd_org])
		list_bidang = dictfetchall(cursor)
	data = {'list_organisasi':list_organisasi,'list_bidang':list_bidang}
	return JsonResponse(data)

# JOEL == MODAL ORGANISASI ==================================================
def mdl_organisasi(request):
	
	# if(jns == 0): # IS SKPD =================
	# 	if referer(request) not in array_skpd(request):
	# 		return render(request,'base/restricted.html')
	# 	else:

	if ((hakakses(request) == 'ADMIN') or (hakakses(request) == 'ADMINANGGARAN')):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeurusan, kodesuburusan, kodeorganisasi, kodeunit,kodeskpd,\
			               kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit as kode, urai \
			               from master.MASTER_ORGANISASI where tahun = %s and kodeurusan <> 0 and kodesuburusan <> 0 \
			               and kodeorganisasi <> '' and  trim(kodeunit)<>'' ORDER BY kodeurusan,kodesuburusan,kodeorganisasi,kodeunit",
			               [tahun_log(request)])
			list_org = dictfetchall(cursor)
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit as kode, urai "\
			               "from public.view_organisasi_user(%s,%s,%s,2) "\
			               "where pilih = 1", [tahun_log(request), username(request), hakakses(request)])
			list_org = dictfetchall(cursor)

	# elif(jns == 1): # IS PPKD =================
	# 	if referer(request) not in array_ppkd(request):
	# 		return render(request,'base/restricted.html')
	# 	else:
			# with connections[tahun_log(request)].cursor() as cursor:
			# 	cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi as kode, urai FROM master.MASTER_ORGANISASI "\
			# 		"WHERE tahun = %s and kodeorganisasi <> '' AND skpkd=1",[tahun_log(request)])
			# 	list_org = dictfetchall(cursor)

	data = {'list_org':list_org}

	return render(request, 'konfig/modal/modal_organisasi.html',data)

def mdl_organisasi_ppkd(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.000' as kode, urai FROM master.master_organisasi WHERE tahun = %s and kodeorganisasi <> '' AND skpkd=1",[tahun_log(request)])
		list_org = dictfetchall(cursor)
	data = {'list_org':list_org}

	return render(request, 'konfig/modal/modal_organisasi.html',data)	

# JOEL 28 Jan 2019 ===================================================
def mdl_kegiatan(request):
	tahun = tahun_log(request)
	skpd  = request.GET.get('id').split(".")
	asal  = request.GET.get('frm').lower()
	arrKeg = []

	print(request.GET)

	# if asal == 'sp2d_laporan':
	# 	ARGTEX = "SELECT '' AS KODEBIDANG, '0'AS KODEPROGRAM, '0'AS KODEKEGIATAN,'BELANJA TIDAK LANGSUNG' AS URAI UNION "
	# else:
	ARGTEX = "SELECT k.kodeunit,k.kodeunit||'-'||mo.URAI AS SUBUNIT, \
		k.kodeurusan||'.'||lpad(k.kodesuburusan::text,2,'0') as kodebidang,\
		0 as kodeprogram ,'0.0' as kodekegiatan,0 as KODESUBKEGIATAN,0 as KODESUBKELUARAN,\
		'PENGELUARAN PEMBIAYAAN' URAI \
		FROM penatausahaan.pembiayaan k left join master.master_organisasi mo ON (mo.TAHUN=K.TAHUN AND mo.KODEURUSAN=K.KODEURUSAN \
		AND mo.KODESUBURUSAN=K.KODESUBURUSAN AND mo.KODEORGANISASI=K.KODEORGANISASI AND mo.KODEUNIT=K.KODEUNIT) \
		WHERE k.TAHUN = %s AND k.KODEURUSAN= %s AND k.KODESUBURUSAN = %s AND k.KODEORGANISASI = %s AND K.KODEUNIT = %s \
		AND k.kodeakun =6  AND k.kodekelompok=2  UNION "

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute(ARGTEX+"SELECT k.kodeunit,k.kodeunit||'-'||mo.URAI AS SUBUNIT, \
			k.KODEBIDANG,k.KODEPROGRAM,k.KODEKEGIATAN,k.KODESUBKEGIATAN,k.KODESUBKELUARAN,k.URAI \
			FROM penatausahaan.kegiatan k left join master.master_organisasi mo ON (mo.TAHUN=K.TAHUN AND mo.KODEURUSAN=K.KODEURUSAN \
			AND mo.KODESUBURUSAN=K.KODESUBURUSAN AND mo.KODEORGANISASI=K.KODEORGANISASI AND mo.KODEUNIT=K.KODEUNIT) \
			WHERE k.TAHUN = %s AND k.KODEURUSAN= %s AND k.KODESUBURUSAN = %s AND k.KODEORGANISASI = %s  AND K.KODEUNIT = %s \
			AND k.KODEKEGIATAN <> '0' AND k.KODESUBKEGIATAN <> 0 AND k.KODESUBKELUARAN = 0 \
			ORDER BY kodeunit,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan",
			[tahun,skpd[0],skpd[1],skpd[2],skpd[3],tahun,skpd[0],skpd[1],skpd[2],skpd[3]])
		list_keg = dictfetchall(cursor)

	aidi = 0
	for i in range(len(list_keg)):
		kdBid = str(list_keg[i]['kodebidang'])
		kdXXX = kdBid+"|"+str(list_keg[i]['kodeprogram'])+"|"+str(list_keg[i]['kodekegiatan'])+"|"+str(list_keg[i]['kodesubkegiatan'])

		if kdBid == "":
			kode_x = str(list_keg[i]['kodeprogram'])+"."+str(list_keg[i]['kodekegiatan'])+"."+str(list_keg[i]['kodesubkegiatan'])
		else:
			kode_x = kdBid+"."+str(list_keg[i]['kodeprogram'])+"."+str(list_keg[i]['kodekegiatan'])+"."+str(list_keg[i]['kodesubkegiatan'])
		aidi += 1

		arrKeg.append({'aidi':aidi,'kode':kode_x,'urai':list_keg[i]['urai'],'kdxx':kdXXX,'subunit':list_keg[i]['subunit'],'kodeunit':list_keg[i]['kodeunit']})		

	arrDT = { 'list_keg':arrKeg, 'frm_asal':asal }

	return render(request, 'konfig/modal/modal_kegiatan.html',arrDT)

