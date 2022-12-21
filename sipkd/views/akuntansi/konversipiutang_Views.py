from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def get_konpiu_load(request):
	tahun_x = tahun_log(request)

	if request.method == 'POST':
		data = request.POST

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM akuntansi.fc_view_konversi_piutang(%s)",[tahun_x])
			arrTBL = dictfetchall(cursor)

		arrDT = {'arrTabel':arrTBL}
		return render(request,'akuntansi/tabel/konpiu.html',arrDT)
	else:
		return render(request,'akuntansi/konpiu.html')

def konpiu_modal_in(request):
	data 	= request.GET
	aksi 	= data.get('ax').lower()
	jenis 	= str(data.get('id').lower())
	akun 	= str(data.get('dt').replace("_","/").replace("+"," ")).split('|')
	ur_b = kd_b_0 = kd_b_1 = kd_b_2 = kd_b_3 = kd_b_4 = ''

	if aksi == 'false':
		kd_a = akun[0].split('.')
		ur_a = akun[1]

		if akun[2] != "":
			kd_b 	= akun[2].split('.')
			ur_b 	= akun[3]
			kd_b_0 	= kd_b[0]
			kd_b_1 	= kd_b[1]
			kd_b_2 	= kd_b[2]
			kd_b_3 	= kd_b[3]
			kd_b_4 	= kd_b[4]

	arrDT = {'jenis':jenis,
		'edkdAkun_A':kd_a[0],'edkdKelompok_A':kd_a[1],'edkdJenis_A':kd_a[2],'edkdObjek_A':kd_a[3],
		'edkdRincObjek_A':kd_a[4],'edUraian_A':ur_a,
		'edkdAkun_B':kd_b_0,'edkdKelompok_B':kd_b_1,'edkdJenis_B':kd_b_2,'edkdObjek_B':kd_b_3,
		'edkdRincObjek_B':kd_b_4,'edUraian_B':ur_b}

	return render(request,'akuntansi/modal/konpiu_in.html',arrDT)

def konpiu_set_simpan(request, jenis):
	tahun = tahun_log(request)
	data  = request.POST

	edkdAkun_A 		= int(data.get('edkdAkun_A'))
	edkdKelompok_A 	= int(data.get('edkdKelompok_A'))
	edkdJenis_A 	= int(data.get('edkdJenis_A'))
	edkdObjek_A 	= str(data.get('edkdObjek_A'))
	edkdRincObjek_A = str(data.get('edkdRincObjek_A'))
	
	if data.get('edkdAkun_B') != "":
		edkdAkun_B 		= int(data.get('edkdAkun_B'))
		edkdKelompok_B 	= int(data.get('edkdKelompok_B'))
		edkdJenis_B 	= int(data.get('edkdJenis_B'))
		edkdObjek_B 	= str(data.get('edkdObjek_B'))
		edkdRincObjek_B = str(data.get('edkdRincObjek_B'))
	else: edkdAkun_B = edkdKelompok_B = edkdJenis_B = edkdObjek_B = edkdRincObjek_B = ""

	if edkdAkun_A == "":
		isSimpan = 0
		pesan = "Rekening Pendapatan masih kosong !"
	else:
		if edkdAkun_B != "":
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE from akuntansi.konversi_akrual_piutang where tahun = %s \
					and kodeakun = %s and kodekelompok = %s and kodejenis = %s \
					and kodeobjek = %s and koderincianobjek = %s",
					[tahun,edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A])

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("INSERT INTO akuntansi.konversi_akrual_piutang (tahun,kodeakun,kodekelompok,kodejenis,\
					kodeobjek,koderincianobjek,a_kodeakun,a_kodekelompok,a_kodejenis,a_kodeobjek,a_koderincianobjek)\
					VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun,edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A,
					edkdAkun_B,edkdKelompok_B,edkdJenis_B,edkdObjek_B,edkdRincObjek_B])
			isSimpan = 1
			pesan = "Konversi rekening piutang berhasil disimpan."
		else:
			isSimpan = 0
			pesan = "Konversi rekening piutang gagal disimpan."

	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)


