from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
import pprint

def sppup(request,jenis):    
    skpd = set_organisasi(request)     
    is_perubahan = perubahan(request) 
    namabank = set_nama_bank(request)        
    path = ''    
    if skpd["kode"] == '': kode = 0
    else: kode = skpd["kode"]

    if jenis=='up':
        path = 'sppup.html'
    elif jenis=='gu':
        path = 'sppgu.html'
    elif jenis=='tu':
        path = 'spptu.html'
    elif jenis=='gunihil':
        path = 'sppgunihil.html'
    elif jenis=='tunihil':
        path = 'spptunihil.html'
    elif jenis=='btlgaji':
        path = 'sppgaji.html'
    elif jenis=='lsbarjas':
        path = 'sppbarjas.html'    
    elif jenis=='persetujuanskpd':
        path = 'persetujuanskpd.html'
    elif jenis=='lpjupgu':
        path = 'lpjupgu.html'
    elif jenis=='lpjtu':
        path = 'lpjtu.html'
    elif jenis=='pengembalianupgutu':
        path = 'pengembalianspp.html'
    elif jenis=='laporanspp':
        path = 'laporanspp.html' 


    data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"],
        'is_perubahan':is_perubahan,'namabank':namabank['list_bank']}
    return render(request, 'spp/'+path+'',data)

def getsppupskpd(request):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None) 

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
       
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM PENATAUSAHAAN.SPP where tahun = %s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') and kodeunit=%s and jenisspp = 'UP' order by nospp",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
            list_up = dictfetchall(cursor)        

        objek = []
        for arr in list_up:
        	objek.append({'tahun':arr['tahun'], 'kodeurusan':arr['kodeurusan'], 'kodesuburusan':arr['kodesuburusan'], 
				'kodeorganisasi':arr['kodeorganisasi'], 'nospp':arr['nospp'], 'tglspp':tgl_indo(arr['tglspp']),
				'bendaharapengeluaran':arr['bendaharapengeluaran'], 'norekeningbendahara':arr['norekeningbendahara'],
				'npwp':arr['npwp'], 'namabank':arr['namabank'], 'sk_up':arr['sk_up'], 
				'tgl_sk_up':tgl_indo(arr['tgl_sk_up']), 'jml_sk_up':arr['jml_sk_up'], 'nospd':arr['nospd'], 
				'tglspd':tgl_indo(arr['tglspd']),'jmlspd':arr['jmlspd'], 'sisadanaspd':arr['sisadanaspd'], 
				'deskripsipekerjaan':arr['deskripsipekerjaan'], 'jumlahspp':arr['jumlahspp'], 'locked':arr['locked'],
                'namarekeningbank':arr['namarekeningbank']})
        
        data = {'list_up' : objek}
        return JsonResponse(data)

    else:
    	return redirect('sipkd:index')

def cektanggaldpa(request):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd')
        jenis = request.POST.get('jns')         

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
       
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT TANGGAL FROM master.MASTER_DASARHUKUM where tahun = %s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') AND KODEUNIT= %s and JENISDPA=%s ",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3], jenis])
            list_dpa = dictfetchall(cursor)        

        data = {}
        for arr in list_dpa:  
            data = {'tanggal':tgl_indo(arr['tanggal'])}
        return JsonResponse(data)

    else:
        return redirect('sipkd:index')

def ceksppup(request):
    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            org = request.POST.get('skpd', None).split('.')
            no_spp = request.POST.get('spp')

            # if no_spp != '':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT COUNT(nospp) FROM PENATAUSAHAAN.SPP where tahun=%s and kodeurusan=%s"
                    " and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and nospp=%s",
                    [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper()])
                hasil = cursor.fetchone()
            return HttpResponse(hasil[0])

def cekskup(request):
    if 'sipkd_username' in request.session:
        
        gets = request.GET.get('id', None) 

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
        

        
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM PENATAUSAHAAN.SK_UP where tahun = %s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0')  and kodeunit=%s ",
                [tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3]])
            list_up = dictfetchall(cursor)
            

        objek = []
        for arr in list_up:
            objek.append({'tahun':arr['tahun'], 'kodeurusan':arr['kodeurusan'], 'kodesuburusan':arr['kodesuburusan'], 
                'kodeorganisasi':arr['kodeorganisasi'], 'tglspp':tgl_indo(arr['tanggal']),
                'sk_up':arr['noskup'], 
                'tgl_sk_up':tgl_indo(arr['tanggal']), 'jml_sk_up':arr['jumlah'], 'nospd':'-', 
                'tglspd':tgl_indo(arr['tanggal']),'jmlspd':arr['jumlah'], 'sisadanaspd':arr['jumlah'], 
                'jumlahspp':arr['jumlah']})

        data = {'list_up' : objek}
        return JsonResponse(data)

def savesppup(request):
    hasil = ''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            org = request.POST.get('organisasi', None).split('.')
            no_spp = request.POST.get('no_spp')
            no_spp_lama = request.POST.get('no_spp_lama')
            tanggal_spp = tgl_short(request.POST.get('tanggal_spp'))
            bendahara = request.POST.get('bendahara')
            norek_bendahara = request.POST.get('norek_bendahara')
            nama_bank = request.POST.get('nama_bank')
            npwp_bendahara = request.POST.get('npwp_bendahara')
            status_keperluan = request.POST.get('status_keperluan')
            nomor_skup = request.POST.get('nomor_skup')
            tanggal_skup = tgl_short(request.POST.get('tanggal_skup'))
            jumlah_skup = request.POST.get('jumlah_skup')
            dasar_spd = request.POST.get('dasar_spd')
            tanggal_spd = tgl_short(request.POST.get('tanggal_spd'))
            jumlah_spd = request.POST.get('jumlah_spd')
            sisa_spd = request.POST.get('sisa_spd')
            aksi = request.POST.get('aksi')
            nm_pemilik_rekening = request.POST.get('nama_rekening_bank')
         

            
            if no_spp != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO PENATAUSAHAAN.SPP (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,TGLSPP,TGLSPP_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"\
                            " DESKRIPSISPP,JUMLAHSPP,BENDAHARAPENGELUARAN,NOREKENINGBENDAHARA,JENISSPP,namabank,sk_up,tgl_sk_up,tglspd,jml_sk_up,jmlspd,nospd,"\
                            " npwp,deskripsipekerjaan,triwulan,sisadanaspd,perubahan,namarekeningbank,uname)"\
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper(),tanggal_spp,tanggal_spp,'',0,0,status_keperluan,sisa_spd, 
                            bendahara,norek_bendahara,'UP',nama_bank,nomor_skup,tanggal_skup,tanggal_spd,jumlah_skup,jumlah_spd,
                            dasar_spd,npwp_bendahara,status_keperluan,1,0,0,nm_pemilik_rekening,username(request)])
                        hasil = ""
                      
                    with connections[tahun_log(request)].cursor() as cursor:
                      
                        cursor.execute("INSERT INTO PENATAUSAHAAN.SPPRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,TANGGAL,JUMLAH)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper(),'',0,'0',0,0,1,1,1,3,1,1,tanggal_spp,jumlah_skup] )
                        hasil = "Data berhasil disimpan!"
                       
                            
                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE PENATAUSAHAAN.SPP SET NOSPP=%s, TGLSPP=%s, TGLSPP_DRAFT=%s, DESKRIPSISPP=%s,"
                            "JUMLAHSPP=%s, BENDAHARAPENGELUARAN=%s, NOREKENINGBENDAHARA=%s, namarekeningbank=%s, namabank=%s, npwp=%s, deskripsipekerjaan=%s,"
                            "sk_up=%s, tgl_sk_up=%s, tglspd=%s, jml_sk_up=%s, jmlspd=%s, nospd=%s, PERUBAHAN=%s, TRIWULAN=%s "
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and NOSPP=%s",
                            [no_spp.upper(),tanggal_spp,tanggal_spp,status_keperluan,jumlah_skup,bendahara,norek_bendahara,nm_pemilik_rekening,
                            nama_bank,npwp_bendahara,status_keperluan,nomor_skup,tanggal_skup,tanggal_spd,jumlah_skup,jumlah_spd,dasar_spd,
                            0,1,tahun_log(request),org[0],org[1],org[2],no_spp_lama.upper()])
                        hasil = "Data berhasil diubah!"
            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def deletesppup(request):
    # get id
    nospp = request.POST.get('nospp')
    organisasi = request.POST.get('org')
    tahun = tahun_log(request)
    hasil = ''
    
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM PENATAUSAHAAN.SPP where tahun=%s and nospp=%s and"\
            " kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s",[tahun,nospp,organisasi])
        hasil = ""
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM PENATAUSAHAAN.SPPRINCIAN where tahun=%s and nospp=%s and"\
            " kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s",[tahun,nospp,organisasi])
        hasil = "Data berhasil dihapus!"

    return HttpResponse(hasil)

