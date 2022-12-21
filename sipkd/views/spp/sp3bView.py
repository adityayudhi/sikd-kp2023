from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
from django.db import IntegrityError
from datetime import datetime
import urllib.parse
import pprint

def sp3b_index(request):

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT urut, kodesumberdana, urai, rekening as norek,
			case when namarekening is not null then rekening||' ('||namarekening||')' 
			else rekening||' (Nama Rekening Belum Diseting)' end as rekening,
			urut||'|'||kodesumberdana||'|'||urai||'|'||rekening as dt_all
			FROM kasda.KASDA_SUMBERDANAREKENING WHERE KODESUMBERDANA <> 99 
			and upper(urai) not like '%%BPD%%' ORDER BY KODESUMBERDANA""")
		jns_rekening = dictfetchall(cursor)

	data = {'jns_rekening' : jns_rekening,}
	return render(request, 'spp/sp3b.html', data)

def sp3b_kegiatan(request):
	org = request.GET.get('id').split('.')     

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT k.KODEUNIT,k.kodeurusan||'.'||lpad(k.kodesuburusan::text,2,'0') as kodebidang,
			0 as kodeprogram,'0' as KODEKEGIATAN,0 as KODESUBKEGIATAN,'PENGELUARAN PEMBIAYAAN' URAI,
			(select urai from master.master_organisasi ms where ms.tahun = k.tahun 
			and ms.kodeurusan = k.kodeurusan and ms.kodesuburusan = k.kodesuburusan 
			and ms.kodeorganisasi = k.kodeorganisasi and ms.kodeunit = k.kodeunit)as URAIUNIT 
			FROM PENATAUSAHAAN.pembiayaan k WHERE k.tahun=%s and k.KODEURUSAN=%s and k.KODESUBURUSAN=%s
			and k.KODEORGANISASI=%s and k.kodeunit=%s and k.kodeakun=6  and k.kodekelompok=2 union 
			SELECT k.KODEUNIT,k.KODEBIDANG,k.KODEPROGRAM,k.KODEKEGIATAN,k.KODESUBKEGIATAN,k.URAI,
			(select urai from master.master_organisasi ms where ms.tahun = k.tahun 
			and ms.kodeurusan = k.kodeurusan and ms.kodesuburusan = k.kodesuburusan 
			and ms.kodeorganisasi = k.kodeorganisasi and ms.kodeunit = k.kodeunit)as URAIUNIT 
			FROM PENATAUSAHAAN.KEGIATAN k WHERE k.tahun=%s and k.KODEURUSAN=%s and k.KODESUBURUSAN=%s
			and k.KODEORGANISASI=%s and k.kodeunit=%s and k.kodesubkegiatan<>0 and k.kodesubkeluaran=0 
			ORDER BY KODEUNIT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan""",
			[tahun_log(request),org[0],org[1],org[2],org[3],tahun_log(request),org[0],org[1],org[2],org[3]])
		list_keg = dictfetchall(cursor)
	

	data = {'list_keg' : list_keg}
	return render(request,'spp/modal/sp3b_modal_kegiatan.html',data)


