from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection,connections
from sipkd.config import *
from support.support_sipkd import *
import datetime, decimal
import pprint

def spm_save_up(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            org = request.POST.get('skpd', '').split('.')
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')            
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            #jml_spp              = request.POST.get('jml_spp').replace(',','.')
            jml_spp              = request.POST.get('jml_spp', '')
            jml_spm              = request.POST.get('jml_spp')
            update_jml_spm       = toAngkaDec(request.POST.get('jml_spp_x'))
            update_jml_spp       = toAngkaDec(request.POST.get('jml_spp_x'))
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            # perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            # triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            
            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,toAngkaDec(jml_spp),toAngkaDec(jml_spp),\
                            '',nama_yang_berhak,no_rek,bank,'UP',0,npwp,informasi,status_keperluan,last_update,1,username(request)])
                       
                        cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s AND KODEUNIT=%s and NOSPM = %s",[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit, no_spm])

                        cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,"
                        "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                        "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,'',0,'0',0,0,1,1,1,3,1,1,toAngkaDec(jml_spp),tgl_draft])

                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"
                        
                elif aksi == "false":
                    try:
                        with connections[tahun_log(request)].cursor() as cursor:
                            cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                                "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                                "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                                "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s and NOSPM=%s",
                                [no_spm,tgl,tgl_draft,\
                                deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spp,nama_yang_berhak,\
                                no_rek,bank,informasi,status_keperluan,npwp,1,\
                                tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])

                            cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and kodeunit=%s and NOSPM = %s",[tahun_log(request), kdurusan,kdsuburusan,kdorganisasi,kdunit, no_spm])
                            cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,'',0,'0',0,0,1,1,1,3,1,1,toAngkaDec(jml_spp),tgl_draft])
                    
                            hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"
                    except Exception as e:
                        hasil = "SPM sudah disetujui, tidak diperkenankan mengubah atau menghapus data"

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_non_angg(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'NON_ANGG',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"
                
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, no_spm_lama])       

                for x in range(len(rekening1)):
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[0]+'.'+split_bidang[1]
                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,"
                        "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                        "KODERINCIANOBJEK,JUMLAH,TANGGAL)"
                        " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,\
                        kdbidang,0,0,kdakun,kdkelompok,kdjenis,kdobjek,\
                        kdrincian,afektasi,tgl_draft])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_gu(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            

            if no_spm != "":
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and kodeunit=%s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm_lama])

                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'GU',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"

                for x in range(len(rekening1)):              
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[1]+'.'+split_bidang[2]
                    kdprogram           = split_bidang[4]
                    kdkegiatan          = split_bidang[5]+'.'+split_bidang[6]
                    kdsubkegiatan       = split_bidang[7]

                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]
                    kdsubrincian        = split_kegiatan[5]


                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPM,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,
                            kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,
                            kdrincian,kdsubrincian,jumlah_spm,tgl_draft])
                        
            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_tu(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            

            if no_spm != "":
                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s \
                        and KODESUBURUSAN = %s and KODEORGANISASI = %s and kodeunit=%s and NOSPM = %s",
                        [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm_lama])
                
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'TU',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and kodeunit=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"

                for x in range(len(rekening1)):              
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[1]+'.'+split_bidang[2]
                    kdprogram           = split_bidang[4]
                    kdkegiatan          = split_bidang[5]+'.'+split_bidang[6]
                    kdsubkegiatan       = split_bidang[7]

                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]
                    kdsubrincian        = split_kegiatan[5]


                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPM,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,
                            kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,
                            kdrincian,kdsubrincian,jumlah_spm,tgl_draft])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')


