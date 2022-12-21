from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def anggarankas(request):

	skpd = set_organisasi(request)
	if skpd["kode"] == '': kode = 0
	else: kode = skpd["kode"]
	btn_upload = ''
	if hakakses(request) =='ADMIN':
		btn_upload = '<span class="input-group-btn">\
						<button onclick="upload()" id="btn_upload" alt="'+reverse('sipkd:modalupload',args=['skpd'])+'"\
		                    class="btn btn-warning btn-sm" title="Upload Data ke SIPKD" type="button">\
		                  <strong><i class="fa fa-upload"></i>&nbsp;&nbsp;Upload</strong>\
		                </button></span>'
	data = {'page':'master','organisasi':skpd["skpd"],'kd_org':kode,'ur_org':skpd["urai"],'btn_upload':btn_upload,}
	return render(request, 'spd/anggarankas.html',data)

def tabsanggarankas(request):

	perubahan = perubahananggaran(request)
	aksi = request.GET.get("ac")
	skpd = request.GET.get("id", 0).split(".")
	arrfilter = [0,0,'0','0']
	list_tot  = ''
	header = ''
	body = ''
	foot = ''
	btn_setuju = ''

	if(skpd != 0):
		for i in range(0,len(skpd)):
			arrfilter[i] = skpd[i]

	arrfilter.insert(0,tahun_log(request))

	if(aksi == "pdptn"):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when lock = 1 then 'checked' else '' end) as pilih, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
				"FROM penatausahaan.fc_angg_kas_pendapatan(%s,%s,%s,%s,%s)",arrfilter)
			list_tbl = dictfetchall(cursor)

	elif(aksi == "btl"):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when lock = 1 then 'checked' else '' end) as pilih, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
				"FROM penatausahaan.fc_angg_kas_belanja(%s,%s,%s,%s,%s)",arrfilter)
			list_tbl = dictfetchall(cursor)

	elif(aksi == "blk"):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when lock = 1 then 'checked' else '' end) as pilih, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna, "\
				"(case when isbold = 0 then '2' when isbold = 2 then '1' else '0' end) as sepasi, "\
				"(case when isbold = 0 then 'italic' when isbold = 1 then 'isbold' else '' end) as tebal, "\
				"(case when isbold = 0 then 'cur_pointer' else '' end) as cursor, "\
				"(case when isbold = 0 then 'Klik Detail Program Kegiatan' else '' end) as detail "\
				"FROM penatausahaan.fc_angg_kas_belanja_langsung(%s,%s,%s,%s,%s)",arrfilter)
			list_tbl = dictfetchall(cursor)


		jan = feb = mar = apr = mei = jun = jul = agu = sep = okt = nov = des = angg = alok = turah = 0
		
		for dt in list_tbl:
			if(dt["isbold"] == 1):
				jan += dt["jan"]
				feb += dt["feb"]
				mar += dt["mar"]
				apr += dt["apr"]
				mei += dt["mei"]
				jun += dt["jun"]
				jul += dt["jul"]
				agu += dt["agu"]
				sep += dt["sep"]
				okt += dt["okt"]
				nov += dt["nov"]
				des += dt["des"]
				angg  += dt["jumlah"]
				alok  += dt["total"]
				turah += dt["sisa"]

		arrnilai = {
			'jan':format_rp(jan),'feb':format_rp(feb),'mar':format_rp(mar),
			'apr':format_rp(apr),'mei':format_rp(mei),'jun':format_rp(jun),
			'jul':format_rp(jul),'agu':format_rp(agu),'sep':format_rp(sep),
			'okt':format_rp(okt),'nov':format_rp(nov),'des':format_rp(des),
			'jumlah':format_rp(angg),'total':format_rp(alok),'sisa':format_rp(turah)}

		list_tot = arrnilai

	elif(aksi == "rinci"):
		program = request.GET.get("pr")
		obj = request.GET.get("kd").split(".")

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.fc_angg_kas_rincian_bl_header(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]+'.'+obj[1],obj[2],obj[3]+'.'+obj[4],obj[5]])
			program = dictfetchall(cursor)

			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
				"FROM penatausahaan.FC_ANGG_KAS_RINCIAN_BL(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]+'.'+obj[1],obj[2],obj[3]+'.'+obj[4],obj[5]])
			list_tbl = dictfetchall(cursor)

		for arr in program:
			list_tot = {'program':arr['program'], 'kegiatan':arr['kegiatan']}

	elif(aksi == "biayain"):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when lock = 1 then 'checked' else '' end) as pilih, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
				"FROM penatausahaan.fc_angg_kas_pembiayaan(%s,%s,%s,%s,%s,'IN')",arrfilter)
			list_tbl = dictfetchall(cursor)

	elif(aksi == "biayaout"):
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
				"(case when lock = 1 then 'checked' else '' end) as pilih, "\
				"(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
				"FROM penatausahaan.fc_angg_kas_pembiayaan(%s,%s,%s,%s,%s,'OUT')",arrfilter)
			list_tbl = dictfetchall(cursor)

	if hakakses(request) =='ADMIN':
		header = '<th rowspan="2" style="background-image:none;">\
                    <input type="checkbox" onclick="cek_uncek_all(this,\'chk_rek\',\''+aksi+'\')"/>\
                </th>'

		for x in range(len(list_tbl)):
			if aksi == 'blk':
				if list_tbl[x]['tebal']=='italic':
					konten = '<input type="hidden" class="hidden" value="'+str(list_tbl[x]['koderekening'])+'" name="kdrek_'+aksi+'">\
			                <input type="hidden" class="hidden" name="cek_'+aksi+'" id="cek_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['lock'])+'">\
			                <input type="hidden" name="sisa_'+aksi+'" id="sisa_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['sisa'])+'">\
			                <input type="checkbox" '+list_tbl[x]['pilih']+' class="chk_rek" \
			                    id="rekchk_'+str(list_tbl[x]['nomor'])+'" '+str(list_tbl[x]['pilih'])+' onClick="checkclick(this, \''+aksi+'_'+str(list_tbl[x]['nomor'])+'\')"/>'
					list_tbl[x]['body'] = '<td align="center">'+konten+'</td>'
				else:
					list_tbl[x]['body']='<td align="center"></td>'
			elif aksi != 'rinci':
				list_tbl[x]['body'] = '<td align="center">\
					                    <input type="hidden" class="hidden" name="cek_'+aksi+'" id="cek_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['lock'])+'">\
					                    <input type="checkbox" '+list_tbl[x]['pilih']+' class="chk_rek"\
					                        id="rekchk_'+str(list_tbl[x]['nomor'])+'" onClick="checkclick(this, \''+aksi+'_'+str(list_tbl[x]['nomor'])+'\')"/>\
					                    <input type="hidden" name="sisa_'+aksi+'"  id="sisa_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['sisa'])+'">\
					                </td>'
		btn_setuju = '<div onclick="proses_setuju_rka(\''+aksi+'\')" class="btn btn-sm btn-primary" title="Setujui Anggaran" id="setuju_rka">\
						        <i class="fa fa-check"></i>&nbsp;&nbsp;Proses Setuju\
						    </div>'
		foot = '<th></th>'

	wr_hijau = wr_kuning = wr_merah = 0
	for x in list_tbl:
		if(x["warna"] == 'hijau'):
			wr_hijau = wr_hijau+1
		elif(x["warna"] == 'kuning'):
			wr_kuning = wr_kuning+1
		elif(x["warna"] == 'merah'):
			wr_merah = wr_merah+1

	data = {'page':aksi, 'perubahan':perubahan, 'list_tbl':ArrayFormater(list_tbl),
		'list_tot':list_tot,'header':header,'body':body,'foot':foot,'btn_setuju':btn_setuju,
		'wr_hijau':wr_hijau, 'wr_kuning':wr_kuning, 'wr_merah':wr_merah}
	return render(request, 'spd/tabel/anggarankas_tabel.html',data)

def aksianggarankas(request):
	perubahan = perubahananggaran(request)
	tahun 	  = tahun_log(request)

	# SIMPAN KLIK KANAN ================================================================================================
	if request.method == 'GET':
		skpd      = request.GET.get("id").split(".")
		aksi      = int(request.GET.get("ac"))
		page      = request.GET.get("pg")
		obj       = request.GET.get("kd").split(".")
		kegt 	  = request.GET.get("kg").split(".")
		jml_angg  = float(request.GET.get("jm"))
		jenis 	  = ''

		nil_14  = (jml_angg/3)
		nil_12  = (jml_angg/12)

		if(page == "pdptn"): jenis = '4' 
		elif(page == "btl"): jenis = '5' 
		elif(page == "rinci"): jenis = '5'
		elif(page == "biayain" or page == "biayaout"): jenis = '6'

		arflP = [tahun,skpd[0],skpd[1],skpd[2],skpd[3],'','0','0','0',obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],jenis,aksi]

		if(aksi == 1):
			arflQ = [nil_14,nil_14,nil_14,0,0,0,0,0,0,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
		elif(aksi == 2):
			arflQ = [0,0,0,nil_14,nil_14,nil_14,0,0,0,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
		elif(aksi == 3):
			arflQ = [0,0,0,0,0,0,nil_14,nil_14,nil_14,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
		elif(aksi == 4):
			arflQ = [0,0,0,0,0,0,0,0,0,nil_14,nil_14,nil_14,tahun,skpd[0],skpd[1],skpd[2],skpd[3],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
		elif(aksi == 12):
			arflQ = [nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,nil_12,tahun,skpd[0],skpd[1],skpd[2],skpd[3],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]

		if(perubahan == 0):
			bulan = "JAN = %s, FEB = %s, MARET = %s, APRIL = %s, MEY = %s, JUN = %s, "\
				"JUL = %s, AGUST = %s, SEPT = %s, OKTO = %s, NOV = %s, DES = %s "
		elif(perubahan == 1):
			bulan = "JAN_P = %s, FEB_P = %s, MARET_P = %s, APRIL_P = %s, MEY_P = %s, JUN_P = %s, "\
				"JUL_P = %s, AGUST_P = %s, SEPT_P = %s, OKTO_P = %s, NOV_P = %s, DES_P = %s "

		if(page == "pdptn"):

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.PENDAPATAN SET "+bulan+" WHERE TAHUN = %s "\
					"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
					"AND KODEUNIT = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
					"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s ",arflQ)
				cursor.execute("select penatausahaan.fc_angg_update_triwulan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",arflP)

		elif(page == "btl"):

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.BELANJA SET "+bulan+" WHERE TAHUN = %s "\
					"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
					"AND KODEUNIT = %s "\
					"AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
					"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s ",arflQ)
				cursor.execute("select penatausahaan.fc_angg_update_triwulan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",arflP)

		elif(page == "rinci"):

			trwul  = (jml_angg/3)
			perbl  = (jml_angg/12)

			if(perubahan == 0):
				bln_rnc = "JAN = %s, FEB = %s, MARET = %s, APRIL = %s, MEY = %s, JUN = %s, "\
					"JUL = %s, AGUST = %s, SEPT = %s, OKTO = %s, NOV = %s, DES = %s "
			elif(perubahan == 1):
				bln_rnc = "JAN_P = %s, FEB_P = %s, MARET_P = %s, APRIL_P = %s, MEY_P = %s, JUN_P = %s, "\
					"JUL_P = %s, AGUST_P = %s, SEPT_P = %s, OKTO_P = %s, NOV_P = %s, DES_P = %s "

			if(aksi == 1):
				arfil = [trwul,trwul,trwul,0,0,0,0,0,0,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
			elif(aksi == 2):
				arfil = [0,0,0,trwul,trwul,trwul,0,0,0,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
			elif(aksi == 3):
				arfil = [0,0,0,0,0,0,trwul,trwul,trwul,0,0,0,tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
			elif(aksi == 4):
				arfil = [0,0,0,0,0,0,0,0,0,trwul,trwul,trwul,tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
			elif(aksi == 12):
				arfil = [perbl,perbl,perbl,perbl,perbl,perbl,perbl,perbl,perbl,perbl,perbl,perbl,tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.BELANJA SET "+bln_rnc+" WHERE TAHUN = %s "\
					"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEUNIT = %s"\
					"AND KODEBIDANG = %s AND KODEPROGRAM = %s AND KODEKEGIATAN = %s AND KODESUBKEGIATAN = %s "\
					"AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
					"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s ", arfil)
				cursor.execute("select penatausahaan.fc_angg_update_triwulan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun,skpd[0],skpd[1],skpd[2],skpd[3],kegt[0]+"."+kegt[1],kegt[2],kegt[3]+"."+kegt[4],kegt[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],jenis,aksi])

		elif(page == "biayain" or page == "biayaout"):
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("UPDATE penatausahaan.PEMBIAYAAN SET "+bulan+" WHERE TAHUN = %s "\
					"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
					"AND KODEUNIT = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
					"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s ",arflQ)
				cursor.execute("select penatausahaan.fc_angg_update_triwulan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",arflP)

		return HttpResponse('Data berhasil disimpan')

	# SIMPAN DATA =============================================================================================
	elif request.method == 'POST':
		data 	= request.POST
		page    = request.GET.get("pg")
		skpd 	= data.get("is_skpd").split(".")

		kdrek 	= data.getlist("kdrek_"+page)
		ls_jum  = [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("jumlah_"+page)]
		jan 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("jan_"+page)]
		feb 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("feb_"+page)]
		mar 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("mar_"+page)]
		apr 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("apr_"+page)]
		mei 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("mei_"+page)]
		jun 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("jun_"+page)]
		jul 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("jul_"+page)]
		agu 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("agu_"+page)]
		sep 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("sep_"+page)]
		okt 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("okt_"+page)]
		nov 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("nov_"+page)]
		des 	= [float(x.replace('.', '').replace(',', '.')) for x in data.getlist("des_"+page)]

		if(perubahan == 0):
			bulan = "JAN = %s, FEB = %s, MARET = %s, APRIL = %s, MEY = %s, JUN = %s, "\
				"JUL = %s, AGUST = %s, SEPT = %s, OKTO = %s, NOV = %s, DES = %s , "\
				"TRIWUL1 = %s, TRIWUL2 = %s, TRIWUL3 = %s, TRIWUL4 = %s "
		elif(perubahan == 1):
			bulan = "JAN_P = %s, FEB_P = %s, MARET_P = %s, APRIL_P = %s, MEY_P = %s, JUN_P = %s, "\
				"JUL_P = %s, AGUST_P = %s, SEPT_P = %s, OKTO_P = %s, NOV_P = %s, DES_P = %s ,"\
				"TRIWUL1_P = %s, TRIWUL2_P = %s, TRIWUL3_P = %s, TRIWUL4_P = %s "

		if(page == "pdptn"):
			for i in range(0,len(kdrek)):
				obj 	= kdrek[i].split(".")
				jumlah  = ls_jum[i]
				triwul1 = jan[i]+feb[i]+mar[i]
				triwul2 = apr[i]+mei[i]+jun[i]
				triwul3 = jul[i]+agu[i]+sep[i]
				triwul4 = okt[i]+nov[i]+des[i]
				arflQ	= [jan[i],feb[i],mar[i],apr[i],mei[i],jun[i],jul[i],agu[i],sep[i],okt[i],nov[i],des[i],
							triwul1, triwul2, triwul3, triwul4, tahun,skpd[0],skpd[1],skpd[2],skpd[3],
							obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
				tot_trw = triwul1+triwul2+triwul3+triwul4

				if(tot_trw > jumlah):
					return HttpResponse('GAGAL MENYIMPAN DATA, total alokasi dana melebihi jumlah anggaran !!')
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.PENDAPATAN SET "+bulan+" WHERE TAHUN = %s "\
							"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
							"AND KODEUNIT = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
							"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s",arflQ)
					
		elif(page == "btl"):
			for i in range(0,len(kdrek)):
				obj 	= kdrek[i].split(".")
				jumlah  = ls_jum[i]
				triwul1 = jan[i]+feb[i]+mar[i]
				triwul2 = apr[i]+mei[i]+jun[i]
				triwul3 = jul[i]+agu[i]+sep[i]
				triwul4 = okt[i]+nov[i]+des[i]
				arflQ	= [jan[i],feb[i],mar[i],apr[i],mei[i],jun[i],jul[i],agu[i],sep[i],okt[i],nov[i],des[i],
							triwul1, triwul2, triwul3, triwul4, tahun,skpd[0],skpd[1],skpd[2],skpd[3],
							obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
				tot_trw = triwul1+triwul2+triwul3+triwul4

				if(tot_trw > jumlah):
					return HttpResponse('GAGAL MENYIMPAN DATA, total alokasi dana melebihi jumlah anggaran !!')
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BELANJA SET "+bulan+" WHERE TAHUN = %s "\
							"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
							"AND KODEUNIT = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
							"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s",arflQ)

		elif(page == "rinci"):
			x_keg = data.get("kegiatan").split(" - ")[0]
			keg   = x_keg.split(".")

			for i in range(0,len(kdrek)):
				obj 	= kdrek[i].split(".")
				jumlah  = ls_jum[i]
				triwul1 = jan[i]+feb[i]+mar[i]
				triwul2 = apr[i]+mei[i]+jun[i]
				triwul3 = jul[i]+agu[i]+sep[i]
				triwul4 = okt[i]+nov[i]+des[i]
				arflQ	= [jan[i],feb[i],mar[i],apr[i],mei[i],jun[i],jul[i],agu[i],sep[i],okt[i],nov[i],des[i],
							triwul1, triwul2, triwul3, triwul4, tahun,skpd[0],skpd[1],skpd[2],skpd[3],
							keg[0]+'.'+keg[1],keg[2],keg[3]+'.'+keg[4],keg[5],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
				tot_trw = triwul1+triwul2+triwul3+triwul4

				if(tot_trw > jumlah):
					return HttpResponse('GAGAL MENYIMPAN DATA, total alokasi dana melebihi jumlah anggaran !!')
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BELANJA SET "+bulan+" WHERE TAHUN = %s "\
							"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
							"AND KODEUNIT = %s AND KODEBIDANG = %s AND KODEPROGRAM = %s AND KODEKEGIATAN = %s "\
							"AND KODESUBKEGIATAN = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
							"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s", arflQ)

		elif(page == "biayain" or page == "biayaout"):
			for i in range(0,len(kdrek)):
				obj 	= kdrek[i].split(".")
				jumlah  = ls_jum[i]
				triwul1 = jan[i]+feb[i]+mar[i]
				triwul2 = apr[i]+mei[i]+jun[i]
				triwul3 = jul[i]+agu[i]+sep[i]
				triwul4 = okt[i]+nov[i]+des[i]
				arflQ	= [jan[i],feb[i],mar[i],apr[i],mei[i],jun[i],jul[i],agu[i],sep[i],okt[i],nov[i],des[i],
							triwul1, triwul2, triwul3, triwul4, tahun,skpd[0],skpd[1],skpd[2],skpd[3],
							obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]]
				tot_trw = triwul1+triwul2+triwul3+triwul4

				if(tot_trw > jumlah):
					return HttpResponse('GAGAL MENYIMPAN DATA, total alokasi dana melebihi jumlah anggaran !!')
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.PEMBIAYAAN SET "+bulan+" WHERE TAHUN = %s "\
							"AND KODEURUSAN = %s AND KODESUBURUSAN = %s AND KODEORGANISASI = %s "\
							"AND KODEUNIT = %s AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s "\
							"AND KODEOBJEK = %s AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s",arflQ)

		return HttpResponse('Data berhasil disimpan')

	else:
		return HttpResponse('Simpan data gagal !!')


