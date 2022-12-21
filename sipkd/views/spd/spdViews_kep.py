# from typing import cast
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def spd_kep(request):
	print('cek')
	return render(request,'spd/spd_kep.html')

# def ambil_bendahara(request):
# 	dataBendahara = ''
# 	kode_organisasi = request.POST.get('kode_organisasi','')
# 	if kode_organisasi!='':
# 		kd_urusan = kode_organisasi.split('.')[0] 
# 		kd_suburusan = kode_organisasi.split('.')[1]
# 		kd_organisasi = kode_organisasi.split('.')[2]
# 		with connections[tahun_log(request)].cursor() as cursor: 
# 			cursor.execute('SELECT * FROM master.pejabat_skpd \
# 							WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and trim(kodeorganisasi) = %s and jenissistem = 2\
# 									and jabatan LIKE \'Bendahara Pengeluaran SKPD\'',[tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi])
# 			dataBendahara = dictfetchall(cursor)
# 	return HttpResponse(json.dumps(dataBendahara))

def rinci_spd_kep(request):
	hasil = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and nospd != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
				and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s',
				[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])
			hasil = ArrayFormater(dictfetchall(cursor))
	data = {
		'hasil':hasil,
	}

	return JsonResponse(data)

def link_tabel_rinci_spd_kep(request):
	data_rincian = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')
	
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and nospd != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT row_number() over() as nomor, \
				nodpa, uraian, anggaran, lalu, sekarang, jumlah, sisa, \
				kodebidang||'|'||kodeprogram||'|'||kodekegiatan||'|'||kodesubkegiatan as kode \
				FROM penatausahaan.fc_view_spd_tbl_rinci_bulanan(%s,%s,%s,%s,%s,%s)",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])
			data_rincian = ArrayFormater(dictfetchall(cursor))

	data = {'dt_rincian':data_rincian}
		
	return render(request,'spd/tabel/tabel_spd_rincian.html', data)

def modal_rinci_spd_kep(request):
	aidirow = request.GET.get("i")
	print(request.GET.get("tk",''))
	token 	= request.GET.get("tk",'').split("|")
	skpd 	= token[0].split(".")
	kdurusan = skpd[0]
	kdsuburusan = skpd[1]
	kdorganisasi = skpd[2]
	kdunit = skpd[3]
	nospd = token[1]
	bulan = token[2]
	jenisdpa = token[3]

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and bulan != '' and jenisdpa != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT nodpa, uraian, coalesce(sekarang,0)as sekarang, \
				coalesce(anggaran,0)||'|'||coalesce(lalu,0)||'|'||coalesce(jumlah,0)||'|'||coalesce(sisa,0) as uang, \
				kodebidang||'|'||kodeprogram||'|'||kodekegiatan||'|'||kodesubkegiatan as kode \
				FROM penatausahaan.fc_view_spd_rincian_bulanan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,bulan,bulan,jenisdpa,0])
			hasil = dictfetchall(cursor)

	data = {'aidirow':aidirow, 'hasil':ArrayFormater(hasil)}
	return render(request,'spd/modal/modal_spd_rinci.html', data)

def cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa):
	jumlah = ''
	if jenisdpa=='DPA-SKPD' or jenisdpa=='DPPA-SKPD':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(*) as jumlah, nospd  FROM penatausahaan.spd WHERE tahun=%s \
				and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
				and jenisdpa in ('DPA-SKPD','DPPA-SKPD')  GROUP BY nospd",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
			jumlah = cursor.fetchone()
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT count(*) as jumlah, nospd  FROM penatausahaan.spd WHERE tahun=%s \
				and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
				and jenisdpa in ('DPA-PPKD','DPPA-PPKD')  GROUP BY nospd",
				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
			jumlah = cursor.fetchone()
	return '0' if jumlah==None else jumlah