def spm_save_gu_nihil(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'GU_NIHIL',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and KODEUNIT=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and KODEUNIT = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm_lama])

                for x in range(len(rekening1)):              
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    # ['0000', '1', '01', '01', '1', '2', '01', '002'] ['5', '1', '2', '01', '01', '24']
                    kdbidang            = split_bidang[1]+'.'+split_bidang[2]
                    kdprogram           = split_bidang[4]
                    kdkegiatan          = split_bidang[5]+'.'+split_bidang[6]
                    kdsubkegiatan       = split_bidang[7]
                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]
                    kdsubrincian        = split_kegiatan[5]


                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,\
                            kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,\
                            kdrincian,kdsubrincian,jumlah_spm,tgl_draft])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_tu_nihil(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''            

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'TU_NIHIL',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and KODEUNIT=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and KODEUNIT = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm_lama])

                for x in range(len(rekening1)):              
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[1]+'.'+split_bidang[2]
                    kdprogram           = split_bidang[4]
                    kdkegiatan          = split_bidang[5]+'.'+split_bidang[6]
                    kdsubkegiatan       = split_bidang[7]
                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]
                    kdsubrincian        = split_kegiatan[5]


                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,kodeunit,NOSPM,"
                            "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                            "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,\
                            kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,\
                            kdrincian,kdsubrincian,jumlah_spm,tgl_draft])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_gj(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = request.POST.get('jml_spm').replace(',','.')
            jml_spm              = request.POST.get('jml_spm').replace(',','.')
            update_jml_spm       = request.POST.get('jml_spp_x').replace(',','.')
            update_jml_spp       = request.POST.get('jml_spp_x').replace(',','.')
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = request.POST.get('npwp')
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            rekening_potongan    = json.loads(request.POST.get('rekening_potongan'))
            # uraian_potongan      = request.POST.get('uraian_potongan')
            jumlah_potongan      = json.loads(request.POST.get('jumlah_potongan'))
            jenis_potongan       = json.loads(request.POST.get('jenis_potongan'))
            kdprogram            = ''
            kdkegiatan            = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,jml_spm,\
                            '',nama_yang_berhak,no_rek,bank,'GJ',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"

                elif aksi == "false":
                    with connections[tahun_log(request)].cursor() as cursor:# if jenis_spm=='ls_ppkd':
                        cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                            "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                            "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                            "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and NOSPM=%s",
                            [no_spm,tgl,tgl_draft,\
                            deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,\
                            no_rek,bank,informasi,status_keperluan,npwp,triwulan,\
                            tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm_lama])
                        hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmrincian where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, no_spm_lama])       

                for x in range(len(rekening1)):
                    rekening            = rekening1[x].split('|')[0]
                    jumlah_spm          = rekening1[x].split('|')[1]
                    pisah_rekening      = rekening.split('-')[0]
                    pisah_kegiatan      = rekening.split('-')[1]
                    split_bidang        = pisah_rekening.split('.')
                    split_kegiatan      = pisah_kegiatan.split('.')
                    kdbidang            = split_bidang[0]+'.'+split_bidang[1]
                    kdprogram           = split_bidang[3]
                    kdkegiatan          = split_bidang[4]
                    kdakun              = split_kegiatan[0]
                    kdkelompok          = split_kegiatan[1]
                    kdjenis             = split_kegiatan[2]
                    kdobjek             = split_kegiatan[3]
                    kdrincian           = split_kegiatan[4]

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,NOSPM,"
                        "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                        "KODERINCIANOBJEK,JUMLAH,TANGGAL)"
                        " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,\
                        kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,\
                        kdrincian,jumlah_spm,tgl_draft])

                with connections[tahun_log(request)].cursor() as cursor:
                    cursor.execute("DELETE FROM penatausahaan.spmpotongan where TAHUN=%s and KODEURUSAN = %s and KODESUBURUSAN = %s and KODEORGANISASI = %s and NOSPM = %s",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, no_spm])
                    
                for p in range(len(rekening_potongan)):
                    if rekening_potongan[p] != "":
                        with connections[tahun_log(request)].cursor() as cursor:
                            cursor.execute("INSERT INTO penatausahaan.spmpotongan (TAHUN,KODEURUSAN,KODESUBURUSAN,\
                                KODEORGANISASI,NOSPM,TANGGAL,REKENINGPOTONGAN,JUMLAH,JENISPOTONGAN) \
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,no_spm,tgl_draft,
                                rekening_potongan[p],toAngkaDec(jumlah_potongan[p]),jenis_potongan[p]])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')

