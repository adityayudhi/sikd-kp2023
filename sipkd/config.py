from django.utils.timezone import utc
import datetime
import base64
import urllib
import locale
from django.db import connection,connections
import re
from django.urls import reverse,resolve
from django.http import HttpResponse, JsonResponse, HttpRequest
from itertools import islice
import os
import re
from django.contrib.staticfiles.templatetags.staticfiles import static

dayList = {
	'Sun' : 'Minggu',
	'Mon' : 'Senin',
	'Tue' : 'Selasa',
	'Wed' : 'Rabu',
	'Thu' : 'Kamis',
	'Fri' : 'Jumat',
	'Sat' : 'Sabtu'
}

arrBulan = {'01':'Januari', '02':'Februari', '03':'Maret', '04':'April', 
	'05':'Mei', '06':'Juni', '07':'Juli', '08':'Agustus',
    '09':'September', '10':'Oktober', '11':'November', '12':'Desember'}

arrMonth = {'Januari':'01', 'Februari':'02', 'Maret':'03', 'April':'04', 
	'Mei':'05', 'Juni':'06', 'Juli':'07', 'Agustus':'08',
    'September':'09', 'Oktober':'10', 'November':'11', 'Desember':'12'}

arrMonth_x = {'Januari':'1', 'Februari':'2', 'Maret':'3', 'April':'4', 
	'Mei':'5', 'Juni':'6', 'Juli':'7', 'Agustus':'8',
    'September':'9', 'Oktober':'10', 'November':'11', 'Desember':'12'}

monthList = {
	'Jan': 'Januari',
	'Feb': 'Februari',
	'Mar': 'Maret',
	'Apr': 'April',
	'May': 'Mei',
	'Jun': 'Juni',
	'Jul': 'Juli',
	'Aug': 'Agustus',
	'Sep': 'September',
	'Oct': 'Oktober',
	'Nov': 'November',
	'Dec': 'Desember'
}

monthDB = {'Januari':'Jan', 'Februari':'Feb', 'Maret':'Mar', 'April':'Apr', 
	'Mei':'May', 'Juni':'Jun', 'Juli':'Jul', 'Agustus':'Aug',
    'September':'Sep', 'Oktober':'Oct', 'November':'Nov', 'Desember':'Dec'}

satuan = ['','Satu','Dua','Tiga','Empat','Lima','Enam','Tujuh','Delapan','Sembilan','Sepuluh','Sebelas']

arrJns_potongan  = [{'kode':'0','nama':'PPn'},{'kode':'1','nama':'PPh-21'},{'kode':'2','nama':'PPh-22'},
		{'kode':'3','nama':'PPh-23'},{'kode':'4','nama':'PPh-25'},{'kode':'5','nama':'PB-1'},{'kode':'6','nama':'IWP-1%'},
		{'kode':'7','nama':'IWP-8%'},{'kode':'8','nama':'Potongan'}]

def username(request):
	return request.session.get('sipkd_username').upper()

def hakakses(request):	
	return request.session.get('sipkd_hakakses').upper()

def hakakses_sipkd(request):	
	return request.session.get('sipkd_hakakses').upper()

def tahun_log(request):
	return request.session.get('sipkd_tahun')

def sipkd_listorganisasi(request):
	return request.session.get('sipkd_listorganisasi')

def modulelist(request):
	return request.session.get('sipkd_modulelist')

def listpilih(request):
	return request.session.get('sipkd_listpilih')

def listsub(request):
	return request.session.get('sipkd_listsub')

def is_bendahara_pembantu(request):
	return request.session.get('is_bendahara_pembantu')

def perubahan(request):
	return request.session.get('sipkd_perubahan')

def perubahananggaran(request):
	return request.session.get('sipkd_perubahananggaran')

def tgl_indo(tgl):
	tanggal = tgl.strftime('%Y/%m/%d')
	pecah   = tanggal.split("/")
	return pecah[2]+" "+arrBulan[pecah[1]]+" "+pecah[0]

def tgl_to_db_original(tgl):
	pecah  = tgl.split(" ")
	return pecah[0]+"/"+arrMonth[pecah[1]]+"/"+pecah[2]
	
