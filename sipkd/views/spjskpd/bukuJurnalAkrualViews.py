from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import pprint

var_nobku = ''
var_jenissp2d = ''
var_ispihakketiga = ''

def buku_jurnal_akrual(request):
	skpd = set_organisasi(request) 

	if skpd["kode"] == '': kode = '0.0.0.0'
	else: kode = skpd["kode"]

	data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"], }

	return render(request, 'spjskpd/bukujurnalakrual.html',data)

def list_jurnal_akrual(request):
	tahun 	= tahun_log(request)
	arrBln	= []
	arrTab 	= []
	gets = request.POST.get('skpd') 
	isppkd = request.POST.get('isppkd') 
	jenis = request.POST.get('jenis',0) 
	bulan = int(request.POST.get('bulan',get_bulan(request)))
	list_jurnal = []

	if gets != '0' or gets != '' or gets != '0.0.0.0':
		aidi = gets.split('.')
	else:
		skpd = '0.0.0.0'
		aidi = skpd.split('.')        

	if(jenis=='0'):
		arg = ""
	elif(jenis=='1' or jenis=='2' or jenis=='3' or jenis=='4' or jenis=='6' or jenis=='7'):
		arg = "and  s.jenisjurnal = "+jenis+""           
	else:
		arg = "and  s.jenisjurnal in (1,5,6,7)" 

	if gets != '0' or gets != '' or gets != '0.0.0.0':

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT distinct s.noref,s.tanggalbukti,s.jenisjurnal,\
				(select uraian from akuntansi.akrual_jenis_jurnal where id=s.jenisjurnal) as namajurnal,\
				s.nobukti,s.keterangan,0 as cek,\
				(select sum(debet) from akuntansi.akrual_jurnal_rincian where tahun=s.tahun and kodeurusan=s.kodeurusan and kodesuburusan=s.kodesuburusan \
				and kodeorganisasi=s.kodeorganisasi and kodeunit=s.kodeunit and isskpd=0  and noref=s.noref ) as debet,\
				(select sum(kredit) from akuntansi.akrual_jurnal_rincian where tahun=s.tahun and kodeurusan=s.kodeurusan and kodesuburusan=s.kodesuburusan \
				and kodeorganisasi=s.kodeorganisasi and kodeunit=s.kodeunit and isskpd=0 and noref=s.noref ) as kredit,\
				case when s.posting=1 then 'Sudah Posting' else 'Belum Posting' end as status,s.posting,\
				case when s.posting=1 then 'hijau' else 'kuning' end as warna \
				from akuntansi.akrual_buku_jurnal s join akuntansi.akrual_jurnal_rincian sr on \
				(s.tahun=sr.tahun and s.kodeurusan=sr.kodeurusan and s.kodesuburusan=sr.kodesuburusan and s.kodeorganisasi=sr.kodeorganisasi \
				and s.kodeunit=sr.kodeunit and s.isskpd=sr.isskpd and s.noref=sr.noref) where s.tahun=%s  and s.kodeurusan=%s and s.kodesuburusan=%s and s.isskpd = 0 \
				and s.kodeorganisasi=%s and s.kodeunit=%s and extract (month from s.tanggalbukti )=%s "+arg+" order by s.tanggalbukti",
				[tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3], bulan])
			list_jurnal =  dictfetchall(cursor)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT ID,URAIAN FROM akuntansi.AKRUAL_JENIS_JURNAL where isskpd=0 ORDER BY ID") 
		list_jenis = dictfetchall(cursor)  

	aidi_bln = 1
	for i in monthList: # monthList -> array from config.py
		arrBln.append({'id':aidi_bln, 'kode':i, 'nama':monthList[i], 'tahun':tahun})
		aidi_bln += 1		      

	data = {'list_jurnal' : ArrayFormater(list_jurnal), 'list_jenis':list_jenis,'arrBln':arrBln, 
		'jenis':jenis, 'bulan':bulan }

	return render(request, 'spjskpd/listjurnalakrual.html', data)