def sp3b_pendapatan(request):
	org = request.GET.get('id').split('.')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT a.kodeurusan, a.kodesuburusan, a.kodeorganisasi, a.kodeunit, b.urai,
			a.kodeakun||'.'||a.kodekelompok||'.'||a.kodejenis||'.'||a.kodeobjek||'.'||a.koderincianobjek||'.'||a.kodesubrincianobjek as kd_rek,
			a.kodeakun, a.kodekelompok, a.kodejenis, a.kodeobjek, a.koderincianobjek,
			a.kodesubrincianobjek, c.urai as uraian, a.jumlah, a.jumlah_p FROM penatausahaan.pendapatan a 
			LEFT JOIN master.master_organisasi b ON
			a.kodeurusan = b.kodeurusan and a.kodesuburusan = b.kodesuburusan and
			a.kodeorganisasi = b.kodeorganisasi and a.kodeunit = b.kodeunit
			LEFT JOIN master.master_rekening c ON
			a.kodeakun = c.kodeakun and a.kodekelompok = c.kodekelompok and a.kodejenis = c.kodejenis and
			a.kodeobjek = c.kodeobjek and a.koderincianobjek = c.koderincianobjek and a.kodesubrincianobjek = c.kodesubrincianobjek
			WHERE a.tahun = %s and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s and a.kodeunit = %s
			ORDER BY a.kodeurusan, a.kodesuburusan, a.kodeorganisasi, a.kodeunit""",
			[tahun_log(request),org[0],org[1],org[2],org[3]])
		dt_pendapatan = dictfetchall(cursor)

	data = {'list_dt':dt_pendapatan}
	return render(request,'spp/modal/sp3b_modal_pendapatan.html',data)

def sp3b_afektasi(request):
	if 'sipkd_username' in request.session:

		gets = request.POST.get('skpd', None) 
		no_sp3b = request.POST.get('nosp3b', None)
		tgl_sp3b = tgl_short(request.POST.get('tgl', None)) 
		kdunit = request.POST.get('kdunit')
		bidang = request.POST.get('bidang') 
		program = request.POST.get('program') 
		kegiatan = request.POST.get('kegiatan')
		subkegiatan = request.POST.get('subkegiatan')
		jenis = request.POST.get('jenis').upper()
		kodekegiatan = ''

		if gets != '0':
			aidi = gets.split('.')
		else:
			skpd = '0.0.0.0'
			aidi = skpd.split('.') 

		if aidi != '0':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
					"(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
					"(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
					"(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
					"(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
					"(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
					"(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
					 ",loloskan "
					" FROM penatausahaan.fc_view_sp3b_rincian(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s) ",
					[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],no_sp3b.upper(),bidang,program,kegiatan,subkegiatan,tgl_sp3b,'LS'])
				list_sp3b = dictfetchall(cursor)

		for x in range(len(list_sp3b)):
			if (list_sp3b[x]['cek']==1):
				if(list_sp3b[x]['uraian']!=None):
					objek = list_sp3b[x]['koderekening']
					objek1 = objek.split('-') 
					koderekening = objek1[0].split('.')
					kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"

		data = {'list_sp3b':ArrayFormater(list_sp3b),'kodekegiatan':kodekegiatan}
		
		return render(request, 'spp/tabel/sp3b_afektasi.html', data)
	else:
		return redirect('sipkd:index')

def sp3b_potongan(request):
	data = request.POST
	tahun_x = tahun_log(request)
	nosp3b   = data.get('nosp3b').upper()

	if data.get('skpd') != "":
		skpd = data.get('skpd').split('.')
	else:
		skpd = '0.0.0.0'.split('.')


	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""select row_number() over() as nomor,
			s.rekeningpotongan,s.jumlah as jumlahpotongan,s.jenispotongan,''as keterangan, idbiling, ntpn, jenispotongan as kdpajak,
				(select kdrek from master.mpajak mp where mp.koderekening=s.rekeningpotongan) as kdrek,	
				(select r.urai as uraipotongan from master.master_rekening r where r.tahun=s.tahun 
				and  r.kodeakun||'.'||r.kodekelompok||'.'||r.kodejenis||'.'||LPAD(r.kodeobjek::text,2,'0')
				||'.'||LPAD(r.koderincianobjek::text,2,'0')||'.'||lpad(kodesubrincianobjek::text,3,'0')
			=s.rekeningpotongan) from penatausahaan.spmpotongan s
			where s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s
			and s.kodeorganisasi = %s and s.kodeunit = %s and UPPER(s.nospm) = %s""",
			[tahun_x, skpd[0], skpd[1], skpd[2], skpd[3], nosp3b])

		hasil = ArrayFormater(dictfetchall(cursor))

	ArrDT = {'potongan':hasil,}
	return render(request,'spp/tabel/sp3b_potongan.html',ArrDT)

def sp3b_bendahara(request):
	org = request.GET.get('id').split('.')     

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM MASTER.PEJABAT_SKPD WHERE tahun=%s and KODEURUSAN=%s and KODESUBURUSAN=%s"
			" and KODEORGANISASI=lpad(%s,2,'0') and kodeunit=%s and JENISSISTEM=%s and UPPER(JABATAN) LIKE (%s)",
			[tahun_log(request),org[0],org[1],org[2],org[3],2,'%BENDAHARA PENGELUARAN%'])
		list_bend = dictfetchall(cursor)

	data = {'list_bend' : list_bend}
	return render(request,'spp/modal/sp3b_modal_bendahara.html',data)