def tgl_to_db(tgl):
	pecah  = tgl.split(" ")
	#return pecah[0]+"/"+arrMonth[pecah[1]]+"/"+pecah[2]
	# return arrMonth[pecah[1]]+"/"+pecah[0]+"/"+pecah[2]
	return pecah[0]+" "+monthDB[pecah[1]]+" "+pecah[2]

def tgl_to_laporan(tgl):
	pecah  = tgl.split(" ")
	return pecah[2]+"-"+arrMonth[pecah[1]]+"-"+pecah[0]

def tgl_short(tgl): # joel 16-Jan-2019 ==========================================
	pecah  = str(tgl).split(" ")
	kunci  = getKeysByValue(monthList, pecah[1])
	for key in kunci:
		bln = key
	return pecah[0]+"-"+bln+"-"+pecah[2]

def get_bulan(request):
	pecah  = str(update_tgl(request)['tglblntahun']).split(" ")
	kunci  = getKeysByValue(monthList, pecah[1])
	for key in kunci:
		bln = key
	return arrMonth_x[monthList[bln]]

def getKeysByValue(Elemen, Cari): # joel 16-Jan-2019 ===========================
	# GET KEY ARRAY BY Value
    Kunci  = list()
    ArrItm = Elemen.items()
    for item  in ArrItm:
        if item[1] == Cari:
            Kunci.append(item[0])
    return  Kunci  

def kata2(x): # joel 16-Jan-2019 ==========================================
	n = int(x)

	if n <= 0:
		hasil = ''
	elif n >= 1 and n <= 11:
		hasil = ' ' + satuan[n]
	elif n >= 12 and n <= 19:
		hasil = kata2(n % 10) + ' Belas'
	elif n >= 20 and n <= 99:
		hasil = kata2(n / 10) + ' Puluh' + kata2(n % 10)
	elif n >= 100 and n <= 199:
		hasil = ' Seratus' + kata2(n-100)
	elif n >= 200 and n <= 999:
		hasil = kata2(n / 100) + ' Ratus' + kata2(n % 100)
	elif n >= 1000 and n <= 1999:
		hasil = ' Seribu' + kata2(n-1000)
	elif n >= 2000 and n <= 999999:
		hasil = kata2(n / 1000) + ' Ribu' + kata2(n % 1000)
	elif n >= 1000000 and n <= 999999999:
		hasil = kata2(n / 1000000) + ' Juta' + kata2(n % 1000000)
	elif n >= 1000000000 and n <= 999999999999:
		hasil = kata2(n / 1000000000) + ' Milyar' + kata2(n % 1000000000)
	elif n >= 1000000000000 and n <= 999999999999999:
		hasil = kata2(n / 1000000000000) + ' Trilyun' + kata2(n % 1000000000000)
	elif n >= 1000000000000000 and n <= 999999999999999999:
		hasil = kata2(n / 1000000000000000) + ' Kwadrilyun' + kata2(n % 1000000000000000)
	else:
		hasil = kata2(n / 1000000000000000000) + ' Kwintrilyun' + kata2(n % 1000000000000000000)

	return hasil

def kataDes(x):  # joel 16-Jan-2019 ==========================================
	n = int(x)

	if n <= 0:
		hasil = ''
	elif n >= 1 and n <= 11:
		hasil = ' ' + satuan[n]
	elif n >= 12 and n <= 19:
		hasil = kataDes(n % 10) + ' Belas'
	elif n >= 20 and n <= 99:
		hasil = kataDes(n / 10) + ' Puluh' + kataDes(n % 10)

	return hasil

def terbilang(x): # joel 16-Jan-2019 ==========================================
	cacah = str(x).split(".")	
	desi  = kataDes(cacah[1])
	hasil = ''

	if(int(cacah[0]) < 0):
		kekata = 'Minus '+kata2(cacah[0].strip('-'))
	elif(int(cacah[0]) == 0):
		kekata = 'Nol'
	else:
		kekata = kata2(cacah[0])

	if desi != '':
		hasil = desi+" Sen"
			
	return kekata+" Rupiah "+hasil

