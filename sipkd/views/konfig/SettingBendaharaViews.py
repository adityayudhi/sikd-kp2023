from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages

from support.support_sipkd import ArrayFormater

import json
import datetime

def modal_bendahara(request):
    tahun = tahun_log(request)
    action = request.GET.get('act', None)
    organisasi = request.GET.get('org', None)
    
    if action=='add':    
        uname = request.GET.get('input', '')
        split_org = organisasi.split('.')
        split_urusan = int(split_org[0])
        split_suburusan = int(split_org[1])
        split_organisasi = int(split_org[2])
        split_unit = str(split_org[3])
        if split_organisasi < 10:
            split_organisasi = '0'+str(split_organisasi)

        checked = pisah = keg_list = hasil = ''
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,kodeunit||' - '||urai_skpd as unit,kodeunit,kodeorganisasi,kodesubkegiatan \
                FROM penatausahaan.fc_view_list_keg_user(%s,%s,%s,%s,%s,%s)",
                [tahun,split_urusan,split_suburusan,split_organisasi,split_unit,uname])
            keg_list = dictfetchall(cursor)

        data = {
            'uname': uname,
            'action':action,
            'keg_list':keg_list,
            'split_urusan':split_urusan,
            'split_suburusan':split_suburusan,
            'split_organisasi':split_organisasi,
            'checked': checked,
            }
    elif action=='edit':
            test = 'Data tidak ditemukan'
            uname = request.GET.get('id', None)
            password = test
            nama_bendahara = test
            split_urusan = 0
            split_suburusan = 0
            split_organisasi = 0
            split_unit = '0000'
            keg_list = []
            selected_keg_list = []
            up_bpp = 0

            # ambil data per bendahara pembantu
            with connections[tahun_log(request)].cursor() as bndhr:
                bndhr.execute('SELECT * FROM penatausahaan.pengguna WHERE tahun=%s AND is_bendahara_pembantu=%s \
                    AND uname = %s', [tahun, 'Y',uname])
                detail_uname = ArrayFormater(dictfetchall(bndhr))[0]

                try:
                    keg_listXX = detail_uname['kegiatan'].split('~')
                    for x in range(len(keg_listXX)):
                        selected_keg_list.append(keg_listXX[x].split('|')[1])

                    split_urusan = detail_uname['kodeurusan']
                    split_suburusan = detail_uname['kodesuburusan']
                    split_organisasi = detail_uname['kodeorganisasi']
                    split_unit = detail_uname['kodeunit']
                    password = detail_uname['pwd']
                    nama_bendahara = detail_uname['nama_bendahara_pembantu']
                    up_bpp = detail_uname['up_bpp']

                    with connections[tahun_log(request)].cursor() as data_keg:
                        data_keg.execute("SELECT *,kodeunit||' - '||urai_skpd as unit,kodeunit,kodeorganisasi,\
                            kodesubkegiatan FROM penatausahaan.fc_view_list_keg_user(%s,%s,%s,%s,%s,%s)",
                            [tahun,split_urusan,split_suburusan,split_organisasi,split_unit,uname])
                        keg_list = dictfetchall(data_keg)
                    # end

                    for keg in keg_list:
                        pembanding = str(keg['kodebidang'])+'-'+str(keg['kodeorganisasi'])+'.'+str(keg['kodeprogram'])+'.'+str(keg['kodekegiatan'])+'.'+str(keg['kodesubkegiatan'])
                        if pembanding in selected_keg_list:
                            keg['checked']="checked"

                except Exception as e:
                    selected_keg_list = []
            # end

            data = {
                'uname': uname,
                'password':password,
                'nama_bendahara':nama_bendahara,
                'action':action,
                'keg_list':keg_list,
                'selected_keg_list':selected_keg_list,
                'split_urusan':split_urusan,
                'split_suburusan':split_suburusan,
                'split_organisasi':split_organisasi,
                'split_unit':split_unit,
                'nilai_up':up_bpp,
                # 'checked': checked,
            }

            print(data)

    return render(request, 'konfig/modal/modal_bendahara.html', data)
    
def getbendahara(request):
    if 'sipkd_username' in request.session:

        gets = request.GET.get('id', None)   

        if ((gets != '0') or (gets != '') or (gets != '0.0.0.0')):
            aidi = gets.split('.')
        else:
            skpd = '0.0.0.0'
            aidi = skpd.split('.')
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute(
                "select (select m.urai from master.master_organisasi m WHERE m.tahun = p.tahun "
                "and m.kodeurusan = p.kodeurusan and m.kodesuburusan = p.kodesuburusan "
                "and m.kodeorganisasi = p.kodeorganisasi and m.kodeunit = p.kodeunit) as urai_skpd, "
                "p.kodeurusan||'.'||p.kodesuburusan||'.'||lpad(p.kodeorganisasi,2,'0') as organisasi,"
                "* from penatausahaan.pengguna p where p.tahun = %s and p.is_bendahara_pembantu =%s"
                "and p.kodeurusan = %s  and p.kodesuburusan = %s "
                "and p.kodeorganisasi = lpad(%s,2,'0') and p.kodeunit = %s ",
                [tahun_log(request),'Y',aidi[0], aidi[1], aidi[2], aidi[3]])
            list_bendahara = dictfetchall(cursor)

        data = {'list_bendahara': list_bendahara}

        return render(request, 'konfig/tabel/tbl_bendahara.html', data)
    else:
        return redirect('sipkd:index')