def sp3b_load(request):
	org = request.GET.get('id').split('.')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""SELECT s.nosp3b,s.tglsp3b,s.urai as keperluan,s.kodeunit,
			s.kodeurusan||'.'||s.kodesuburusan||'.'||s.kodeorganisasi||'.'||s.kodeunit||' - '||o.urai as organisasi, 
			coalesce(sr.kodebidang,'') as kodebidang, coalesce(sr.kodeprogram::text,'') as kodeprogram,
			coalesce(sr.kodekegiatan,'') as kodekegiatan,coalesce(sr.kodesubkegiatan::text,'') as kodesubkegiatan,
			coalesce(k.urai,'') as uraikeg,sum (sr.jumlah) as jumlah
			FROM penatausahaan.sp3b s
			JOIN master.master_organisasi o ON o.tahun=s.tahun and o.kodeurusan=s.kodeurusan 
			and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit
			LEFT JOIN penatausahaan.spmrincian sr ON (sr.tahun=s.tahun 
			and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi 
			and sr.kodeunit=s.kodeunit and sr.nospm=s.nosp3b)
			LEFT JOIN penatausahaan.kegiatan k ON k.tahun=s.tahun 
			and k.kodeurusan=s.kodeurusan and k.kodesuburusan=s.kodesuburusan and k.kodeorganisasi=s.kodeorganisasi 
			and k.kodeunit=s.kodeunit and  k.kodebidang = sr.kodebidang and k.kodeprogram = sr.kodeprogram 
			and k.kodekegiatan = sr.kodekegiatan and k.kodesubkegiatan = sr.kodesubkegiatan
			WHERE (s.nosp3b not in (select b.nosp3b from penatausahaan.sp2b b where b.tahun = s.tahun 
			and b.kodeurusan = s.kodeurusan and b.kodesuburusan = s.kodesuburusan 
			and b.kodeorganisasi = s.kodeorganisasi and b.kodeunit=s.kodeunit)) 
			and s.tahun = %s and s.kodeurusan = %s and s.kodesuburusan = %s and s.kodeorganisasi = %s and s.kodeunit = %s
			GROUP BY s.nosp3b,s.tglsp3b,keperluan,s.kodeunit,organisasi,sr.kodebidang,sr.kodeprogram,sr.kodekegiatan,
			sr.kodesubkegiatan,uraikeg
			ORDER BY s.tglsp3b,s.nosp3b""",
			[tahun_log(request),org[0],org[1],org[2],org[3]])
		list_sp3b = ArrayFormater(dictfetchall(cursor))

	data = {'list_sp3b':list_sp3b}
	return render(request, 'spp/modal/sp3b_modal_lihat.html', data)

def sp3b_ceknomor(request):
	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			gets = request.POST.get('skpd') 
			nosp3b = request.POST.get('nosp3b') 

			if gets != '0':
				aidi = gets.split('.')
			else:
				skpd = '0.0.0.0'
				aidi = skpd.split('.')

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT count(nosp3b) as nosp3b FROM penatausahaan.sp3b WHERE TAHUN=%s and UPPER(nosp3b)=%s "
					"and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = lpad(%s,2,'0') and kodeunit = %s",
					[tahun_log(request),nosp3b.upper(),aidi[0], aidi[1], aidi[2], aidi[3]])
				cek_nosp3b = dictfetchall(cursor)

			data = {}
			for arr in cek_nosp3b:
				data = {'nosp3b':arr['nosp3b']}

			return JsonResponse(data)

		### GET untuk ambil data LIHAT SP3B ==============================================================================
		else: 
			list_sp3b = ''
			gets = request.GET.get('id') 
			nosp3b = request.GET.get('tk') 

			if gets != '0':
				aidi = gets.split('.')
			else:
				skpd = '0.0.0.0'
				aidi = skpd.split('.')

			if nosp3b != '':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("""SELECT s.kodesumberdana_kasda,s.saldoawal,s.pendapatan,s.bendaharapenerima,s.jabatan,
						s.kodeakun, s.kodekelompok, s.kodejenis, s.kodeobjek, s.koderincianobjek, s.kodesubrincianobjek, c.urai as uraian,
						s.kodeakun||'.'||s.kodekelompok||'.'||s.kodejenis||'.'||s.kodeobjek||'.'||s.koderincianobjek||'.'||s.kodesubrincianobjek as kd_rekening,
						p.nip,p.norekbank,p.namabank,p.npwp,p.nama,p.namarekeningbank FROM PENATAUSAHAAN.sp3b s 
						JOIN master.pejabat_skpd p ON p.tahun = s.tahun 
						and p.kodeurusan = s.kodeurusan and p.kodesuburusan = s.kodesuburusan 
						and p.kodeorganisasi = s.kodeorganisasi and p.kodeunit=s.kodeunit and p.jabatan = s.jabatan
						LEFT JOIN master.master_rekening c ON c.tahun = s.tahun and
						c.kodeakun = s.kodeakun and c.kodekelompok = s.kodekelompok and c.kodejenis = s.kodejenis and
						c.kodeobjek = s.kodeobjek and c.koderincianobjek = s.koderincianobjek and c.kodesubrincianobjek = s.kodesubrincianobjek 
						where s.tahun = %s and s.kodeurusan = %s  and s.kodesuburusan = %s 
						and s.kodeorganisasi = lpad(%s,2,'0') and s.kodeunit = %s and s.nosp3b = %s""",
						[tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3], nosp3b])
					list_sp3b = ArrayFormater(dictfetchall(cursor))  

			return JsonResponse(list_sp3b, safe=False)

	else:
		return redirect('sipkd:index')

def sp3b_simpan(request):
	hasil = ''
	tahun = tahun_log(request)

	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			dtx = request.POST

			aksi = dtx.get('aksi').lower()
			rek_kasda = dtx.get('jenis_rekening')
			nm_rek_kasda = dtx.get('nm_jns_rekening')
			org = dtx.get('organisasi').split('.')
			no_sp3b = dtx.get('no_sp3b').upper()
			no_sp3b_lama = dtx.get('no_sp3b_lama').upper()
			tanggal_sp3b = tgl_short(dtx.get('tanggal_sp3b'))
			status_keperluan = dtx.get('status_keperluan')
			saldo_awal = toAngkaDec(dtx.get('saldo_awal'))
			jum_pendapatan = toAngkaDec(dtx.get('jum_pendapatan'))
			bendahara = dtx.get('bendahara')
			norek_bendahara = dtx.get('norek_bendahara')
			nama_bank = dtx.get('nama_bank')
			npwp_bendahara = dtx.get('npwp_bendahara')
			bend_jabatan = dtx.get('bend_jabatan')
			nm_pemilik_rekening = dtx.get('nama_rekening_bank')
			rek_pend = dtx.get('kd_rekening').split('.') ## Kode Rekening Pendapatan 
			total_sp3b = dtx.get('total_spp')

			rek_afek = dtx.getlist('afektasispp')
			rek_pots = dtx.getlist('cut_kdrek')
			jns_cut  = dtx.getlist('jns_cut')
			idbiling = dtx.getlist('idbiling')
			ntpn 	 = dtx.getlist('ntpn')
			jml_pot  = dtx.getlist('jml_pot')

			if no_sp3b != '':
				if aksi == 'true': ## ADD data
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("""INSERT INTO penatausahaan.sp3b (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,
							nosp2b,nosp3b,tglsp2b,tglsp3b,uptdpenerima,saldoawal,pendapatan,bendaharapenerima,
							kodeakun,kodekelompok,kodejenis,kodeobjek,koderincianobjek,kodesubrincianobjek,
							urai,jabatan,kodesumberdana_kasda) 
							VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							[tahun,org[0],org[1],org[2],org[3],'',no_sp3b,'NOW()',tanggal_sp3b,'',saldo_awal,jum_pendapatan,bendahara,
							rek_pend[0],rek_pend[1],rek_pend[2],rek_pend[3],rek_pend[4],rek_pend[5],status_keperluan,bend_jabatan,rek_kasda])

						### SIMPAN JUGA KE TABEL SPM ===== dengan isi field sp3b = 1
						cursor.execute("""INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,
							NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,
							DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,
							PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME,sp3b,rekeningpengeluaran)
							VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							[tahun,org[0],org[1],org[2],org[3],no_sp3b,tanggal_sp3b,tanggal_sp3b,'',0,0,
							'','','NOW()',0,total_sp3b,'',bend_jabatan,norek_bendahara,nama_bank,'LS',0,npwp_bendahara,
							'',status_keperluan,'NOW()',0,username(request),1,nm_rek_kasda])

						hasil = "Data SP3B dengan nomor : "+no_sp3b+" berhasil disimpan!"
						
				elif aksi == 'false':
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("""UPDATE penatausahaan.sp3b SET nosp3b = %s, tglsp3b = %s, uptdpenerima = %s, 
							saldoawal = %s, pendapatan = %s, bendaharapenerima = %s, kodeakun = %s, kodekelompok = %s,
							kodejenis = %s, kodeobjek = %s, koderincianobjek = %s, kodesubrincianobjek = %s, 
							urai = %s, jabatan = %s, kodesumberdana_kasda = %s
							WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s 
							and kodeunit = %s and nosp3b = %s""",
							[no_sp3b,tanggal_sp3b,'',saldo_awal,jum_pendapatan,bendahara,
							rek_pend[0],rek_pend[1],rek_pend[2],rek_pend[3],rek_pend[4],rek_pend[5],
							status_keperluan,bend_jabatan,rek_kasda,tahun,org[0],org[1],org[2],org[3],no_sp3b_lama])

						### SIMPAN JUGA KE TABEL SPM ===== dengan isi field sp3b = 1
						cursor.execute("""UPDATE penatausahaan.spm SET NOSPM = %s, TANGGAL = %s, TANGGAL_DRAFT = %s, 
							KODEBIDANG = %s, KODEPROGRAM = %s, KODEKEGIATAN = %s, DESKRIPSISPP = %s, NOSPP = %s,
							TGLSPP = %s, JUMLAHSPP = %s, JUMLAHSPM = %s, PEMEGANGKAS = %s, NAMAYANGBERHAK = %s,
							NOREKBANK = %s, BANK = %s, JENISSPM = %s, PERUBAHAN = %s, NPWP = %s, INFORMASI = %s, 
							STATUSKEPERLUAN = %s, LASTUPDATE = %s, TRIWULAN = %s, UNAME = %s, rekeningpengeluaran = %s
							WHERE TAHUN = %s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s 
							and KODEUNIT = %s and NOSPM = %s and sp3b = 1""",

							[no_sp3b,tanggal_sp3b,tanggal_sp3b,'',0,0,'','','NOW()',0,total_sp3b,'',bend_jabatan,norek_bendahara,
							nama_bank,'LS',0,npwp_bendahara,'',status_keperluan,'NOW()',0,username(request),nm_rek_kasda,
							tahun,org[0],org[1],org[2],org[3],no_sp3b_lama])

						hasil = "Data SP3B dengan nomor : "+no_sp3b+" berhasil diupdate!"
				else:
					hasil = ""
					return redirect('sipkd:index')

				### HAPUS RINCIAN dan POTONGAN jika EDIT data =========================
				### RINCIAN dan POTONGAN SP3B tersimpan di tabel tersebut.
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("""DELETE FROM penatausahaan.spmrincian where tahun=%s and kodeurusan = %s 
						and kodesuburusan = %s and kodeorganisasi = %s and kodeunit=%s and NOSPM = %s""",
						[tahun,org[0],org[1],org[2],org[3],no_sp3b_lama])

					cursor.execute("""DELETE FROM penatausahaan.spmpotongan where TAHUN=%s and KODEURUSAN = %s 
						and KODESUBURUSAN = %s and KODEORGANISASI = %s and KODEUNIT = %s and NOSPM = %s""",
						[tahun,org[0],org[1],org[2],org[3],no_sp3b_lama])

				for x in range(len(rek_afek)):
					pecah = rek_afek[x].split('|')
					norek = pecah[0].split('-')
					jml_1 = toAngkaDec(pecah[1])

					keg = norek[0].split('.') ### 1.02.2.2.02.3
					kdbidang      = keg[0]+'.'+keg[1] # 1.02
					kdprogram     = keg[2] # 2
					kdkegiatan    = keg[3]+'.'+keg[4] # 2.02
					kdsubkegiatan = keg[5] # 3

					bel = norek[1].split('.') ### 5.1.2.01.01.0024
					kdakun        = bel[0]
					kdkelompok    = bel[1]
					kdjenis       = bel[2]
					kdobjek       = bel[3]
					kdrincian     = bel[4]
					kdsubrincian  = bel[5]

					### SIMPAN RICIAN ======================
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("""INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,
							KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,
							KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL) 
							VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							[tahun,org[0],org[1],org[2],org[3],no_sp3b,
							kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,
							kdrincian,kdsubrincian,jml_1,tanggal_sp3b])

				### SIMPAN POTONGAN ======================
				for p in range(len(rek_pots)):
					if rek_pots[p] != "":
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("""INSERT INTO penatausahaan.spmpotongan (TAHUN,KODEURUSAN,KODESUBURUSAN,
								KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,REKENINGPOTONGAN,JUMLAH,JENISPOTONGAN, idbiling, ntpn) 
								VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
								[tahun,org[0],org[1],org[2],org[3],no_sp3b,tanggal_sp3b,
								rek_pots[p],toAngkaDec(jml_pot[p]),jns_cut[p], idbiling[p], ntpn[p]])

			return HttpResponse(hasil)

		else:
			return redirect('sipkd:index')
	else:
		return redirect('sipkd:index')

def sp3b_delete(request):
	hasil = ''
	tahun = tahun_log(request)
	nosp3b = request.POST.get('nosp3b')
	gets  = request.POST.get('org') 

	if gets != '0':
		skpd = gets
	else:
		skpd = '0.0.0.0'

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("""DELETE FROM PENATAUSAHAAN.SP3B where tahun = %s and nosp3b = %s and 
			kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit = %s""",
			[tahun,nosp3b,skpd])

		cursor.execute("""DELETE FROM PENATAUSAHAAN.SPM where tahun = %s and nospm = %s and sp3b = 1 and
			kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit = %s""",
			[tahun,nosp3b,skpd])

		hasil = "Data berhasil dihapus!"

	return HttpResponse(hasil)

def sp3b_report(request):
	tahun = tahun_log(request)

	if 'sipkd_username' in request.session:
		if request.method == 'POST':
			post = request.POST
			lapParm = {}
			
			organisasi  = post.get('org').split('.')
			tgl_sp3b = tgl_to_db(post.get('tgl_sp3b')).split('/')
			bulan = 1

			lapParm['report_type']      = 'pdf'
			lapParm['file']         	= 'penatausahaan/spp/sp3b.fr3'
			lapParm['tahun']            = "'"+tahun+"'"  
			lapParm['nomer']            = "'"+post.get('nomer_sp3b')+"'"
			lapParm['kodeurusan']       = organisasi[0]
			lapParm['kodesuburusan']    = organisasi[1]
			lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
			lapParm['kodeunit']   		= "'"+organisasi[3]+"'"   

			lapParm['bulanSPP']         = int(bulan)    
			lapParm['bulanKegiatan']    = ''
			lapParm['isppkd']       	= 0        
			lapParm['idpa']             = "'"+post.get('id_mengajukan')+"'"
			lapParm['idpa2']            = "'"+post.get('id_pelaksana')+"'"
			lapParm['idpa1']        	= "'"+post.get('id_pelaksana')+"'"

			return HttpResponse(laplink(request, lapParm))

		### LOAD PERTAMA ============================================================================
		else:
			gets = request.GET.get('id', None)
			hidden_pelaksana = ''

			if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
				aidi = gets.split('.')
			else:
				skpd = '0.0.0.0'
				aidi = skpd.split('.')  

			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
					" and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and jenissistem=%s ",
					[tahun,aidi[0],aidi[1],aidi[2],aidi[3],2])
				
				bendahara = dictfetchall(cursor)

			data = {'bendahara' : bendahara, 'hidden_pelaksana' : hidden_pelaksana,}
			return render(request,'spp/modal/sp3b_modal_laporan.html',data)
	else:
		return redirect('sipkd:index')