from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from support.support_sipkd import *
from django.conf import settings

import openpyxl
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import time, os
import pandas as pd
# import numpy as np

def sync_datasipd(request):
    tahun = tahun_log(request)

    skpd = set_organisasi(request)
    if skpd["kode"] == '': kode = 0
    else: kode = skpd["kode"]
    btn_upload = ''
    if hakakses(request) =='ADMIN':
        btn_upload = '<span class="input-group-btn">\
                        <button onclick="upload()" id="btn_upload" alt="'+reverse('sipkd:modalupload',args=['skpd'])+'"\
                            class="btn btn-warning btn-sm" title="Upload Data ke SIPKD" type="button">\
                          <strong><i class="fa fa-upload"></i>&nbsp;&nbsp;Upload</strong>\
                        </button></span>'
    data = {'page':'master','organisasi':skpd["skpd"],'kd_org':kode,'ur_org':skpd["urai"],'btn_upload':btn_upload,}

    return render(request, 'konfig/sync_datasipd.html',data)

def tabssyncsipd(request):

    perubahan = perubahananggaran(request)
    aksi = request.GET.get("ac")
    skpd = request.GET.get("id", 0).split(".")
    arrfilter = [0,0,'0','0']
    list_tot  = ''
    header = ''
    body = ''
    foot = ''
    btn_setuju = ''

    if(skpd != 0):
        for i in range(0,len(skpd)):
            arrfilter[i] = skpd[i]

    arrfilter.insert(0,tahun_log(request))

    if(aksi == "pdptn"):
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when lock = 1 then 'checked' else '' end) as pilih, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
                "FROM penatausahaan.fc_angg_kas_pendapatan(%s,%s,%s,%s,%s)",arrfilter)
            list_tbl = dictfetchall(cursor)

    elif(aksi == "btl"):
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when lock = 1 then 'checked' else '' end) as pilih, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
                "FROM penatausahaan.fc_angg_kas_belanja(%s,%s,%s,%s,%s)",arrfilter)
            list_tbl = dictfetchall(cursor)

    elif(aksi == "blk"):
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when lock = 1 then 'checked' else '' end) as pilih, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna, "\
                "(case when isbold = 0 then '2' when isbold = 2 then '1' else '0' end) as sepasi, "\
                "(case when isbold = 0 then 'italic' when isbold = 1 then 'isbold' else '' end) as tebal, "\
                "(case when isbold = 0 then 'cur_pointer' else '' end) as cursor, "\
                "(case when isbold = 0 then 'Klik Detail Program Kegiatan' else '' end) as detail "\
                "FROM penatausahaan.fc_angg_kas_belanja_langsung(%s,%s,%s,%s,%s)",arrfilter)
            list_tbl = dictfetchall(cursor)


        jan = feb = mar = apr = mei = jun = jul = agu = sep = okt = nov = des = angg = alok = turah = 0
        
        for dt in list_tbl:
            if(dt["isbold"] == 1):
                jan += dt["jan"]
                feb += dt["feb"]
                mar += dt["mar"]
                apr += dt["apr"]
                mei += dt["mei"]
                jun += dt["jun"]
                jul += dt["jul"]
                agu += dt["agu"]
                sep += dt["sep"]
                okt += dt["okt"]
                nov += dt["nov"]
                des += dt["des"]
                angg  += dt["jumlah"]
                alok  += dt["total"]
                turah += dt["sisa"]

        arrnilai = {
            'jan':format_rp(jan),'feb':format_rp(feb),'mar':format_rp(mar),
            'apr':format_rp(apr),'mei':format_rp(mei),'jun':format_rp(jun),
            'jul':format_rp(jul),'agu':format_rp(agu),'sep':format_rp(sep),
            'okt':format_rp(okt),'nov':format_rp(nov),'des':format_rp(des),
            'jumlah':format_rp(angg),'total':format_rp(alok),'sisa':format_rp(turah)}

        list_tot = arrnilai

    elif(aksi == "rinci"):
        program = request.GET.get("pr")
        obj = request.GET.get("kd").split(".")

        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT * FROM penatausahaan.fc_angg_kas_rincian_bl_header(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]+'.'+obj[1],obj[2],obj[3]+'.'+obj[4],obj[5]])
            program = dictfetchall(cursor)

            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
                "FROM penatausahaan.FC_ANGG_KAS_RINCIAN_BL(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [tahun_log(request),skpd[0],skpd[1],skpd[2],skpd[3],obj[0]+'.'+obj[1],obj[2],obj[3]+'.'+obj[4],obj[5]])
            list_tbl = dictfetchall(cursor)

        for arr in program:
            list_tot = {'program':arr['program'], 'kegiatan':arr['kegiatan']}

    elif(aksi == "biayain"):
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when lock = 1 then 'checked' else '' end) as pilih, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
                "FROM penatausahaan.fc_angg_kas_pembiayaan(%s,%s,%s,%s,%s,'IN')",arrfilter)
            list_tbl = dictfetchall(cursor)

    elif(aksi == "biayaout"):
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT *,ROW_NUMBER () OVER () as nomor, "\
                "(case when lock = 1 then 'checked' else '' end) as pilih, "\
                "(case when total<jumlah then 'kuning' when total>jumlah then 'merah' else 'hijau' end) as warna "\
                "FROM penatausahaan.fc_angg_kas_pembiayaan(%s,%s,%s,%s,%s,'OUT')",arrfilter)
            list_tbl = dictfetchall(cursor)

    if hakakses(request) =='ADMIN':
        header = '<th rowspan="2" style="background-image:none;">\
                    <input type="checkbox" onclick="cek_uncek_all(this,\'chk_rek\',\''+aksi+'\')"/>\
                </th>'

        for x in range(len(list_tbl)):
            if aksi == 'blk':
                if list_tbl[x]['tebal']=='italic':
                    konten = '<input type="hidden" class="hidden" value="'+str(list_tbl[x]['koderekening'])+'" name="kdrek_'+aksi+'">\
                            <input type="hidden" class="hidden" name="cek_'+aksi+'" id="cek_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['lock'])+'">\
                            <input type="hidden" name="sisa_'+aksi+'" id="sisa_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['sisa'])+'">\
                            <input type="checkbox" '+list_tbl[x]['pilih']+' class="chk_rek" \
                                id="rekchk_'+str(list_tbl[x]['nomor'])+'" '+str(list_tbl[x]['pilih'])+' onClick="checkclick(this, \''+aksi+'_'+str(list_tbl[x]['nomor'])+'\')"/>'
                    list_tbl[x]['body'] = '<td align="center">'+konten+'</td>'
                else:
                    list_tbl[x]['body']='<td align="center"></td>'
            elif aksi != 'rinci':
                list_tbl[x]['body'] = '<td align="center">\
                                        <input type="hidden" class="hidden" name="cek_'+aksi+'" id="cek_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['lock'])+'">\
                                        <input type="checkbox" '+list_tbl[x]['pilih']+' class="chk_rek"\
                                            id="rekchk_'+str(list_tbl[x]['nomor'])+'" onClick="checkclick(this, \''+aksi+'_'+str(list_tbl[x]['nomor'])+'\')"/>\
                                        <input type="hidden" name="sisa_'+aksi+'"  id="sisa_'+aksi+'_'+str(list_tbl[x]['nomor'])+'" value="'+str(list_tbl[x]['sisa'])+'">\
                                    </td>'
        btn_setuju = '<div onclick="proses_setuju_rka(\''+aksi+'\')" class="btn btn-sm btn-primary" title="Setujui Anggaran" id="setuju_rka">\
                                <i class="fa fa-check"></i>&nbsp;&nbsp;Proses Setuju\
                            </div>'
        foot = '<th></th>'

    wr_hijau = wr_kuning = wr_merah = 0
    for x in list_tbl:
        if(x["warna"] == 'hijau'):
            wr_hijau = wr_hijau+1
        elif(x["warna"] == 'kuning'):
            wr_kuning = wr_kuning+1
        elif(x["warna"] == 'merah'):
            wr_merah = wr_merah+1

    data = {'page':aksi, 'perubahan':perubahan, 'list_tbl':ArrayFormater(list_tbl),
        'list_tot':list_tot,'header':header,'body':body,'foot':foot,'btn_setuju':btn_setuju,
        'wr_hijau':wr_hijau, 'wr_kuning':wr_kuning, 'wr_merah':wr_merah}
    return render(request, 'konfig/tabel/syncsipd_tabel.html',data)

def modal_upload_syncsipd(request, page):
    if request.method == 'GET':
        data = {'page':page}
        return render(request, 'konfig/modal/syncsipd_upload.html', data)

    elif request.method == 'POST':
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        kodeskpd = request.POST['kodeskpd']
        print(kodeskpd)

        update_ = tanggal(request)['get_jadwal_nomor']
        if update_ > 0:
            keterangan = f'Pergeseran ke {update_}'
        else:
            keterangan = 'Murni'

        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = os.path.join(settings.BASE_DIR, 'media', fileName)
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                if int(end):
                    empexceldata = pd.read_excel(os.path.join(settings.BASE_DIR, 'media', fileName))
                    print(page)
                    # pd.DataFrame(empexceldata, columns=['Kode Program', ''])
                    if page in ['pdptn','biayain','biayaout']:
                        if page == 'pdptn':
                            tabel_insert = 'temporary_sipd.rak_pendapatan'
                            pkey = 'rak_pendapatan_pkey'
                        elif page == 'biayain' or page == 'biayaout':
                            tabel_insert = 'temporary_sipd.rak_pembiayaan'
                            pkey = 'rak_pembiayaan_pkey'

                        for indices, row in empexceldata.iterrows():
                            with connections[tahun_log(request)].cursor() as cursor:
                                cursor.execute(f"""INSERT INTO {tabel_insert} (tahun,daerah,kodeurusan,namaurusan,kodebidangurusan,namabidangurusan,kodeskpd,namaskpd,kodesubskpd,namasubskpd,kodeprogram,namaprogram,kodeakun,
                                                    namaakun,nilairincian,totalrak,bulan1,bulan2,bulan3,bulan4,bulan5,bulan6,bulan7,bulan8,bulan9,bulan10,bulan11,bulan12,update,keterangan) 
                                                    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                    ON CONFLICT ON CONSTRAINT {pkey} DO UPDATE SET totalrak = %s, bulan1 = %s, bulan2 = %s,bulan3 = %s,bulan4 = %s,bulan5 = %s,
                                                    bulan6 = %s,bulan7 = %s,bulan8 = %s,bulan9 = %s,bulan10 = %s,bulan11 = %s,bulan12 = %s, keterangan = %s""",
                                                    [row['Tahun'], row['Daerah'], row['Kode Urusan'], row['Nama Urusan'], row['Kode Bidang Urusan'], row['Nama Bidang Urusan'], row['Kode SKPD'], 
                                                    row['Nama SKPD'], row['Kode Sub SKPD'], row['Nama Sub SKPD'], row['Kode Program'], row['Nama Program'], row['Kode Akun'], row['Nama Akun'], row['Nilai Rincian'], 
                                                    row['Total RAK'], row['bulan1'], row['bulan2'], row['bulan3'], row['bulan4'], row['bulan5'], row['bulan6'], row['bulan7'], row['bulan8'], row['bulan9'], row['bulan10'], 
                                                    row['bulan11'], row['bulan12'], update_,keterangan,
                                                    row['Total RAK'], row['bulan1'], row['bulan2'], row['bulan3'], row['bulan4'], row['bulan5'], row['bulan6'], row['bulan7'], row['bulan8'], row['bulan9'], row['bulan10'], 
                                                    row['bulan11'], row['bulan12'], keterangan])
                            with connections[tahun_log(request)].cursor() as cursor:
                                cursor.execute("SELECT * FROM temporary_sipd.fc_olah_rak_pendapatan_pembiayaan_parsial(%s,%s,%s)",[tahun_log(request), update_, kodeskpd])
                    elif page in ['blk']:
                        tabel_insert = 'temporary_sipd.rak_belanja'
                        pkey = 'rak_belanja_pkey'
                        for indices, row in empexceldata.iterrows():
                            with connections[tahun_log(request)].cursor() as cursor:
                                cursor.execute(f"""INSERT INTO {tabel_insert} (tahun,daerah,kode_urusan,nama_urusan,kode_bidang_urusan,nama_bidang_urusan,kode_skpd,nama_skpd,kode_sub_skpd,nama_sub_skpd,kode_program,nama_program,kode_kegiatan,
                                                nama_kegiatan,kode_sub_kegiatan,nama_sub_kegiatan,kode_akun,nama_akun,nilai_rincian,total_rak,bulan1,bulan2,bulan3,bulan4,bulan5,bulan6,bulan7,bulan8,bulan9,bulan10,bulan11,bulan12,update,keterangan) 
                                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                                    ON CONFLICT ON CONSTRAINT {pkey} DO UPDATE SET nilai_rincian = %s, total_rak = %s, bulan1 = %s, bulan2 = %s,bulan3 = %s,bulan4 = %s,bulan5 = %s,
                                                    bulan6 = %s,bulan7 = %s,bulan8 = %s,bulan9 = %s,bulan10 = %s,bulan11 = %s,bulan12 = %s, keterangan = %s""",
                                                    [row['Tahun'],  row['Daerah'],   row['Kode Urusan'],   row['Nama Urusan'],   row['Kode Bidang Urusan'],    row['Nama Bidang Urusan'], row['Kode SKPD'],   row['Nama SKPD'], row['Kode Sub SKPD'],   row['Nama Sub SKPD'],
                                                    row['Kode Program'],    row['Nama Program'],   row['Kode Kegiatan'], row['Nama Kegiatan'],   row['Kode Sub Kegiatan'], row['Nama Sub Kegiatan'],   row['Kode Akun'], row['Nama Akun'],   row['Nilai Rincian'], 
                                                    row['Total RAK'],   row['bulan1'],    row['bulan2'], row['bulan3'],  row['bulan4'],   row['bulan5'],    row['bulan6'], row['bulan7'],  row['bulan8'],   row['bulan9'],    row['bulan10'],    row['bulan11'],    row['bulan12'],
                                                    update_, keterangan,
                                                    row['Nilai Rincian'], row['Total RAK'], row['bulan1'], row['bulan2'], row['bulan3'], row['bulan4'], row['bulan5'], row['bulan6'], row['bulan7'], row['bulan8'], row['bulan9'], row['bulan10'], 
                                                    row['bulan11'], row['bulan12'], keterangan])

                        with connections[tahun_log(request)].cursor() as cursor:
                                cursor.execute("SELECT * FROM temporary_sipd.fc_olah_rak_belanja_parsial(%s,%s,%s)",[tahun_log(request), update_, kodeskpd])

                        
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            # else:
            #     path = 'media/' + existingPath
            #     model_id = File.objects.get(existingPath=existingPath)
            #     if model_id.name == fileName:
            #         if not model_id.eof:
            #             with open(path, 'ab+') as destination: 
            #                 destination.write(file)
            #             if int(end):
            #                 model_id.eof = int(end)
            #                 model_id.save()
            #                 res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
            #             else:
            #                 res = JsonResponse({'existingPath':model_id.existingPath})    
            #             return res
            #         else:
            #             res = JsonResponse({'data':'EOF found. Invalid request'})
            #             return res
            #     else:
            #         res = JsonResponse({'data':'No such file exists in the existingPath'})
            #         return res
                    
        data = {}
        return JsonResponse(data)
    return HttpResponse('ERROR !')
