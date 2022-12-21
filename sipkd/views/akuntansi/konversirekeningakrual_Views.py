from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def get_koreak_load(request):
	tahun_x = tahun_log(request)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodeakun, urai, kodeakun||'-'||urai AS urairekening FROM master.master_rekening \
			WHERE tahun = %s AND kodeakun IN (4,5,6) AND kodekelompok = 0 \
			order by kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek ",[tahun_x])
		arrTBL = ArrayFormater(dictfetchall(cursor))

	arrDT = {'arrJenis':arrTBL, 'jenis':'all'}
	return render(request,'akuntansi/koreak.html',arrDT)

def koreak_get_tbl_awal(request):
	tahun_x 	= tahun_log(request)
	data  		= request.POST
	jns_belanja = int(data.get("jns_belanja"))
	jns_akun 	= int(data.get("jns_akun"))
	arrTBL  	= []
	gdlo 		= ''

	if(jns_akun == 1 or jns_akun == 2 or jns_akun == 3): hidden = "hidden"
	else: hidden = ""

	if (jns_belanja == 0 or jns_akun == 4 or jns_akun == 5 or jns_akun == 3 or jns_akun == 6 or jns_akun == 2): where = ""
	if (jns_akun == 1): where = "where a_kodeakun=1 and a_kodekelompok<>3"
	elif (jns_akun == 4): gdlo = 'Rekening Pendapatan LO PMD 64'
	elif (jns_belanja == 0 and jns_akun == 5): gdlo = 'Rekening Beban LO PMD 64'
	elif (jns_belanja == 1 and jns_akun == 5):
		where = "where a_kodeakun=5 and a_kodekelompok=1"
		gdlo  = 'Rekening Beban LO PMD 64'
	elif (jns_belanja == 2 and jns_akun == 5):
		where = "where a_kodeakun=5 and a_kodekelompok=2"
		gdlo  = 'Rekening Beban LO PMD 64'
	elif (jns_belanja == 3 and jns_akun == 5):
		where = "where a_kodeakun=5 and a_kodekelompok in (3,4)"
		gdlo  = 'Rekening Aset PMD 64'
	elif (jns_belanja == 4 and jns_akun == 5):
		where = "where b_kodeakun=0 or b_kodeakun is null and a_kodeakun=5 and a_kodekelompok=2  "
		gdlo  = 'Rekening Aset PMD 64'
	# elif (jns_belanja == 4 and jns_akun == 5):
	# 	where = "where a_kodeakun=5 and a_kodekelompok=4"
	# 	gdlo  = 'Rekening Beban LO PMD 64'
	elif (jns_akun == 6): gdlo = 'Afektasi Rekening Aset & Kewajiban'

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM akuntansi.fc_view_konversi_akrual(%s,%s) "+where+" \
			order by a_kodeakun,a_kodekelompok,a_kodejenis,a_kodeobjek,a_koderincianobjek,a_kodesubrincianobjek",
			[tahun_x,jns_akun])
		arrTBL = dictfetchall(cursor)

	arrDT = {'arrTabel':arrTBL,'hidden':hidden, 'gdlo':gdlo}
	return render(request,'akuntansi/tabel/koreak.html',arrDT)