def konfigurasi(request): # joel =======================================================
	# SET ARRAY INPUT DEFAULT SETING APP ABPD KE TABEL MASTER.KONFIGURASI
	arrSetConf = {
		'sipkd_judul' 		: 'Sistem Informasi',
		'sipkd_judul_sub' 	: 'Keuangan Daerah',
		'sipkd_judul_sing' 	: 'SIKD',
		'sipkd_keyword' 	: 'sistem, informasi, pengelolaan, keuangan, daerah, sipkd, kabupaten',
		'sipkd_run_text'	: 'Sistem Informasi Keuangan Daerah TA. '+update_tgl(request)['tahunsaiki'],
		'nama_kabupaten' 	: 'Kabupaten Aplikasi',
		'nama_provinsi' 	: 'Provinsi Aplikasi',
		'copyright_text'	: 'G!NTemplate | Copyright',
		'nama_konsultan'	: 'Global Intermedia Nusantara',
		'konsultan_sing' 	: 'G!N',
		'logo_kabupaten'	: 'lambang.png' }

	arrConf = {}

	# CEK NAMAKONFIGURASI ADA ATAU TIDAK ========================================
	for x in arrSetConf.keys():
		with connection.cursor() as cursor:
			cursor.execute("SELECT count(ID) AS jml FROM MASTER.KONFIGURASI "\
				"WHERE NAMAKONFIGURASI = %s",[x])
			x_jml = dictfetchall(cursor)

		# CARI MAXSIMAL ID [update 22 Jan 2019] =================================
		# karena Sequences id konfigurasi tidak jalan
		with connection.cursor() as cursor:
			cursor.execute("SELECT max(ID)+1 AS id FROM master.konfigurasi")
			maxid = dictfetchall(cursor)
		for y in maxid:
			aidi = int(y["id"])
			
		# JIKA TIDAK ADA MAKA INSERT ============================================
		for z in x_jml:
			if(z["jml"] == 0):
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO MASTER.KONFIGURASI (ID, NAMAKONFIGURASI, KONFIGVALUE) "\
						"VALUES (%s,%s,%s)",[aidi,x,arrSetConf[x]])

	# AMBIL DATA KONFIGURASI ====================================================
	with connection.cursor() as cursor:
		cursor.execute("SELECT NAMAKONFIGURASI,KONFIGVALUE FROM MASTER.KONFIGURASI")
		dt_conf = dictfetchall(cursor)

	for y in range(len(dt_conf)):
		for x in arrSetConf.keys():
			if(x == dt_conf[y]["namakonfigurasi"]):
				arrConf[x] = dt_conf[y]["konfigvalue"]

	return arrConf

def set_organisasi(request):

	kd_org = ''
	ur_org = ''
	organisasi = ''
	# arrOrg = {}

	if(hakakses(request) in tanggal(request)['bukan_admin']):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit as kode, urai "\
			    "from public.view_organisasi_user(%s,%s,%s,2) "\
			    "where pilih = 1 ORDER BY kodeurusan, kodesuburusan, kodeorganisasi,kodeunit ASC", [tahun_log(request), username(request), hakakses(request)])
			list_org = dictfetchall(cursor)	

		for x in list_org:
			kd_org = x["kode"]
			ur_org = x["urai"]
			organisasi = x["kode"]+" - "+x["urai"]

	arrOrg = {'kode':kd_org, 'urai':ur_org, 'skpd':organisasi}

	return arrOrg

def set_menu(request):
	dt_menu = ""

	# print(modulelist(request))
	if('sipkd_username' in request.session):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT ('/'||link_page) as link, * FROM PENATAUSAHAAN.SET_MENU "\
				"WHERE id_menu = 0 AND id_menu_sub = 0 AND status = true "\
				"AND id_modul in ("+modulelist(request)+") "\
				"ORDER BY id_modul,id_menu,id_menu_sub ASC")
			dt_induk = dictfetchall(cursor)

			cursor.execute("SELECT ('/sipkd/'||modul||'/'||link_page) as link, * FROM PENATAUSAHAAN.SET_MENU "\
				"WHERE id_menu <> 0 AND id_menu_sub = 0 AND status = true "\
				"AND id_modul||'.'||id_menu in ("+listpilih(request)+") "\
				"ORDER BY id_modul,id_menu,id_menu_sub ASC")
			dt_anak1 = dictfetchall(cursor)

			cursor.execute("SELECT ('/sipkd/'||modul||'/'||link_page) as link, * FROM PENATAUSAHAAN.SET_MENU "\
				"WHERE id_menu <> 0 AND id_menu_sub <> 0 AND status = true "\
				"AND id_modul||'.'||id_menu||'.'||id_menu_sub in ("+listsub(request)+") "\
				"ORDER BY id_modul,id_menu,id_menu_sub ASC")
			dt_anak2 = dictfetchall(cursor)

		dt_menu = {'induk':dt_induk, 'anak1':dt_anak1, 'anak2':dt_anak2}
	return dt_menu	