def ambil_data_akrual_skpd(request):
	hasil = ''
	hasil_tabel = ''

	if request.method == 'POST':
		org = request.POST.get('organisasi').split('.')
		noref = request.POST.get('noref')

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM akuntansi.AKRUAL_BUKU_JURNAL where tahun = %s and kodeurusan = %s\
				and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s \
				and kodeunit = %s and noref = %s and isskpd = 0", 
				[tahun_log(request),org[0],org[1],org[2],org[3],noref])
			hasil = dictfetchall(cursor)
		
		if hasil != '':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT sr.kodebidang||'.'||sr.kodeorganisasi||'.'||sr.kodeprogram||'.'||sr.kodekegiatan||'.'||sr.kodesubkegiatan||'-'||\
					sr.kodeakun||'.'||sr.kodekelompok||'.'||sr.kodejenis||'.'||lpad(sr.kodeobjek::text,2,'0')||'.'||lpad(sr.koderincianobjek::text,2,'0')||'.'||lpad(sr.kodesubrincianobjek::text,4,'0')\
					as koderekening, (select urai from master.master_rekening where tahun=sr.tahun and kodeakun=sr.kodeakun and kodekelompok=sr.kodekelompok\
					and kodejenis=sr.kodejenis and kodeobjek=sr.kodeobjek and koderincianobjek=sr.koderincianobjek and kodesubrincianobjek=sr.kodesubrincianobjek) as uraian, \
					sr.debet,sr.kredit, sr.kodeurusan,sr.kodesuburusan,sr.kodeorganisasi\
					from akuntansi.akrual_jurnal_rincian  sr where sr.tahun=%s  and sr.kodeurusan=%s \
					and sr.kodesuburusan=%s and sr.kodeorganisasi=%s and sr.kodeunit=%s and sr.noref=%s \
					and sr.isskpd=0 order by sr.urut",[tahun_log(request),org[0],org[1],org[2],org[3],noref])
				hasil_tabel = dictfetchall(cursor)
		
	data = {
		'var_noref' : hasil[0]['noref'],
		'var_nobukti' : hasil[0]['nobukti'],
		'var_urai' : hasil[0]['keterangan'],
		'var_nobku' : hasil[0]['no_bku'],
		'var_jenissp2d' : hasil[0]['jenissp2d'],
		'var_ispihakketiga' : hasil[0]['ispihakketiga'],
		'var_tglbukti' : hasil[0]['tanggalbukti'],
		'var_jenisjurnal' : hasil[0]['jenisjurnal'],
		'hasil_untuk_tabel':convert_tuple(hasil_tabel),
	}
	return JsonResponse(data)

def modal_tambah_akrual_skpd(request):

	jenisnya = request.GET.get('act').lower()

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT ID,URAIAN FROM akuntansi.AKRUAL_JENIS_JURNAL \
			where isskpd=0 and id <> 0 ORDER BY ID") 
		list_jenis = dictfetchall(cursor)  

	data = {'list_jenis':list_jenis, 'jenisnya':jenisnya}
	return render(request, 'spjskpd/modal/modal_input_akrual_skpd.html', data)

def noref_baru_akrual_skpd(request):
	noref = ''

	org = request.POST.get('organisasi').split('.')
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('SELECT hasil FROM akuntansi."fc_otomatis_no_jurnal"(%s,%s,%s,%s,%s,0)',
			[tahun_log(request),org[0],org[1],org[2],org[3]])
		noref = cursor.fetchone()
	
	data = {
		'noref':noref,
	}
	return JsonResponse(data)

def tampilkantransaksi_akrual_skpd(request):
	global var_nobku
	global var_jenissp2d
	global var_ispihakketiga

	a = request.POST.get('a')
	b = request.POST.get('b')
	org = request.POST.get('organisasi').split('.')
	cb_jenis = request.POST.get('cb_jenis')


	hasilskpdbku = ''
	hasilSP2D = ''
	hasilskpdpenerimaan = ''
	hasilskpdsetor = ''
	hasil_untuk_tabel = ''
	
	if b=='SP2D' or b=='SP2D-GJ' or b=='SPJ' or b=='BAYAR-GJ' or b=='PUNGUT-PAJAK' or b=='SETOR-PAJAK' or b=='RK-PPKD' or b=='KOREKSI PENERIMAAN' or b=='KOREKSI PENGELUARAN':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from pertanggungjawaban.skpd_bku where tahun=%s and kodeurusan = %s \
				and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s and kodeunit = %s \
				and isskpd=0 and no_bku=%s",
				[tahun_log(request), org[0], org[1], org[2], org[3], a])
			hasilskpdbku = dictfetchall(cursor)

	elif b=='TIDAK-CAIR':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from penatausahaan.sp2d where tahun=%s and kodeurusan = %s and kodesuburusan = %s \
				and replace(KODEORGANISASI,' ', '') = %s and kodeunit = %s and nosp2d=%s",
				[tahun_log(request), org[0], org[1], org[2], org[3], a])
			hasilSP2D = dictfetchall(cursor)
	elif b=='PUNGUT PENDAPATAN':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from pertanggungjawaban.skpd_penerimaan where tahun=%s and kodeurusan = %s \
				and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s and kodeunit = %s and isskpd=0 \
				and no_bku=%s and jenis_transaksi='PUNGUT'",[tahun_log(request), org[0], org[1], org[2], org[3], a])
			hasilskpdpenerimaan = dictfetchall(cursor)
	elif b=='SETOR PENDAPATAN':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select * from pertanggungjawaban.skpd_penerimaan where tahun=%s and kodeurusan = %s \
				and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s and kodeunit = %s and isskpd=0 \
				and no_bku=%s and jenis_transaksi='SETOR'",[tahun_log(request), org[0], org[1], org[2], org[3], a])
			hasilskpdsetor = dictfetchall(cursor)


	if hasilskpdbku != '':
		var_nobukti = hasilskpdbku[0]['bukti']
		if b=='SP2D-GJ' or b=='SP2D':
			var_urai = 'Penerimaan '+hasilskpdbku[0]['urai']
		else:
			var_urai = hasilskpdbku[0]['urai']

		var_nobku = hasilskpdbku[0]['no_bku']
		var_jenissp2d = hasilskpdbku[0]['jenis_sp2d']
		var_ispihakketiga = hasilskpdbku[0]['is_pihak_ketiga']
		var_tglbukti = hasilskpdbku[0]['tgl_bku']

		# print('SELECT koderekening, uraian, debet, kredit, urutan \
		# 		FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s,%s)',
		# 		[tahun_log(request), org[0], org[1], org[2], cb_jenis, var_nobku, hasilskpdbku[0]['jenis_bku'],''])

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
				FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s,%s)',
				[tahun_log(request), org[0], org[1], org[2], cb_jenis, var_nobku, hasilskpdbku[0]['jenis_bku'],''])
			hasil_untuk_tabel = dictfetchall(cursor)

	elif hasilSP2D != '':
		var_nobukti = hasilSP2D[0]['nosp2d']
		var_urai = 'SP2D Tidak Cair Pada No '+hasilSP2D[0]['nosp2d']+' Untuk '+hasilSP2D[0]['informasi']

		var_nobku = '0'
		var_jenissp2d = hasilSP2D[0]['jenissp2d']
		var_ispihakketiga = '1'
		var_tglbukti = hasilSP2D[0]['tanggal']

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
				FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s,%s)',
				[tahun_log(request), org[0], org[1], org[2], cb_jenis, 0, 'TIDAK-CAIR',''])
			hasil_untuk_tabel = dictfetchall(cursor)

	elif hasilskpdpenerimaan != '':

		var_nobukti = hasilskpdpenerimaan[0]['nobukti']
		var_urai = hasilskpdpenerimaan[0]['urai']

		var_nobku = hasilskpdpenerimaan[0]['no_bku']
		var_jenissp2d = ''
		var_ispihakketiga = '0'
		var_tglbukti = hasilskpdpenerimaan[0]['tgl_bukti']
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
				FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s,%s)',
				[tahun_log(request), org[0], org[1], org[2], cb_jenis, var_nobku, 'PUNGUT PENDAPATAN'])
			hasil_untuk_tabel = dictfetchall(cursor)

	elif hasilskpdsetor != '':
		# pprint.pprint(hasilskpdsetor)
		var_nobukti = hasilskpdsetor[0]['nobukti']
		var_urai = hasilskpdsetor[0]['urai']

		var_nobku = hasilskpdsetor[0]['no_bku']
		var_jenissp2d = ''
		var_ispihakketiga = '0'
		var_tglbukti = hasilskpdsetor[0]['tgl_bku']
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
				FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s,%s)',
				[tahun_log(request), org[0], org[1], org[2], cb_jenis, var_nobku, 'SETOR PENDAPATAN'])
			hasil_untuk_tabel = dictfetchall(cursor)
	
	data = {
	'var_noref':'',
	'var_nobukti': var_nobukti,
	'var_urai': var_urai,
	'var_nobku': var_nobku,
	'var_jenissp2d': var_jenissp2d,
	'var_ispihakketiga': var_ispihakketiga,
	'var_tglbukti': var_tglbukti,
	'var_jenisjurnal' : cb_jenis,
	'hasil_untuk_tabel': convert_tuple(hasil_untuk_tabel),

	}
	return JsonResponse(data)

