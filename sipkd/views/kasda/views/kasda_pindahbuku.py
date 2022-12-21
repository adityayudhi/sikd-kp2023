from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def index(request):
	dt_sumberdana = put_kasda_sumberdana(request)
	data = {'dt_sumdan':dt_sumberdana,}

	return render(request, 'kasda/kasda_pindahbuku.html', data)

def simpan(request,jenis): 
	isSimpan = 0
	data 	 = request.POST
	uname_x  = username(request)
	tahun 	 = tahun_log(request)
	tgl_saiki = 'now()'

	# JENIS UNTUK ADD dan EDIT ====================================================
	if jenis.lower() == 'upper': 
		aksi 			= data.get('aksi')
		no_bukukas 		= data.get('no_bukukas')
		no_bukukas_xx 	= data.get('no_bukukas_xx')
		no_bukti 		= data.get('no_bukti')
		no_bukti_xx 	= data.get('no_bukti_xx')
		skpd 			= data.get('organisasi').split('.')
		tgl_bukti 		= tgl_short(data.get('tgl_bukti'))
		tgl_transaksi 	= tgl_short(data.get('tgl_transaksi'))
		sumdana_fr	 	= data.get('sumber_dana_from')
		sumdana_to		= data.get('sumber_dana_to') 
		deskripsi 		= data.get('deskripsi')
		jml_transaksi 	= toAngkaDec(data.get('jml_transaksi'))
		kdBidang 		= skpd[0]+'.'+skpd[1].zfill(2)


		# AKSI ADD -> INSERT =====================================================
		if aksi.lower() == 'true':
			with connections[tahun_log(request)].cursor() as cursor:
				no_bukukas = cek_kasda_autoNoKas(request) ### dari support_sipkd
				if no_bukti != '':
					if cek_noBukti(tahun,no_bukti) >= 1: ### dari support_sipkd
						isSimpan = 0
						pesan 	 = 'Transaksi dengan nomor : '+no_bukti+', sudah digunakan !!'
					else:
						if no_bukukas != '' and data.get('organisasi') != '':
							try:
								cursor.execute("INSERT INTO kasda.kasda_transaksi(\
								tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nobukukas,nobukti,\
								deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi,lastupdate,\
								username,locked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun,skpd[0],skpd[1],skpd[2],skpd[3],no_bukukas,no_bukti,deskripsi,'0',
								tgl_transaksi,tgl_bukti,'99','PINDAHBUKU',tgl_saiki,uname_x,'T'])
								
								xx_nobukas = no_bukukas
								isSimpan = 1
								pesan 	 = 'Nomor Transaksi : '+no_bukti+' berhasil disimpan !'

							except IntegrityError as e:
								isSimpan = 0
								pesan 	 = 'Nomor Transaksi : '+no_bukti+' sudah ada !'
						else:
							isSimpan = 0
							pesan 	 = 'Lengkapi data terlebih dahulu !'
				else:
					isSimpan = 0
					pesan 	 = 'Lengkapi data terlebih dahulu !'
			
		# AKSI EDIT -> UPDATE ====================================================
		else: 
			cek_lock = cek_kasda_isLocked(tahun,no_bukukas_xx,no_bukti_xx) ### dari support_sipkd

			if cek_lock == 'Y':
				isSimpan = 0
				pesan = 'Nomor Buku Kas: "'+no_bukukas_xx+'" telah di ACC oleh pimpinan. Anda tidak diperkenankan mengedit data tersebut!'
			elif no_bukti_xx != no_bukti and cek_noBukti(tahun,no_bukti_xx) >= 1 and no_bukukas == no_bukukas_xx:
				isSimpan = 0
				pesan 	 = 'Transaksi dengan nomor : '+no_bukti_xx+', sudah digunakan !!'
			elif no_bukukas != no_bukukas_xx and cek_NoBuKas(tahun,no_bukukas) >= 1:
				isSimpan = 0
				pesan 	 = 'Nomor Buku Kas : '+no_bukukas+', sudah digunakan !!'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					try:
						cursor.execute("UPDATE kasda.kasda_transaksi SET nobukukas=%s, nobukti = %s, tglbukti = %s,\
							kodesumberdana = %s, tanggal = %s, deskripsi = %s, lastupdate = %s,\
							jenistransaksi = %s, kdlokasi = %s, username = %s,kodeurusan=%s,\
							kodesuburusan=%s, kodeorganisasi=%s, kodeunit=%s WHERE tahun = %s\
							AND nobukukas = %s",[ no_bukukas,no_bukti,tgl_bukti,'99',tgl_transaksi,deskripsi,
							tgl_saiki,'PINDAHBUKU','0',uname_x,skpd[0],skpd[1],skpd[2],skpd[3],tahun,no_bukukas_xx])

						if no_bukukas != no_bukukas_xx:
							cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s AND nobukukas = %s ",
							[tahun,no_bukukas_xx])
							xx_nobukas = no_bukukas
						else:
							xx_nobukas = no_bukukas_xx
							
						isSimpan = 1
						pesan = 'Perubahan nomor Buku Kas : '+no_bukukas_xx+' berhasil disimpan !'

					except IntegrityError as e:
						isSimpan = 0
						pesan 	 = 'Nomor Transaksi : '+no_bukti_xx+' sudah ada !'

		# SIMPAN DETAIL
		# ARRAY untuk simpan detail transaksi
		arrTepungKanji = [{'field':'PENGELUARAN','kdsub':1,'kdsum':sumdana_fr},
			{'field':'PENERIMAAN','kdsub':2,'kdsum':sumdana_to}]

		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN WHERE kasda
				cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s AND nobukukas = %s ",
					[tahun,xx_nobukas])

				# INSERT INTO TABEL RINCIAN 
				for dx in arrTepungKanji:
					cursor.execute("INSERT INTO kasda.KASDA_TRANSAKSI_DETIL(TAHUN,NOBUKUKAS,\
					KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,\
					KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,\
					KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,\
					"+dx['field']+",KD_SUMBER_DANA,KODESUBKELUARAN) \
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
					[tahun,xx_nobukas,skpd[0],skpd[1],skpd[2],skpd[3],kdBidang,0,0,'0',0,0,0,0,0,dx['kdsub'],jml_transaksi,dx['kdsum'],0])

	# UNTUK DELETE ===============================================================
	else: 
		no_bukukas_xx = data['nobkas']
		no_bukti_xx = data['nobuk']
		cek_lock = cek_kasda_isLocked(tahun,no_bukukas_xx,no_bukti_xx) ### dari support_sipkd

		if cek_lock == 'Y':
			isSimpan = -1
			pesan = 'Nomor Buku Kas: "'+no_bukukas_xx+'" telah di ACC oleh pimpinan. Anda tidak diperkenankan menghapus data tersebut!'
		else:
			if data['aksi'].lower() == 'false':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO kasda.kasda_transaksi_del(tahun,nobukukas,nobukti,\
						kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
						deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi,lastupdate,\
						username,locked,username_del,tgl_del)\
						SELECT tahun,nobukukas,nobukti,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
						deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi,lastupdate,\
						username,locked,%s,%s \
						FROM kasda.kasda_transaksi WHERE tahun = %s AND nobukukas = %s",
						[uname_x, tgl_saiki, tahun, no_bukukas_xx])

					cursor.execute("INSERT INTO kasda.kasda_transaksi_detil_del(tahun,nobukukas,\
						kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
						kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,\
						kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,\
						penerimaan,pengeluaran,username_del,tgl_del) \
						SELECT tahun,nobukukas,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,\
						kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,\
						kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,\
						penerimaan,pengeluaran,%s,%s \
						FROM kasda.kasda_transaksi_detil WHERE tahun = %s AND nobukukas = %s",
						[uname_x, tgl_saiki, tahun, no_bukukas_xx])

					cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s AND nobukukas = %s",
						[tahun, no_bukukas_xx])
					cursor.execute("DELETE FROM kasda.kasda_transaksi WHERE tahun = %s AND nobukukas = %s",
						[tahun, no_bukukas_xx])

					isSimpan = 0
					pesan = 'Data Transaksi Dengan Nomor Buku Kas: '+no_bukukas_xx+', berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)