# def cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa,jenis=False):
# 	jumlah = ''
# 	if jenisdpa=='DPA-SKPD' or jenisdpa=='DPPA-SKPD':
# 		# count(*) as jumlah
# 		if jenis == True:
# 			with connections[tahun_log(request)].cursor() as cursor:
# 				cursor.execute("SELECT 1 as jumlah, nospd  FROM penatausahaan.spd \
# 					WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
# 					and jenisdpa in ('DPA-SKPD','DPPA-SKPD')\
# 					 GROUP BY nospd",
# 					[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
# 				jumlah = cursor.fetchone()
# 		else:
# 			with connections[tahun_log(request)].cursor() as cursor:
# 				cursor.execute("SELECT 0 as jumlah, nospd  FROM penatausahaan.spd \
# 					WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
# 					and jenisdpa in ('DPA-SKPD','DPPA-SKPD')\
# 					 GROUP BY nospd",
# 					[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit])
# 				jumlah = cursor.fetchone()
# 	else:
# 		with connections[tahun_log(request)].cursor() as cursor:
# 			cursor.execute("SELECT count(*) as jumlah,nospd  FROM penatausahaan.spd \
# 				WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
# 				and jenisdpa in ('DPA-PPKD','DPPA-PPKD') and  BULAN_AWAL=%s \
# 				GROUP BY nospd",
# 				[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
# 			jumlah = cursor.fetchone()
# 	return '0' if jumlah==None else jumlah

def cek_data_spd(request, nospd):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT count(*) as jumlah FROM penatausahaan.spd \
			WHERE tahun=%s and nospd=%s",[tahun_log(request),nospd])
		jumlah = cursor.fetchone()
	return '0' if jumlah==None else jumlah

def simpan_spd_kep(request):
	skpd = request.POST.get('skpd_spd','').split(".")
	kdurusan = skpd[0]
	kdsuburusan = skpd[1]
	kdorganisasi = skpd[2]
	kdunit = skpd[3]
	nospd = request.POST.get('no_spd','').upper()
	bulan = request.POST.get('bulan','')
	jenisdpa = request.POST.get('jnsdpa','')
	jumlah_total = request.POST.get('jum_tot_spd','')
	tanggal_draft = tgl_to_db(request.POST.get('tanggal_spd','')) 
	bendahara = request.POST.get('bendahara_kep','')
	isSimpan = request.POST.get('isSimpan')
	no_spdold = request.POST.get('no_spdold','').upper()

	# TambahFitur: Input Ketentuan Lain Lain
	ketentuan = request.POST.get('ketentuan','')
	print(ketentuan)
	# EndTambahFitur: Input Ketentuan Lain Lain

	# TABEL RINCIAN SPD
	nodparinci = request.POST.getlist('nodparinci')
	kodebelanja = request.POST.getlist('kodebelanja')
	jml_spd_now = request.POST.getlist('jml_spd_now')

	jumlah = ''
	hasil = ''
	is_hasil = 0

	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
		with connections[tahun_log(request)].cursor() as cursor:
			# Kalau buat SPD baru
			if isSimpan=='true':
				# if int(cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa)[0])!=0:
				# 	is_hasil = 0
				# 	hasil = 'SPD pada bulan ini sudah pernah dibuat !'
				# else:
				if nospd!='' or jenisdpa!='' or bendahara!='':
					if int(cek_data_spd(request, nospd)[0])!=0:
						is_hasil = 0
						hasil = 'Nomor SPD sudah ada !'
					else:
						try:
							# TambahFitur: Input Ketentuan Lain Lain
							cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
								nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,\
								jumlahspd,uname, uraian) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
								[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,tanggal_draft,tanggal_draft,tanggal_draft, 
								bendahara, bulan,bulan,jenisdpa, jumlah_total,username(request), ketentuan])
							# EndTambahFitur: Input Ketentuan Lain Lain
							is_hasil = 1
							hasil = 'Simpan SPD berhasil !'
						except IntegrityError as e:
							is_hasil = 0
							hasil = 'Nomor SPD sudah ada !'
				else:
					is_hasil = 0
					hasil = 'Lengkapi data terlebih dahulu !'
			# Kalau update data SPD
			else:
				if int(cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa)[0])!=0:
					try:
						# TambahFitur: Input Ketentuan Lain Lain
						cursor.execute('UPDATE penatausahaan.spd set nospd=%s, tanggal_draft=%s, tanggal=%s, tgldpa=%s, \
							bendaharapengeluaran=%s, jenisdpa=%s, bulan_awal=%s,bulan_akhir=%s, uraian=%s WHERE tahun = %s \
							and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and upper(nospd) = %s',
							[nospd, tanggal_draft,tanggal_draft,tanggal_draft, bendahara, jenisdpa,bulan,bulan,ketentuan,
							tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spdold])
						# EndTambahFitur: Input Ketentuan Lain Lain
						is_hasil = 1
						hasil = 'Simpan SPD berhasil !'
					except IntegrityError as e:
						is_hasil = 0
						hasil = 'Nomor SPD sudah ada !'
				else:
					# pass
					if nospd!='' or jenisdpa!='' or bendahara!='':
						if int(cek_data_spd(request, nospd)[0])!=0:
							is_hasil = 0
							hasil = 'Nomor SPD sudah ada !'
						else:
							try:
								cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
									nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,\
									uname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
									[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,tanggal_draft,tanggal_draft,tanggal_draft, bendahara, bulan,bulan,jenisdpa,username(request)])
								is_hasil = 1
								hasil = 'Simpan SPD berhasil !'
							except IntegrityError as e:
								is_hasil = 0
								hasil = 'Nomor SPD sudah ada !'

			# insert SPD rincian (ADD dan UPDATE)
			if is_hasil == 1:
				# HAPUS TABEL SPD RINCIAN WHERE NO.SPD
				cursor.execute("DELETE FROM penatausahaan.spdrincian WHERE tahun = %s AND nospd = %s \
					AND kodeurursan = %s AND kodesuburusan = %s AND kodeorganisasi = %s AND kodeunit = %s",
					[tahun_log(request),nospd,kdurusan,kdsuburusan,kdorganisasi,kdunit])

				for x in range(len(nodparinci)):
					if nodparinci[x] != "":
						mai_lope = kodebelanja[x].split("|")
						kdbidang = mai_lope[0]
						kdprogram = mai_lope[1]
						kdkegiatan = mai_lope[2]
						kdsubkegiatan = mai_lope[3]
						kdsubkeluaran = 0
						mau_uangbeb = toAngkaDec(jml_spd_now[x])
						#mau_uangbeb = jml_spd_now[x]
						# INSERT TABEL SPD RINCIAN
						cursor.execute("INSERT INTO penatausahaan.spdrincian (tahun, kodeurursan, kodesuburusan, kodeorganisasi, kodeunit, nospd, \
							kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, kodesubkeluaran, jumlah) \
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,
							kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,kdsubkeluaran,mau_uangbeb])

	return HttpResponse(hasil)