def loadspp(request,jenis):
    org = request.GET.get('id').split('.') 
    tanggal_spp = ''

    if jenis=='non_angg':
        jenis = 'non angg' 
   
    if jenis=='gj':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'-'||o.urai "
                "from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan "
                "and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi ) as organisasi,s.deskripsispp as keperluan,"
                "(select sum (jumlah) from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospp=s.nospp ) as jumlah,"
                "(select kodebidang from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospp=s.nospp limit 1 ) as kodebidang,"
                "(select kodeprogram from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospp=s.nospp limit 1 ) as kodeprogram,"
                "(select kodekegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nospp=s.nospp limit 1 ) as kodekegiatan,"
                "s.kodeurusan,s.kodesuburusan,s.kodeorganisasi FROM penatausahaan.spp s  where s.tahun=%s and kodeurusan=%s and kodesuburusan=%s "
                "and kodeorganisasi=lpad(%s,2,'0') and s.jenisspp=%s",
                [tahun_log(request),org[0],org[1],org[2],jenis.upper()])
            list_spp = dictfetchall(cursor)
    elif jenis=='ls':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai "
                "from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan "
                "and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.deskripsispp as keperluan,"
                "(select sum (jumlah) from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp ) as jumlah,"
                "(select kodebidang from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp limit 1 ) as kodebidang,"
                "(select kodeprogram from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodeprogram,"
                "(select kodekegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodekegiatan,"
                "(select kodesubkegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodesubkegiatan,"
                "s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit FROM penatausahaan.spp s  where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s "
                "and s.kodeorganisasi=%s and s.kodeunit=%s and s.jenisspp=%s",
                [tahun_log(request),org[0],org[1],org[2],org[3],jenis.upper()])
            list_spp = dictfetchall(cursor)
        # print("SELECT s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai "
        #         "from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan "
        #         "and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.deskripsispp as keperluan,"
        #         "(select sum (jumlah) from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
        #         "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp ) as jumlah,"
        #         "(select kodebidang from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
        #         "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp limit 1 ) as kodebidang,"
        #         "(select kodeprogram from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
        #         "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodeprogram,"
        #         "(select kodekegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
        #         "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1 ) as kodekegiatan,"
        #         "s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit FROM penatausahaan.spp s  where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s "
        #         "and s.kodeorganisasi=%s and s.kodeunit=%s and s.jenisspp=%s",
        #         [tahun_log(request),org[0],org[1],org[2],org[3],jenis.upper()])
    else:
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||kodeunit||'-'||o.urai "
                "from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan "
                "and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.deskripsispp as keperluan, "
                "(select sum (sr.jumlah) from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan "
                "and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp ) as jumlah, "
                "s.kodeurusan,s.kodesuburusan,s.kodeorganisasi FROM penatausahaan.spp s  where s.tahun=%s and s.kodeurusan=%s "
                "and s.kodesuburusan=%s and s.kodeorganisasi=%s and kodeunit=%s and s.jenisspp=%s",
                [tahun_log(request),org[0],org[1],org[2],org[3],jenis.upper()])
            list_spp = dictfetchall(cursor)

    objek = []
    for arr in list_spp:
        if jenis=='ls':
            objek.append({'nospp':arr['nospp'],'organisasi':arr['organisasi'],'keperluan':arr['keperluan'],
                'jumlah':arr['jumlah'],'tanggal':tgl_indo(arr['tanggal']),'kodebidang':arr['kodebidang'],
                'kodeprogram':arr['kodeprogram'],'kodekegiatan':arr['kodekegiatan'],'kodesubkegiatan':arr['kodesubkegiatan']})
        else:
            objek.append({'nospp':arr['nospp'],'organisasi':arr['organisasi'],'keperluan':arr['keperluan'],
                'jumlah':arr['jumlah'],'tanggal':tgl_indo(arr['tanggal'])})

    data = {'list_spp':objek}
    return render(request, 'spp/modal/modal_spp.html', data)

def ambilkegiatan(request):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd') 
        kodebidang = request.POST.get('kodebidang')   
        kodeprogram = request.POST.get('kodeprogram')    
        kodekegiatan = request.POST.get('kodekegiatan')   

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
       
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT urai FROM PENATAUSAHAAN.KEGIATAN where tahun = %s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') and kodebidang=%s "
                "and kodeprogram=%s and kodekegiatan=%s ",
                [tahun_log(request),aidi[0], aidi[1], aidi[2], kodebidang,kodeprogram,kodekegiatan])
            list_spp = dictfetchall(cursor)        

        data = {}
        for arr in list_spp:  
            data = {'urai':arr['urai']}
        return JsonResponse(data)

    else:
        return redirect('sipkd:index')

def loadbendahara(request):
    org = request.GET.get('id').split('.')     

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT * FROM MASTER.PEJABAT_SKPD WHERE tahun=%s and KODEURUSAN=%s and KODESUBURUSAN=%s"
            " and KODEORGANISASI=lpad(%s,2,'0') and kodeunit=%s and JENISSISTEM=%s and UPPER(JABATAN) LIKE (%s)",
            [tahun_log(request),org[0],org[1],org[2],org[3],2,'%BENDAHARA PENGELUARAN%'])
        list_bend = dictfetchall(cursor)

    data = {'list_bend' : list_bend}
    return render(request,'spp/modal/modal_bendahara.html',data)