def update_tgl(request):
	now = datetime.datetime.now()
	hari = datetime.datetime.now().strftime("%a")
	tanggal = datetime.datetime.now().strftime("%d")
	bulan = datetime.datetime.now().strftime("%b")
	bulan_angka = datetime.datetime.now().strftime("%m")
	tahunsaiki = datetime.datetime.now().strftime("%Y")
	tglblntahun = tanggal+' '+monthList[bulan]+' '+tahunsaiki

	tahunawal = datetime.datetime.now().date().replace(month=1, day=1)
	hari_awal = tahunawal.strftime("%a")
	tanggal_awal = tahunawal.strftime("%d")
	bulan_awal = tahunawal.strftime("%b")
	tahunsaiki_awal = tahunawal.strftime("%Y")

	# awal tahun mauludy
	tglblntahun_awal = tanggal_awal+' '+monthList[bulan_awal]+' '+tahunsaiki_awal
	# awal tahun mauludy
	tgl_lengkap = dayList[hari]+', '+tglblntahun
	tglblnThLog = tanggal+' '+monthList[bulan]

	return {"tgl_lengkap":tgl_lengkap,"tglblntahun":tglblntahun,"tahunsaiki":tahunsaiki,"tglblnThLog":tglblnThLog,"now":now, "bulan_angka":bulan_angka}

# tanggal global
def tanggal(request):
	tgllengkap  = update_tgl(request)['tgl_lengkap']
	thnlogin 	= ''
	tglsekarang = update_tgl(request)['tglblntahun']
	perubangg   = ""
	configurasi = konfigurasi(request)
	setmenu     = set_menu(request)
	akseshak    = ""
	awaltahun	= '01 Januari '+update_tgl(request)['tahunsaiki']	
	tglblnTh_Log= ""
	awal_tahun  = ""
	akhir_tahun  = ""
	bukan_admin = ["OPERATORSKPD", "BPP", "BENDAHARAKELUAR", "BENDAHARATERIMA"]
	bulan_angka = update_tgl(request)['bulan_angka']

	if(tahun_log(request)):
		thnlogin  = tahun_log(request)
		akseshak  = hakakses(request)
		tglblnTh_Log = update_tgl(request)['tglblnThLog']+" "+thnlogin
		awal_tahun = "01 Januari "+thnlogin
		akhir_tahun = "31 Desember "+thnlogin

	if(perubahan(request) == 1):
		perubangg = " Perubahan"
	
	return {"tanggal":tgllengkap, 'tglsekarang':tglsekarang, 'tgl_login':tglblnTh_Log, 'tahun':thnlogin, 
		'perubangg':perubangg,'conf':configurasi, 'st_menu':setmenu, 'hakakses':akseshak,'awal_tahun':awal_tahun,
		'perubahan':perubahan(request),'awaltahun':awaltahun,'akhir_tahun':akhir_tahun,'bukan_admin':bukan_admin, "bulan_angka":bulan_angka}# select query, function/store procedure
		
def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]


def dictfetchall_format(cursor):
	columns = [col[0] for col in cursor.description]
	return diformat([ dict(zip(columns, row)) for row in cursor.fetchall() ])

def diformat(arg):
	hasil = {}
	for x in range(len(arg)):
		for a,b in arg[x].items():
			hasil[a]=tgl_indo(b) if type(b)==datetime.datetime else b
	return [hasil]

# encrypt decrypt
def decode_base64(data):
    missing_padding = len(data) % 4    
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)    
    return base64.decodebytes(data.encode())

def decrypt(isi,key='%arimaniz&'):
	i = 1
	hsl = ''
	s = decode_base64(isi)
	#print s
	for i in range(len(s)):
		char = s[i:i+1]

		ordchar = ord(char)
		hs = (i % len(isi))-1
		if i == len(key):
			hs = 9
		elif i> len(key):
			hs = (i-len(key) % len(isi)-1)

		if hs == -1:
			hs = len(key)-1

		keychar = key[hs:hs+1]
		ordkeychar = ord(keychar)
		jml = ordchar - ordkeychar
		char = chr(jml)
		hsl += char

	return str(hsl)

