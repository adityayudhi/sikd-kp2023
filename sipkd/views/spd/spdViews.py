from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from django.contrib import messages
from support.support_sipkd import *
from django.db import IntegrityError

import json

def spd(request):
    tahun_x = tahun_log(request)

    with connections[tahun_log(request)].cursor() as cursor:
        # cursor.execute("SELECT DISTINCT update,keterangan FROM temporary_sipd.rak_belanja \
        #   WHERE tahun = %s ",[tahun_x])
        cursor.execute("SELECT nomor as update, uraian as keterangan from master.penjadwalan_penatausahaan \
            WHERE tahun = %s order by nomor desc ",[tahun_x])
        jns_apbd = dictfetchall(cursor)
    x_nomor_spd = generate_no(request, tahun_log(request), 'SPD')
    
    
    data = { 'jns_apbd':jns_apbd, 'x_nomor_spd':x_nomor_spd }

    return render(request,'spd/spd.html', data)

# def ambil_bendahara(request):
#   dataBendahara = ''
#   kode_organisasi = request.POST.get('kode_organisasi','')
#   if kode_organisasi!='':
#       kd_urusan = kode_organisasi.split('.')[0] 
#       kd_suburusan = kode_organisasi.split('.')[1]
#       kd_organisasi = kode_organisasi.split('.')[2]
#       with connections[tahun_log(request)].cursor() as cursor:
#           cursor.execute('SELECT * FROM master.pejabat_skpd \
#                           WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and trim(kodeorganisasi) = %s and jenissistem = 2\
#                                   and jabatan LIKE \'Bendahara Pengeluaran SKPD\'',[tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi])
#           dataBendahara = dictfetchall(cursor)
#   return HttpResponse(json.dumps(dataBendahara))

def rinci_spd(request):
    hasil = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    nospd = request.POST.get('nospd','')
    
    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and kdunit != '' and nospd != '':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute('SELECT * FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
                and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s',
                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])
            hasil = dictfetchall(cursor)
    
    data = { 'hasil':hasil, }
    return JsonResponse(data)

def link_tabel_rinci_spd(request):
    data_rincian = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    nospd = request.POST.get('nospd','')
    bln_awal = request.POST.get('bln_awal','')
    bln_akhir = request.POST.get('bln_akhir','')
    triwulan = int(request.POST.get('triwulan',''))
    jenisdpa = request.POST.get('jenisdpa','')
    jnsapbd = request.POST.get('jnsapbd','')
    

    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '' and triwulan != '' and jenisdpa != '':
        
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute('SELECT nodpa, uraian, anggaran, lalu, sekarang, jumlah, sisa \
                FROM penatausahaan.fc_view_spd_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,bln_awal,bln_akhir,jenisdpa,triwulan])
            data_rincian = dictfetchall(cursor)
        
    data = {
        'data_rincian':convert_tuple(data_rincian),
    }
    
    return JsonResponse(data)

def cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan,jenisdpa):
    jumlah = ''
    if jenisdpa=='DPA-SKPD' or jenisdpa=='DPPA-SKPD':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT count(tahun) as jumlah, nospd  FROM penatausahaan.spd \
                WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
                and jenisdpa in ('DPA-SKPD','DPPA-SKPD') and  BULAN_AWAL=%s \
                GROUP BY nospd",
                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
            jumlah = cursor.fetchone()
    else:
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT count(tahun) as jumlah,nospd  FROM penatausahaan.spd \
                WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s \
                and jenisdpa in ('DPA-PPKD','DPPA-PPKD') and  BULAN_AWAL=%s \
                GROUP BY nospd",
                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,bulan])
            jumlah = cursor.fetchone()
    return '0' if jumlah==None else jumlah

def cek_data_spd(request, nospd):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT count(*) as jumlah FROM penatausahaan.spd \
            WHERE tahun=%s and nospd=%s",[tahun_log(request),nospd])
        jumlah = cursor.fetchone()
    return '0' if jumlah==None else jumlah