def loadpihakketiga(request):
    org = request.GET.get('id').split('.')     

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT NAMAPERUSAHAAN,BENTUKPERUSAHAAN,ALAMATPERUSAHAAN,NAMAPIMPINANPERUSAHAAN,NPWP,NAMABANK,NOREKPERUSAHAAN,NAMAREKENINGBANK,NOKONTRAK  FROM penatausahaan.SPP WHERE tahun=%s and KODEURUSAN=%s and KODESUBURUSAN=%s"
            " and KODEORGANISASI=lpad(%s,2,'0') and jenisspp='LS' "
            "GROUP BY NAMAPERUSAHAAN,BENTUKPERUSAHAAN,ALAMATPERUSAHAAN,NAMAPIMPINANPERUSAHAAN,NPWP,NAMABANK,NOREKPERUSAHAAN,NAMAREKENINGBANK,NOKONTRAK",
            [tahun_log(request),org[0],org[1],org[2]])
        list_pihak = dictfetchall(cursor)

    data = {'list_pihak' : list_pihak}
    return render(request,'spp/modal/modal_pihakketiga.html',data)

def loadkegiatan(request):
    org = request.GET.get('id').split('.')     

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,URAI FROM PENATAUSAHAAN.KEGIATAN WHERE tahun=%s and KODEURUSAN=%s and KODESUBURUSAN=%s"
            " and KODEORGANISASI=%s and kodeunit=%s  and kodesubkegiatan<>0 and kodesubkeluaran=0 ORDER BY KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,kodesubkegiatan",
            [tahun_log(request),org[0],org[1],org[2],org[3]])
        list_keg = dictfetchall(cursor)

    data = {'list_keg' : list_keg}
    return render(request,'spp/modal/modal_kegiatan.html',data)

def loadlpjspp(request,jenis):
    org = request.GET.get('id').split('.')   
    jenis = jenis.upper()
    if jenis=='GU' or jenis=='GU_NIHIL':
        jenisspp = "'GU','GU_NIHIL'"
    else:
        jenisspp = "TU_NIHIL"
        # jenisspp = ",".join(repr(e) for e in ['GU','GU_NIHIL'])
    # print(jenisspp)
    if jenis=='GU':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.nospj,s.tglspj,s.keperluan,(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) from penatausahaan.spj_skpd_rinc_sub1 sr "
                "where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and "
                "sr.kodeorganisasi=s.kodeorganisasi and sr.nospj=s.nospj ) as jumlah,extract (month from s.tglspj) as bulan,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi "
                "FROM penatausahaan.spj_skpd s  where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s and s.kodeorganisasi=%s "
                "and s.jenis='GU' and (s.nospj  not in (select nospj from penatausahaan.spp where tahun=%s"
                "and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and jenisspp in (%s)  ) ) order by s.tglspj,s.nospj",
                [tahun_log(request),org[0],org[1],org[2],tahun_log(request),org[0],org[1],org[2],jenisspp])
            list_lpj = dictfetchall(cursor)
    else:
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT s.nospj,s.tglspj,s.keperluan,(select (CASE WHEN sum(jumlah) is NULL THEN 0.00 ELSE sum(jumlah) END) from penatausahaan.spj_skpd_rinc_sub1 sr "
                "where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and "
                "sr.kodeorganisasi=s.kodeorganisasi and sr.nospj=s.nospj ) as jumlah,extract (month from s.tglspj) as bulan,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi "
                "FROM penatausahaan.spj_skpd s  where s.tahun=%s and s.kodeurusan=%s and s.kodesuburusan=%s and s.kodeorganisasi=%s "
                "and s.jenis='TU' and (s.nospj  not in (select nospj from penatausahaan.spp where tahun=%s"
                "and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and jenisspp in (%s)  ) ) order by s.tglspj,s.nospj",
                [tahun_log(request),org[0],org[1],org[2],tahun_log(request),org[0],org[1],org[2],jenisspp])
            list_lpj = dictfetchall(cursor)

    objek = []
    for arr in list_lpj:
        objek.append({'nospj':arr['nospj'],'tglspj':tgl_indo(arr['tglspj']),'keperluan':arr['keperluan'],
            'jumlahspj':arr['jumlah']})

    data = {'list_lpj' : objek}

    return render(request,'spp/modal/modal_lpjspp.html',data)

def listpersetujuan(request):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None) 
        isppkd = request.POST.get('isppkd', None)  
        print (gets)

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')        

        total_spp = 0
        total_setuju = 0
        if(isppkd=='1'):
            jenis = " AND JENISSPP IN ('LS_PPKD','NON ANGG')"            
        else:
            jenis = " AND JENISSPP NOT IN ('LS_PPKD','NON ANGG')" 
                  
        
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT NOSPP,JENISSPP,TGLSPP,KEPERLUAN,dasarspd,kegiatan,JUMLAH,0 as CEK,idspp " 
                "FROM penatausahaan.fc_lihat_spp_skpd(%s,%s,%s,%s,%s) "
                "WHERE locked='T' "+jenis+"",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
           
            list_spp = dictfetchall(cursor)  

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT NOSPP,JENISSPP,TGLSPP,NOSPM,KEPERLUAN,dasarspd,kegiatan,JUMLAH,tanggal,0 as CEK,idspp " 
                "FROM penatausahaan.fc_lihat_spp_skpd(%s,%s,%s,%s,%s) "
                "WHERE locked='Y' "+jenis+"",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
            list_setuju = dictfetchall(cursor)      

        objek = []
        for arr in list_setuju:
            total_setuju += arr['jumlah']
            objek.append({'nospp':arr['nospp'], 'jenisspp':arr['jenisspp'], 'tglspp':arr['tglspp'], 'nospm':arr['nospm'],
                'keperluan':arr['keperluan'], 'dasarspd':arr['dasarspd'],'idspp':arr['idspp'],
                'kegiatan':arr['kegiatan'], 'jumlah':arr['jumlah'], 'cek':arr['cek'],'tanggal':tgl_indo(arr['tanggal'])})

        for total in list_spp:
            total_spp += total['jumlah']

        if total_spp == 0:
            total_spp = '0,00'
        if total_setuju == 0:
            total_setuju = '0,00'

        data = {'list_spp' : list_spp, 'list_setuju' : objek,'total_spp' : total_spp,'total_setuju':total_setuju}
        return render(request, 'spp/list_persetujuanspp.html', data)

    else:
        return redirect('sipkd:index')

def loadppkd(request,jenis):
    kd_org = ''
    ur_org = ''
    organisasi = '' 
    path = ''

    if jenis=='persetujuanppkd':
        path = 'persetujuanppkd.html' 
    if jenis=='btlppkd':
        path = 'btlppkd.html' 
    elif jenis=='nonanggaran':
        path = 'sppnonangg.html' 
    
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi as kode, urai "\
            "from master.master_organisasi "\
            "where tahun=%s and kodeorganisasi <> '' and skpkd=1", [tahun_log(request)])
        list_org = dictfetchall(cursor) 

    for x in list_org:
        kd_org = x["kode"]
        ur_org = x["urai"]
        organisasi = x["kode"]+" - "+x["urai"]    

    data = {'organisasi':organisasi,'kd_org':kd_org, 'ur_org':ur_org}
    return render(request, 'spp/'+path+'',data)