def encrypt(isi,key='%arimaniz&'):
	i = 1
	hsl = ''
	s = isi
	#print s
	for i in range(len(s)):
		char = s[i:i+1]

		ordchar = ord(char)
		hs = (i % len(isi))-1
		if i == len(key):
			hs = 9
		elif i> len(key):
			hs = (i-len(key) % len(isi)-1)

		if hs == -1:
			hs = len(key)-1

		keychar = key[hs:hs+1]
		ordkeychar = ord(keychar)
		jml = ordchar + ordkeychar
		char = chr(jml)
		hsl += char		
	return base64.b64encode(hsl.encode('latin',errors = 'ignore')).decode('ascii')

# CONVERT ARRAY MENJADI URL / LINK
def laplink(request, isi):
	# hasil  = '&'.join(["{}={}".format(k, v) for k, v in isi.items()])
	isi['tahun_console'] = tahun_log(request)
	hasil  = urllib.parse.urlencode(isi)
	lapurl = f"http://{request.META['HTTP_HOST']}/report_sikd/?"+hasil	
	return lapurl

def format_rp(value, with_prefix=False, desimal=2):
    rupiah = ''
    if value == '':
        value = 0.00
        
    rp = '{:,}'.format(value).replace('.','|').replace(',','.').replace('|',',')

    

    # return 'Rp. '+rp
    return rp

    #locale.setlocale(locale.LC_NUMERIC, 'IND')
    #rupiah = locale.format("%.*f", (desimal, angka), True)
    #if with_prefix:
     #   return "Rp. {}".format(rupiah)
    #return rupiah

def referer(request):
	ref=re.sub('^https?:\/\/', '', request.META.get('HTTP_REFERER')).split('/')
	referer=''
	
	referer = '/'+ref[1]+'/'+ref[2]+'/'+ref[3]+'/'
	return referer

def array_skpd(request):
	array_skpd=[
		reverse('sipkd:prarkabtlskpd'),
		reverse('sipkd:rkabtlskpd'),
		reverse('sipkd:uploaddatadpadppa'),
		reverse('sipkd:rkabelanjalangsung'),
		reverse('sipkd:prarkabelanjalangsung'),
	]
	return array_skpd

def array_ppkd(request):
	array_ppkd=[
		reverse('sipkd:prarkabtlppkd'),
		reverse('sipkd:rkabtlppkd'),
		reverse('sipkd:uploaddatadpadppappkd')
	]
	return array_ppkd

def read_file_fa(request):
	array = []
	fh = open('assets_root/fonts/css/font-awesome.css',"r")

	with fh as f:
		for line in islice(f, 164, None):
			if "fa-" in line: 
				array.append(line.split(':')[0].split(".")[1])
	return array

def coba(request):
	os.startfile("E:/django-sipkd/sikd/apbd/report/ReportServerConsole.exe")
	return HttpResponse('aasd')

def toAngkaDec(rp):
	x = rp.split(",")
	y = int(x[0].replace('.',''))
	z = str(y)+"."+x[1]
	return z

def set_nama_bank(request):

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * from kasda.kasda_sumberdanarekening where kodesumberdana<>99 ")
		list_bank = dictfetchall(cursor)	

	# print(list_bank)
	# for x in list_bank:
	# 	rekening = x["rekening"]
	# 	bank = x["bank"]		

	arrBank = {'list_bank':list_bank}

	return arrBank

def js(request):
	cjs = ''
	m_modul = ''
	style_spp = ''
	style_spjskpd = ''
	base_64 = ''
	if tahun_log(request):
		cjs = '<script src="'+static('js/modul/config.js')+'"></script>'
		m_modul = '<script src="'+static('js/main-modul.js')+'"></script>'
		base_64 = '<script src="'+static('js/base64.js')+'"></script>'
		
		if(request.path.split('/')[2]=='spp'):
			style_spp = '<script src="'+static('js/modul/spp.js')+'"></script>'
		elif(request.path.split('/')[2]=='spjskpd'):
			style_spjskpd = '<script src="'+static('js/modul/spjskpd.js')+'"></script>'
		
	return {"cjs":cjs, "m_modul":m_modul,"style_spp":style_spp, "base_64":base_64,"style_spjskpd":style_spjskpd}