def load_data(request):
	tahun = tahun_log(request)
	psdt = request.POST
	skpd = psdt['skpd'].split('.')
	nobukas = psdt['nobkas']
	nobukti = psdt['no_bukti']

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select d.kodebidang||'.'||d.kodeorganisasi||'.'||d.kodeprogram||'.'||d.kodekegiatan\
			||'.'||d.kodesubkegiatan||'-'||d.KodeAkun||'.'||d.KodeKelompok\
			||'.'||d.KodeJenis||'.'||lpad(d.kodeobjek::text,2,'0')||'.'||lpad(d.koderincianobjek::text,2,'0')\
			||'.'||lpad(d.kodesubrincianobjek::text,4,'0') AS KODEREKENING,t.*,r.*,d.*,\
			d.kodeurusan||'.'||d.kodesuburusan||'.'||d.kodeorganisasi||'.'||d.kodeunit as skpd,\
			(select urai from master.master_organisasi mo where mo.tahun=d.tahun and mo.kodeurusan = t.kodeurusan\
			and mo.kodesuburusan = t.kodesuburusan and mo.kodeorganisasi = t.kodeorganisasi \
			and mo.kodeunit = t.kodeunit) as organisasi\
			from kasda.kasda_transaksi t join  kasda.KASDA_TRANSAKSI_DETIL d on d.nobukukas=t.nobukukas \
			and d.tahun=t.tahun left join master.master_rekening r on\
			r.kodeakun=d.kodeakun and r.kodekelompok=d.kodekelompok and r.kodejenis=d.kodejenis \
			and r.kodeobjek=d.kodeobjek and r.koderincianobjek=d.koderincianobjek \
			and r.kodesubrincianobjek=d.kodesubrincianobjek and r.tahun=d.tahun\
			where t.tahun=%s and t.nobukukas=%s and d.kodeakun=0\
			order by d.kodeakun,d.kodekelompok,d.kodejenis,d.kodeobjek,d.koderincianobjek,d.kodesubrincianobjek",
			[tahun,nobukas])
		
		hsl = dictfetchall(cursor)

	if(hsl):
		for i in range(len(hsl)):
			if(hsl[0]['locked'] == 'T'):
				PESAN 	= ''
			else:
				PESAN 	= 'Nomor Buku Kas: '+hsl[0]['nobukukas']+', tidak bisa diedit atau dihapus karena sudah disetujui/diproses!'
			
			ArrDT = {
				"TGLTRANS" 		: tgl_indo(hsl[0]["tanggal"]),
				"TGLBUKTI" 		: tgl_indo(hsl[0]["tglbukti"]),
				"KDSUMDAN_FR" 	: hsl[0]["kd_sumber_dana"],
				"KDSUMDAN_TO" 	: hsl[1]["kd_sumber_dana"],
				"DESKRIPSI" 	: hsl[0]["deskripsi"], 
				"LOCKED" 		: hsl[0]["locked"],
				"NOBUKAS_X"		: hsl[0]['nobukukas'],
				"JML_TRANSAKSI"	: hsl[0]['pengeluaran'],
				"PESAN" 		: PESAN,
			}
	else:
		ArrDT = {'PESAN':'Data Transaksi tidak ditemukan!'}

	return JsonResponse(ArrDT)