def aksipersetujuanrka(request):
	if request.method == 'POST':
		perubahan = perubahananggaran(request)
		tahun 	  = tahun_log(request)
		data 	  = request.POST
		page      = request.GET.get("pg")
		skpd 	  = data.get("organisasi").split(".")
		pesan 	  = ''

		if(perubahan == 0): lock = "LOCK = %s"
		else: lock = "LOCK_P = %s"

		if(page == 'pdptn'):
			kdrek = data.getlist("kdrek_pdptn")
			for i in range(0,len(kdrek)):
				obj = kdrek[i].split(".")
				lck = data.getlist("cek_pdptn")[i]

				if (data.getlist("sisa_pdptn")[i] == '0.00') or (data.getlist("sisa_pdptn")[i] == '0,00'):
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.PENDAPATAN SET "+lock+" WHERE TAHUN = %s AND KODEURUSAN = %s \
						  AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
						  AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s AND KODEOBJEK = %s \
						  AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s",[lck,tahun,skpd[0],
						  skpd[1],skpd[2],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]])

					status = True
				else:
					status = False

		elif(page == 'btl'):
			kdrek = data.getlist("kdrek_btl")
			for i in range(0,len(kdrek)):
				obj = kdrek[i].split(".")
				lck = data.getlist("cek_btl")[i]

				if (data.getlist("sisa_btl")[i] == '0.00') or (data.getlist("sisa_btl")[i] == '0,00'):
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BELANJA SET "+lock+" WHERE TAHUN = %s AND KODEURUSAN = %s \
						  AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
						  AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s AND KODEOBJEK = %s \
						  AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s ",[lck,tahun,skpd[0],
						  skpd[1],skpd[2],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]])

					status = True
				else:
					status = False

		elif(page == 'blk'):
			kdrek = data.getlist("kdrek_blk")
			for i in range(0,len(kdrek)):
				obj = kdrek[i].split(".")
				lck = data.getlist("cek_blk")[i]
				
				if (data.getlist("sisa_blk")[i] == '0.00') or (data.getlist("sisa_blk")[i] == '0,00'):
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.BELANJA SET "+lock+" WHERE TAHUN = %s AND KODEURUSAN = %s \
						  AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
						  AND KODEBIDANG = %s AND KODEPROGRAM = %s AND KODEKEGIATAN = %s AND KODESUBKEGIATAN = %s",
						  [lck,tahun,skpd[0],skpd[1],skpd[2],obj[0]+'.'+obj[1],obj[2],obj[3]+'.'+obj[4],obj[5]])

					status = True
				else:
					status = False

		
		elif(page == 'biayain' or page == 'biayaout'):
			kdrek = data.getlist("kdrek_"+page)
			for i in range(0,len(kdrek)):
				obj = kdrek[i].split(".")
				lck = data.getlist("cek_"+page)[i]
				
				if (data.getlist("sisa_"+page)[i] == '0.00') or (data.getlist("sisa_"+page)[i] == '0,00'):
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.PEMBIAYAAN SET "+lock+" WHERE TAHUN = %s AND KODEURUSAN = %s \
						  AND KODESUBURUSAN = %s AND KODEORGANISASI = %s \
						  AND KODEAKUN = %s AND KODEKELOMPOK = %s AND KODEJENIS = %s AND KODEOBJEK = %s \
						  AND KODERINCIANOBJEK = %s AND KODESUBRINCIANOBJEK = %s",[lck,tahun,skpd[0],
						  skpd[1],skpd[2],obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]])

					status = True
				else:
					status = False

		if (status == True):
			pesan = {'sts':'success','msg':'Data Persetujuan berhasil disimpan'}
		else:
			pesan = {'sts':'error','msg':'Persetujuan DITOLAK, masih ada Sisa Alokasi'}

		return JsonResponse(pesan)