def tampilkanTransaksiSKP_akrual_skpd(request):
	a = request.POST.get('a')
	b = request.POST.get('b')
	org = request.POST.get('organisasi').split('.')
	hasilskp = ''
	hasil_untuk_tabel = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.skp where tahun=%s and kodeurusan = %s and kodesuburusan = %s \
			and replace(KODEORGANISASI,' ', '') = %s and nomor = %s",[tahun_log(request), org[0], org[1], org[2], a])
		hasilskp = dictfetchall(cursor)

	if hasilskp != '':
		var_nobukti = hasilskp[0]['nomor']
		var_urai = hasilskp[0]['uraian']
	
		# var_nobku = hasilskp[0]['no_bku']
		# var_jenissp2d = ''
		# var_ispihakketiga = '0'
		var_tglbukti = hasilskp[0]['tanggal']
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan FROM akuntansi.fc_AKRUAL_TO_JURNAL(%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), org[0], org[1], org[2], cb_jenis, 0, b])
			hasil_untuk_tabel = dictfetchall(cursor)

	data = {
		'hasil_untuk_tabel':convert_tuple(hasil_untuk_tabel),
	}
	return JsonResponse(data)

def tampilkanTransaksisp2b_akrual_skpd(request):
	a = request.POST.get('a')
	b = request.POST.get('b')
	org = request.POST.get('organisasi').split('.')
	hasilsp2b = ''
	hasil_untuk_tabel = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select * from penatausahaan.sp2b where tahun=%s and kodeurusan = %s and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s and nosp2b = %s",[tahun_log(request), org[0], org[1], org[2], a])
		hasilsp2b = dictfetchall(cursor)

	if hasilsp2b != '':
		var_nobukti = hasilsp2b[0]['nosp2b']
		var_urai = hasilsp2b[0]['deskripsi']
	
		# var_nobku = hasilsp2b[0]['no_bku']
		# var_jenissp2d = ''
		# var_ispihakketiga = '0'
		var_tglbukti = hasilsp2b[0]['tglsp2b']
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * FROM akuntansi."fc_sp2b_akrual_to_jurnal"(%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), org[0], org[1], org[2], cb_jenis, 0, b, var_nobukti])
			hasil_untuk_tabel = dictfetchall(cursor)

	data = {
		'hasil_untuk_tabel':convert_tuple(hasil_untuk_tabel),
	}
	return JsonResponse(data)

