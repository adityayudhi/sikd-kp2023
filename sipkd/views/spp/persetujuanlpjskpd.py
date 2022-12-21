from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import pprint

def persetujuanlpjskpd(request):
    skpd = set_organisasi(request)
    is_perubahan = perubahan(request)
    namabank = set_nama_bank(request)

    if skpd["kode"] == '':
        kode = 0
    else:
        kode = skpd["kode"]
    data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"],
        'is_perubahan':is_perubahan,'namabank':namabank['list_bank']}
    return render(request, 'spp/persetujuanlpjskpd.html',data)

def listpersetujuanlpj(request):
    if 'sipkd_username' in request.session:
        gets = request.POST.get('skpd', None) 
        isppkd = request.POST.get('isppkd', None)  
        

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
            cursor.execute("SELECT a.NOSPJ as nospj,a.tglspj as tglspj,\
                ROW_NUMBER() OVER (ORDER BY a.nospj) AS idspj, a.kodeunit,a.KEPERLUAN,a.nosp2d,a.jenis,0 as CEK, \
                (SELECT SUM(jumlah) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE \
                    b.tahun = a.tahun and b.kodeurusan = a.kodeurusan and b.kodesuburusan = a.kodesuburusan \
                    and b.kodeorganisasi = a.kodeorganisasi and b.kodeunit = a.kodeunit and b.nospj = a.nospj) as jumlah \
                FROM penatausahaan.spj_skpd a \
                WHERE a.tahun = %s and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s \
                and a.kodeunit = %s and a.locked='T' ",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
           
            list_spp = dictfetchall(cursor)  

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT a.NOSPJ as nospj,a.tglspj as tglspj,\
                ROW_NUMBER() OVER (ORDER BY a.nospj) AS idspj,a.kodeunit, a.KEPERLUAN,a.nosp2d,a.jenis,0 as CEK, \
                (SELECT SUM(jumlah) FROM penatausahaan.spj_skpd_rinc_sub1 b WHERE \
                    b.tahun = a.tahun and b.kodeurusan = a.kodeurusan and b.kodesuburusan = a.kodesuburusan \
                    and b.kodeorganisasi = a.kodeorganisasi and b.kodeunit = a.kodeunit and b.nospj = a.nospj) as jumlah \
                FROM penatausahaan.spj_skpd a \
                WHERE a.tahun = %s and a.kodeurusan = %s and a.kodesuburusan = %s and a.kodeorganisasi = %s \
                and a.kodeunit = %s and a.locked='Y'",
                [tahun_log(request),aidi[0], aidi[1], aidi[2],aidi[3]])
            list_setuju = dictfetchall(cursor)      

        objek = []
        for arr in list_setuju:
            total_setuju += 0 if arr['jumlah'] == None else arr['jumlah']
            objek.append({'nospj':arr['nospj'], 'jenis':arr['jenis'], 'tglspj':arr['tglspj'],
                'keperluan':arr['keperluan'],'idspj':arr['idspj'],'kodeunit':arr['kodeunit'],
                'jumlah':arr['jumlah'], 'cek':arr['cek'],'tglspj':tgl_indo(arr['tglspj'])})

        for total in list_spp:
            total_spp += 0 if total['jumlah'] == None else total['jumlah']

        if total_spp == 0:
            total_spp = '0,00'
        if total_setuju == 0:
            total_setuju = '0,00'

        data = {'list_spp' : ArrayFormater(list_spp), 'list_setuju' : ArrayFormater(objek),'total_spp' : total_spp,'total_setuju':total_setuju}
        return render(request, 'spp/list_persetujuanlpj.html', data)

    else:
        return redirect('sipkd:index')

def setuju_draftlpj(request):
    hasil = ''
    lock = request.GET.get('act')
    
    if request.method == 'POST':
        tahun = tahun_log(request)
        gets = request.POST.get('skpd', None)    
        kdunit = request.POST.get('kdunit')

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
                nospj = split_spp[1] 
        
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.spj_skpd set locked=%s where tahun=%s"
                        " and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit = %s "
                        " and nospj in (%s)",[locked,tahun,aidi[0],aidi[1],aidi[2],aidi[3],nospj])
                if(locked == "Y"):
                    hasil = "LPJ Telah di Setujui"
                else:
                    hasil = "LPJ Telah di Unlock"
    return HttpResponse(hasil)