def spm_save_ls(request,jenis_spm):
    hasil=''
    if 'sipkd_username' in request.session:

        if request.method == 'POST':

            org = request.POST.get('skpd', '').split('.')
            kdurusan             = request.POST.get('kdurusan','')
            kdsuburusan          = request.POST.get('kdsuburusan','')
            kdorganisasi         = request.POST.get('kdorganisasi','')
            kdunit               = request.POST.get('kdunit','')
            no_spm               = request.POST.get('no_spm').upper()
            no_spm_lama          = request.POST.get('no_spm_lama').upper()
            tgl                  = tgl_short(request.POST.get('tgl_spm'))
            tgl_draft            = tgl_short(request.POST.get('tgl_spm'))
            deskripsi_spp        = request.POST.get('deskripsi_spp')
            no_spp               = request.POST.get('no_spp')
            tgl_spp              = tgl_short(request.POST.get('tgl_spp'))
            jml_spp              = toAngkaDec(request.POST.get('jml_spp'))
            jml_spm              = toAngkaDec(request.POST.get('jml_spp'))
            update_jml_spm       = toAngkaDec(request.POST.get('jml_spp_x'))
            update_jml_spp       = toAngkaDec(request.POST.get('jml_spp_x'))
            nama_yang_berhak     = request.POST.get('nama_bendahara')
            no_rek               = request.POST.get('norek_bendahara')
            bank                 = request.POST.get('nama_bank')
            # jenis_spm            = request.POST.get('jenis_spm')
            perubahan            = request.POST.get('perubahan')
            npwp                 = str(request.POST.get('npwp'))
            informasi            = request.POST.get('informasi')
            status_keperluan     = request.POST.get('status_keperluan')
            triwulan             = request.POST.get('triwulan')
            last_update          = update_tgl(request)['now']
            aksi                 = request.POST.get('aksi')
            afektasi             = request.POST.get('spm_sekarang')
            rekening1            = json.loads(request.POST.get('spm_rekening1'))
            rekening_potongan    = json.loads(request.POST.get('rekening_potongan'))
            # uraian_potongan      = request.POST.get('uraian_potongan')
            jumlah_potongan      = json.loads(request.POST.get('jumlah_potongan'))
            jenis_potongan       = json.loads(request.POST.get('jenis_potongan'))
            idbiling             = json.loads(request.POST.get('idbiling'))
            ntpn                 = json.loads(request.POST.get('ntpn'))
            kdbidang             = ''
            kdbidang             = ''
            kdakun               = ''
            kdkelompok           = ''
            kdjenis              = ''
            kdobjek              = ''
            kdrincian            = ''

            is_next = False

            if no_spm != "":
                if aksi == "true":
                    with connections[tahun_log(request)].cursor() as cursor:
                        # print("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                        #     "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                        #     " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        #     [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,
                        #     jml_spm,'',nama_yang_berhak,no_rek,bank,'LS',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])

                        cursor.execute("INSERT INTO penatausahaan.spm (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,TANGGAL_DRAFT,KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,"
                            "DESKRIPSISPP,NOSPP,TGLSPP,JUMLAHSPP,JUMLAHSPM,PEMEGANGKAS,NAMAYANGBERHAK,NOREKBANK,BANK,JENISSPM,PERUBAHAN,NPWP,INFORMASI,STATUSKEPERLUAN,LASTUPDATE,TRIWULAN,UNAME)"
                            " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl,tgl_draft,'',0,0,deskripsi_spp,no_spp,tgl_spp,jml_spp,
                            jml_spm,'',nama_yang_berhak,no_rek,bank,'LS',perubahan,npwp,informasi,status_keperluan,last_update,triwulan,username(request)])
                        
                        hasil = "Data SPM dengan nomor : "+no_spm+" berhasil disimpan!"
                    is_next = True

                elif aksi == "false":
                    try:
                        with connections[tahun_log(request)].cursor() as cursor: # if jenis_spm=='ls_ppkd':
                            cursor.execute("UPDATE penatausahaan.spm SET NOSPM=%s, TANGGAL=%s, TANGGAL_DRAFT=%s,"
                                "DESKRIPSISPP=%s, NOSPP=%s, TGLSPP=%s, JUMLAHSPP=%s, JUMLAHSPM=%s, NAMAYANGBERHAK=%s,"
                                "NOREKBANK=%s, BANK=%s, INFORMASI=%s, STATUSKEPERLUAN=%s, NPWP=%s, TRIWULAN=%s"
                                "WHERE TAHUN=%s and KODEURUSAN=%s and KODESUBURUSAN=%s and KODEORGANISASI=%s and KODEUNIT=%s and NOSPM=%s",
                                [no_spm,tgl,tgl_draft,
                                deskripsi_spp,no_spp,tgl_spp,update_jml_spp,update_jml_spm,nama_yang_berhak,
                                no_rek,bank,informasi,status_keperluan,npwp,triwulan,
                                tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm_lama])
                            hasil = "Data SPM dengan nomor "+no_spm+" berhasil diubah!"
                        is_next = True
                    except Exception as e:
                        hasil = "SPM telah disetujui, tidak diperkenankan mengubah atau menghapus data"

                if is_next:
                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("DELETE FROM penatausahaan.spmrincian where tahun=%s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodeunit=%s and NOSPM = %s",
                            [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm_lama])

                    with connections[tahun_log(request)].cursor() as cursor:
                        cursor.execute("DELETE FROM penatausahaan.spmpotongan where TAHUN=%s and KODEURUSAN = %s \
                            and KODESUBURUSAN = %s and KODEORGANISASI = %s and KODEUNIT = %s and NOSPM = %s",
                            [tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, no_spm])

                    for x in range(len(rekening1)):              
                        rekening            = rekening1[x].split('|')[0]
                        jumlah_spm          = rekening1[x].split('|')[1]
                        pisah_rekening      = rekening.split('-')[0]
                        pisah_kegiatan      = rekening.split('-')[1]
                        split_bidang        = pisah_rekening.split('.') # 0001. 1. 01 .01 .1 .2. 01 .001
                        split_kegiatan      = pisah_kegiatan.split('.') # 5. 1. 1. 03 .07 .002

                        kdbidang            = split_bidang[1]+'.'+split_bidang[2] # 1.01
                        kdprogram           = split_bidang[4] # 1
                        kdkegiatan          = split_bidang[5]+'.'+split_bidang[6] # 2.01
                        kdsubkegiatan       = split_bidang[7] # 001

                        kdakun              = split_kegiatan[0]
                        kdkelompok          = split_kegiatan[1]
                        kdjenis             = split_kegiatan[2]
                        kdobjek             = split_kegiatan[3]
                        kdrincian           = split_kegiatan[4]
                        kdsubrincian        = split_kegiatan[5]
                        
                        with connections[tahun_log(request)].cursor() as cursor:
                            cursor.execute("INSERT INTO penatausahaan.spmrincian (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSPM,"
                                "KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,"
                                "KODERINCIANOBJEK,KODESUBRINCIANOBJEK,JUMLAH,TANGGAL)"
                                " VALUES (%s,%s,%s,lpad(%s,2,'0'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                [tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,\
                                kdbidang,kdprogram,kdkegiatan,kdsubkegiatan,0,kdakun,kdkelompok,kdjenis,kdobjek,\
                                kdrincian,kdsubrincian,jumlah_spm,tgl_draft])

                    if len(idbiling) == 0 or len(idbiling) != len(rekening_potongan):
                        idbiling.append('-')

                    if len(ntpn) == 0 or len(ntpn) != len(rekening_potongan):
                        ntpn.append('-')

                    for p in range(len(rekening_potongan)):
                        if rekening_potongan[p] != "":
                            with connections[tahun_log(request)].cursor() as cursor:
                                cursor.execute("INSERT INTO penatausahaan.spmpotongan (TAHUN,KODEURUSAN,KODESUBURUSAN,\
                                    KODEORGANISASI,KODEUNIT,NOSPM,TANGGAL,REKENINGPOTONGAN,JUMLAH,JENISPOTONGAN, idbiling, ntpn) \
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdunit,no_spm,tgl_draft,
                                    rekening_potongan[p],toAngkaDec(jumlah_potongan[p]),jenis_potongan[p], idbiling[p], ntpn[p]])

            return HttpResponse(hasil)
    else:
        return redirect('sipkd:index')