def setuju_draft(request):
    hasil = ''
    lock = request.GET.get('act')
    
    if request.method == 'POST':
        tahun = tahun_log(request)
        gets = request.POST.get('skpd', None)        
        if(lock == 'lock'):
            locked = 'Y'
            chkspp = request.POST.getlist('cek_draft')
            nomor = request.POST.getlist('nomer_draft')
        else:
            locked = 'T'  
            chkspp = request.POST.getlist('cek_spp')
            nomor = request.POST.getlist('nomer_spp')

        skpd = '0.0.0.0'
        if gets=='0':                        
            aidi = skpd.split('.')  
        else:
            aidi = gets.split('.') 

        
        for i in range(0,len(chkspp)):
            cek = chkspp[i]            
            nomer_spp = nomor[i]
            spp = cek+':'+nomer_spp  
            split_spp = spp.split(':')

            if(split_spp[0]=='1'):
                nospp = split_spp[1] 
        
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.spp set locked=%s where tahun=%s"
                        " and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s"
                        " and kodeunit=%s and NOSPP in (%s)",[locked,tahun,aidi[0],aidi[1],aidi[2],aidi[3],nospp])
                if(locked == "Y"):
                    hasil = "SPP Telah di Setujui"
                else:
                    hasil = "SPP Telah di Unlock"
    return HttpResponse(hasil)

def listafektasi(request,jenis):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None) 
        no_spp = request.POST.get('spp', None)
        tgl_spp = tgl_short(request.POST.get('tgl', None)) 
        isppkd = request.POST.get('isppkd', None) 
        bidang = request.POST.get('bidang') 
        program = request.POST.get('program') 
        kegiatan = request.POST.get('kegiatan')
        subkegiatan = request.POST.get('subkegiatan')
        jenis = jenis.upper()
        hidden = ''

        if jenis== 'GU' or jenis=='GU_NIHIL':
            hidden = 'hidden'

        if jenis=='NON_ANGG':
            jenis='NON ANGG'        

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.') 

        print (kegiatan+' '+subkegiatan)

        if isppkd=='0' and aidi[0] !='0' :            
            if jenis=='GU' or jenis=='GU_NIHIL':
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
                        "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                        "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                        "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                        "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                        "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
                        "(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
                        " FROM penatausahaan.fc_view_spp_rincian(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) ",
                        [tahun_log(request),aidi[0], aidi[1], aidi[2],no_spp.upper(),'',0,0,tgl_spp,jenis])
                    list_spp = dictfetchall(cursor)
            elif jenis=='LS':
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
                        "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                        "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                        "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                        "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                        "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
                        "(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
                        " FROM penatausahaan.fc_view_spp_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",

                        [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],no_spp.upper(),bidang,program,kegiatan,subkegiatan,tgl_spp,jenis])
                   
                    list_spp = dictfetchall(cursor)
            else:
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
                        "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                        "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                        "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                        "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                        "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
                        "(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
                        "FROM penatausahaan.fc_view_spp_rincian_ppkd(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s) ",
                        [tahun_log(request),aidi[0], aidi[1], aidi[2],no_spp.upper(),tgl_spp,jenis])
                    list_spp = dictfetchall(cursor)
        else:
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
                        "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                        "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                        "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                        "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                        "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
                        "(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor " 
                        "FROM penatausahaan.fc_view_spp_rincian_ppkd(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s) ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2],no_spp.upper(),tgl_spp,'LS_PPKD'])
                list_spp = dictfetchall(cursor)

        kodekegiatan = ''
        for x in range(len(list_spp)):
            if (list_spp[x]['cek']==1):
                if(list_spp[x]['uraian']!=None):
                    objek = list_spp[x]['koderekening']
                    objek1 = objek.split('-') 
                    koderekening = objek1[0].split('.')
                    kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"

        kodekegiatan = "("+kodekegiatan[1:len(kodekegiatan)]+")"
            
        data = {'list_spp' : list_spp,'kodekegiatan':kodekegiatan,'hidden':hidden}
        return render(request, 'spp/tabel/tabel_spp_afektasi.html', data)

    else:
        return redirect('sipkd:index')

def listlpjspp(request,jenis):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None) 
        no_lpj = request.POST.get('nolpj', None)
        tgl_spp = tgl_short(request.POST.get('tgl', None)) 
        jenis = jenis.upper() 
        hidden = 'hidden'               

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.') 
                    
        if jenis=='GU' or jenis=='GU_NIHIL':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT cek,otorisasi,koderekening,uraian,"
                    "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                    "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                    "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                    "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                    "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah,"
                    "(CASE WHEN sisa is NULL THEN 0.00 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
                    " FROM penatausahaan.fc_view_spj_upgutu_to_spp(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s) ",
                    [tahun_log(request),aidi[0], aidi[1], aidi[2],no_lpj,tgl_spp,jenis])
                list_spp = dictfetchall(cursor)                   
            
        data = {'list_spp' : list_spp, 'hidden':hidden}
        return render(request, 'spp/tabel/tabel_spp_afektasi.html', data)

    else:
        return redirect('sipkd:index')

def ambilspp(request,jenis):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd') 
        nospp = request.POST.get('nospp') 
        jenis = jenis.upper()

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
       
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM PENATAUSAHAAN.SPP where tahun = %s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') and kodeunit=%s  and NOSPP=%s",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3], nospp])
            list_spp = dictfetchall(cursor)        

        data = {}
        for arr in list_spp:
            if arr['npwp'] == '-' or arr['npwp'] == '':
                npwp = '00.000.000.0-000.000'
            else:
                npwp = arr['npwp']

            if jenis=='LS':
                data = {'tahun':arr['tahun'], 'kodeurusan':arr['kodeurusan'], 'kodesuburusan':arr['kodesuburusan'], 
                    'kodeorganisasi':arr['kodeorganisasi'], 'nospp':arr['nospp'], 'tglspp':tgl_indo(arr['tglspp']),
                    'bendaharapengeluaran':arr['bendaharapengeluaran'], 'norekeningbendahara':arr['norekeningbendahara'],
                    'npwp':npwp, 'namabank':arr['namabank'], 'triwulan':arr['triwulan'], 'perubahan':arr['perubahan'],  
                    'deskripsispp':arr['deskripsispp'], 'locked':arr['locked'],'nospj':arr['nospj'],
                    'namaperusahaan':arr['namaperusahaan'],'alamatperusahaan':arr['alamatperusahaan'],
                    'namapimpinanperusahaan':arr['namapimpinanperusahaan'],'norekperusahaan':arr['norekperusahaan'],
                    'nokontrak':arr['nokontrak'],'kegiatanlanjutan':arr['kegiatanlanjutan'],
                    'deskripsipekerjaan':arr['deskripsipekerjaan'],'deskripsispp':arr['deskripsispp'],
                    'waktupelaksanaan':arr['waktupelaksanaan'],'jenisdpa':arr['jenisdpa'],'tgldpa':tgl_indo(arr['tgldpa']),
                    'bentuk_perusahaan':arr['bentukperusahaan'],'nama_rekening_bank':arr['namarekeningbank'],
                    'pesan':'SPP Telah Disetujui Anda Tidak Diperkenankan Mengganti'}
            else:
                data = {'tahun':arr['tahun'], 'kodeurusan':arr['kodeurusan'], 'kodesuburusan':arr['kodesuburusan'], 
                    'kodeorganisasi':arr['kodeorganisasi'], 'nospp':arr['nospp'], 'tglspp':tgl_indo(arr['tglspp']),
                    'bendaharapengeluaran':arr['bendaharapengeluaran'], 'norekeningbendahara':arr['norekeningbendahara'],
                    'npwp':npwp, 'namabank':arr['namabank'], 'triwulan':arr['triwulan'], 'perubahan':arr['perubahan'],  
                    'deskripsispp':arr['deskripsispp'], 'locked':arr['locked'],'nospj':arr['nospj'],
                    'namaperusahaan':arr['namaperusahaan'],'alamatperusahaan':arr['alamatperusahaan'],
                    'namapimpinanperusahaan':arr['namapimpinanperusahaan'],'norekperusahaan':arr['norekperusahaan'],
                    'nokontrak':arr['nokontrak'],'kegiatanlanjutan':arr['kegiatanlanjutan'],
                    'deskripsipekerjaan':arr['deskripsipekerjaan'],'deskripsispp':arr['deskripsispp'],
                    'bentuk_perusahaan':arr['bentukperusahaan'],'nama_rekening_bank':arr['namarekeningbank'],
                    'pesan':'SPP Telah Disetujui Anda Tidak Diperkenankan Mengganti'}
        return JsonResponse(data)
        

    else:
        return redirect('sipkd:index')