def cek_bendahara(request):
    tahun = tahun_log(request)
    kode = request.GET.get('kode', None)
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM penatausahaan.fc_sipkd_view_pengguna(%s) WHERE uname=%s", [tahun,kode])
        hasil = cursor.fetchone()
    return HttpResponse(hasil)


def simpan_bendahara(request):
    if request.method == 'POST':
        tahun = tahun_log(request)
        uname = request.POST['user_name'].upper()       
        action = request.POST['action']
        skpd = request.POST.getlist('skpd')
        nama_bendahara = request.POST['nama_bendahara']
        urusan = request.POST['split_urusan']
        suburusan = request.POST['split_suburusan']
        organisasi = request.POST['split_organisasi']
        kodeunit = request.POST.get('kodeunit')
        nilai_up = request.POST.get('nilai_up')
        print(request.POST)
        kode_keg = '~'.join(request.POST.getlist('keg_list[]'))
        response = ""

        if action == 'add':
            password = encrypt(request.POST['password'].upper())
            with connections[tahun_log(request)].cursor() as cursor:
                cursor.execute("SELECT count(*) as status FROM penatausahaan.pengguna WHERE tahun = %s and uname = %s", [tahun,uname.replace(" ", "")])
                jumlah_user = cursor.fetchone()
            if jumlah_user[0]==0:
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO penatausahaan.pengguna (tahun,uname,pwd,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,"
                        "hakakses,is_bendahara_pembantu,kegiatan,nama_bendahara_pembantu,organisasi,up_bpp, nama_lengkap) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun, uname.replace(" ", ""), password, urusan, suburusan, organisasi, kodeunit,
                         'BPP', 'Y', kode_keg, nama_bendahara, urusan+'.'+suburusan+'.'+organisasi+'.'+kodeunit+'|',nilai_up,nama_bendahara])
                response = "User "+uname.replace(" ", "")+" Berhasil Dibuat !"
            else:
                response = "Username Sudah Digunakan !"
        elif action == 'edit':
            try:
                password = encrypt(request.POST['password'].upper())
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.pengguna SET tahun=%s, kodeurusan=%s, kodesuburusan=%s, kodeorganisasi=%s,kodeunit=%s, "
                                    "hakakses=%s,  is_bendahara_pembantu=%s, kegiatan=%s, nama_bendahara_pembantu=%s, organisasi=%s, up_bpp=%s, nama_lengkap=%s "
                                    "WHERE uname=%s",
                                    [tahun, password, urusan, suburusan, organisasi,kodeunit, 'BPP', 'Y', kode_keg, nama_bendahara, urusan+'.'+suburusan+'.'+organisasi+'.'+kodeunit+'|',nilai_up,nama_bendahara, uname])
            except Exception as e:
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("UPDATE penatausahaan.pengguna SET tahun=%s, kodeurusan=%s, kodesuburusan=%s, kodeorganisasi=%s, kodeunit=%s,"
                        "hakakses=%s,  is_bendahara_pembantu=%s, kegiatan=%s, nama_bendahara_pembantu=%s, organisasi=%s,up_bpp=%s, nama_lengkap=%s "
                        "WHERE uname=%s",
                        [tahun, urusan, suburusan, organisasi,kodeunit, 'BPP', 'Y', kode_keg, nama_bendahara, urusan+'.'+suburusan+'.'+organisasi+'.'+kodeunit+'|',nilai_up,nama_bendahara,uname])
            response = "Data User "+uname.replace(" ", "")+" Berhasil Diubah!"

    return HttpResponse(response)

def hapus_bendahara(request):
    tahun = tahun_log(request)
    uname = request.POST.get('uname')
    hasil = ''
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("DELETE FROM penatausahaan.pengguna WHERE tahun=%s and uname=%s", [tahun,uname])
    hasil = "Data berhasil dihapus!"
    return HttpResponse(hasil)



def settingbendahara(request):
    skpd = set_organisasi(request)
    if skpd["kode"] == '':
        kode = 0
    else:
        kode = skpd["kode"]

    data = {'organisasi': skpd["skpd"], 'kd_org': kode, 'ur_org': skpd["urai"]}
    return render(request, 'konfig/bendahara.html', data)