def koreak_modal_in(request):
	data 	= request.GET
	aksi 	= data.get('ax').lower()
	jenis 	= int(data.get('id'))
	akun 	= str(data.get('dt').replace("_","/").replace("+"," ")).split('|')
	ur_c = kd_c_0 = kd_c_1 = kd_c_2 = kd_c_3 = kd_c_4 = kd_c_5 = ''
	ur_b = kd_b_0 = kd_b_1 = kd_b_2 = kd_b_3 = kd_b_4 = kd_b_5 = ''
	lblkorolari = 'Rekening Berbasis Akrual'

	if jenis == 2: hidden = "hidden"
	else: hidden = ""

	if aksi == 'false':
		kd_a = akun[0].split('.')
		ur_a = akun[1]

		if akun[2] != 'None':
			kd_c 	= akun[2].split('.')
			ur_c 	= akun[3]
			kd_c_0 	= kd_c[0]
			kd_c_1 	= kd_c[1]
			kd_c_2 	= kd_c[2]
			kd_c_3 	= kd_c[3]
			kd_c_4 	= kd_c[4]
			kd_c_5 	= kd_c[5]

		if akun[4] != "None":
			kd_b 	= akun[4].split('.')
			ur_b 	= akun[5]
			kd_b_0 	= kd_b[0]
			kd_b_1 	= kd_b[1]
			kd_b_2 	= kd_b[2]
			kd_b_3 	= kd_b[3]
			kd_b_4 	= kd_b[4]
			kd_b_5 	= kd_b[5]

		if int(kd_a[0]) == 4: 
			lblkorolari = 'Rekening Pendapatan LO'
		if int(kd_a[0]) == 5 and int(kd_a[1]) == 2 and int(kd_a[2]) == 3: 
			lblkorolari = 'Rekening Aset'
		if (int(kd_a[0]) == 5 and int(kd_a[1]) == 2 and int(kd_a[2]) == 2) or (int(kd_a[0]) == 5 and int(kd_a[1]) == 2 and int(kd_a[2]) == 1) or (int(kd_a[0]) == 5 and int(kd_a[1]) == 1):
			lblkorolari = 'Rekening Beban LO' 


	arrDT = {'hidden':hidden, 'lblkorolari':lblkorolari,
		'edkdAkun_A':kd_a[0],'edkdKelompok_A':kd_a[1],'edkdJenis_A':kd_a[2],'edkdObjek_A':kd_a[3],
		'edkdRincObjek_A':kd_a[4],'edkdSubRincObjek_A':kd_a[5],'edUraian_A':ur_a,
		'edkdAkun_C':kd_c_0,'edkdKelompok_C':kd_c_1,'edkdJenis_C':kd_c_2,'edkdObjek_C':kd_c_3,
		'edkdRincObjek_C':kd_c_4,'edkdSubRincObjek_C':kd_c_5,'edUraian_C':ur_c,
		'edkdAkun_B':kd_b_0,'edkdKelompok_B':kd_b_1,'edkdJenis_B':kd_b_2,'edkdObjek_B':kd_b_3,
		'edkdRincObjek_B':kd_b_4,'edkdSubRincObjek_B':kd_b_5,'edUraian_B':ur_b,
	}
	return render(request,'akuntansi/modal/koreak_in.html',arrDT)

