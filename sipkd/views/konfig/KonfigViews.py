from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

import json
import datetime

def isimodal(request):
    action = request.GET.get('act')
    uname = request.GET.get('id')
    hakakses = request.GET.get('pilih', None)
    view_uname = view_password = view_hakakses = readonly = hasil = ''
    list_hakakses = [
        {'label': '-- PILIH --', 'hakakses_db': '--PILIH--'},
        # {'label': 'ADMIN', 'hakakses_db': 'ADMIN', 'selected': ''},
        {'label': 'AKUNTANSI', 'hakakses_db': 'AKUNTANSI', 'selected': ''},
        {'label': 'ADMIN ANGGARAN', 'hakakses_db': 'ADMINANGGARAN', 'selected': ''},       
        {'label': 'ANGGARAN', 'hakakses_db': 'ANGGARAN', 'selected': ''},
        {'label': 'BELANJA', 'hakakses_db': 'BELANJA', 'selected': ''},
        {'label': 'BELANJA BL', 'hakakses_db': 'BELANJABL', 'selected': ''},
        {'label': 'BELANJA BTL', 'hakakses_db': 'BELANJABTL', 'selected': ''},
        {'label': 'KABID AKUNTANSI', 'hakakses_db': 'KABIDAKUNTANSI', 'selected': ''},
        {'label': 'KABID ANGGARAN', 'hakakses_db': 'KABIDANGGARAN', 'selected': ''},
        {'label': 'KABID BELANJA', 'hakakses_db': 'KABIDBELANJA', 'selected': ''},
        {'label': 'KEPALA SKPD', 'hakakses_db': 'KEPALASKPD', 'selected': ''},
        {'label': 'PPKD', 'hakakses_db': 'PPKD', 'selected': ''},
        {'label': 'SKPD Bendahara Pengeluaran', 'hakakses_db': 'BENDAHARAKELUAR', 'selected': ''},
        {'label': 'SKPD Bendahara Penerimaan', 'hakakses_db': 'BENDAHARATERIMA', 'selected': ''},
        {'label': 'VERIFIKASI', 'hakakses_db': 'VERIFIKASI', 'selected': ''},
        {'label': 'NON AKSES', 'hakakses_db': 'NONAKSES', 'selected': ''},
        {'label': 'OPERATOR SKPD', 'hakakses_db': 'OPERATORSKPD', 'selected': ''},
        {'label': 'SKPD', 'hakakses_db': 'SKPD', 'selected': ''},
        {'label': 'BPK', 'hakakses_db': 'BPK', 'selected': ''},
        {'label': 'KASDA', 'hakakses_db': 'KASDA', 'selected': ''},
    ]

    if hakakses_sipkd(request) == 'OPERATORSKPD':
        list_hakakses = [
            {'label': '-- PILIH --', 'hakakses_db': '--PILIH--'},
            {'label': 'SKPD Bendahara Pengeluaran', 'hakakses_db': 'BENDAHARAKELUAR', 'selected': ''},
            {'label': 'SKPD Bendahara Penerimaan', 'hakakses_db': 'BENDAHARATERIMA', 'selected': ''},
        ]

    if action == 'edit':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM penatausahaan.pengguna WHERE uname = %s", [uname])
            hasil = dictfetchall(cursor)
            for hasilnya in hasil:
                view_uname = hasilnya['uname']
                view_password = decrypt(hasilnya['pwd']).upper()
                view_hakakses = hasilnya['hakakses']
        urutan = next((index for (index, d) in enumerate(list_hakakses) if d["hakakses_db"] == view_hakakses), None)
        list_hakakses[urutan]['selected'] = 'selected'
        readonly = 'readonly'

    data = {
        'act': action,
        'list_hakakses': list_hakakses,
        'jenis': 'isi_modal',
        'view_uname': view_uname,
        'view_password':view_password,
        'readonly': readonly,
    }
    return render(request, 'konfig/modal_settingPengguna.html', data)
    


def get_organisasi(request):
    tahun = tahun_log(request)
    uname = request.GET.get('input', None)
    hakakses = request.GET.get('pilih', None)
    action = request.GET.get('act', None)
    checked = view_organisasi = pisah = organisasi_list = hasil = ''
    if hakakses=='ADMIN':
        checked = 'checked'

    print(sipkd_listorganisasi(request))

    with connections[tahun_log(request)].cursor() as cursor:
        if hakakses_sipkd(request) == 'OPERATORSKPD':
            cursor.execute("SELECT *, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi2 FROM view_organisasi_user(%s,%s,%s,%s) \
                WHERE kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit = %s",
                [tahun,uname,hakakses,'2', sipkd_listorganisasi(request)])
        else:
            cursor.execute("SELECT *, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi2 FROM view_organisasi_user(%s,%s,%s,%s)",[tahun,uname,hakakses,'2'])
        organisasi_list = dictfetchall(cursor)
        if action=='edit':
            
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT * FROM penatausahaan.pengguna WHERE uname = %s",[uname])
                hasil = dictfetchall(cursor)
                for hasilnya in hasil:                    
                    view_organisasi = hasilnya['organisasi'].split('|')
                panjang_data = len(view_organisasi)
                for i in range(panjang_data):
                    pisah = view_organisasi[i].split('.')
                    pisah_urusan = int(pisah[0])
                    pisah_suburusan = int(pisah[1]) 
                    pisah_organisasi = int(pisah[2])
                    pisah_unit = pisah[3]

                    if pisah_organisasi < 10:
                        pisah_organisasi = '0'+str(pisah_organisasi)
                    for i, j in enumerate(organisasi_list):
                        if j['kodeurusan']==pisah_urusan and j['kodesuburusan']==pisah_suburusan and j['kodeorganisasi2']==str(pisah_organisasi) and j['kodeunit'] == pisah_unit:
                            organisasi_list[i].update({"checked": "checked"})

        data = {
            'uname': uname,
            'hakakses': hakakses,
            'action':action,
            'jenis':'list_organisasi',
            'organisasi_list':organisasi_list,
            'checked': checked,
            }
    return render(request, 'konfig/modal_settingPengguna.html',data)