def tampilaknpenutup_lra_skpd(request):
	a = request.POST.get('a')
	b = request.POST.get('b')

	org = request.POST.get('organisasi').split('.')
	hasilnya = ''
	bulan = request.POST.get('bulan')
	

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
			FROM akuntansi.fc_akrual_view_penutup_lra(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request),
			org[0],org[1],org[2],org[3],'01-jan-'+tahun_log(request)+'','31-dec-'+tahun_log(request)+'',0,bulan])
		hasilnya = dictfetchall(cursor)

	data = {
		'hasilnya':convert_tuple(hasilnya),
	}
	return JsonResponse(data)

def tampilaknpenutup_lo_skpd(request):
	a = request.POST.get('a')
	b = request.POST.get('b')
	

	org = request.POST.get('organisasi').split('.')
	hasilnya = ''

	bulan = request.POST.get('bulan')

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('SELECT koderekening, uraian, debet, kredit, urutan \
			FROM akuntansi.fc_akrual_view_penutup_lo(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request),
			org[0],org[1],org[2],org[3],'01-jan-'+tahun_log(request)+'','31-dec-'+tahun_log(request)+'',0,bulan])
		hasilnya = dictfetchall(cursor)

	data = {
		'hasilnya':convert_tuple(hasilnya),
	}
	return JsonResponse(data)

def posting_jurnal(request):
    hasil = ''

    if request.method == 'POST':
    	array_index = json.loads(request.POST.get('array_index'))
    	org = request.POST.get('organisasi').split('.')
    	postingan = request.POST.get('act')
    	lock = request.POST.get('act')
    	tahun = tahun_log(request)

    	if(lock == 'posting'):
    		posting = '1'
    	else:
    		posting = '0'

    	for i in range(len(array_index)):
    		with connections[tahun_log(request)].cursor() as cursor:
    			cursor.execute("UPDATE akuntansi.AKRUAL_BUKU_JURNAL set posting=%s where tahun=%s"
                    " and KODEURUSAN=%s and KODESUBURUSAN=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') and isskpd=0"
                    " and kodeunit=%s and NOREF = %s",[posting,tahun,org[0],org[1],org[2],org[3],array_index[i].split('^')[0]])
    		
    		with connections[tahun_log(request)].cursor() as cursor:
    			cursor.execute("UPDATE akuntansi.AKRUAL_JURNAL_RINCIAN set posting=%s where tahun=%s and KODEURUSAN=%s \
    				and KODESUBURUSAN=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') and isskpd=0\
                    and kodeunit=%s and NOREF = %s",[posting,tahun,org[0],org[1],org[2],org[3],array_index[i].split('^')[0]])
    		
    		if(posting == "1"):
    			hasil = "Proses Posting ke Buku Besar Berhasil"
    		else:
    			hasil = "Proses Un Posting Buku Besar Berhasil"

    return HttpResponse(hasil)

def delete_jurnal(request):
    hasil = ''
    lock = request.GET.get('act')
    
    if request.method == 'POST':
    	array_index = json.loads(request.POST.get('array_index'))
    	org = request.POST.get('organisasi').split('.')
    	tahun = tahun_log(request)

    	for i in range(len(array_index)):

	        with connections[tahun_log(request)].cursor() as cursor:
	            cursor.execute("DELETE FROM akuntansi.AKRUAL_BUKU_JURNAL where tahun=%s"
	                    " and KODEURUSAN=%s and KODESUBURUSAN=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') and isskpd=0"
	                    " and kodeunit=%s and NOREF in (%s)",[tahun,org[0],org[1],org[2],org[3],array_index[i].split('^')[0]])
	        
	        with connections[tahun_log(request)].cursor() as cursor:
	            cursor.execute("DELETE FROM akuntansi.AKRUAL_JURNAL_RINCIAN where tahun=%s"
	                    " and KODEURUSAN=%s and KODESUBURUSAN=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') and isskpd=0"
	                    " and kodeunit=%s and NOREF in (%s)",[tahun,org[0],org[1],org[2],org[3],array_index[i].split('^')[0]])
    return HttpResponse(hasil)

def loadlaporanakrual(request):
    gets = str(request.GET.get('skpd'))    
    urai = str(request.GET.get('urai')).replace('+',' ')


    if gets != '0' or gets != '' or gets != '0.0.0.0':
        aidi = gets.split('.')
    else:
        skpd = '0.0.0.0'
        aidi = skpd.split('.')  
   
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
            "and kodeurusan=%s and kodesuburusan=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') "
            "and kodeunit=%s and jenissistem=%s order by id ",
            [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],2])
        bendahara = dictfetchall(cursor) 

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT kodeakun as kode, urai as nama FROM master.master_rekening "
			"WHERE tahun = %s AND kodekelompok = 0 ORDER BY kodeakun",[tahun_log(request)])
        arrjns_akun = dictfetchall(cursor)

    arrjns_lap = [{'kode':'0','nama':'==== Pilih Jenis Laporan ===='}, #0 
    		{'kode':'1','nama':'Buku Jurnal Umum ( JU )'}, #1
			{'kode':'2','nama':'Buku Jurnal Penyesuaian'}, #2
			{'kode':'3','nama':'Buku Besar ( BB )'}, #3
			{'kode':'4','nama':'Jurnal Penutup'}, #4
			{'kode':'5','nama':'Neraca Saldo'}, #5
			{'kode':'6','nama':'Kertas Kerja'}, #6
			{'kode':'7','nama':'Laporan Realisasi Semester Pertama (Prognosis)'}, #7
			{'kode':'8','nama':'Laporan Realisasi Anggaran'}, #8
			{'kode':'9','nama':'Laporan Operasional'}, #9
			{'kode':'10','nama':'Neraca'}, #10
			{'kode':'11','nama':'Laporan Perubahan Ekuitas'}, #11	
			{'kode':'12','nama':'Sekat Laporan'},		
		]   

    data = {        
        'bendahara' : bendahara, 'skpd':gets, 'urai':urai, 'jns_lap':arrjns_lap,
        'jns_akun':arrjns_akun
    }
    return render(request,'spjskpd/modal_laporan_akrual.html',data)