def simpan_spd(request):
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    nospd = request.POST.get('nospd','').upper()
    bulan = request.POST.get('bulan','')
    bln_awal = request.POST.get('bln_awal','')
    bln_akhir = request.POST.get('bln_akhir','')
    jenisdpa = request.POST.get('jenisdpa','')
    jumlah_total = request.POST.get('jumlah_total','')
    tanggal_draft =  request.POST.get('tanggal_draft','') 
    tanggal_dpa =  request.POST.get('tanggal_dpa','')
    bendahara = request.POST.get('bendahara','')
    isSimpan = request.POST.get('isSimpan','')
    spd_rincian = json.loads(request.POST.get('spd_rincian'))
    jenisapbd = request.POST.get('jenisapbd','')

    jumlah = ''
    data = {}
    hasil = ''
    is_success = False
    next_to_rincian = False
    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '':
        with connections[tahun_log(request)].cursor() as cursor:
            # Kalau buat SPD baru
            if isSimpan=='true':
                # if int(cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bln_awal,jenisdpa)[0])!=0:
                #     hasil = 'SPD pada bulan ini sudah pernah dibuat !'
                # else:
                if nospd!='' or jenisdpa!='' or bendahara!='':
                    if int(cek_data_spd(request, nospd)[0])!=0:
                        hasil = f'Nomor SPD {nospd} sudah ada !'
                    else:
                        try:
                            cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,\
                                kodeorganisasi,kodeunit,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,\
                                bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname,pergeseran) \
                                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,
                                tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_dpa),
                                bendahara,bln_awal,bln_akhir,jenisdpa,jumlah_total,username(request),jenisapbd])
                            hasil = 'Simpan SPD berhasil !'
                            next_to_rincian = True
                            is_success = True
                        except IntegrityError as e:
                            hasil = 'Nomor SPD sudah ada, silahkan hubungi administrator!'
                else:
                    hasil = 'Lengkapi data terlebih dahulu !'
            # Kalau update data SPD
            else:
                if int(cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bln_awal,jenisdpa)[0])!=0:
                    try:
                        cursor.execute('UPDATE penatausahaan.spd set nospd=%s, tanggal_draft=%s, tanggal=%s, tgldpa=%s, bendaharapengeluaran=%s, jenisdpa=%s, jumlahspd=%s, uname = %s,pergeseran=%s WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s',[nospd, tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_dpa), bendahara, jenisdpa, jumlah_total,username(request),jenisapbd,tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,cek_data(request,kdurusan,kdsuburusan,kdorganisasi,kdunit,bln_awal, jenisdpa)[1]])
                        hasil = 'Ubah SPD berhasil !'
                        is_success = True
                        next_to_rincian = True
                    except IntegrityError as e:
                        hasil = 'Nomor SPD sudah ada !'
                else:
                    if nospd!='' or jenisdpa!='' or bendahara!='':
                        if int(cek_data_spd(request, nospd)[0])!=0:
                            hasil = 'Nomor SPD sudah ada !'
                        else:
                            try:
                                cursor.execute('INSERT INTO penatausahaan.spd (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nospd,tanggal_draft,tanggal,tgldpa,bendaharapengeluaran,bulan_awal,bulan_akhir,jenisdpa,jumlahspd,uname,pergeseran) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,tgl_to_db(tanggal_draft),tgl_to_db(tanggal_draft),tgl_to_db(tanggal_dpa), bendahara, bln_awal,bln_akhir,jenisdpa, jumlah_total,username(request),jenisapbd])
                                hasil = 'Simpan SPD berhasil !'
                                next_to_rincian = True
                                is_success = True
                            except IntegrityError as e:
                                hasil = 'Nomor SPD sudah ada !'

            if next_to_rincian:
                # HAPUS RINCIAN DULU
                cursor.execute("DELETE FROM penatausahaan.spdrincian WHERE tahun=%s and kodeurursan=%s "
                    "and kodesuburusan=%s and kodeorganisasi=%s and kodeunit=%s and nospd=%s",
                    [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd])

                # SIMPAN RINCIAN
                for i in range(0,len(spd_rincian)):
                    kode = spd_rincian[i]['kode'].split(".") # ['1', '1', '01', '0003', '1', '01', '2', '2', '01', '11']
                    uang = toAngkaDec(spd_rincian[i]['uang'])

                    kdurusan = kode[0]
                    kdsuburusan = kode[1]
                    kdorganisasi = kode[2]
                    kdunit = kode[3]
                    kdbidang = kode[4]+"."+kode[5]
                    kdprogram = kode[6]
                    kdkegiatan = kode[7]+"."+kode[8]
                    kdsubkegiatan = kode[9]

                    cursor.execute("INSERT INTO penatausahaan.spdrincian (tahun,kodeurursan,kodesuburusan,kodeorganisasi,kodeunit,\
                        nospd,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan,kodesubkeluaran,jumlah) \
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,nospd,kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,uang])                                     
                        
                    hasil = "Data berhasil disimpan!"
                    is_success = True

    data['hasil'] = hasil
    data['is_success'] = is_success
    return JsonResponse(data)

def hapus_spd(request):
    hasil = ''
    kdurusan = request.POST.get('kdurusan','')
    kdsuburusan = request.POST.get('kdsuburusan','')
    kdorganisasi = request.POST.get('kdorganisasi','')
    kdunit = request.POST.get('kdunit','')
    nospd = request.POST.get('nospd','')
    
    if kdurusan!='' and kdsuburusan != '' and kdorganisasi != '':
        with connections[tahun_log(request)].cursor() as cursor:
            cursor.execute("SELECT LOCKED FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
                and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
                [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
            jumlah = cursor.fetchone()

            if jumlah[0]=='Y':
                hasil = 'SPD sudah di lock !'
            else:
                cursor.execute("DELETE FROM penatausahaan.spd WHERE tahun = %s and kodeurusan = %s \
                    and kodesuburusan = %s and kodeorganisasi = %s and kodeunit = %s and nospd = %s",
                    [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospd])
                hasil = 'Data SPD berhasil dihapus !'
    return HttpResponse(hasil)

def render_cetak_spd(request):
    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1 \
            FROM master.pejabat_skpkd where jenissistem=2 and tahun=%s and upper(jabatan) \
            LIKE '%%BENDAHARA UMUM%%'",[tahun_log(request)])
        pejabat = dictfetchall(cursor)
    
    data = {
        'pejabat':pejabat,
    }
    return render(request, 'spd/modal/modal_cetak_spd.html',data)

def cetak_spd(request):

    post    = request.POST
    lapParm = {}
    skpd    = post.get('skpd').split('.')
    no_spd = post.get('no_spd')
    id_jabatan = post.get('id_jabatan')
    triwulan = post.get('triwulan')
    tipe = post.get('tipe', '')

    lapParm['file']         = 'penatausahaan/spd/SPD.fr3'
    lapParm['NOMER'] = "'"+no_spd+"'"
    lapParm['tahun'] = "'"+tahun_log(request)+"'"
    lapParm['ID'] = "'"+id_jabatan+"'"              
    lapParm['KodeUrusan'] = "'"+skpd[0]+"'"
    lapParm['KodeSubUrusan'] = "'"+skpd[1]+"'"
    lapParm['KodeOrganisasi'] = "'"+skpd[2]+"'"
    lapParm['KodeUnit'] = "'"+skpd[3]+"'"
    lapParm['triwulan'] = triwulan
    if tipe == 'excel':
        lapParm['report_type'] = 'xml'
    else:
        lapParm['report_type'] = 'pdf'

    return HttpResponse(laplink(request, lapParm))