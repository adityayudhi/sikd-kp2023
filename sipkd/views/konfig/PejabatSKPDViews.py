from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

import json



def pejabatskpd(request):
    skpd = set_organisasi(request)
    if skpd["kode"] == '': kode = 0
    else: kode = skpd["kode"]

    data = {'organisasi':skpd["skpd"],'kd_org':kode, 'ur_org':skpd["urai"]}
    return render(request, 'konfig/pejabatskpd.html', data)

# tambah pejabat skpd
def addpejabatskpd(request):
    action = request.GET.get('act')
    idpejabat = request.GET.get('id')
    organisasi = request.GET.get('org')    
    tahun = tahun_log(request)
    namapejabat = nip = pangkat = jabatan = norek = namarekeningbank = bank = npwp =''
    
    # master jabatan
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT urai from master.MASTERJABATAN where isskpd=0 and jenissistem=2 order by urut")
        master_jabatan = dictfetchall(cursor)

    # kode pejabat skpd
    if action == 'add':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT case when max(id)+1 is null then 0 else max(id)+1 end  as id from master.PEJABAT_SKPD where tahun=%s and jenissistem=2 and "\
                "kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s",[tahun,organisasi])
            max_pejabat = dictfetchall(cursor)
            for result in max_pejabat:
                idpejabat = result['id']

    if action == 'edit' :
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * from master.PEJABAT_SKPD where tahun= %s and jenissistem=2 and id=%s and "\
                "kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s", [tahun,idpejabat,organisasi])
            hasil = dictfetchall(cursor)
            for result in hasil:
                idpejabat = result['id']
                namapejabat = result['nama']
                nip = result['nip']
                pangkat = result['pangkat']
                jabatan = result['jabatan']
                norek = result['norekbank']
                namarekeningbank = result['namarekeningbank']
                bank = result['namabank']
                npwp = result['npwp']
                nik = result['nik']

    data = {
        'idpejabat': idpejabat, 
        'master_jabatan':master_jabatan,
        'action' : action,
        'namapejabat' : namapejabat,
        'nip' : nip,
        'pangkat' : pangkat,
        'jabatan' : jabatan,
        'organisasi' : organisasi,
        'norek':norek,
        'namarekeningbank':namarekeningbank,
        'bank':bank,
        'npwp':npwp,
        'nik':nik,
    } 
    return render(request, 'konfig/modal/addpejabatskpd.html', data)

def load_bank_pejabat(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def getpejabatskpd(request):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)   

        if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute(
                "select ROW_NUMBER () OVER (ORDER BY id) as no, "
                "kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit as organisasi,"
                "* from master.pejabat_skpd where tahun = %s and kodeurusan = %s  and kodesuburusan = %s "
                "and kodeorganisasi = lpad(%s,2,'0') and kodeunit = %s and jenissistem = 2 order by id",
                [tahun_log(request),aidi[0], aidi[1], aidi[2], aidi[3]])
            list_skpd = dictfetchall(cursor)

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select urai from master.masterjabatan where isskpd = 0 and jenissistem = 2 order by urut")
            ms_jbtn = dictfetchall(cursor)

        data = {'list_skpd': list_skpd, 'ms_jbtn': ms_jbtn}

        return render(request, 'konfig/list_pejabatskpd.html', data)

    else:
        return redirect('sipkd:index')


def combopejabatskpd(request):
    if 'sipkd_username' in request.session:

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("select urai from master.masterjabatan where isskpd = 0 and jenissistem = 2 order by urut")
            ms_jbtn = dictfetchall(cursor)

        aidi = request.GET.get('id', None)
        telo = ""
        for dt in ms_jbtn:
            telo += "<option value='" + dt['urai'] + "'>" + dt['urai'] + "</option>"

 
        combo = "<select class='dropdown-in-table' id='jabatan_" + aidi + "' name='jabatan'>"\
           "<option value='0'>-- Silahkan Pilih --</option>" + telo + "</select>"

        return HttpResponse(combo)
  
    else:
        return redirect('sipkd:index')


def savepejabatskpd(request):
    hasil = ''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            org = request.POST.get('organisasi', None).split('.')
            aidi = request.POST.get('idpejabat')
            nama = request.POST.get('namapejabat')
            nip = request.POST.get('nip')
            nik = request.POST.get('nik')
            pang = request.POST.get('pangkat')
            jabt = request.POST.get('jabatan')
            action = request.POST.get('action')

            no_rek_bank     = request.POST.get('norek')
            nama_rek_bank   = request.POST.get('nama_rekening_bank')
            nama_bank       = request.POST.get('nama_bank')
            npwp            = request.POST.get('npwp')

            if nama != "":
                print(action)
                if action == 'add':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO MASTER.PEJABAT_SKPD (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,ID,"\
                            " NAMA,PANGKAT,JABATAN,NIP,NOREKBANK,NAMABANK,NPWP,jenissistem,namarekeningbank,nik)"\
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request), org[0], org[1], org[2],org[3], aidi, nama, pang, jabt, nip, no_rek_bank, nama_bank,npwp, '2', nama_rek_bank, nik])
                    hasil = "Data berhasil disimpan!"
                elif action == 'edit':
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE MASTER.PEJABAT_SKPD set NAMA=%s, NIP=%s, PANGKAT=%s, JABATAN=%s, NOREKBANK=%s,NAMABANK=%s,NPWP=%s,namarekeningbank=%s ,nik=%s"\
                            " where tahun=%s and kodeurusan=%s and kodesuburusan=%s and lpad(kodeorganisasi,2,'0')=%s "\
                            " and kodeunit=%s and id=%s and jenissistem=%s",[nama, nip, pang, jabt, no_rek_bank, nama_bank,npwp,nama_rek_bank, nik, tahun_log(request), org[0], org[1], org[2],org[3], aidi, '2'])
                    hasil = "Data berhasil diubah!"
            # messages.success(request, "Data berhasil disimpan!")
            return HttpResponse(hasil)

    else:
        return redirect('sipkd:index')

# hapus pejabatskpd
def deletepejabatskpd(request):
    # get id
    aidi = request.POST.get('id')
    organisasi = request.POST.get('org')
    tahun = tahun_log(request)
    hasil = ''

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM MASTER.PEJABAT_SKPD where tahun=%s and id=%s and"\
            " kodeurusan||'.'||kodesuburusan||'.'||lpad(kodeorganisasi,2,'0')||'.'||kodeunit=%s",
            [tahun,aidi,organisasi])
    hasil = "Data berhasil dihapus!"
    return HttpResponse(hasil)
    