def ceknomerspp(request):
    if 'sipkd_username' in request.session:
        gets = request.POST.get('skpd') 
        nospp = request.POST.get('spp') 

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT count(nospp) as nospp FROM penatausahaan.spp WHERE TAHUN=%s and UPPER(NOSPP)=%s "
                "and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') and kodeunit=%s",
                [tahun_log(request),nospp.upper(),aidi[0], aidi[1], aidi[2],org[3]])
            cek_spp = dictfetchall(cursor)

        data = {}
        for arr in cek_spp:
            data = {'nospp':arr['nospp']}

        return JsonResponse(data)
    else:
        return redirect('sipkd:index')

def ambilspd(request):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None)         
        tgl_spp = tgl_to_db_original(request.POST.get('tgl', None))
        isppkd = request.POST.get('isppkd', None)
        # print(gets)

        tgl = tgl_spp.split('/')          

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')

        if isppkd=='1':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT nospd,to_char(tglspd,'dd/mm/yyyy') as tglspd,sum(jumlahspd) as jumlahspd "
                    "FROM penatausahaan.fc_view_spd(%s,%s,%s,lpad(%s,2,'0'),%s) where KODEPROGRAM=0 and KODEKEGIATAN=0 "
                    "and isskpd=1 and xkodekegiatan is null group by nospd,tglspd",
                    [tahun_log(request),aidi[0],aidi[1],aidi[2],int(tgl[1])])
                list_spd = dictfetchall(cursor) 
        else:
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT distinct(nospd),to_char(tglspd,'dd/mm/yyyy') as tglspd,jumlahspd,tglspd as urut "
                    "FROM penatausahaan.fc_view_spd(%s,%s,%s,lpad(%s,2,'0'),%s) where KODEPROGRAM=0 and KODEKEGIATAN=0 "
                    "and isskpd=0 and xkodekegiatan is not null  order by urut",
                    [tahun_log(request),aidi[0],aidi[1],aidi[2],int(tgl[1])])
                list_spd = dictfetchall(cursor)

        data = {'list_spd' : list_spd}
        return render(request, 'spp/tabel/tabel_spd.html', data)

    else:
        return redirect('sipkd:index')

def simpanspp(request,jenis):
    hasil = ''
    if 'sipkd_username' in request.session:
        if request.method == 'POST':
            jenis = jenis.upper()
            org = request.POST.get('organisasi').split('.')
            no_spp = request.POST.get('no_spp')
            no_spp_lama = request.POST.get('no_spp_lama')
            tanggal_spp = tgl_short(request.POST.get('tanggal_spp'))
            bendahara = request.POST.get('bendahara')
            norek_bendahara = request.POST.get('norek_bendahara')
            nama_bank = request.POST.get('nama_bank')
            npwp_bendahara = request.POST.get('npwp_bendahara')
            status_keperluan = request.POST.get('status_keperluan')            
            aksi = request.POST.get('aksi')
            nm_pemilik_rekening = request.POST.get('nama_rekening_bank')
            if jenis=='TU':
                total = request.POST.get('totalspp') 
            else:
                total = request.POST.get('total_spp')
                        
            triwulan = request.POST.get('st_triwulan')
            perubahan = request.POST.get('st_perubahan')
            rincian = request.POST.getlist('afektasispp')
            tanggal = request.POST.get('tanggal_spp').split(' ')
            tw = int(arrMonth[tanggal[1]])
            nospj = ''
            jenisdpa = '' 
            tgldpa = 'NOW()' 
            nomordpa = ''
            namaperusahaan = ''
            bentukperusahaan = ''
            alamatperusahaan = ''
            pimpinan = ''
            npwp = ''
            bankperusahaan = ''
            rekperusahaan = ''
            nomerkontrak = ''
            pelaksanaan = ''

            if jenis=='GU' or jenis=='GU_NIHIL' or jenis=='TU_NIHIL':
                nospj = request.POST.get('no_lpj') 
            if jenis=='LS':
                jenisdpa = request.POST.get('jenis_dpa')
                tgldpa = tgl_short(request.POST.get('tanggal_dpa'))
                nomordpa = request.POST.get('nomor_dpa')
                namaperusahaan = request.POST.get('nama_perusahaan')
                bentukperusahaan = request.POST.get('bentuk_perusahaan')
                alamatperusahaan = request.POST.get('alamat_perusahaan')
                pimpinan = request.POST.get('pimp_perusahaan')
                npwp_bendahara = request.POST.get('npwp_perusahaan')                
                rekperusahaan = request.POST.get('norek_perusahaan')
                nomerkontrak = request.POST.get('nomor_kontrak')
                pelaksanaan = request.POST.get('pelaksanaan')
                nama_bank = request.POST.get('bank_perusahaan')
                

            if jenis=='NON_ANGG':
                jenis = 'NON ANGG'
                if tw <= 3:
                    triwulan = 1
                elif tw <= 6:
                    triwulan = 2
                elif tw <= 9:
                    triwulan = 3
                else:
                    triwulan = 4  

            if no_spp != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO PENATAUSAHAAN.SPP (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,TGLSPP,TGLSPP_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"\
                            " DESKRIPSISPP,NOSPD,TGLSPD,SISADANASPD,JMLSPD,JUMLAHSPP,BENDAHARAPENGELUARAN,NOREKENINGBENDAHARA,JENISSPP,jenisdpa,tgldpa,nodpa,namabank,"\
                            " namaperusahaan,bentukperusahaan,alamatperusahaan,namapimpinanperusahaan,norekperusahaan,nokontrak,"\
                            " npwp,deskripsipekerjaan,triwulan,perubahan,nospj,waktupelaksanaan,namarekeningbank,uname )"\
                            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper(),tanggal_spp,tanggal_spp,'',0,0,status_keperluan,'','NOW()',0,0,total,
                            bendahara,norek_bendahara,jenis,jenisdpa,tgldpa,nomordpa,nama_bank,namaperusahaan,bentukperusahaan,alamatperusahaan,
                            pimpinan,rekperusahaan,nomerkontrak,npwp_bendahara,status_keperluan,
                            triwulan,perubahan,nospj,pelaksanaan,nm_pemilik_rekening,username(request)])
                        hasil = ""                    
                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE PENATAUSAHAAN.SPP SET NOSPP=%s, TGLSPP=%s, TGLSPP_DRAFT=%s, DESKRIPSISPP=%s,"
                            "JUMLAHSPP=%s, BENDAHARAPENGELUARAN=%s, NOREKENINGBENDAHARA=%s, namarekeningbank=%s, jenisdpa=%s, tgldpa=%s, nodpa=%s,"
                            "namabank=%s, namaperusahaan=%s, bentukperusahaan=%s, alamatperusahaan=%s, namapimpinanperusahaan=%s,"
                            "norekperusahaan=%s, nokontrak=%s, npwp=%s, deskripsipekerjaan=%s,"
                            "PERUBAHAN=%s, TRIWULAN=%s, NOSPJ=%s, waktupelaksanaan=%s "
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s and NOSPP=%s",
                            [no_spp.upper(),tanggal_spp,tanggal_spp,status_keperluan,total,bendahara,norek_bendahara,nm_pemilik_rekening,jenisdpa,tgldpa,nomordpa,
                            nama_bank,namaperusahaan,bentukperusahaan,alamatperusahaan,pimpinan,rekperusahaan,nomerkontrak, npwp_bendahara, status_keperluan,
                            perubahan,triwulan,nospj,pelaksanaan,tahun_log(request),org[0],org[1],org[2],org[3],no_spp_lama.upper()])
                        hasil = ""

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.SPPRINCIAN WHERE tahun=%s and KODEURUSAN=%s "
                        "and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s  and NOSPP=%s",
                        [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper()])
                
                for i in range(0,len(rincian)):
                    obj = rincian[i].split("|")
                    if len(obj[0].split('.')) != 5:
                        obj1 = obj[0].split("-") #rekening
                        obj2 = toAngkaDec(obj[1]) #jumlah
                        objek1 = obj1[0].split(".") #kodeorganisasi bidang
                        objek2 = obj1[1].split(".") #koderekening

                        if obj2!='0.00':
                            with connections[tahun_log(request)].cursor() as cursor:
                                 cursor.execute("INSERT INTO PENATAUSAHAAN.SPPRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,"
                                    "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                                    "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,KODESUB1,KODESUB2,KODESUB3,TANGGAL,JUMLAH)"
                                    " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper(),objek1[0]+"."+objek1[1],objek1[2],objek1[3]+"."+objek1[4],objek1[5],0,
                                    objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],objek2[5],0,0,0,tanggal_spp,obj2])                                     
                            hasil = "Data berhasil disimpan!"
                            # print("INSERT INTO PENATAUSAHAAN.SPPRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPP,"
                            #         "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            #         "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,KODESUB1,KODESUB2,KODESUB3,TANGGAL,JUMLAH)"
                            #         " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            #         [tahun_log(request),org[0],org[1],org[2],org[3],no_spp.upper(),objek1[0]+"."+objek1[1],objek1[2],objek1[3]+"."+objek1[4],objek1[5],0,
                            #         objek2[0],objek2[1],objek2[2],objek2[3],objek2[4],objek2[5],0,0,0,tanggal_spp,obj2])                                     
                                                      

            return HttpResponse(hasil)

    else:
        return redirect('sipkd:index')