def mdl_akrual_rekening(request,jenis):
	tahun 	= tahun_log(request)
	data 	= request.POST
	pilter 	= ""

	edkdAkun_A 		= int(data.get('edkdAkun_A'))
	edkdKelompok_A 	= int(data.get('edkdKelompok_A'))
	edkdJenis_A 	= int(data.get('edkdJenis_A'))
	edkdObjek_A 	= str(data.get('edkdObjek_A'))
	edkdRincObjek_A = str(data.get('edkdRincObjek_A'))
	edkdSubRincObjek_A = str(data.get('edkdSubRincObjek_A'))

	if jenis.lower() == 'kas': # JENIS AKUN KAS ===============================================
		pilter = 'AND kodeakun = '+str(edkdAkun_A)+' AND kodekelompok = '+str(edkdKelompok_A)+' AND kodejenis = '+str(edkdJenis_A)+''
		dbase  = 'master.MASTER_REKENING'

	elif jenis.lower() == 'akrual': # JENIS AKUN AKRUAL ======================================
		dbase  = 'master.MASTER_REKENING'
		if data.get('edkdAkun_B') != "":
			edkdAkun_B 		= int(data.get('edkdAkun_B'))
			edkdKelompok_B 	= int(data.get('edkdKelompok_B'))
			edkdJenis_B 	= int(data.get('edkdJenis_B'))
			edkdObjek_B 	= str(data.get('edkdObjek_B'))
			edkdRincObjek_B = str(data.get('edkdRincObjek_B'))
			edkdSubRincObjek_B = str(data.get('edkdSubRincObjek_B'))
		else:
			edkdAkun_B = edkdKelompok_B = edkdJenis_B = edkdObjek_B = edkdRincObjek_B = edkdSubRincObjek_B = ""

		if (edkdAkun_A == 5):
				pilter = ''
	# 	if (edkdAkun_A == 1): pilter =' AND kodeakun = 1 AND kodekelompok <> 3'
	# 	if (edkdAkun_A == 2): pilter =' AND kodeakun = 2'
	# 	if (edkdAkun_A == 3): pilter =' AND kodeakun = 3'
	# 	if (edkdAkun_A == 4): pilter =' AND kodeakun = 4'
	# 	if (edkdAkun_A == 5): pilter =' AND kodeakun in (5,6)'
	# 	if (edkdAkun_A == 6): pilter =' AND kodeakun in (7)'

	# 	# TANAH
	# 	if (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and edkdObjek_A == '01'):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis = 1'
	# 	# PERALATAN dan MESIN
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) in [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,32]):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis = 2'
	# 	# GEDUNG dan BANGUNAN
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and edkdObjek_A == '26'):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis = 3'
	# 	# JALAN dan JARINGAN
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) in [21,22,23,24,25]):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis = 4'
	# 	# ASET LAINNYA
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) in [27,28,29]):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis = 5'
	# 	# NON APBD
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) >= 31):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 2 AND kodejenis > 5'
	# 	elif (edkdAkun_A == 5 and edkdKelompok_A == 1 and edkdJenis_A != 1 ):
	# 		pilter = ' AND kodeakun = 5 AND kodekelompok = 1 AND kodejenis in (3,4,5,6) or (kodeakun = 5 AND kodekelompok = 3 ) or kodeakun = 6'

	# elif jenis.lower() == 'piutang': # JENIS AKUN PIUTANG ==========================================
	# 	dbase  = 'akuntansi.AKRUAL_MASTER_REKENING'
	# 	if (edkdAkun_A == 4):
	# 		pilter = ' AND kodeakun = 1 AND kodekelompok = 1 AND kodejenis = 3'

	else: # JENIS AKUN KOLORARI ====================================================================
		dbase  = "master.MASTER_REKENING"
		if data.get('edkdAkun_C') != "":
			edkdAkun_C 		= int(data.get('edkdAkun_C'))
			edkdKelompok_C 	= int(data.get('edkdKelompok_C'))
			edkdJenis_C 	= int(data.get('edkdJenis_C'))
			edkdObjek_C 	= str(data.get('edkdObjek_C'))
			edkdRincObjek_C = str(data.get('edkdRincObjek_C'))
			edkdSubRincObjek_C = str(data.get('edkdSubRincObjek_C'))
		else:
			edkdAkun_C = edkdKelompok_C = edkdJenis_C = edkdObjek_C = edkdRincObjek_C = edkdSubRincObjek_C = ""

		if (edkdAkun_A == 4):
				pilter = 'AND kodeakun = 7'

		# if (edkdAkun_B == 5 and edkdKelompok_B == 1):
		# 	pilter = ' AND kodeakun = 9 AND kodekelompok = 1'
		# elif (edkdAkun_B == 4 and edkdKelompok_B == 1):
		# 	pilter = ' AND kodeakun = 8 AND kodekelompok = 1'
		# elif (edkdAkun_B == 4 and edkdKelompok_B != 1):
		# 	pilter = ' AND kodeakun = 8 AND kodekelompok <> 1'

		# if (edkdAkun_A == 5 and edkdKelompok_A == 1 and edkdJenis_A != 1):
		# 	pilter = ' AND kodeakun = 9 AND kodekelompok = 1 AND kodejenis in (3,4,5,6,7,8,9) or (kodeakun = 9 AND kodekelompok = 2)'
		# # TANAH
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and edkdObjek_A == '01'):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 1'
		# # PERALATAN dan MESIN
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and (int(edkdObjek_A) >= 2 and int(edkdObjek_A) <= 20)):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 2'
		# # GEDUNG dan BANGUNAN
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and edkdObjek_A == '26'):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 3'
		# # JALAN dan JARINGAN
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) in [21,22,23,24,25]):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 4'
		# # ASET LAINNYA
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) in [27,28,29]):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 5'
		# # SENJATA LAINNYA
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) == 30):
		# 	pilter = ' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 2 AND kodeobjek in (31,32,33,34,35)'
		# # NON APBD
		# elif (edkdAkun_A == 5 and edkdKelompok_A == 2 and edkdJenis_A == 3 and int(edkdObjek_A) >= 31):
		# 	pilter =' AND kodeakun = 1 AND kodekelompok = 3 AND kodejenis = 5'
		# elif (edkdAkun_B == 7):
		# 	pilter =' AND kodeakun = 2 AND kodekelompok in (1,2) or (kodeakun = 1 AND kodekelompok = 2)'

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT KODEAKUN||'.'||KODEKELOMPOK||'.'||KODEJENIS||'.'||lpad(KODEOBJEK::TEXT,2,'0')||'.'||lpad(KODERINCIANOBJEK::TEXT,2,'0')||'.'||lpad(KODESUBRINCIANOBJEK::TEXT,2,'0') as KODEREKENING,URAI \
 			FROM "+dbase+" WHERE TAHUN = %s AND koderincianobjek <> 0 AND kodesubrincianobjek <> 0 "+pilter+" ORDER BY KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK",[tahun])
		arrTBL = dictfetchall(cursor)

	arrDT = {'jenis':jenis.lower(), 'hasil':arrTBL}
	return render(request,'akuntansi/modal/akrual_rekening.html',arrDT)