# def cetak_laporan_akrual_skpd(request):
# 	post 	= request.POST
# 	lapParm = {}
	
# 	skpd 	= post.get('skpd').split('.')
# 	index_laporan = int(post.get('index_laporan'))
# 	jenis_akun = post.get('jenis_akun')
# 	tgl_awal = post.get('tgl_awal')
# 	tgl_akhir = post.get('tgl_akhir')
# 	id_pengguna_anggaran = post.get('id_pengguna_anggaran')
# 	id_ppk = post.get('id_ppk')
# 	tgl_cetak = post.get('tgl_cetak')

# 	if index_laporan == 1:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuJurnal.fr3'
# 	elif index_laporan == 2:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuJurnalPenyesuaian.fr3'
# 	elif index_laporan == 3:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuBesar.fr3'
# 		lapParm['jenisakun'] = "'"+jenis_akun+"'"
# 	elif index_laporan == 4:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/JurnalPenutup.fr3'
# 	elif index_laporan == 5:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/NeracaSaldo.fr3'
# 	elif index_laporan == 6:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/kertaskerja.fr3'
# 	elif index_laporan == 7:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/prognosis.fr3'
# 	elif index_laporan == 8:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/Lra.fr3'
# 	elif index_laporan == 9:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/LO.fr3'
# 	elif index_laporan == 10:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/NeracaSKPD.fr3'
# 	elif index_laporan == 11:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/LPE.fr3'
# 	elif index_laporan == 12:
# 		lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/sekatlaporan.fr3'
	
# 	tgl_kemarin = str(int(tgl_to_laporan(tgl_akhir).split('-')[0])-1)+'-'+tgl_to_laporan(tgl_akhir).split('-')[1]+'-'+tgl_to_laporan(tgl_akhir).split('-')[2]
	

# 	lapParm['tahun'] = "'"+tahun_log(request)+"'"			
# 	lapParm['kodeurusan'] = ""+skpd[0]+""
# 	lapParm['kodesuburusan'] = ""+skpd[1]+""
# 	lapParm['kodeorganisasi'] = "'"+skpd[2]+"'"
# 	lapParm['kodeunit'] = "'"+skpd[3]+"'"
# 	lapParm['idpa'] = ""+id_pengguna_anggaran+""	
# 	lapParm['idppk'] = ""+id_ppk+""
# 	lapParm['tglawal'] = "'"+tgl_to_laporan(tgl_awal)+"'"
# 	lapParm['tglakhir'] = "'"+tgl_to_laporan(tgl_akhir)+"'"	
# 	lapParm['periodeawal'] =""+tgl_awal+""
# 	lapParm['periodeakhir'] = ""+tgl_akhir+""
# 	lapParm['tglkemarin'] = "'"+tgl_kemarin+"'"
# 	lapParm['report_type'] = 'pdf'
# 	lapParm['isskpd'] = "0"
# 	lapParm['TGLCETAK'] = ""+tgl_cetak+""
	
# 	# lapParm['tglto'] = "'"+tgl_to_laporan(tgl_awal)+"'"
# 	# lapParm['tglfrom'] = "'"+tgl_to_laporan(tgl_akhir)+"'"

# 	# http://localhost/reportsvc_sipkd/?file=PPKSKPD/Akrual/BukuBesar.fr3&jenisakun=1&tahun='2019'&kodeurusan=1&kodesuburusan=2&kodeorganisasi='01'&idpa=0&idppk=0&tglawal='2019-01-01'&tglakhir='2019-12-31'&periodeawal=01+Januari+2019&periodeakhir=31+Desember+2019&tglkemarin='2018-12-31'&report_type=pdf&isskpd=0&TGLCETAK=16+Juli+2019&tglto='2019-01-01'&tglfrom='2019-12-31'
# 	return HttpResponse(laplink(request, lapParm))

