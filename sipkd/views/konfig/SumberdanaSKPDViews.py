from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

import json


def sumberdanaskpd(request):
    # rekening sumberdana  
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT * FROM penatausahaan.fc_view_sumber_rekening(%s) order by out_kodesumberdana ASC",[tahun_log(request)])
        smbr_rek = dictfetchall(cursor)

    # sumber dana
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT kodesumberdana, urai from penatausahaan.sumberdanarekening ORDER BY kodesumberdana ASC")
        smbr_dana = dictfetchall(cursor)       

    data = {'smbr_rek': smbr_rek, 'smbr_dana': smbr_dana}
    return render(request, 'konfig/sumberdana.html', data)

def addsumberdanaskpd(request):
    action = request.GET.get('act')
    urut = request.GET.get('id')
    kodesumberdana = urai = rekening = bank_asal = bank =''
    maxdana = []
   	 # master sumberdana
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT kodesumberdana, urai from penatausahaan.sumberdanarekening ORDER BY kodesumberdana")
        master_dana = dictfetchall(cursor)           

    if action == 'add' :
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT max(urut)+1 as urut FROM penatausahaan.sumberdanarekening")
            masxdana = dictfetchall(cursor)
            for result in masxdana:
                urut = result['urut']

    if action == 'edit' :
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * from penatausahaan.sumberdanarekening where urut=%s", [urut])
            hasil = dictfetchall(cursor)
            for result in hasil:
                kodesumberdana = result['kodesumberdana']
                urai = result['urai']
                rekening = result['rekening']
                urut = result['urut']
                bank_asal = result['bank_asal']
                bank = result['bank']             

    data = {
    	'master_dana' : master_dana,
        'action' : action,
        'urut': urut,
        'kodesumberdana': kodesumberdana,         
        'urai' : urai,
        'rekening' : rekening,
        'bank_asal' : bank_asal,           
        'bank' : bank
    }
    return render(request, 'konfig/modal/sumberdana.html', data)

def savesumberdanaskpd(request):
    # post method
    if request.method == 'POST':    
        action = request.POST.get('action') 
        sumberdana = request.POST.get('sumberdana', None).split(' - ')
        urut = request.POST.get('urut')
        rekening = request.POST.get('rekening')
        bank_asal = request.POST.get('bank_asal')
        bank = request.POST.get('bank')
        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("INSERT INTO penatausahaan.sumberdanarekening (kodesumberdana,urai,rekening,urut,bank_asal,bank)"\
                    "VALUES (%s,%s,%s,%s,%s,%s)",[sumberdana[0], sumberdana[1], rekening, urut, bank_asal, bank])
                # notif success
            messages.success(request, "Sumberdana berhasil disimpan!")
            
        elif action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("UPDATE penatausahaan.sumberdanarekening set kodesumberdana=%s, urai=%s, rekening=%s, bank_asal=%s, bank=%s where urut=%s",
                    [sumberdana[0], sumberdana[1], rekening, bank_asal, bank, urut])
                    # notif success
            messages.success(request, "Sumberdana berhasil diubah!")
    return HttpResponseRedirect(reverse('sipkd:sumberdanaskpd'))

def sumberdanamodal(request):
    return render(request, 'konfig/modal/sumberdana.html')

def cek_rekening(request):
    tahun = tahun_log(request)
    kode = request.GET.get('kode', None)
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("select * from penatausahaan.SP2D where norekbankasal=%s and tahun=%s limit 1", [kode,tahun])
        hasil = cursor.fetchone()
    return HttpResponse(hasil)

# hapus sumberdanaskpd
def deletesumberdanaskpd(request):
    # get id
    aidi = request.POST.get('kode')
    rek = request.POST.get('rekening')
    hasil = ''
 
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM penatausahaan.sumberdanarekening where kodesumberdana=%s and rekening=%s",[aidi,rek])
    hasil = "Data berhasil dihapus!"
    return HttpResponse(hasil)
  
def load_bank_sumberdana(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def combosumberdanaskpd(request):
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