def loadlaporanspp(request,jenis):
    gets = str(request.GET.get('skpd'))
    jenis = jenis.upper()
    if jenis=='NON_ANGG':
        jenis = 'NON ANGG'
    
    if gets != '0':
        aidi = gets.split('.')
    else:
        skpd = '0.0.0.0'
        aidi = skpd.split('.')   

    # ambil dasar hukum
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("select * from master.master_dasarhukum where tahun=%s"
            " and kodeurusan=0 and kodesuburusan=0 order by nourut",
            [tahun_log(request)])
        dasarhukum = dictfetchall(cursor)

    # ambil pejabat otorisasi
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1  from master.pejabat_skpd where tahun=%s "
            " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and upper(jabatan) not like %s and jenissistem=%s ",
            [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%BENDAHARA%',2])
        otorisasi = dictfetchall(cursor)

    # ambil bendahara
    if jenis=='LS_PPKD' or jenis=='NON ANGG':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select * from master.pejabat_skpd where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0')and kodeunit=%s and upper(jabatan) like %s and jenissistem=%s ",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%PPKD%',2])
            bendahara = dictfetchall(cursor)
    else:
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan from master.pejabat_skpd where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s  and upper(jabatan) like %s and jenissistem=%s ",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%BENDAHARA PENGELUARAN%',2])
            bendahara = dictfetchall(cursor)

    # ambil pptk
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1  from master.pejabat_skpd where tahun=%s "
            " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and jenissistem=%s ",
            [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],2])
        pptk = dictfetchall(cursor)

    # ambil peneliti
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT * FROM master.pejabat_skpd where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') "
            " and kodeunit=%s and jenissistem=%s",
            [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],2])
        peneliti = dictfetchall(cursor)
    
    dasar_hukum = []
    for arr in dasarhukum:
        dasar_hukum.append({'nourut':arr['nourut'],'nomordasarhukum':arr['nomordasarhukum'],
            'dasarhukum':arr['dasarhukum'],'tanggal':tgl_indo(arr['tanggal'])})

    jenisspp = ['LS_PPKD','UP','GU','GU_NIHIL','TU','GJ','LS','NON ANGG']  

    hidden_otorisasi = ''
    hidden_peneliti = ''
    hidden_pptk = ''
    if jenis=='LS_PPKD' or jenis=='NON ANGG':
        hidden_otorisasi = 'hidden'
        hidden_peneliti = 'hidden' 
        hidden_pptk = 'hidden'
    elif jenis=='UP' or jenis=='GU' or jenis=='TU' or jenis=='GU_NIHIL':
        hidden_otorisasi = '' 
        hidden_peneliti = ''
        hidden_pptk = 'hidden'
    elif jenis=='GJ':
        hidden_otorisasi = 'hidden'
        hidden_peneliti = ''
        hidden_pptk = 'hidden'
    elif jenis=='LS':
        hidden_otorisasi = 'hidden' 
        hidden_peneliti = ''
        hidden_pptk = '' 

    data = {
        'dasarhukum' : dasar_hukum,
        'bendahara' : bendahara,
        'otorisasi' : otorisasi,
        'peneliti' : peneliti,
        'pptk' : pptk,
        'jenisspp' : jenisspp,
        'jenis' : jenis,
        'hidden_otorisasi' : hidden_otorisasi,
        'hidden_peneliti' : hidden_peneliti,
        'hidden_pptk' : hidden_pptk
    }
    return render(request,'spp/modal/modal_laporan.html',data)