def cetak_laporan_akrual_skpd(request):
	post 	= request.POST
	lapParm = {}
	
	skpd 	= post.get('skpd').split('.')
	index_laporan = int(post.get('index_laporan'))
	jenis_akun = post.get('jenis_akun')
	level_lap = int(post.get('level_lap'))
	tgl_awal = post.get('tgl_awal')
	tgl_akhir = post.get('tgl_akhir') 
	id_pengguna_anggaran = post.get('id_pengguna_anggaran')
	id_ppk = post.get('id_ppk')
	tgl_cetak = post.get('tgl_cetak')
	lap_type = post.get('lap_type').lower()


	if index_laporan == 1:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuJurnal.fr3'
	elif index_laporan == 2:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuJurnalPenyesuaian.fr3'
	elif index_laporan == 3:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/BukuBesar.fr3'
		lapParm['jenisakun'] = "'"+jenis_akun+"'"
	elif index_laporan == 4:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/JurnalPenutup.fr3'
	elif index_laporan == 5:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/NeracaSaldo.fr3'
	elif index_laporan == 6:
		lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/kertaskerja.fr3'

	elif index_laporan == 7:
		if level_lap == 1:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/prognosis.fr3'
		elif level_lap == 2:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/prognosis_objek.fr3'
		elif level_lap == 3:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/prognosis_rincianobjek.fr3'
		elif level_lap == 4:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/prognosis_subrincianobjek.fr3'

	elif index_laporan == 8:
		if level_lap == 1:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/Lra.fr3'
		elif level_lap == 2:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/Lra_objek.fr3'
		elif level_lap == 3:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/Lra_rincianobjek.fr3'
		elif level_lap == 4:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/Lra_subrincianobjek.fr3'

	elif index_laporan == 9:
		if level_lap == 1:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/LO.fr3'
		elif level_lap == 2:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/LO_objek.fr3'
		elif level_lap == 3:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/LO_rincianobjek.fr3'
		elif level_lap == 4:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/LO_subrincianobjek.fr3'

	elif index_laporan == 10:
		if level_lap == 1:
			lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/NeracaSKPD.fr3'
		elif level_lap == 2:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/NeracaSKPD_objek.fr3'
		elif level_lap == 3:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/NeracaSKPD_rincianobjek.fr3'
		elif level_lap == 4:
			lapParm['file'] = 'penatausahaan/PPKSKPD/Akrual/NeracaSKPD_subrincianobjek.fr3'

	elif index_laporan == 11:
		lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/LPE.fr3'
	elif index_laporan == 12:
		lapParm['file'] = 'penatausahaan/PPKSKPD/akrual/sekatlaporan.fr3'
	
	tgl_kemarin = str(int(tgl_to_laporan(tgl_akhir).split('-')[0])-1)+'-'+tgl_to_laporan(tgl_akhir).split('-')[1]+'-'+tgl_to_laporan(tgl_akhir).split('-')[2]
	

	lapParm['tahun'] = "'"+tahun_log(request)+"'"			
	lapParm['kodeurusan'] = ""+skpd[0]+""
	lapParm['kodesuburusan'] = ""+skpd[1]+""
	lapParm['kodeorganisasi'] = "'"+skpd[2]+"'"
	lapParm['kodeunit'] = "'"+skpd[3]+"'"
	lapParm['idpa'] = ""+id_pengguna_anggaran+""	
	lapParm['idppk'] = ""+id_ppk+""
	lapParm['tglawal'] = "'"+tgl_to_laporan(tgl_awal)+"'"
	lapParm['tglakhir'] = "'"+tgl_to_laporan(tgl_akhir)+"'"	
	lapParm['periodeawal'] =""+tgl_awal+""
	lapParm['periodeakhir'] = ""+tgl_akhir+""
	lapParm['tglkemarin'] = "'"+tgl_kemarin+"'"
	lapParm['report_type'] = lap_type
	lapParm['isskpd'] = "0"
	lapParm['TGLCETAK'] = ""+tgl_cetak+""
	
	# lapParm['tglto'] = "'"+tgl_to_laporan(tgl_awal)+"'"
	# lapParm['tglfrom'] = "'"+tgl_to_laporan(tgl_akhir)+"'"

	# http://localhost/reportsvc_sipkd/?file=PPKSKPD/Akrual/BukuBesar.fr3&jenisakun=1&tahun='2019'&kodeurusan=1&kodesuburusan=2&kodeorganisasi='01'&idpa=0&idppk=0&tglawal='2019-01-01'&tglakhir='2019-12-31'&periodeawal=01+Januari+2019&periodeakhir=31+Desember+2019&tglkemarin='2018-12-31'&report_type=pdf&isskpd=0&TGLCETAK=16+Juli+2019&tglto='2019-01-01'&tglfrom='2019-12-31'
	return HttpResponse(laplink(request, lapParm))

def loadpenggunaanggaran(request):
	gets = str(request.POST.get('skpd'))	
	isi_bendahara = ''

	if gets != '0':
		aidi = gets.split('.')
	else:
		skpd = '0.0.0'
		aidi = skpd.split('.')  

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
			" and kodeurusan=%s and kodesuburusan=%s and replace(KODEORGANISASI,' ', '')=lpad(%s,2,'0') and kodeunit=%s and jenissistem=%s order by id ",
			[tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],2])
		bendahara = dictfetchall(cursor)
	for x in range(len(bendahara)):            
		isi_bendahara += '<option value="'+str(bendahara[x]['id'])+'|'+bendahara[x]['nama']+'|'+bendahara[x]['nip']+'|'+bendahara[x]['pangkat']+'">'+bendahara[x]['jabatan']+'</option>'       

	data = {            
		'isi_bendahara' : isi_bendahara            
	}

	return JsonResponse(data)