def cek_data_user(request):
    tahun = tahun_log(request)
    kode = request.GET.get('kode', None)
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM penatausahaan.fc_sipkd_view_pengguna(%s) WHERE uname=%s", [tahun,kode])
        hasil = cursor.fetchone()
    return HttpResponse(hasil)


def save_user(request):
    if request.method == 'POST':
        tahun = tahun_log(request)
        uname = request.POST['user_name'].upper()
        password = encrypt(request.POST['password'].upper())
        jns_jabatan = request.POST['jns_jabatan']
        action = request.POST['action']
        skpd = request.POST.getlist('skpd')
        value = last_organisasi = kode_urusan = kode_suburusan = kode_organisasi = fix_skpd = ''
        panjang = 0
        
        if jns_jabatan in ['OPERATORSKPD','BENDAHARAKELUAR','BENDAHARATERIMA','KEPALASKPD','PPKD','SKPD_P']:
            panjang = len(skpd)
            last_organisasi = skpd[panjang - 1]
            value = last_organisasi.split('.')
            
            fix_skpd = last_organisasi
            kode_urusan = value[0]
            kode_suburusan = value[1]
            kode_organisasi = value[2]
            kode_unit = value[3]
        else:
            fix_skpd = '|'.join(skpd)
            kode_urusan = 0
            kode_suburusan = 0
            kode_organisasi = ''
            kode_unit = ''

        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT count(*) as status FROM penatausahaan.pengguna WHERE tahun = %s and uname = %s", [tahun,uname.replace(" ", "")])
                jumlah_user = cursor.fetchone()
            if jumlah_user[0]==0:
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO penatausahaan.pengguna (tahun,uname,pwd,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,hakakses,organisasi,nama_lengkap) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun, uname.replace(" ", ""), password, kode_urusan, kode_suburusan, kode_organisasi, kode_unit,
                         jns_jabatan, fix_skpd, uname.replace(" ", "")])
                messages.success(request, "User "+uname.replace(" ", "")+" Berhasil Dibuat !")
            else:
                messages.error(request, "Username Sudah Digunakan !")
        elif action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute(
                    "UPDATE penatausahaan.pengguna SET tahun=%s, pwd=%s, kodeurusan=%s, kodesuburusan=%s, kodeorganisasi=%s, kodeunit=%s, hakakses=%s, organisasi=%s WHERE uname=%s",
                    [tahun, password, kode_urusan, kode_suburusan, kode_organisasi, kode_unit, jns_jabatan, fix_skpd,
                     uname])
            messages.success(request, "Data User "+uname.replace(" ", "")+" Berhasil Diubah!")
    return redirect('sipkd:settingpengguna')


def hapus_user(request):
    tahun = tahun_log(request)
    uname = request.POST.get('uname')
    hasil = ''
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM penatausahaan.pengguna WHERE tahun=%s and uname=%s", [tahun,uname])
    hasil = "Data berhasil dihapus!"
    return HttpResponse(hasil)

def get_terbilang(request):
    angka = request.POST.get('rp')        
    hasil = terbilang(angka)
    return HttpResponse(hasil)