def cetaklaporanspp(request,jenis):
    post    = request.POST
    lapParm = {}
    where0  = ""
    where1  = ""
    jenis = jenis.upper()       
    
    organisasi  = post.get('org').split('.')
    tanggal_spp = tgl_to_db_original(post.get('tgl_spp')).split('/')
    bulan = tanggal_spp[1]        

    if jenis=='LS_PPKD':
        lapParm['file']         = 'penatausahaan/spp/spp_ls_ppkd.fr3'
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"  
    elif jenis=='UP':
        lapParm['file']         = 'penatausahaan/spp/spp_up.fr3' 
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"
        lapParm['idpa']         = "'"+post.get('id_otorisasi')+"'" 
        lapParm['idpeneliti']   = "'"+post.get('id_peneliti')+"'"
    elif jenis=='GU' or jenis=='GU_NIHIL':
        lapParm['file']         = 'penatausahaan/spp/spp_gu.fr3' 
        lapParm['kodekegiatan'] = post.get('kodekegiatan')
        lapParm['noLPJ']        = "'"+post.get('nomer_lpj')+"'"
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"
        lapParm['idpa']         = "'"+post.get('id_otorisasi')+"'" 
        lapParm['idpeneliti']   = "'"+post.get('id_peneliti')+"'"
    elif jenis=='TU':
        lapParm['file']         = 'penatausahaan/spp/spp_tu.fr3' 
        lapParm['kodekegiatan'] = post.get('kodekegiatan')        
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"
        lapParm['idpa']         = "'"+post.get('id_otorisasi')+"'" 
        lapParm['idpeneliti']   = "'"+post.get('id_peneliti')+"'"
    elif jenis=='GJ':
        lapParm['file']         = 'penatausahaan/spp/spp_ls_gj.fr3' 
        lapParm['kodekegiatan'] = ''        
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"        
        lapParm['idpeneliti']   = "'"+post.get('id_peneliti')+"'"
    elif jenis=='NON ANGG':
        lapParm['file']         = 'penatausahaan/spp/SPP_LS_NON_ANGG.fr3' 
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"     
    elif jenis=='LS':
        lapParm['file']         = 'penatausahaan/spp/spp_ls_barjas.fr3' 
        lapParm['id']           = "'"+post.get('id_mengajukan')+"'"
        lapParm['idpptk']         = "'"+post.get('id_pptk')+"'" 
        lapParm['idpeneliti']   = "'"+post.get('id_peneliti')+"'"   
        
    nomer_spp = post.get('nomer_spp')
    lapParm['tahun']            = "'"+tahun_log(request)+"'"  
    lapParm['NOSPP']            = "'"+nomer_spp.upper()+"'"  
    lapParm['report_type']      = 'pdf'
    lapParm['kodeurusan']       = organisasi[0]
    lapParm['kodesuburusan']    = organisasi[1]
    lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"
    lapParm['kodeunit']   = "'"+organisasi[3]+"'"
    lapParm['idperda']          = "'"+post.get('id_perda')+"'" 
    lapParm['bulan']            = int(bulan)    
    lapParm['nospd']            = "" 
    lapParm['where']            = where0
    lapParm['where1']           = where1


    return HttpResponse(laplink(request, lapParm))

def listdataspj(request,jenis):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd')
        jenis = jenis.upper() 
        path = ''  

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')                        
        
        if jenis=='GU':
            path = 'tabel_lpjupgu.html'
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT * ,0 as cek, to_char( tglspj, 'dd/mm/yyyy') as tanggal, "
                    "(CASE WHEN jumlahspj is NULL THEN 0.00 ELSE jumlahspj END) as jumlahspj " 
                    "FROM penatausahaan.fc_skpd_view_spj(%s,%s,%s,lpad(%s,2,'0')) WHERE jenis=%s ",
                    [tahun_log(request),aidi[0],aidi[1],aidi[2],'GU'])
                list_lpj = dictfetchall(cursor)
        elif jenis=='TU':        
            path = 'tabel_lpjtu.html'
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT * ,0 as cek, to_char( tglspj, 'dd/mm/yyyy') as tanggal, "
                    "(CASE WHEN jumlahsp2d is NULL THEN 0.00 ELSE jumlahsp2d END) as jumlahsp2d, "
                    "(CASE WHEN jumlahsetor is NULL THEN 0.00 ELSE jumlahsetor END) as jumlahsetor, "
                    "(CASE WHEN sisasp2d is NULL THEN 0.00 ELSE sisasp2d END) as sisasp2d "
                    "FROM penatausahaan.fc_skpd_view_spj(%s,%s,%s,lpad(%s,2,'0')) WHERE jenis=%s ",
                    [tahun_log(request),aidi[0],aidi[1],aidi[2],'TU'])
                list_lpj = dictfetchall(cursor) 
        else:
            path = 'tabel_pengembalian.html'  
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT *, tglsts as tanggal, " 
                    "(CASE WHEN jumlah is NULL THEN 0.00 ELSE jumlah END) as jumlah " 
                    "FROM pertanggungjawaban.view_daftar_pengembalian(%s,%s,%s,lpad(%s,2,'0')) ",
                    [tahun_log(request),aidi[0],aidi[1],aidi[2]])
                list_lpj = dictfetchall(cursor)

        data = {'list_lpj' : list_lpj}
        return render(request, 'spp/tabel/'+path+'', data)

    else:
        return redirect('sipkd:index')

def laporanspp(request,jenis):
    if 'sipkd_username' in request.session:
        gets = str(request.POST.get('skpd'))        
        jenis = jenis.upper()
        if gets == '0':
            isi_pengguna = '<option value="x|0|0|0">-- Pilih Pengguna Anggaran --</option>'
            isi_bendahara = '<option value="x|0|0|0">-- Pilih Bendahara Pengeluaran --</option>'
        else:
            isi_pengguna = ''
            isi_bendahara = ''
        
        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')   

        # ambil pengguna
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT id,NAMA,NIP,pangkat, jabatan||' ('||nama||')' AS JABATAN  from master.pejabat_skpd  where tahun=%s"
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and upper(jabatan) like %s and jenissistem=%s",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%ANGGARAN%',2])
            pengguna = dictfetchall(cursor)
        for x in range(len(pengguna)):            
            isi_pengguna += '<option value="'+str(pengguna[x]['id'])+'|'+pengguna[x]['nama']+'|'+pengguna[x]['nip']+'|'+pengguna[x]['pangkat']+'">'+pengguna[x]['jabatan']+'</option>'
            
        # ambil bendahara
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan  from master.pejabat_skpd where tahun=%s "
                " and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=lpad(%s,2,'0') and kodeunit=%s and upper(jabatan) like %s and jenissistem=%s ",
                [tahun_log(request),aidi[0],aidi[1],aidi[2],aidi[3],'%BENDAHARA%',2])
            bendahara = dictfetchall(cursor)         
        for x in range(len(bendahara)):            
            isi_bendahara += '<option value="'+str(bendahara[x]['id'])+'|'+bendahara[x]['nama']+'|'+bendahara[x]['nip']+'|'+bendahara[x]['pangkat']+'">'+bendahara[x]['jabatan']+'</option>'       
        
        data = {
            'isi_pengguna' : isi_pengguna,
            'isi_bendahara' : isi_bendahara            
        }
    return JsonResponse(data)