def simpan_akrual_skpd(request):
	hasil = ''
	arr_fix = json.loads(request.POST.get('arr_fix'))
	org = request.POST.get('organisasi').split('.')
	cb_jenis = int(request.POST.get('cb_jenis'))
	var_jenis_transaksi = request.POST.get('var_jenis_transaksi')
	isSimpan = request.POST.get('isSimpan')
	noref = request.POST.get('noref')
	nobukti = request.POST.get('nobukti')
	uraian = request.POST.get('uraian')
	tgl = request.POST.get('tgl')


	jml_debet = 0
	jml_kredit = 0
	jenissp2d = ''
	global var_nobku
	global var_jenissp2d
	global var_ispihakketiga
	ispihakketiga = ''
	lanjut = 'no'

	var_jenissp2d = ''
	var_nobku = '0'
	var_jenis_transaksi = ''
	var_ispihakketiga = '0'

	if request.method == 'POST':
		for x in range(len(arr_fix)):
			jml_debet = jml_debet+float(arr_fix[x].split('^')[1])
			jml_kredit = jml_kredit+float(arr_fix[x].split('^')[2])
		
		if jml_debet!=jml_kredit:
			hasil = 'Jumlah debet dengan kredit tidak sama!'
			raise ValueError('Jumlah debet dengan kredit tidak sama!')
		else:
			if (cb_jenis!=1) and (var_jenis_transaksi=='SP2D' or var_jenis_transaksi=='SP2D-GJ'
				 or var_jenis_transaksi=='SPJ' or var_jenis_transaksi=='BAYAR-GJ' or var_jenis_transaksi=='PUNGUT-PAJAK' or var_jenis_transaksi=='RK-PPKD'
				 or var_jenis_transaksi=='SETOR-PAJAK'  or var_jenis_transaksi=='PUNGUT PENDAPATAN' or var_jenis_transaksi=='SETOR PENDAPATAN'
				 or var_jenis_transaksi=='SKR' or var_jenis_transaksi=='SKP' or var_jenis_transaksi=='KOREKSI PENERIMAAN'
				 or var_jenis_transaksi=='KOREKSI PENGELUARAN' or var_jenis_transaksi=='TIDAK-CAIR' or var_jenis_transaksi=='SP2B' or var_jenis_transaksi=='AWAL') and (isSimpan=='true'):
				if var_jenis_transaksi=='SKR' or var_jenis_transaksi=='SKP':
					var_jenissp2d = ''
					var_nobku = '0'
					var_ispihakketiga = '0'
				elif var_jenis_transaksi=='SP2B' or var_jenis_transaksi=='AWAL':
					var_jenissp2d = ''
					var_nobku = '0'
					var_ispihakketiga = '1'

			if (cb_jenis!=1) and (var_jenis_transaksi=='SP2D' or var_jenis_transaksi=='SP2D-GJ'
				 or var_jenis_transaksi=='SPJ' or var_jenis_transaksi=='BAYAR-GJ' or var_jenis_transaksi=='PUNGUT-PAJAK' or var_jenis_transaksi=='RK-PPKD'
				 or var_jenis_transaksi=='SETOR-PAJAK'  or var_jenis_transaksi=='PUNGUT PENDAPATAN' or var_jenis_transaksi=='SETOR PENDAPATAN'
				 or var_jenis_transaksi=='SKR' or var_jenis_transaksi=='SKP' or var_jenis_transaksi=='KOREKSI PENERIMAAN'
				 or var_jenis_transaksi=='KOREKSI PENGELUARAN' or var_jenis_transaksi=='TIDAK-CAIR' or var_jenis_transaksi=='SP2B' or var_jenis_transaksi=='AWAL') and (isSimpan=='false'):
				if var_jenis_transaksi=='SKR' or var_jenis_transaksi=='SKP':
					var_jenissp2d = ''
					var_nobku = '0'
					var_ispihakketiga = '0'
				elif var_jenis_transaksi=='SP2B' or var_jenis_transaksi=='AWAL':
					var_jenissp2d = ''
					var_nobku = '0'
					var_ispihakketiga = '1'
			
			if cb_jenis==1:
				var_jenissp2d = ''
				var_nobku = '0'
				var_jenis_transaksi = 'NA'
				var_ispihakketiga = '0'

			if cb_jenis==3:
				var_jenissp2d = ''
				var_nobku = '0'
				var_jenis_transaksi = 'JS'
				var_ispihakketiga = '0'

			if cb_jenis==4:
				var_jenissp2d = ''
				var_nobku = '0'
				var_jenis_transaksi = 'JPLRA'
				var_ispihakketiga = '0'

			if cb_jenis==5:
				var_jenissp2d = ''
				var_nobku = '0'
				var_jenis_transaksi = 'JPLO'
				var_ispihakketiga = '0'
			
			try:
				if len(arr_fix) != 0:
					if isSimpan == 'true':
						try:
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("INSERT INTO akuntansi.AKRUAL_BUKU_JURNAL (TAHUN,KODEURUSAN,KODESUBURUSAN,\
								KODEORGANISASI,KODEUNIT,ISSKPD,NOREF,NOBUKTI,JENISJURNAL,KETERANGAN,POSTING,TANGGALBUKTI,USERNAME,NO_BKU,\
								ISPIHAKKETIGA,JENIS_TRANSAKSI,JENISSP2D) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[
								tahun_log(request), org[0], org[1], org[2], org[3], 0, noref, nobukti, cb_jenis, uraian, 1, tgl_to_db(tgl), 
								username(request), var_nobku, var_ispihakketiga, var_jenis_transaksi, var_jenissp2d])
							lanjut = 'yes'
						except BaseException as e:
							print('errornya ', e)
							lanjut = 'no'
					else:
						try:
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("UPDATE akuntansi.AKRUAL_BUKU_JURNAL SET \
						  			NOBUKTI = %s, JENISJURNAL= %s, KETERANGAN= %s, TANGGALBUKTI=%s WHERE TAHUN= %s AND KODEURUSAN=%s \
						  			AND KODESUBURUSAN=%s AND replace(KODEORGANISASI,' ', '')=%s AND KODEUNIT=%s AND ISSKPD=0 AND NOREF= %s",[nobukti, cb_jenis, 
						  uraian, tgl_to_db(tgl), tahun_log(request), org[0], org[1], org[2], org[3], noref])
							lanjut = 'yes'
						except BaseException as e:
							lanjut = 'no'
					if lanjut != 'no':
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("DELETE FROM akuntansi.AKRUAL_JURNAL_RINCIAN WHERE tahun = %s \
								and kodeurusan = %s and kodesuburusan = %s and replace(KODEORGANISASI,' ', '') = %s \
								AND KODEUNIT=%s and isskpd = 0 and noref = %s",[
								tahun_log(request), org[0], org[1], org[2], org[3], noref])

						for x in range(len(arr_fix)):
							pecah_rek1 = arr_fix[x].split('^')[0].split('-')[0].split('.')
							pecah_rek2 = arr_fix[x].split('^')[0].split('-')[1].split('.')
							
							with connections[tahun_log(request)].cursor() as cursor:
								cursor.execute("INSERT INTO akuntansi.AKRUAL_JURNAL_RINCIAN (TAHUN,\
									KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOREF,\
									KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,\
									KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK,\
									URUT,ISSKPD,DEBET,KREDIT,POSTING) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[
									tahun_log(request), org[0], org[1], org[2], org[3], noref, 
									pecah_rek1[0]+'.'+pecah_rek1[1], pecah_rek1[3], pecah_rek1[4], pecah_rek1[5], 
									pecah_rek2[0], pecah_rek2[1], pecah_rek2[2], pecah_rek2[3], pecah_rek2[4], pecah_rek2[5], 
									x+1, 0, float(arr_fix[x].split('^')[1]),float(arr_fix[x].split('^')[2]), 1])
					
			except BaseException as e:
				raise ValueError('GAGAL operasi insert atau update jurnal SKPD ')
				print('GAGAL operasi insert atau update jurnal SKPD', e)
	return HttpResponse(hasil)