def hapus_spd_kep(request):
	hasil = ''
	kdurusan = request.POST.get('kdurusan','')
	kdsuburusan = request.POST.get('kdsuburusan','')
	kdorganisasi = request.POST.get('kdorganisasi','')
	kdunit = request.POST.get('kdunit','')
	nospd = request.POST.get('nospd','')
	
	if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT LOCKED FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
				and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
			jumlah = cursor.fetchone()

			if jumlah[0]=='Y':
				hasil = 'SPD sudah di lock !'
			else:
				cursor.execute("DELETE FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
					and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
					[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
				hasil = 'Data SPD berhasil dihapus !'
	return HttpResponse(hasil)

def render_cetak_spd_kep(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1  FROM master.pejabat_skpkd \
			where jenissistem=2 and tahun=%s and upper(jabatan) LIKE '%%BENDAHARA UMUM%%'",[tahun_log(request)])
		pejabat = dictfetchall(cursor)
	
	data = {
		'pejabat':pejabat,
	}
	return render(request, 'spd/modal/modal_cetak_spd.html',data)

def cetak_spd_kep(request):
	post 	= request.POST
	lapParm = {}
	skpd 	= post.get('skpd').split('.')
	no_spd = post.get('no_spd')
	id_jabatan = post.get('id_jabatan')

	lapParm['file'] 		= 'penatausahaan/spd/SPD.fr3'
	lapParm['NOMER'] = "'"+no_spd+"'"
	lapParm['tahun'] = "'"+tahun_log(request)+"'"
	lapParm['ID'] = "'"+id_jabatan+"'"				
	lapParm['KodeUrusan'] = "'"+skpd[0]+"'"
	lapParm['KodeSubUrusan'] = "'"+skpd[1]+"'"
	lapParm['KodeOrganisasi'] = "'"+skpd[2]+"'"
	lapParm['KodeUnit'] = "'"+skpd[3]+"'"
	lapParm['report_type'] = 'pdf'


	return HttpResponse(laplink(request, lapParm))

# # tambahan autonospd
def autonospd_kep(request):
	try:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT nospd FROM penatausahaan.spd WHERE tahun=%s \
				ORDER BY nospd DESC LIMIT 1", [tahun_log(request)])
			nospd = dictfetchall(cursor)

		print(len(nospd))

		if len(nospd) < 1:
			nomorbaru = 1
			nomorbaru = str(nomorbaru).zfill(4)
		else:
			for arr in nospd:
				data = arr['nospd']
			data = data.replace(' ', '')
			data = data.split('/')
			nomorbaru = str(int(data[0])+1)
			nomorbaru = nomorbaru.zfill(4)
			
		nomorbaru = f"{nomorbaru}/SPD/{tahun_log(request)}"
		data = {'nospd': nomorbaru}
		# print(nomorbaru)
	except:
		data = {'nospd': ''}
		
	return JsonResponse(data)

def cetakdpa(request):
	if request.method == 'GET':
		return render(request, 'spd/modal/modal_cetak_dpa.html',{})
	if request.method == 'POST':
		post 	= request.POST
		lapParm = {}
		where0 	= ""
		where1  = ""

		organisasi 	= post.get('organisasi').split('.')
		program 	= post.get('program')
		kegiatan 	= post.get('kegiatan')

		pchprog 	= program.split('.')
		pchkegn 	= kegiatan.split('.')

		penjadwalan1 = post.get('jadwal_penatausahaan_1', '')
		penjadwalan2 = post.get('jadwal_penatausahaan_2', '')

		lapParm['file'] 		= 'anggaran/dpa_skpd.fr3'	
		lapParm['xperubahan'] 	= '0'

		if((program != '0') and (kegiatan == '0')):
			where0 = f" and a.kodebidang='{pchprog[0]}.{pchprog[1]}' and a.kodeprogram={pchprog[2]}"
			where1 = f" and a.kodebidang='{pchprog[0]}.{pchprog[1]}' and a.kodeprogram={pchprog[2]}"
		elif((program != '0') and (kegiatan != '0')):
			where0 = f" and a.kodebidang='{pchprog[0]}.{pchprog[1]}' and a.kodeprogram={pchprog[2]} and a.kodekegiatan='{pchkegn[3]}.{pchkegn[4]}'"
			where1 = f" and a.kodebidang='{pchprog[0]}.{pchprog[1]}' and a.kodeprogram={pchprog[2]} and a.kodekegiatan='{pchkegn[3]}.{pchkegn[4]}'"

		lapParm['tahun'] 			= "'"+tahun_log(request)+"'"
		lapParm['hakakses'] 		= "'"+hakakses(request)+"'"
		lapParm['jenissistem'] 		= '1'
		lapParm['report_type'] 		= 'pdf'
		lapParm['kodeurusan'] 		= "'"+organisasi[0]+"'"
		lapParm['kodesuburusan'] 	= "'"+organisasi[1]+"'"
		lapParm['kodeorganisasi'] 	= "'"+organisasi[2]+"'"
		lapParm['kodeunit'] 		= "'"+organisasi[3]+"'"
		lapParm['idpa'] 			= "'"+post.get('jabatan')+"'"
		lapParm['temp'] 			= post.get('cek_cbx')
		lapParm['TGLCETAK'] 		= post.get('tanggal_cetak')
		lapParm['halaman']			= "'"+post.get('halaman')+"'"
		lapParm['where'] 			= where0
		lapParm['where1'] 			= where1

		# tambahan penjadwalan
		lapParm['jadwal1']			= "'"+post.get('jadwal_penatausahaan_1')+"'"
		lapParm['jadwal2']			= "'"+post.get('jadwal_penatausahaan_2')+"'"

		return HttpResponse(laplink(request, lapParm))
	

def load_data_cetak_dpa(request):
	skpd = request.GET.get('skpd', 0).split('.')
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""select * from master.pejabat_skpd where tahun = %s 
			and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s
			and kodeunit = %s and jenissistem = 1 order by id""", [tahun_log(request), skpd[0], skpd[1], skpd[2], skpd[3] ])
		pejabat = ArrayFormater(dictfetchall(cursor))
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""select kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, urai from penatausahaan.kegiatan 
			where tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s
			and kodeunit = %s and kodebidang<>'0' and kodeprogram<>0 and kodekegiatan='0' and kodesubkegiatan=0 and kodesubkeluaran=0
			order by kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan""", [tahun_log(request), skpd[0], skpd[1], skpd[2], skpd[3] ])
		program = ArrayFormater(dictfetchall(cursor))

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""select kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan, urai from penatausahaan.kegiatan 
			where tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s
			and kodeunit = %s and kodebidang<>'0' and kodeprogram<>0 and kodekegiatan<>'0' and kodesubkegiatan=0 and kodesubkeluaran=0
			order by kodebidang, kodeprogram, kodekegiatan, kodesubkegiatan""", [tahun_log(request), skpd[0], skpd[1], skpd[2], skpd[3] ])
		kegiatan = ArrayFormater(dictfetchall(cursor))

	return JsonResponse({'pejabat':pejabat,'program': program,'kegiatan': kegiatan})