def cetakregisterspp(request):
    post    = request.POST
    lapParm = {}
    where0  = ""
    where1  = "" 
    jenis   = post.get('jns_laporan') 
     
    if jenis == '1':
        lapParm['file']         = 'penatausahaan/spp/register_spp.fr3'
    else:
        lapParm['file']         = 'penatausahaan/spp/register_sppspmsp2d.fr3'
    
    organisasi  = post.get('organisasi').split('.') 
    isskpd      = post.get('is_skpkd') 


    lapParm['tahun']            = "'"+tahun_log(request)+"'"        
    lapParm['report_type']      = 'pdf'
    lapParm['kodeurusan']       = organisasi[0]
    lapParm['kodesuburusan']    = organisasi[1]
    lapParm['kodeorganisasi']   = "'"+organisasi[2]+"'"   
    lapParm['tglawal']          = "'"+tgl_short(post.get('periode_tgl1'))+"'"   
    lapParm['tglakhir']         = "'"+tgl_short(post.get('periode_tgl2'))+"'"   
    lapParm['tglcetak']         = post.get('tanggal_cetak')  
    lapParm['ISPPKD']           = isskpd
    lapParm['id']               = "'"+post.get('bendahara')+"'"
    lapParm['idpa']             = "'"+post.get('pengguna')+"'"
    lapParm['where']            = where0
    lapParm['where1']           = where1

    return HttpResponse(laplink(request, lapParm))

def getkegiatan(request):
    if 'sipkd_username' in request.session:

        gets = request.POST.get('skpd', None) 
        no_spp = request.POST.get('nospp', None)
        tgl_spp = tgl_short(request.POST.get('tglspp', None))          
        
        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')               
            
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT kodebidang,kodeprogram,kodekegiatan,cek,otorisasi,koderekening,uraian,"
                "(CASE WHEN anggaran is NULL THEN 0 ELSE anggaran END) as anggaran,"
                "(CASE WHEN batas is NULL THEN 0 ELSE batas END) as batas,"
                "(CASE WHEN lalu is NULL THEN 0 ELSE lalu END) as lalu,"
                "(CASE WHEN sekarang is NULL THEN 0 ELSE sekarang END) as sekarang,"
                "(CASE WHEN jumlah is NULL THEN 0 ELSE jumlah END) as jumlah,"
                "(CASE WHEN sisa is NULL THEN 0 ELSE sisa END) as sisa,ROW_NUMBER () OVER () as nomor "
                " FROM penatausahaan.fc_view_spp_tu_kegiatan(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) ",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],no_spp.upper(),'',0,0,tgl_spp,'TU'])
            list_spp = dictfetchall(cursor)        
            
        kodekegiatan = ''
        for x in range(len(list_spp)):
            if (list_spp[x]['cek']==1):
                if(list_spp[x]['uraian']!=None):
                    objek = list_spp[x]['koderekening']
                    objek1 = objek.split('-') 
                    koderekening = objek1[0].split('.')
                    kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"

        kodekegiatan = "("+kodekegiatan[1:len(kodekegiatan)]+")"
            
        data = {'list_spp' : list_spp,'kodekegiatan':kodekegiatan}
        return render(request, 'spp/tabel/tabel_spp_kegiatan.html', data)

    else:
        return redirect('sipkd:index')

def getbelanja(request):
    if 'sipkd_username' in request.session:        

        gets = request.POST.get('organisasi') 
        no_spp = request.POST.get('no_spp')
        tgl_spp = tgl_short(request.POST.get('tanggal_spp'))
        kegiatan = request.POST.getlist('spptukdrek')
        

        if gets != '0':
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')               
            
        kodekegiatan = ''
        for i in range(0,len(kegiatan)):
            cek = "'"+kegiatan[i]+"'"
            kodekegiatan += ','+cek       
        
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT kodeakun,kodebidang,kodeprogram,kodekegiatan,cek,otorisasi,koderekening,uraian,"
                "(CASE WHEN anggaran is NULL THEN 0.00 ELSE anggaran END) as anggaran,"
                "(CASE WHEN batas is NULL THEN 0.00 ELSE batas END) as batas,"
                "(CASE WHEN lalu is NULL THEN 0.00 ELSE lalu END) as lalu,"
                "(CASE WHEN sekarang is NULL THEN 0.00 ELSE sekarang END) as sekarang,"
                "(CASE WHEN (lalu+sekarang) is NULL THEN 0.00 ELSE (lalu+sekarang) END) as jumlah,"
                "(CASE WHEN (anggaran-sekarang-lalu) is NULL THEN 0.00 ELSE (anggaran-sekarang-lalu) END) as sisa,ROW_NUMBER () OVER () as nomor "
                " FROM penatausahaan.fc_view_spp_rincian(%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s) "
                "WHERE kodebidang||'.'||lpad(%s,2,'0')||'.'||kodeprogram||'.'||kodekegiatan in ("+kodekegiatan[1:]+")",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],no_spp.upper(),'',0,0,tgl_spp,'TU',aidi[2]])
            list_spp = dictfetchall(cursor) 

            kodekegiatan = ''
            for x in range(len(list_spp)):
                if (list_spp[x]['cek']==1):
                    if(list_spp[x]['uraian']!=None):
                        objek = list_spp[x]['koderekening']
                        objek1 = objek.split('-') 
                        koderekening = objek1[0].split('.')
                        kodekegiatan = kodekegiatan+",'"+koderekening[0]+"."+koderekening[1]+"."+koderekening[3]+"."+koderekening[4]+"'"

            kodekegiatan = "("+kodekegiatan[1:len(kodekegiatan)]+")"            
            
        data = {'list_spp' : list_spp, 'kodekegiatan':kodekegiatan}
        return render(request, 'spp/tabel/tabel_spp_belanja.html', data)

    else:
        return redirect('sipkd:index')

def sumspptu(request):
    if 'sipkd_username' in request.session:
        post    = request.POST
        sppsekarang = post.get('sekarang',0)
        batasspp = post.get('batas',0)
        spplalu = post.get('lalu',0)
        sppangg = post.get('anggaran',0)
        totalangg = post.get('totangg',0)
        totallalu = post.get('totlal',0)
        totaljumlah = post.get('totjml',0)
        totalsisa = post.get('totsis',0)
        rekening = post.get('rekening','')
        pesan = ''
        sekarang = 0
        sppjumlah = 0
        
        if sppsekarang != '0':
            # print(float(spplalu))
            jumlah = float(sppsekarang) + float(spplalu)            
            if jumlah > float(batasspp) :
                sekarang = float(batasspp) - float(spplalu)
                sppjumlah = float(spplalu) + sekarang
                pesan = 'Rekening '+rekening+' melebihi batas. Batas SPP sebesar Rp.'+sekarang+'. Harap Ubah Anggaran Kas dan Perbaiki SPD di Bidang Anggaran!' 
            else:
                sekarang = float(sppsekarang)
                sppjumlah = float(spplalu) + float(sppsekarang)

            sisaangg = float(sppangg) - sppjumlah
        else:
            sppsekarang = 0
            sppjumlah = float(spplalu)
            sisaangg =  float(sppangg) - sppjumlah           

        data = {'sppsekarang' : sppsekarang, 'sppjumlah' : sppjumlah,
            'sisaanggaran': sisaangg, 'pesan':pesan}
        return JsonResponse(data)

    else:
        return redirect('sipkd:index')

def hitungsisatu(request):
    if 'sipkd_username' in request.session:
        post    = request.POST
        arrjml = post.getlist('arrjml',0)
        arrsis = post.get('arrsis',0)
        arrsek = post.get('arrsek',0)
        total = 0        

        for i in range(0,len(arrjml)):
            total += arrjml[i] 

            print(total)

        data = {'list':arrjml}
        return JsonResponse(data)

    else:
        return redirect('sipkd:index')