def modal_ambil_jurnal(request):
	
	if request.method == 'POST':
		data = request.POST
		tgl_awal = tgl_short(data.get('bulan_dari'))
		tgl_akhir = tgl_short(data.get('bulan_sampai'))
		org = request.POST.get('eskapede').split('.')
		jenis = data.get('jenis_data')


		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * \
				FROM akuntansi.fc_dump_jurnal_umum_skpd (%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request),
				org[0],org[1],org[2],org[3],'ADMIN',tgl_awal,tgl_akhir,jenis])
			hasilnya = dictfetchall(cursor)

		data = {'pesan':'Ambil Jurnal Berhasil'}
		return JsonResponse(data)

	else:
		arrjns_data = [
			{'kode':'','nama':'==== Pilih Jenis Data Yang Akan Diambil ===='},
    		{'kode':'BKU_PENERIMAAN','nama':'1. Data Penerimaan'},
			{'kode':'BKU_PENGELUARAN','nama':'2. Data Pengeluaran'},
		]

		data = {'list_jenis':arrjns_data}

		return render(request, 'spjskpd/modal/modal_ambil_jurnal.html', data)

def modal_rekening_jurnal(request):

	if request.method == 'POST':
		data = request.POST
		skpd = data.get("id").split(".")
		kodeakun = data.get("kd")

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun,koderekening,uraian \
				from akuntansi.fc_akrual_viw_rekening_jurnal(%s,%s,%s,%s,%s) \
				WHERE kodeakun = %s ORDER BY koderekening",
				[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],kodeakun])
			rekening = dictfetchall(cursor)

		data = {'pagess':'isi_tabel','dt_rek':rekening}
		return render(request, 'spjskpd/modal/modal_rekening_jurnal.html', data)

	else:
		skpd = request.GET.get("id").split(".")

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun, urai FROM master.master_rekening \
				WHERE tahun = %s AND kodekelompok = 0 \
				ORDER BY kodeakun",[tahun_log(request)])
			jenis = dictfetchall(cursor)

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeakun,koderekening,uraian \
				from akuntansi.fc_akrual_viw_rekening_jurnal(%s,%s,%s,%s,%s)\
				WHERE kodeakun = 0 ORDER BY koderekening",[tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3]])
			rekening = dictfetchall(cursor)

		data = {'pagess':'headeer','dt_rek':rekening,'jns_pilter':jenis}
		return render(request, 'spjskpd/modal/modal_rekening_jurnal.html', data)
