from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from support.support_sipkd import *
from django.db import IntegrityError

import datetime
import json

def index(request):
	dt_sumberdana = put_kasda_sumberdana(request)

	data = {'dt_sumdan':dt_sumberdana,}

	return render(request, 'kasda/kasda_sts.html', data)

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
		sumdana			= data.get('sumber_dana')
		deskripsi 		= data.get('deskripsi')
		dat_kdrek 		= data.getlist('cut_kdrek')
		dat_JmlTerima 	= data.getlist('jml_Penerimaan')
		dat_JmlKeluar 	= data.getlist('jml_Pengeluaran')

		# AKSI ADD -> INSERT =====================================================
		if aksi.lower() == 'true':
			with connections[tahun_log(request)].cursor() as cursor:
				no_bukukas = cek_kasda_autoNoKas(request) ### dari support_sipkd
				if no_bukti != '':
					if cek_noBukti(tahun,no_bukti) >= 1: ### dari support_sipkd
						isSimpan = 0
						pesan 	 = 'STS dengan nomor : '+no_bukti+', sudah digunakan !!'
					else:
						if no_bukukas != '' and data.get('organisasi') != '':
							try:
								cursor.execute("INSERT INTO kasda.kasda_transaksi(\
								tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nobukukas,nobukti,\
								deskripsi,kdlokasi,tanggal,tglbukti,kodesumberdana,jenistransaksi,lastupdate,\
								username,locked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
								[tahun,skpd[0],skpd[1],skpd[2],skpd[3],no_bukukas,no_bukti,deskripsi,'0',
								tgl_transaksi,tgl_bukti,sumdana,'STS',tgl_saiki,uname_x,'T'])
								
								xx_nobukas = no_bukukas
								isSimpan = 1
								pesan 	 = 'Nomor STS : '+no_bukti+' berhasil disimpan !'

							except IntegrityError as e:
								isSimpan = 0
								pesan 	 = 'Nomor STS : '+no_bukti+' sudah ada !'
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
				pesan 	 = 'STS dengan nomor : '+no_bukti_xx+', sudah digunakan !!'
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
							AND nobukukas = %s",[ no_bukukas,no_bukti,tgl_bukti,sumdana,tgl_transaksi,deskripsi,
							tgl_saiki,'STS','0',uname_x,skpd[0],skpd[1],skpd[2],skpd[3],tahun,no_bukukas_xx])

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
						pesan 	 = 'Nomor STS : '+no_bukti_xx+' sudah ada !'

		# SIMPAN DETAIL
		if isSimpan == 1:
			with connections[tahun_log(request)].cursor() as cursor:
				# HAPUS TABEL RINCIAN WHERE kasda
				cursor.execute("DELETE FROM kasda.kasda_transaksi_detil WHERE tahun = %s AND nobukukas = %s ",
					[tahun,xx_nobukas])
				# INSERT INTO TABEL RINCIAN dat_kdrek
				for p in range(len(dat_kdrek)):
					if dat_kdrek[p] != "":
						obj0 = dat_kdrek[p].split("-")
						obj1 = obj0[0].split(".")
						obj2 = obj0[1].split(".")
						rpin = toAngkaDec(dat_JmlTerima[p])
						rpot = toAngkaDec(dat_JmlKeluar[p])

						cursor.execute("INSERT INTO kasda.KASDA_TRANSAKSI_DETIL (TAHUN,NOBUKUKAS,\
						KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,\
						KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,\
						KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,\
						PENERIMAAN,PENGELUARAN,KODESUBKELUARAN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						[tahun,xx_nobukas,skpd[0],skpd[1],skpd[2],skpd[3],obj1[0]+'.'+obj1[1],0,0,'0',
						obj2[0],obj2[1],obj2[2],obj2[3],obj2[4],obj2[5],rpin,rpot,0])

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
					pesan = 'Data STS Dengan Nomor Buku Kas: '+no_bukukas_xx+', berhasil dihapus'

	# hasil olah data kirim ke ajax -> json
	hasil = {'pesan':pesan, 'issimpan':isSimpan}
	return JsonResponse(hasil)