# REKENING PENCAIRAN ---------------------------------------------------------------------------------
def rekening_pencairan(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT a.urut,a.kodesumberdana,a.urai,a.rekening,a.bank, \
            (select count(b.norekbankasal) from penatausahaan.sp2d b \
            where b.norekbankasal = a.rekening and b.bankasal = a.bank) as pakai \
            FROM kasda.kasda_sumberdanarekening a \
            ORDER BY a.urut,a.kodesumberdana")
        hasil = dictfetchall(cursor)

    dtX = {'hasil':hasil}
    return render(request, 'konfig/rekening_pencairan.html',dtX)

def loadmodal_rekpen(request):
    aksi = request.GET.get('act').lower()
    no_urut = kdsumberdana = disable = uraian = no_rekening = nama_bank = ''

    if aksi == 'add':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT coalesce(max(urut),0)+1 AS maks FROM kasda.kasda_sumberdanarekening")
            hasil = dictfetchall(cursor)
        kdsumberdana = hasil[0]['maks']
        no_urut = kdsumberdana

    elif aksi == 'edit':
        urut = int(request.GET.get('id'))
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT a.urut,a.kodesumberdana,a.urai,a.rekening,a.bank, \
                (select count(b.norekbankasal) from penatausahaan.sp2d b \
                where b.norekbankasal = a.rekening and b.bankasal = a.bank) as pakai \
                FROM kasda.kasda_sumberdanarekening a WHERE a.urut = %s ",[urut])
            hasil = dictfetchall(cursor)

        for x in hasil:
            no_urut = x['urut']
            kdsumberdana = x['kodesumberdana']
            uraian = x['urai']
            no_rekening = x['rekening']
            nama_bank = x['bank']

            if x['pakai'] != 0:
                disable = "disabled='disabled'" 
            else:
                disable = ""

    dtX = {'aksi':aksi, 'no_urut':no_urut, 'kdsumberdana':kdsumberdana, 'disable':disable, 'uraian':uraian,
        'no_rekening':no_rekening, 'nama_bank':nama_bank}

    return render(request, 'konfig/modal/mdl_rek_pencairan.html',dtX)

def simpan_rekpen(request):
    if request.method == 'POST':
        action = request.POST.get('aksi').lower()
        no_urut = int(request.POST.get('no_urut'))
        kdsumberdana = int(request.POST.get('kdsumberdana'))
        uraian = request.POST.get('uraian')
        no_rekening = request.POST.get('no_rekening')
        nama_bank = request.POST.get('nama_bank')

        if action == 'add':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("INSERT INTO kasda.kasda_sumberdanarekening \
                    (urut,kodesumberdana,urai,rekening,bank,tanggal) VALUES (%s,%s,%s,%s,%s,%s)",
                    [no_urut, kdsumberdana, uraian, no_rekening, nama_bank,'NOW()'])
            hasil = "Rekening Pencairan berhasil ditambahkan!"

        elif action == 'edit':
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("UPDATE kasda.kasda_sumberdanarekening SET \
                    kodesumberdana = %s, urai = %s, rekening = %s, bank = %s WHERE urut = %s",
                    [kdsumberdana, uraian, no_rekening, nama_bank, no_urut])
            hasil = "Rekening Pencairan berhasil diubah!"
    
    return HttpResponse(hasil)

def hapus_rekpen(request):
    if request.method == 'POST':
        urut = int(request.POST.get('urut'))
        kode = int(request.POST.get('kode'))
        reke = request.POST.get('rekening')

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("DELETE FROM kasda.kasda_sumberdanarekening \
                WHERE urut = %s AND kodesumberdana = %s AND rekening = %s",[urut,kode,reke])
        hasil = "Data berhasil dihapus!"
        
    return HttpResponse(hasil)

def autosugestion_bndhr(request):
    tahun = tahun_log(request)

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT distinct norekbank, bank, npwp, namayangberhak FROM penatausahaan.sp2d \
            where tahun = %s ORDER BY namayangberhak",[tahun])
        hasil = dictfetchall(cursor)

    data = {'hasil':hasil}

    return JsonResponse(data)
    
def pejabat_modal(request):
    tahun_x  = tahun_log(request)
    aksi     = str(request.GET.get("ax").lower())
    skpd     = request.GET.get('id').split('.')
    nomor_kontrak = ""
    hasil    = []

    if aksi == "false":
        # nomor_kontrak = str(request.GET.get("dt").replace("_","/").replace("+"," "))
        nomor_kontrak = urllib.parse.unquote(request.GET.get("dt"))
    arrDT = {'aksi':aksi, 'skpd':request.GET.get('id'), 'arrTBL':hasil, 'lengTBL':len(hasil)}

    return render(request,'konfig/modal/addpejabatskpd.html',arrDT)

def load_bank_pencairan(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def combopencairanskpd(request):
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

def load_bank_up(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def load_bank_gu(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def load_bank_tu(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def load_bank_ls(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)
 
def load_bank_gunihil(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])  
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def load_bank_tunihil(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("""SELECT kodebank, namabank, keterangan
            FROM master.master_bank""",
            [tahun_log(request)])
        bank = dictfetchall(cursor)

    data = {'list_bank' : bank}
    return render(request,'konfig/modal/modal_bank.html',data)

def tunihil(request):
	tahun_x = tahun_log(request)
	akses_x = hakakses(request).upper()
	sipkd_perubahan = perubahan(request)

	arrPerubahan = [{'kode':'0','nama':'Sebelum Perubahan'},{'kode':'1','nama':'Sesudah Perubahan'}]
	arrPeriod 	 = [{'kode':'0','nama':'-- Pilih Triwulan --'}, 
		{'kode':'1','nama':'Triwulan I'}, {'kode':'2','nama':'Triwulan II'},
		{'kode':'3','nama':'Triwulan III'}, {'kode':'4','nama':'Triwulan IV'}]

	arrDT = { 'akses':akses_x, 'perubahan':str(sipkd_perubahan),
		'arrPerubahan':arrPerubahan, 'arrPeriode':arrPeriod, 'jenis':'TU' }
		
	return render(request,'sp2d/tu_nihil.html',arrDT)