def koreak_set_simpan(request,jenis):
	tahun = tahun_log(request)
	data  = request.POST

	# print(data)
# 'edkdAkun_A': ['5'], 'edkdKelompok_A': ['1'], 'edkdJenis_A': ['01'], 'edkdObjek_A': ['01'], 
# 'edkdRincObjek_A': ['01'], 'edkdSubRincObjek_A': ['01'], 'edUraian_A': ['Belanja Gaji Pokok PNS'], 
# 'edkdAkun_C': ['8'], 'edkdKelompok_C': ['1'], 'edkdJenis_C': ['01'], 'edkdObjek_C': ['01'], 
# 'edkdRincObjek_C': ['01'], 'edkdSubRincObjek_C': ['01'], 'edUraian_C': ['Beban Gaji Pokok PNS'], 
# 'edkdAkun_B': ['8'], 'edkdKelompok_B': ['1'], 'edkdJenis_B': ['1'], 'edkdObjek_B': ['01'], 
# 'edkdRincObjek_B': ['01'], 'edkdSubRincObjek_B': ['01'], 'edUraian_B': ['Beban Gaji Pokok PNS'], 
# 'jns_akun': ['5-BELANJA DAERAH']}>



	jns_akun 		= data.get('jns_akun').upper()
	edUraian_A		= str(data.get('edUraian_A'))
	edkdAkun_A 		= int(data.get('edkdAkun_A'))
	edkdKelompok_A 	= int(data.get('edkdKelompok_A'))
	edkdJenis_A 	= int(data.get('edkdJenis_A'))
	edkdObjek_A 	= str(data.get('edkdObjek_A'))
	edkdRincObjek_A = str(data.get('edkdRincObjek_A'))
	edkdSubRincObjek_A = str(data.get('edkdSubRincObjek_A'))
	
	if data.get('edkdAkun_B') != "":
		edUraian_B		= str(data.get('edUraian_B'))
		edkdAkun_B 		= int(data.get('edkdAkun_B'))
		edkdKelompok_B 	= int(data.get('edkdKelompok_B'))
		edkdJenis_B 	= int(data.get('edkdJenis_B'))
		edkdObjek_B 	= str(data.get('edkdObjek_B'))
		edkdRincObjek_B = str(data.get('edkdRincObjek_B'))
		edkdSubRincObjek_B = str(data.get('edkdSubRincObjek_B'))
	else: 
		edUraian_B = edkdAkun_B = edkdKelompok_B = edkdJenis_B = edkdObjek_B = edkdRincObjek_B = edkdSubRincObjek_B = ""

	# if data.get('edkdAkun_C') != "":
	edUraian_C		= str(data.get('edUraian_C'))
	edkdAkun_C 		= int(data.get('edkdAkun_C'))
	edkdKelompok_C 	= int(data.get('edkdKelompok_C'))
	edkdJenis_C 	= int(data.get('edkdJenis_C'))
	edkdObjek_C 	= str(data.get('edkdObjek_C'))
	edkdRincObjek_C = str(data.get('edkdRincObjek_C'))
	edkdSubRincObjek_C = str(data.get('edkdSubRincObjek_C'))
	# else: edkdAkun_C = edkdKelompok_C = edkdJenis_C = edkdObjek_C = edkdRincObjek_C = edkdSubRincObjek_C = ""

	if edkdAkun_A == "":
		isSimpan = 0
		pesan = "Jenis Akun : "+jns_akun+", rekening berbasis kas masih kosong !"
	else:
		if edkdAkun_B != "" or edkdAkun_C != "":
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("DELETE from akuntansi.konversi_akrual where tahun = %s \
					and kodeakun = %s and kodekelompok = %s and kodejenis = %s \
					and kodeobjek = %s and koderincianobjek = %s and kodesubrincianobjek = %s",
					[tahun,edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A,edkdSubRincObjek_A])

			print('masuk delete data')

		if edkdAkun_A == 4 or edkdAkun_A == 5 or edkdAkun_A == 6:
			if edkdAkun_B != "" or edkdAkun_C != "":
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO akuntansi.konversi_akrual (tahun,lob_urai,\
						kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,\
						lob_kodeakun,lob_kodekelompok,lob_kodejenis,lob_kodeobjek,lob_koderincianobjek,lob_kodesubrincianobjek,\
						a_kodeakun,a_kodekelompok,a_kodejenis,a_kodeobjek,a_koderincianobjek,a_kodesubrincianobjek)\
						VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun,edUraian_C,
						edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A,edkdSubRincObjek_A,
						edkdAkun_C,edkdKelompok_C,edkdJenis_C,edkdObjek_C,edkdRincObjek_C,edkdSubRincObjek_C,
						edkdAkun_B,edkdKelompok_B,edkdJenis_B,edkdObjek_B,edkdRincObjek_B,edkdSubRincObjek_B])
				isSimpan = 1
				pesan = "Jenis Akun : "+jns_akun+", konversi rekening akrual berhasil disimpan."

				print([tahun,
						edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A,edkdSubRincObjek_A,
						edkdAkun_C,edkdKelompok_C,edkdJenis_C,edkdObjek_C,edkdRincObjek_C,edkdSubRincObjek_C,
						edkdAkun_B,edkdKelompok_B,edkdJenis_B,edkdObjek_B,edkdRincObjek_B,edkdSubRincObjek_B])
			else:
				isSimpan = 0
				pesan = "Konversi rekening akrual gagal disimpan."
		# else:
			# if edkdAkun_B != "":
			# 	with connections[tahun_log(request)].cursor() as cursor:
			# 		cursor.execute("INSERT INTO akuntansi.konversi_akrual (tahun,kodeakun,kodekelompok,kodejenis,\
			# 			kodeobjek,koderincianobjek,kodesubrincianobjek,\
			# 			a_kodeakun,a_kodekelompok,a_kodejenis,a_kodeobjek,a_koderincianobjek,a_kodesubrincianobjek)\
			# 			VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
			# 			[tahun,edkdAkun_A,edkdKelompok_A,edkdJenis_A,edkdObjek_A,edkdRincObjek_A,edkdSubRincObjek_A,
			# 			edkdAkun_B,edkdKelompok_B,edkdJenis_B,edkdObjek_B,edkdRincObjek_B,edkdSubRincObjek_B])
			# 	isSimpan = 1
			# 	pesan = "Jenis Akun : "+jns_akun+", konversi rekening akrual berhasil disimpan."
			# else:
			# 	isSimpan = 0
			# 	pesan = "Konversi rekening akrual gagal disimpan."


	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def koreak_frm_lap(request):
	tahun = tahun_log(request)

	if request.method == 'POST':
		data 	= request.POST
		lapParm = {}
		kodeakun 	= int(data.get('jns_akun'))
		belanja 	= int(data.get('jns_belanja'))
	
		lapParm['report_type'] 		= 'pdf'
		if kodeakun == 2:
			lapParm['file'] 		= 'penatausahaan/akuntansi/konversirekeningkewajiban.fr3'
		else:
			lapParm['file'] 		= 'penatausahaan/akuntansi/konversirekening.fr3'
		lapParm['tahun'] 			= tahun
		lapParm['kodeakun'] 		= "'"+str(kodeakun)+"'"

		return HttpResponse(laplink(request, lapParm))
