from sipkd.config import *
from django.db import connection,connections
from django.urls import reverse,resolve
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template import RequestContext
import datetime, decimal
import re
import json

def template(request):
	organisasi = ''
	organisasi_ppkd = ''
	persetujuan_spm = ''
	kegiatan = ''
	organisasi_ppkd = ''
	btn_bendahara = ''
	btn_rekening = ''
	btn_simpan = ''
	btn_hapus  = ''
	btn_cetak	= ''
	btn_edit    =''
	btn_lihat_spd = ''
	btn_tambah_spd = ''
	btn_lihat_spp = ''
	btn_tambah_spp = ''
	btn_lihat_spm = ''
	btn_lihat_spm_ls = ''
	btn_tambah_spm = ''
	btn_lihat_sp2d = ''
	btn_tambah_sp2d = ''
	btn_tambah_data = ''
	btn_setuju	= ''
	btn_unlock	= ''
	btn_next = ''
	btn_prev = ''
	src_bend_pihak3 = ''
	src_spm = ''
	btn_tambah = ''
	btn_cetak_modal = ''		
	btn_spp_spm = ''
	lihat_rekening_pendapatan = ''
	btn_lihat_sumberdana = ''
	
	if (tahun_log(request)):
		skpd = set_organisasi(request)

		if hakakses(request) not in tanggal(request)['bukan_admin']:
			organisasi='  <input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="">\
	                <input type="hidden" id="kd_org2" value="">\
	                <input type="hidden" id="kd_org2_urai" value="">\
	                <span class="input-group-addon btn btn-primary" onclick="showModal(this,\'list_org\')" title="Cari Data" alt="'+reverse('sipkd:list_organisasi')+'" id="cari_data_organisasi">\
	                	<i class="fa fa-binoculars"></i>\
	                </span>'

			kegiatan='  <input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_keg" value="" placeholder="Kegiatan">\
	                <input type="hidden" id="kd_keg2" value="">\
	                <input type="hidden" id="kd_keg2_urai" value="">\
	                <span class="input-group-addon btn btn-primary" onclick="showModal(this,\'list_keg\')" title="Cari Data" alt="'+reverse('sipkd:list_kegiatan')+'" id="cari_data_kegiatan">\
	                	<i class="fa fa-binoculars"></i>\
	                </span>'

			persetujuan_spm='  <input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="" placeholder="Organisasi">\
	                <input type="hidden" id="kd_org2" value="" onChange="LoadData_Persetujuan_SPM(this.value)">\
	                <input type="hidden" id="kd_org2_urai" value="">\
	                <span class="input-group-addon btn btn-primary" onclick="showModal(this,\'list_org\')" title="Cari Data" alt="'+reverse('sipkd:list_organisasi')+'" id="cari_data_organisasi">\
	                	<i class="fa fa-binoculars"></i>\
	                </span>'

		else:
			organisasi = '<input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="'+skpd["skpd"]+'">\
	                <input type="hidden" id="kd_org2" value="'+skpd["kode"]+'">\
	                <input type="hidden" id="kd_org2_urai" value="'+skpd["urai"]+'">\
	                <span class="input-group-addon"><i class="fa fa-binoculars"></i></span>'

	    # TOMBOL TOMBOL 
		btn_simpan = '<div class="btn btn-sm btn-success" style="width:100%;" title="Simpan Data" id="btn_simpan">\
			            <i class="fa fa-floppy-o"></i>&nbsp;&nbsp;Simpan\
			        </div>'
		btn_hapus  = '<div class="btn btn-sm btn-danger" style="width:100%;" title="Hapus Data" id="btn_hapus">\
			            <i class="fa fa-trash-o"></i>&nbsp;&nbsp;Hapus\
			        </div>'
		btn_cetak	= '<div class="btn btn-sm btn-warning" style="width:100%;" title="Cetak Data" id="btn_cetak">\
			            <i class="fa fa-print"></i>&nbsp;&nbsp;Cetak\
			        </div>'
		btn_edit    = '<div class="btn btn-sm btn-info" style="width:100%;" title="Edit Data" id="btn_edit">\
			            <i class="fa fa-pencil"></i>&nbsp;&nbsp;Edit\
			        </div>'		
		btn_cetak_modal	= '<div class="btn btn-sm btn-warning" style="width:100%;" title="Cetak Data" id="btn_cetak_modal">\
			            <i class="fa fa-print"></i>&nbsp;&nbsp;Cetak\
			        </div>'		
		btn_lihat_spd = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Data SPD" id="btn_lihat_spd">\
			            	<i class="fa fa-search"></i>&nbsp;&nbsp;LIHAT SPD\
			        	</div>'
		btn_tambah_spd = '<div class="btn btn-sm btn-success" style="width:100%;" title="Tambah Data SPD" id="btn_tambah_spd">\
				            	<i class="fa fa-plus-square"></i>&nbsp;&nbsp;SPD BARU\
				        	</div>'
		btn_lihat_spp = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Data SPD" id="btn_lihat_spd">\
			            	<i class="fa fa-search"></i>&nbsp;&nbsp;LIHAT SPD\
			        	</div>'
		btn_tambah_spp = '<div class="btn btn-sm btn-success" style="width:100%;" title="Tambah Data SPD" id="btn_tambah_spd">\
				            	<i class="fa fa-plus-square"></i>&nbsp;&nbsp;SPD BARU\
				        	</div>'
		btn_lihat_spm = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Data SPM" id="btn_lihat_spm">\
			            	<i class="fa fa-search"></i>&nbsp;&nbsp;LIHAT SPM\
			        	</div>'
		btn_lihat_spm_ls = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Data SPM" id="btn_lihat_spm_ls">\
			            	<i class="fa fa-search"></i>&nbsp;&nbsp;LIHAT SPM\
			        	</div>'
		btn_tambah_spm = '<div class="btn btn-sm btn-success" style="width:100%;" title="Tambah Data SPM" id="btn_tambah_spm">\
				            	<i class="fa fa-plus-square"></i>&nbsp;&nbsp;SPM BARU\
				        	</div>'
		btn_lihat_sp2d = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Data SP2D" id="btn_lihat_sp2d">\
			            	<i class="fa fa-search"></i>&nbsp;&nbsp;LIHAT SP2D\
			        	</div>'
		btn_tambah_sp2d = '<div class="btn btn-sm btn-success" style="width:100%;" title="Tambah Data SP2D" id="btn_tambah_sp2d">\
				            	<i class="fa fa-plus-square"></i>&nbsp;&nbsp;SP2D BARU\
				        	</div>'
		btn_tambah_data = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Tambah Data" id="btn_tambah_data">\
					            <i class="fa fa-floppy-o"></i>&nbsp;&nbsp;Tambah\
					        </div>'
		btn_setuju = '<div class="btn btn-sm btn-primary" style="width:100%;" id="btn_setuju" title="Setujui">\
	                <i class="fa fa-check-square"></i>&nbsp;Proses Setujui\
	                </div>'
		btn_unlock = '<div class="btn btn-sm btn-primary" style="width:100%;" id="btn_unlock" title="Unlock">\
	                <i class="fa fa-unlock"></i>&nbsp;Unlock\
	                </div>'
		btn_next = '<div class="btn btn-sm btn-primary" style="width:100%;" id="btn_next" title="Next">\
						<i class="fa fa-arrow-right"></i>&nbsp;Next\
					</div>'
		btn_prev = '<div class="btn btn-sm btn-primary" style="width:100%;" id="btn_prev" title="Previous">\
						<i class="fa fa-arrow-left"></i>&nbsp;Back\
					</div>'
		#organisasi_ppkd = '  <input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="'+get_PPKD(request)[0]['kode']+' - '+get_PPKD(request)[0]['urai']+'">\
	       #         <input type="hidden" id="kd_org2" value="'+get_PPKD(request)[0]['kode']+'">\
	       #         <input type="hidden" id="kd_org2_urai" value="'+get_PPKD(request)[0]['urai']+'">\
	       #         <span class="input-group-addon btn" title="Cari Data"  disabled="disabled" id="cari_data_organisasi">\
	       #         	<i class="fa fa-binoculars"></i>\
	       #         </span>'
		src_bend_pihak3 = '<div class="input-group">\
		    		<input type="text" class="form-control input-sm" value="" \
		    		placeholder="Bendahara Pengeluaran / Pihak Ketiga" id="bendahara" name="bendahara">\
		    		<label class="input-group-addon baten" for="bendahara" id="src_bend_pihak3"\
		    		style="cursor: pointer;"><i class="fa fa-search-plus"></i></label>\
            	</div>'
		src_spm = '<div class="input-group">\
            		<input type="text" class="form-control input-sm" value=""\
                    	placeholder="No. SPM" id="no_spm" name="no_spm" style="text-transform: uppercase;">\
				  	<label class="input-group-addon baten" for="no_spm" id="src_spm"\
				  		style="cursor: pointer;"><i class="fa fa-search-plus"></i></label>\
            	</div>'
		btn_tambah = '<div class="btn btn-sm btn-success" style="width:100%;" title="Tambah Data" id="btn_tambah">\
					<i class="fa fa-plus-square"></i>&nbsp;&nbsp;Tambah</div>'
		btn_spp_spm = '<label class="input-group-addon baten" for="no_spp" id="btn_spp_spm" style="cursor: pointer;"> <i class="fa fa-search-plus"></i></label>'
		btn_bendahara = '<label class="input-group-addon baten" for="bendahara" id="btn_bendahara" style="cursor: pointer;"> <i class="fa fa-search-plus"></i></label>'
		btn_rekening = '<label class="input-group-addon baten" for="rekening" id="btn_rekening" style="cursor: pointer;"> <i class="fa fa-search-plus"></i></label>'
		lihat_rekening_pendapatan = '<span class="btn btn-sm btn-primary btn_dlm_tabel lihat_rekening_pendapatan" title="Lihat Data" id="lihat_rekening_pendapatan" onClick="fungsi_tombol_rekening()">\
				        		<i class="fa fa-binoculars"></i>\
				        	</span>'
		btn_lihat_sumberdana = '<div class="btn btn-sm btn-primary" style="width:100%;" title="Lihat Sumberdana" id="btn_lihat_sumberdana">\
			            	<i class="fa fa-search"></i>&nbsp;\
			        	</div>'

	return {'organisasi':organisasi,'kegiatan':kegiatan,'persetujuan_spm':persetujuan_spm,'btn_bendahara':btn_bendahara,'btn_simpan':btn_simpan,'btn_hapus':btn_hapus,'btn_cetak':btn_cetak, 'btn_cetak_modal':btn_cetak_modal,'btn_edit':btn_edit,	'btn_lihat_spd':btn_lihat_spd,'btn_lihat_spp':btn_lihat_spp,'btn_lihat_spm':btn_lihat_spm,
			'btn_lihat_sp2d':btn_lihat_sp2d,'btn_tambah_spd':btn_tambah_spd,'btn_tambah_spp':btn_tambah_spp,
			'btn_tambah_spm':btn_tambah_spm,'btn_lihat_spm':btn_lihat_spm,'btn_lihat_spm_ls':btn_lihat_spm_ls,'btn_tambah_sp2d':btn_tambah_sp2d,'btn_tambah_data':btn_tambah_data,
			'btn_setuju':btn_setuju,'btn_unlock':btn_unlock,'btn_next':btn_next,'btn_prev':btn_prev,'organisasi_ppkd':organisasi_ppkd,
			'src_bend_pihak3':src_bend_pihak3,'src_spm':src_spm,'btn_tambah':btn_tambah,'btn_spp_spm':btn_spp_spm,'btn_rekening':btn_rekening,'btn_organisasi_spm':organisasi,'btn_organisasi_data_spjskpd':organisasi,'lihat_rekening_pendapatan':lihat_rekening_pendapatan,
			'btn_lihat_sumberdana':btn_lihat_sumberdana,}

def list_organisasi(request):
	list_organisasi = ''
	
	if hakakses(request) == 'ADMIN' or hakakses(request) == 'ADMINANGGARAN' or hakakses(request) == 'KABIDANGGARAN' or hakakses(request) == 'VERIFIKASI' or hakakses(request) =='KABIDAKUNTANSI' or hakakses(request) =='AKUNTANSI':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT skpkd, kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi,\
				kodeunit, urai, skpkd FROM master.master_organisasi\
				WHERE tahun = %s and kodeurusan <> 0 and kodesuburusan <> 0 and kodeorganisasi <> '' and kodeunit <> ''\
				ORDER BY kodeurusan,kodesuburusan,kodeorganisasi,kodeunit",[tahun_log(request)])
			list_organisasi = dictfetchall(cursor)
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi, \
				kodeunit, urai, skpkd FROM view_organisasi_user(%s,%s,%s,%s) \
				WHERE pilih = 1",[tahun_log(request), username(request).upper(), hakakses(request), 2])
			list_organisasi = dictfetchall(cursor)
	
	data={



		'list_organisasi':list_organisasi
	}
	return render(request,'base/modal/modal_listorg.html',data)

def is_skpkd(request):
	var_tahun = tahun_log(request)
	var_kdurusan = request.POST.get('g','').split('.')[0]
	var_kdsuburusan = request.POST.get('g','').split('.')[1]
	var_kdorganisasi = request.POST.get('g','').split('.')[2]

	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT skpkd FROM master.master_organisasi WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s", [var_tahun, var_kdurusan, var_kdsuburusan, var_kdorganisasi])
		hasil = cursor.fetchone()
	
	return HttpResponse(hasil)

def list_kegiatan(request):
	kduru = request.GET.get('kdurusan','')
	kdsub = request.GET.get('kdsuburusan','')
	kdorg = request.GET.get('kdorganisasi','')
	kduni = request.GET.get('kdunit','')

	# if hakakses(request) == 'ADMIN' or hakakses(request) == 'ADMINANGGARAN' or hakakses(request) == 'KABIDANGGARAN':
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,URAI \
			FROM penatausahaan.kegiatan WHERE TAHUN = %s AND KODEURUSAN= %s \
			AND KODESUBURUSAN = %s AND KODEORGANISASI = %s AND KODEKEGIATAN <> '0' AND KODESUBKEGIATAN <> 0\
			ORDER BY KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN",
			[tahun_log(request),kduru,kdsub,kdorg])
		list_kegiatan = dictfetchall(cursor)

	data={
		'list_kegiatan':list_kegiatan
	}
	return render(request,'base/modal/modal_listkeg.html', data)

def get_arg(request,asal,js_arg):
	arg = ""
	qry_tbl = ""
	kolom = ""
	group_by = ""
	order_by = ""
	table_column = "MODAL"
	query = "no"
	tahun = str(tahun_log(request))
	qry_tbl_argument = []
	is_safe = False

	if asal!='':
		if asal == 'spd':
			if (hakakses(request) == "ANGGARAN"):
				if (username(request)!=''):
					arg = "AND kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ("+hakakses_user(request, username(request))['kode']+")"
				else:
					arg = "AND kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ('')"
			else:
				arg = ""

			kolom = "s.nospd,s.tanggal,s.tgldpa,(select o.KODEURUSAN||'.'||o.KODESUBURUSAN||'.'||o.KODEORGANISASI||'.'||o.KODEUNIT||' - '||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.pergeseran,s.jumlahspd,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit"
			qry_tbl = "penatausahaan.spd s  where s.tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = "ORDER BY s.nospd"			
			table_column = 'NOSPD,TANGGAL,TANGGAL DPA,SKPD,PERGESERAN,JUMLAH'
			query = "yes"
		elif asal == 'sp2d_src_bendahara':
			arg = "WHERE TAHUN = '"+tahun+"'"
			qry_tbl = "penatausahaan.SP2D"
			kolom = "DISTINCT NOREKBANK,BANK AS NAMABANK,NPWP,NAMAYANGBERHAK AS NAMA,COUNT(DISTINCT NOREKBANK) AS ID"
			group_by = "GROUP BY NOREKBANK,BANK,NPWP,NAMAYANGBERHAK"
			order_by = "ORDER BY NOREKBANK"
			table_column = 'NO REKENING,NAMA BANK,NPWP,NAMA BENDAHARA / PIHAK KETIGA'
			query = "yes"

		elif asal == 'btn_lihat_sp2d':
			skpd 	= js_arg[0].split(".")
			kdur 	= str(skpd[0])
			kdsub 	= str(skpd[1])
			kdorg 	= str(skpd[2])
			jnsSPM 	= str(js_arg[1])

			arg = "where s.tahun = '"+tahun+"' and s.kodeurusan = "+kdur+" \
				and s.kodesuburusan = "+kdsub+" and kodeorganisasi = '"+kdorg+"' and s.jenissp2d = '"+jnsSPM+"'"
			qry_tbl = "penatausahaan.SP2D s"
			kolom = "s.nosp2d,s.tanggal,s.NOSPM,(select o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan \
				and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi ) as organisasi, \
				s.statuskeperluan as keperluan,\
				(select sum (jumlah) from penatausahaan.sp2drincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan\
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.nosp2d=s.nosp2d ) as jumlah \
				,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi"
			group_by = ""
			order_by = "ORDER BY s.tanggal,s.nosp2d"
			table_column = 'NO SP2D,TANGGAL,NO SPM,ORGANISASI,KEPERLUAN,JUMLAH'
			query = "yes"

		elif asal == 'src_spm':
			skpd 	= js_arg[0].split(".")
			kdur 	= str(skpd[0])
			kdsub 	= str(skpd[1])
			kdorg 	= str(skpd[2])
			kdunit 	= str(skpd[3])
			jnsSPM 	= str(js_arg[1]).upper()

			arg = "where s.tahun ='"+tahun+"' and s.kodeurusan = "+kdur+" \
				and s.kodesuburusan = "+kdsub+" and s.kodeorganisasi = '"+kdorg+" and s.kodeunit='"+kdunit+"' ' \
				and s.jenisspm='"+jnsSPM+"' and  locked = 'Y' \
				and (nospm not in (select nospm from penatausahaan.sp2d where tahun = '"+tahun+"' \
				and kodeurusan = "+kdur+" and kodesuburusan = "+kdsub+" \
				and kodeorganisasi = '"+kdorg+"' and kodeunit='"+kdunit+"' and jenissp2d ='"+jnsSPM+"'))"
			qry_tbl = "penatausahaan.spm s"
			kolom = "s.nospm,s.tanggal,(select o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan\
				and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.statuskeperluan as keperluan, \
				(select sum (jumlah) from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan \
				and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm ) as jumlah, \
				s.kodeurusan,s.kodesuburusan,s.kodeorganisasi"
			group_by = ""
			order_by = "ORDER BY s.tanggal,s.NOSPM"
			table_column = 'NO SPM,TANGGAL,ORGANISASI,KEPERLUAN,JUMLAH'
			query = "yes"		
		elif asal == 'spm_sp2d':
			kd_urusan = js_arg[0].split('.')[0]
			kd_suburusan = js_arg[0].split('.')[1]
			kd_organisasi = js_arg[0].split('.')[2]
			kd_unit = js_arg[0].split('.')[3]

			arg = "WHERE TRIM(o_JENISSPM)='"+js_arg[1]+"' AND o_LOCKED= 'Y' and(o_nospm not in (select nospm from penatausahaan.sp2d where tahun='"+tahun_log(request)+"' and kodeurusan="+kd_urusan+" and kodesuburusan="+kd_suburusan+" and kodeorganisasi='"+kd_organisasi+"' and kodeunit='"+kd_unit+"'))"
	
			kolom = "o_NOSPM,o_TANGGAL,o_ORGANISASI,o_KEPERLUAN,o_JUMLAH,o_KODEURUSAN,o_KODESUBURUSAN,o_KODEORGANISASI,o_KODEBIDANG,o_KODEPROGRAM,o_KODEKEGIATAN"
			qry_tbl = "penatausahaan.fc_lihat_spm_for_sp2d('"+tahun_log(request)+"',"+kd_urusan+","+kd_suburusan+",'"+kd_organisasi+"','"+kd_unit+"')"
			group_by = ""
			order_by = "ORDER BY o_NOSPM"
			table_column = 'NOSPM,TANGGAL,ORGANISASI,JUMLAH'
			query = "yes"
		elif asal == 'sp2d_up':
			kolom = "s.nosp2d,s.tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||o.kodeorganisasi||'.'||o.kodeunit||'-'||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit) as organisasi,s.statuskeperluan as keperluan,s.nospm,s.jumlahsp2d as jumlah,s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit"
			qry_tbl = "penatausahaan.sp2d s  where s.tahun='"+tahun_log(request)+"' and s.jenissp2d='UP'"
			group_by = ""
			order_by = "ORDER BY tanggal, nosp2d"
			table_column = 'NOSP2D,TANGGAL,ORGANISASI,KEPERLUAN,NOSPM,JUMLAH'
			query = "yes"
		elif asal == 'lht_bdhr':
			kolom = "distinct norekbank,bank,npwp,namayangberhak"
			qry_tbl = "penatausahaan.sp2d where tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = ""
			table_column = 'NOREKBANK,BANK,NPWP,NAMAYANGBERHAK'
			query = "yes"
		elif asal=='pejabat_lap_spd':
			arg = "where jenissistem=2 and tahun='"+tahun_log(request)+"' and upper(jabatan) like '%%BENDAHARA UMUM%%' "
			kolom = "id, NAMA,NIP,pangkat, jabatan||' ('||nama||')' AS JABATAN1"
			qry_tbl = "master.pejabat_skpkd"
			group_by = ""
			order_by = ""
			table_column = 'ID,NAMA,NIP,PANGKAT'
			query = "yes"
		elif asal =='cari_kegiatan_rkpa':
			kd_urusan = js_arg[0].split('.')[0]
			kd_suburusan = js_arg[0].split('.')[1]
			kd_organisasi = js_arg[0].split('.')[2]
			kd_unit = js_arg[0].split('.')[3]

			kolom = "*"
			qry_tbl = "penatausahaan.fc_view_keg_browse('"+tahun_log(request)+"',"+kd_urusan+","+kd_suburusan+",'"+kd_organisasi+"','"+kd_unit+"')"
			group_by = ""
			order_by = "ORDER BY o_kodebidang,o_kodeprogram,o_kodekegiatan,o_kodesubkegiatan"
			table_column = 'KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,URAI'
			query = "yes"
		elif asal =='rekening_rkpa':
			kd_urusan = js_arg[0].split('.')[0]
			kd_suburusan = js_arg[0].split('.')[1]
			kd_organisasi = js_arg[0].split('.')[2]
			kd_unit = js_arg[0].split('.')[3]

			kd_bidang = js_arg[1].split(' - ')[0].split('.')[0]+'.'+js_arg[1].split(' - ')[0].split('.')[1]
			kd_program = js_arg[1].split(' - ')[0].split('.')[2]
			kd_kegiatan = js_arg[1].split(' - ')[0].split('.')[3]+'.'+js_arg[1].split(' - ')[0].split('.')[4]
			kd_subkegiatan = js_arg[1].split(' - ')[0].split('.')[5]

			kolom = "*"
			qry_tbl = "penatausahaan.fc_view_browse_rekening('"+tahun_log(request)+"',"+kd_urusan+","+kd_suburusan+",'"+kd_organisasi+"','"+kd_unit+"','"+kd_bidang+"',"+kd_program+",'"+kd_kegiatan+"',"+kd_subkegiatan+")"
			group_by = ""
			order_by = ""
			table_column = 'KODE,URAI'
			query = "yes"
		elif asal == 'sp2d_gu':
			if (hakakses(request) == "BELANJA"):
				if (username(request)!=''):
					arg = "and JENISSP2D='GU' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi in ("+username(request)+")"
				else:
					arg = "and JENISSP2D='GU' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi in ('')"
			else:
				arg = "and JENISSP2D='GU'"			
			kolom = "s.nosp2d,s.tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||o.kodeorganisasi||'-'||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi ) as organisasi,s.statuskeperluan as keperluan,s.nospm,s.jumlahsp2d as jumlah"
			qry_tbl = "penatausahaan.sp2d s  where s.tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = "ORDER BY tanggal, nosp2d"
			table_column = 'NOSP2D,TANGGAL,ORGANISASI,KEPERLUAN,NOSPM,JUMLAH'
			query = "yes"
		elif asal == 'sp2d_tu':
			if (hakakses(request) == "BELANJA"):
				if (username(request)!=''):
					arg = "and JENISSP2D='TU' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi in ("+username(request)+")"
				else:
					arg = "and JENISSP2D='TU' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi in ('')"
			else:
				arg = "and JENISSP2D='TU'"
			
			kolom = "s.nosp2d,s.tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||o.kodeorganisasi||'-'||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi ) as organisasi,s.statuskeperluan as keperluan,s.nospm,s.jumlahsp2d as jumlah"
			qry_tbl = "penatausahaan.sp2d s  where s.tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = "ORDER BY tanggal, nosp2d"
			table_column = 'NOSP2D,TANGGAL,ORGANISASI,KEPERLUAN,NOSPM,JUMLAH'
			query = "yes"
		elif asal == 'sp2d_gunihil':
			if (hakakses(request) == "BELANJA"):
				if (username(request)!=''):
					arg = "and JENISSP2D='GU_NIHIL' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ("+username(request)+")"
				else:
					arg = "and JENISSP2D='GU_NIHIL' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ('')"
			else:
				arg = "and JENISSP2D='GU_NIHIL'"
			
			kolom = "s.nosp2d,s.tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||o.kodeorganisasi||'.'||o.kodeunit||'-'||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.statuskeperluan as keperluan,s.nospm,s.jumlahsp2d as jumlah"
			qry_tbl = "penatausahaan.sp2d s  where s.tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = "ORDER BY tanggal, nosp2d"
			table_column = 'NOSP2D,TANGGAL,ORGANISASI,KEPERLUAN,NOSPM,JUMLAH'
			query = "yes"

		elif asal == 'sp2d_tunihil':
			if (hakakses(request) == "BELANJA"):
				if (username(request)!=''):
					arg = "and JENISSP2D='TU_NIHIL' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ("+username(request)+")"
				else:
					arg = "and JENISSP2D='TU_NIHIL' and  kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ('')"
			else:
				arg = "and JENISSP2D='TU_NIHIL'"
			
			kolom = "s.nosp2d,s.tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||o.kodeorganisasi||'.'||o.kodeunit||'-'||o.urai from master.master_organisasi o where o.tahun=s.tahun and o.kodeurusan=s.kodeurusan and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,s.statuskeperluan as keperluan,s.nospm,s.jumlahsp2d as jumlah"
			qry_tbl = "penatausahaan.sp2d s  where s.tahun='"+tahun_log(request)+"'"
			group_by = ""
			order_by = "ORDER BY tanggal, nosp2d"
			table_column = 'NOSP2D,TANGGAL,ORGANISASI,KEPERLUAN,NOSPM,JUMLAH'
			query = "yes"

		elif asal == 'SPP':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			kodeunit = js_arg[0].split('.')[3]
				
			arg = "WHERE o.tahun=s.tahun and o.kodeurusan=s.kodeurusan \
					and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit = s.kodeunit ) as organisasi,\
					s.deskripsispp as keperluan, \
					(select (case when sum(sr.jumlah) is null then 0 else sum(sr.jumlah) end) from penatausahaan.spprincian \
					sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp) \
					as jumlah, \
					s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit FROM penatausahaan.spp s\
					where s.tahun='"+tahun_log(request)+"' and s.kodeurusan="+kodeurusan+"  and s.kodesuburusan="+kodesuburusan+" and s.kodeorganisasi='"+kodeorganisasi+"'\
					and s.jenisspp='"+js_arg[1]+"' and locked='Y' and  s.nospp not in (select nospp from penatausahaan.spm where tahun='"+tahun_log(request)+"' and kodeurusan="+kodeurusan+"  \
					and kodesuburusan="+kodesuburusan+" and kodeorganisasi='"+kodeorganisasi+"')"
			qry_tbl = "master.master_organisasi o"
			kolom = "s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai"
			order_by = "ORDER BY nospp"
			table_column = 'NOSPP,TANGGAL,ORGANISASI,KEPERLUAN,JUMLAH'
			query = "yes"

		elif asal == 'SPM':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			kodeunit= js_arg[0].split('.')[3]	
			
			arg = " WHERE o.tahun=s.tahun and o.kodeurusan=s.kodeurusan \
					and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit) as organisasi,\
					s.statuskeperluan as keperluan, s.nospp, \
					(select (case when sum(sr.jumlah) is null then 0 else sum(sr.jumlah) end) from penatausahaan.spmrincian \
					sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm) \
					as jumlah, \
					s.kodeurusan,s.kodesuburusan,s.kodeorganisasi,s.kodeunit FROM penatausahaan.spm \
					s  where s.tahun='"+tahun_log(request)+"' and s.kodeurusan="+kodeurusan+"  and s.kodesuburusan="+kodesuburusan+" and s.kodeorganisasi='"+kodeorganisasi+"' \
					and s.jenisspm='"+js_arg[1]+"'"
			qry_tbl = "master.master_organisasi o"
			kolom = "s.nospm,s.tanggal as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai"
			order_by = "ORDER BY nospm"
			table_column = 'NOSPM,TANGGAL,ORGANISASI,KEPERLUAN,NOSPP,JUMLAH'
			query = "yes"

		elif asal == 'SPM_LS':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			
			arg = "WHERE o.tahun=s.tahun and o.kodeurusan=s.kodeurusan \
					and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,\
					s.statuskeperluan as keperluan, s.nospp, \
					(select sum (sr.jumlah) from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm) \
					as jumlah, \
					(select kodebidang from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1) \
					as kodebidang, \
					(select kodeprogram from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1) \
					as kodeprogram, \
					(select kodekegiatan from penatausahaan.spmrincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospm=s.nospm limit 1) \
					as kodekegiatan FROM penatausahaan.spm \
					s  where s.tahun='"+tahun_log(request)+"' and s.kodeurusan="+kodeurusan+"  and s.kodesuburusan="+kodesuburusan+" and s.kodeorganisasi='"+kodeorganisasi+"' \
					and s.jenisspm='"+js_arg[1]+"'"
			qry_tbl = "master.master_organisasi o"
			kolom = "s.nospm,s.tanggal as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai"
			order_by = "ORDER BY nospm, tanggal"
			table_column = 'NOSPM,TANGGAL,ORGANISASI,KEPERLUAN,NOSPP,JUMLAH'
			query = "yes"

		elif asal == 'SPP_LS':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			# kodeunit = js_arg[0].split('.')[3]
			
			arg = "WHERE o.tahun=s.tahun and o.kodeurusan=s.kodeurusan \
					and o.kodesuburusan=s.kodesuburusan and o.kodeorganisasi=s.kodeorganisasi and o.kodeunit=s.kodeunit ) as organisasi,\
					s.deskripsispp as keperluan, \
					(select sum (sr.jumlah) from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp) \
					as jumlah, s.kodeunit, \
					(select kodebidang from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1) \
					as kodebidang, \
					(select kodeprogram from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit  and sr.nospp=s.nospp limit 1) \
					as kodeprogram, \
					(select kodekegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp limit 1) \
					as kodekegiatan, \
					(select kodesubkegiatan from penatausahaan.spprincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and \
					sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nospp=s.nospp limit 1) \
					as kodesubkegiatan FROM penatausahaan.spp \
					s  where s.tahun='"+tahun_log(request)+"' and s.kodeurusan="+kodeurusan+"  and s.kodesuburusan="+kodesuburusan+" and s.kodeorganisasi='"+kodeorganisasi+"' \
					and s.jenisspp='"+js_arg[1]+"' and locked='Y' and s.nospp not in (select nospp from penatausahaan.spm where tahun='"+tahun_log(request)+"' and kodeurusan="+kodeurusan+"  \
					and kodesuburusan="+kodesuburusan+" and kodeorganisasi='"+kodeorganisasi+"' )"
			qry_tbl = "master.master_organisasi o"
			kolom = "s.nospp,s.tglspp as tanggal,(select o.kodeurusan||'.'||o.kodesuburusan||'.'||lpad(o.kodeorganisasi,2,'0')||'.'||o.kodeunit||'-'||o.urai"
			order_by = "ORDER BY nospp, tanggal"
			table_column = 'NOSPP,TANGGAL,ORGANISASI,KEPERLUAN,JUMLAH,KODEUNIT'
			query = "yes"

		elif asal == 'bendahara':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			kodeunit = js_arg[0].split('.')[3]

			arg = "where tahun='"+tahun_log(request)+"' and kodeurusan="+kodeurusan+"  and kodesuburusan="+kodesuburusan+" and kodeorganisasi='"+kodeorganisasi+"' and kodeunit='"+kodeunit+"'"
			qry_tbl = "penatausahaan.spm"
			kolom = "norekbank,bank,npwp,namayangberhak"
			order_by = "ORDER BY nospm"
			table_column = 'NO Rekening,Bank,NPWP,Nama Bendahara'
			query = "yes"

		elif asal == 'rekening':

			arg = "where tahun='"+tahun_log(request)+"' and kodeakun=2 and kodekelompok=1 and kodejenis in (1,3) and koderincianobjek <>0 "
			qry_tbl = "master.master_rekening"
			kolom = "kodeakun||'.'||kodekelompok||'.'||kodejenis||'.'||lpad(kodeobjek::text,2,'0')||'.'||lpad(koderincianobjek::text,2,'0') as rekeningpotongan,urai"
			order_by = "ORDER BY kodeakun"
			table_column = 'NO Rekening,Uraian'
			query = "yes"	
		elif asal == 'lihat_rekening_pendapatan':
			arg = "where tahun='"+tahun_log(request)+"' and kodeakun=4 and kodekelompok=1 AND KODEJENIS<>0 AND KODEOBJEK <> 0 AND KODERINCIANOBJEK <> 0 AND KODESUBRINCIANOBJEK <> 0"
			qry_tbl = "master.master_rekening"
			kolom = "KODEAKUN||'.'||KODEKELOMPOK||'.'||KODEJENIS||'.'||lpad(KODEOBJEK::text,2,'0')||'.'||lpad(KODERINCIANOBJEK::text,2,'0')||'.'||lpad(KODESUBRINCIANOBJEK::text,4,'0') AS KODEREKENING, URAI,0 as JUMLAH"
			order_by = "ORDER BY kodeakun,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK,KODESUBRINCIANOBJEK"
			table_column = 'NO Rekening,Uraian'
			query = "yes"

		elif asal == 'no_ketetapan':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			kodeunit = js_arg[0].split('.')[3]

			arg = "where s.tahun ='"+tahun_log(request)+"' and s.kodeurusan="+kodeurusan+" and s.kodesuburusan="+kodesuburusan+" and s.kodeorganisasi='"+kodeorganisasi+"' and s.kodeunit='"+kodeunit+"' and s.isskpd=1"
			qry_tbl = "penatausahaan.skp s"
			kolom = "S.NOMOR,S.TANGGAL,S.JENIS,S.URAIAN,S.WAJIBBAYAR,(select sum(sr.jumlah) as jumlah from penatausahaan.skp_rincian sr where sr.tahun=s.tahun and sr.kodeurusan=s.kodeurusan and sr.kodesuburusan=s.kodesuburusan and sr.kodeorganisasi=s.kodeorganisasi and sr.kodeunit=s.kodeunit and sr.nomor=s.nomor and sr.isskpd=s.isskpd ),S.ALAMAT,S.NOMORPOKOK"
			order_by = "ORDER BY nomor,tanggal"
			table_column = 'Nomor,Tanggal,Jenis,Uraian,Wajib Bayar,Jumlah'
			query = "yes"
			
		elif asal == 'browse_no_bukti_akrual':
			kodeurusan = js_arg[1].split('.')[0]
			kodesuburusan = js_arg[1].split('.')[1]
			kodeorganisasi = js_arg[1].split('.')[2]
			kodeunit = js_arg[1].split('.')[3]
			xbulan = js_arg[2]

			if js_arg[0]=='2':
				qry_tbl = "akuntansi.fc_akrual_view_transaksi_jurnal('"+tahun_log(request)+"',"+kodeurusan+","+kodesuburusan+",'"+kodeorganisasi+"','"+kodeunit+"',"+xbulan+",0)"
				kolom = "nobukti,jenisbku,nobku,tglbukti,deskripsi,penerima,nominal,ispihakketiga"
				order_by = "ORDER BY tglbukti"
				table_column = 'No. Bukti,Jenis BKU,No. BKU,Tgl. Bukti,Deskripsi,Penerima,Nominal'
				query = "yes"
			elif js_arg[0]=='1':
				arg = "where tahun='"+tahun_log(request)+"' and kodeakun=4 and kodekelompok=1 AND KODEJENIS<>0 AND KODEOBJEK <> 0 AND KODERINCIANOBJEK <> 0"
				qry_tbl = "master.master_rekening"
				kolom = "KODEAKUN||'.'||KODEKELOMPOK||'.'||KODEJENIS||'.'||lpad(KODEOBJEK::text,2,'0')||'.'||lpad(KODERINCIANOBJEK::text,2,'0') AS KODEREKENING, URAI,0 as JUMLAH"
				order_by = "ORDER BY kodeakun,KODEKELOMPOK,KODEJENIS,KODEOBJEK,KODERINCIANOBJEK"
				table_column = 'No Rekening,Uraian'
				query = "yes"

		elif asal == 'lihat_rekening_akrual_skpd':
			kodeurusan = js_arg[0].split('.')[0]
			kodesuburusan = js_arg[0].split('.')[1]
			kodeorganisasi = js_arg[0].split('.')[2]
			kodeunit = js_arg[0].split('.')[3]

			qry_tbl = "akuntansi.fc_akrual_viw_rekening_jurnal('"+tahun_log(request)+"',"+kodeurusan+","+kodesuburusan+",'"+kodeorganisasi+"','"+kodeunit+"')"
			kolom = "koderekening,uraian"
			order_by = ""
			table_column = 'No. Rekening, Uraian'
			query = "yes"

		elif asal == 'ambil_sumdan_':
			kodeurusan = js_arg[1].split('.')[0]
			kodesuburusan = js_arg[1].split('.')[1]
			kodeorganisasi = js_arg[1].split('.')[2]
			kodeunit = js_arg[1].split('.')[3]

			kodebidang = js_arg[0].split('.')[0]+'.'+js_arg[0].split('.')[1]
			kodeprogram = js_arg[0].split('.')[2]
			kodekegiatan = js_arg[0].split('.')[3]+'.'+js_arg[0].split('.')[4]
			kodesubkegiatan = js_arg[0].split('.')[5]
			
			qry_tbl = "SELECT * FROM penatausahaan.load_sumberdanasp2d(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			qry_tbl_argument = [tahun_log(request),kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,kodebidang,kodeprogram,kodekegiatan,kodesubkegiatan]
			
			kolom = "out_kodesumberdana,out_namasumberdana"
			order_by = ""
			table_column = 'KODE SUMBERDANA,URAIAN'
			query = "direct"
			is_safe = True

			
	data = {
		'arg':arg,
		'qry_tbl':qry_tbl,
		'kolom':kolom,
		'group_by':group_by,
		'order_by':order_by,
		'table_column':table_column,
		'query':query,
		'qry_tbl_argument':qry_tbl_argument,
		'is_safe':is_safe,
	}
	return data

def ambil_bendahara(request):
	dataBendahara = ''
	kode_organisasi = request.POST.get('kode_organisasi','')
	if kode_organisasi!='':
		kd_urusan = kode_organisasi.split('.')[0] 
		kd_suburusan = kode_organisasi.split('.')[1]
		kd_organisasi = kode_organisasi.split('.')[2]
		kd_unit = kode_organisasi.split('.')[3]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute('SELECT * FROM master.pejabat_skpd WHERE tahun = %s and kodeurusan = %s \
				and kodesuburusan = %s and trim(kodeorganisasi) = %s and trim(kodeunit) = %s and jenissistem = 2\
				and upper(jabatan) LIKE upper(\'Bendahara Pengeluaran\')',[tahun_log(request),kd_urusan,kd_suburusan,kd_organisasi,kd_unit])			
			dataBendahara = dictfetchall(cursor)
		
	return HttpResponse(json.dumps(dataBendahara))
	
def load_modal(request):
	asal = request.POST.get('asal','')
	js_arg = json.loads(request.POST.get('js_arg'))
	argument = get_arg(request,asal,js_arg)
	list_tbl = ''
	array = []
	arra = []

	if argument['query']=='yes':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT "+argument['kolom']+" FROM "+argument['qry_tbl']+" "+argument['arg']+" "+argument['group_by']+" "+argument['order_by']+"")
			list_tbl = dictfetchall(cursor)
		for x in range(len(list_tbl)):
			array.append([tgl_indo(things) if type(things)==datetime.datetime or type(things)==datetime.date else format_rp(things) if type(things)==decimal.Decimal else str(things) for things in list_tbl[x].values()])

	elif argument['query']=='direct':
		with connections[tahun_log(request)].cursor() as cursor:
			if argument['is_safe']:
				cursor.execute(argument['qry_tbl'], argument['qry_tbl_argument'])
			else:
				cursor.execute(argument['qry_tbl'])
			list_tbl = dictfetchall(cursor)
		for x in range(len(list_tbl)):
			array.append([tgl_indo(things) if type(things)==datetime.datetime or type(things)==datetime.date else format_rp(things) if type(things)==decimal.Decimal else str(things) for things in list_tbl[x].values()])

	data = {
		'list_tbl':list_tbl,
		'array':array,
		'kolom':argument['table_column'].split(','),
	}
	
	return render(request, 'base/modal/load_modal.html',data)


def convert_tuple(arg):
	array = []
	for x in range(len(arg)):
		array.append([str(things) for things in arg[x].values()])
	return array

def select_jabatan_skpd(tabel,field_id,jenissistem,isskpd,tahun):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" WHERE jenissistem='2' and isskpd='0' ",[jenissistem,isskpd])
		hasil = cursor.fetchone()
	return hasil[0]

def select_jabatan_skpkd(tabel,field_id,jenissistem,isskpd,tahun):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" where jenissistem='2' and isskpd='1' ",[jenissistem,isskpd])
		hasil = cursor.fetchone()

	return hasil[0]

# JOEL ADD
# UNTUK MENGAMBIL DATA PPKD/SKPKD
def get_PPKD(request):
	tahun = tahun_log(request)
	ppkd  = ''
	
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||LPAD(kodeorganisasi, 2, '0')AS kode, "\
			"urai FROM master.master_organisasi WHERE tahun = %s and kodeorganisasi <> '' and skpkd=1",[tahun])
		ppkd = dictfetchall(cursor)

	return ppkd
def get_pejabat_pengesah(request):
	tahun = tahun_log(request)

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select id,nama,nip,pangkat,jabatan||' ('||nama||')' AS jabatan1 from master.pejabat_skpkd \
			where tahun = %s and jenissistem = 2 ORDER BY id",[tahun])
		hasil = dictfetchall(cursor)
	
	return hasil

# TAMBAHAN JOEL 25-Jan-2019 ============================================
# untuk cek nomor sp2d sudah ada atau belum 
def ck_no_sp2d(tahun, nosp2d):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT count(nosp2d) AS jml FROM penatausahaan.sp2d \
			WHERE tahun = %s AND UPPER(nosp2d) = %s", [tahun, nosp2d])
		hasil = dictfetchall(cursor)

	for x in hasil:
		cinta = x['jml']

	return cinta

def ck_no_sp2b(tahun, nosp2b):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT count(nosp2d) AS jml FROM penatausahaan.sp2d \
			WHERE tahun = %s AND UPPER(nosp2d) = %s AND sp2b=1", [tahun, nosp2b])
		hasil = dictfetchall(cursor)

	for x in hasil:
		cinta = x['jml']

	return cinta

# JOEL 30 Jan 2019 ================================
# cari tanggal pembuatan sp2d (persetujuan)
def getTgl_sp2d(thn,us_SKPD):
	frm_tgl = []

	if us_SKPD != "":
		ARGTEX = " and kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi||'.'||kodeunit in ("+us_SKPD+")"
	else:
		ARGTEX = ""

	with connections[thn].cursor() as cursor:
		cursor.execute("SELECT DISTINCT tanggal FROM penatausahaan.sp2d \
			WHERE tahun = %s "+ARGTEX+" ORDER BY tanggal DESC",[thn])
		hasil = dictfetchall(cursor)
		
		# UPDATE 15/6/22
		if len(hasil)!=0:
			for x in hasil:
				sexy = {'indo':tgl_indo(x['tanggal']),'todb':tgl_short(tgl_indo(x['tanggal']))}
				frm_tgl.append(sexy)
				
		else:
			tgl_db = datetime.date.today()
			sexy = {'indo':tgl_indo(tgl_db),'todb':tgl_short(tgl_indo(tgl_db))}
			frm_tgl.append(sexy)

	return frm_tgl

# JOEL 31 Jan 2019 ================================
# cari tanggal advis
def getTgl_advis_sp2d(thn):
	frm_tgl = []

	with connections[thn].cursor() as cursor:
		cursor.execute("SELECT DISTINCT tanggal FROM penatausahaan.sp2d WHERE tahun = %s\
			 AND jenissp2d NOT IN ('GU_NIHIL') ORDER BY tanggal DESC",[thn])
		hasil = dictfetchall(cursor)

		for x in hasil:
			sexy = {'indo':tgl_indo(x['tanggal']),'todb':tgl_short(tgl_indo(x['tanggal']))}
			frm_tgl.append(sexy)

	return frm_tgl

# JOEL 19 Feb 2019 ================================
# cari tanggal pembuatan LPJ (persetujuan)
def getTgl_lpj(thn,us_SKPD):
	frm_tgl = []

	if us_SKPD != "":
		ARGTEX = " and kodeurusan||'.'||kodesuburusan||'.'||kodeorganisasi in ("+us_SKPD+")"
	else:
		ARGTEX = ""

	with connections[thn].cursor() as cursor:
		cursor.execute("SELECT DISTINCT tglspj AS tanggal FROM penatausahaan.spj_pkd \
			WHERE tahun = %s "+ARGTEX+" ORDER BY tanggal DESC",[thn])
		hasil = dictfetchall(cursor)

		for x in hasil:
			sexy = {'indo':tgl_indo(x['tanggal']),'todb':tgl_short(tgl_indo(x['tanggal']))}
			frm_tgl.append(sexy)

	return frm_tgl

def ambilsp2d(request):
	hasil = ''
	skpd = request.POST.get('skpd')
	nosp2d = request.POST.get('nosp2d')

	if skpd!='' and nosp2d!='':
		kd_urusan = skpd.split('.')[0]
		kd_suburusan = skpd.split('.')[1]
		kd_organisasi = skpd.split('.')[2]
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.sp2d WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nosp2d = %s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, nosp2d.upper()])
			hasil = dictfetchall(cursor)

	data = {
		'hasilnya':hasil,
	}
	return JsonResponse(data)

def ambilspm(request):
	hasil = ''
	skpd = request.POST.get('skpd')
	nospm = request.POST.get('nospm')
	
	if skpd!='' and nospm!='':
		kd_urusan = skpd.split('.')[0]
		kd_suburusan = skpd.split('.')[1]
		kd_organisasi = skpd.split('.')[2]
		
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.spm WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nospm = %s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, nospm])
			hasil = dictfetchall(cursor)

	data = {
		'hasilnya':hasil,
	}
	return JsonResponse(data)

def ambilBank(request):
	rekening = ''
	koderekening  = request.POST.get('koderekening','')
	if koderekening!= '':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM penatausahaan.sumberdanarekening WHERE rekening =%s",[koderekening])
			rekening = dictfetchall(cursor)
	data = {
		'rekening':rekening,
	}
	return JsonResponse(data)

def ambilKegiatan(request):
	skpd =request.POST.get('skpd','')
	tgl_sp2d =  request.POST.get('tgl_sp2d',tanggal(request)['tglsekarang'])
	nosp2d = request.POST.get('nosp2d','')
	jenis = request.POST.get('jenis','')
	hasil = ''
	print('cek1')
	# koyone ra kanggo
	if skpd!='':
		kdurusan = skpd.split('.')[0]
		kdsuburusan = skpd.split('.')[1]
		kdorganisasi = skpd.split('.')[2]
		kdunit = skpd.split('.')[3]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa, cek FROM penatausahaan.fc_view_sp2d_tu_kegiatan(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nosp2d, '', 0, '0', 0, tgl_to_db(tgl_sp2d), jenis])
			hasil = dictfetchall(cursor)
		print('cekcok')
	data = {
		'hasilnya':convert_tuple(hasil),
	}
	return JsonResponse(data)

def ambilKegiatan_spm(request):
	skpd =request.POST.get('skpd','')
	tgl_spm =  request.POST.get('tgl_spm',tanggal(request)['tglsekarang'])
	nospm = request.POST.get('nospm','')
	jenis = request.POST.get('jenis','')
	hasil = ''
	print('cek2')

	if skpd!='':
		kdurusan = skpd.split('.')[0]
		kdsuburusan = skpd.split('.')[1]
		kdorganisasi = skpd.split('.')[2]
		kdunit = skpd.split('.')[3]
		print(tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospm, '', 0, '0', 0, tgl_to_db(tgl_spm), jenis)
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("""SELECT koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa, cek FROM 
				penatausahaan.fc_view_spm_rincian_to_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",[tahun_log(request), kdurusan, kdsuburusan, kdorganisasi, kdunit, nospm, '', 0, '0', 0, tgl_to_db(tgl_spm), jenis])
			hasil = dictfetchall(cursor)
			print(hasil)
	data = {
		'hasilnya':convert_tuple(hasil),
	}
	return JsonResponse(data)


def ambilRekening(request):
	rekening = ''
	skpd  = request.POST.get('skpd','')
	print('cek 3')
	tgl_sp2d = request.POST.get('tgl_sp2d',tanggal(request)['tglsekarang'])
	tgl_spm = request.POST.get('tgl_spm',tanggal(request)['tglsekarang'])
	nosp2d = request.POST.get('nosp2d','')
	nospm = request.POST.get('nospm','')
	kegiatan = ",".join( repr(e) for e in json.loads(request.POST.get('kegiatan')))
	jenis = request.POST.get('jenis')
	
	if skpd!= '':
		if len(json.loads(request.POST.get('kegiatan')))==0:
			kegiatan = repr('')

		kd_urusan = skpd.split('.')[0]
		kd_suburusan = skpd.split('.')[1]
		kd_organisasi = skpd.split('.')[2]
		kd_unit = skpd.split('.')[3]

		if nospm=='':
			print(kegiatan)
			# 1.01.01.5.2.02.1
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT cek, koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa, sumberdana||'-'||kodesumberdana as sumdan, otorisasi FROM penatausahaan.fc_view_sp2d_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d, '', 0, '0', 0, tgl_to_db(tgl_spm), jenis])
				rekening = dictfetchall(cursor)
		else:
			print(tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nospm, '', 0, 0, 0, tgl_to_db(tgl_spm), jenis)
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT cek, koderekening, uraian, anggaran, batas, lalu, sekarang, jumlah, sisa, sumberdana||'-'||kodesumberdana as sumdan, otorisasi FROM penatausahaan.fc_view_spm_rincian(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nospm, '', 0, '0', 0, tgl_to_db(tgl_spm), jenis])
				rekening = dictfetchall(cursor)

	data = {
		'rekening':convert_tuple(rekening),
	}
	
	return JsonResponse(data)

# def ambilSumberdana(request):
# 	isSimpan = request.POST.get('isSimpan','')
# 	arg = ''
# 	if isSimpan != '':
# 		if isSimpan == 'true':
# 			arg = 'WHERE xkodekegiatan in () and sumberdana is not null'
# 		else:
# 			arg = 'WHERE koderekening in () and sumberdana is not null'

# 		with connections[tahun_log(request)].cursor() as cursor:
# 			cursor.execute("SELECT kodesumberdana, sumberdana from ")
# 	data = {
# 		''
# 	}
# 	return JsonResponse(data)

def ambilSumberDanaAwal(request):
	rekening = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT rekening FROM penatausahaan.sumberdanarekening GROUP BY rekening ")
		rekening = dictfetchall(cursor)
		
	data = {
		'sumdanawal':rekening,	
	}
	return JsonResponse(data)

def check_locked_sp2d(request, skpd, nosp2d):
	hasil_locked = ''
	
	if skpd!='' and nosp2d!='':
		kd_urusan = skpd.split('.')[0]
		kd_suburusan =skpd.split('.')[1]
		kd_organisasi =skpd.split('.')[2]

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT locked FROM penatausahaan.sp2d WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and nosp2d = %s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, nosp2d])
			hasil_locked = cursor.fetchone()
		
	return '0' if hasil_locked==None else hasil_locked[0]

def check_before_sp2d(request, skpd, nosp2d):
	hasil_otorisasi = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT o_otorisasi FROM penatausahaan.")
	return hasil_otorisasi

def get_kodesumdan(request, rekening):
	kodesumdan = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodesumberdana FROM kasda.kasda_sumberdanarekening WHERE rekening = %s", [rekening])
		kodesumdan=cursor.fetchone()
	
	return '0' if kodesumdan==None else kodesumdan[0]

# HAPUS DAN SIMPAN SP2D GU, TU, GU_NIHIL
def hapus_gutugunihil(request):
	hasil = ""
	skpd = request.POST.get('skpd','')
	nosp2d = request.POST.get('nosp2d','')
	if hakakses(request)!='BELANJA':
		if skpd!='' and nosp2d != '':
			kd_urusan = skpd.split('.')[0]
			kd_suburusan = skpd.split('.')[1]
			kd_organisasi = skpd.split('.')[2]
			kd_unit = skpd.split('.')[3]

			if check_locked_sp2d(request, skpd, nosp2d)=='T':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE from penatausahaan.SP2D where tahun=%s\
								and kodeurusan=%s and kodesuburusan=%s\
								and kodeorganisasi=%s and kodeunit=%s and NOSP2D=%s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d])
					cursor.execute("DELETE from penatausahaan.SP2DRINCIAN where tahun=%s\
								and kodeurusan=%s and kodesuburusan=%s\
								and kodeorganisasi=%s and kodeunit=%s and NOSP2D=%s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d])
					hasil = 'Hapus data berhasil.'
	else:
		hasil = 'Anda tidak mempunyai akses untuk menghapus SP2D !, hubungi admin!'
	return HttpResponse(hasil)

def simpan_gutugunihil(request, jenisnya):
	hasil = ''

	skpd = request.POST.get('skpd')
	tgl_sp2d = request.POST.get('tgl_sp2d')
	nosp2d = request.POST.get('nosp2d').upper()
	where_nosp2d = request.POST.get('where_nosp2d').upper()
	nospm = request.POST.get('nospm').upper()
	kegiatan = json.loads(request.POST.get('kegiatan'))
	rinci = json.loads(request.POST.get('rinci'))
	isSimpan = request.POST.get('isSimpan')
	TGLSPM = request.POST.get('TGLSPM')
	jumlahspm = request.POST.get('jumlahspm')
	pemegangkas = request.POST.get('pemegangkas')
	sumberdana = json.loads(request.POST.get('sumberdana'))
	namayangberhak = request.POST.get('namayangberhak')
	triwulan = request.POST.get('triwulan')
	informasi = request.POST.get('informasi')
	deskripsispm = request.POST.get('deskripsispm')
	perubahan = request.POST.get('perubahan')
	statuskeperluan = request.POST.get('statuskeperluan')
	jumlahsp2d = request.POST.get('jumlahsp2d')
	bankasal = request.POST.get('bankasal')
	norekbank = request.POST.get('norekbank')
	norekbankasal = request.POST.get('norekbankasal')
	bank = request.POST.get('bank')
	NPWP = request.POST.get('NPWP')
	lastupdate = tgl_to_db(update_tgl(request)['tglblntahun'])
	sumdan = ','.join(list(set([x.split('-')[0] for x in sumberdana])))
	jumlahperrekening = json.loads(request.POST.get('jumlah'))
	
	if skpd!='':
		kd_urusan = skpd.split('.')[0]
		kd_suburusan = skpd.split('.')[1]
		kd_organisasi = skpd.split('.')[2]
		kd_unit = skpd.split('.')[3]

		if isSimpan=='false':
			if check_locked_sp2d(request, skpd, where_nosp2d)=='T':
				try:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE penatausahaan.SP2D SET\
									 NOSP2D=%s,\
									 TANGGAL=%s,\
									 TANGGAL_DRAFT=%s,\
									 NOSPM=%s,\
									 TGLSPM=%s,\
									 jumlahspm=%s,\
									 pemegangkas=%s,\
									 sumberdana=%s,\
									 namayangberhak=%s,\
									 triwulan=%s,\
									 lastupdate=%s,\
									 informasi=%s,\
									 deskripsispm=%s,\
									 perubahan=%s,\
									 statuskeperluan=%s,\
									 jumlahsp2d=%s,\
									 bankasal=%s,\
									 norekbank=%s,\
									 norekbankasal=%s,\
									 bank=%s,\
									 NPWP=%s\
									 WHERE TAHUN=%s\
									 AND KODEURUSAN=%s\
									 AND KODESUBURUSAN=%s\
									 AND KODEORGANISASI=%s\
									 AND KODEUNIT=%s\
									 AND NOSP2D=%s",[nosp2d, tgl_to_db(tgl_sp2d), tgl_to_db(tgl_sp2d), nospm, tgl_to_db(TGLSPM), jumlahspm, pemegangkas, sumdan, namayangberhak, triwulan, lastupdate, informasi,
									  deskripsispm, perubahan, statuskeperluan, jumlahsp2d, bankasal, norekbank, norekbankasal, bank, NPWP, tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, where_nosp2d])
						hasil = 'Update SP2D '+jenisnya.upper()+' Berhasil'
				except IntegrityError as e:
					hasil = 'Nomor SPD sudah ada !'
		else:
			try:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.SP2D (tahun,kodeurusan,kodesuburusan,kodeorganisasi,kodeunit,nosp2d,tanggal,tanggal_draft,norekbank,bank,npwp,\
							nospm,tglspm,jumlahspm,pemegangkas,namayangberhak,kodebidang,kodeprogram,kodekegiatan,triwulan,\
							lastupdate,jenissp2d,sumberdana,informasi,deskripsispm,\
							perubahan,rekeningpengeluaran,statuskeperluan,jumlahsp2d,norekbankasal,bankasal,uname ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi,kd_unit, nosp2d, tgl_to_db(tgl_sp2d), tgl_to_db(tgl_sp2d), norekbank, bank, NPWP,
							 nospm, tgl_to_db(TGLSPM), jumlahspm, pemegangkas, namayangberhak, '','0','0', triwulan,
							 lastupdate, jenisnya.upper(), sumdan, informasi, deskripsispm, 
							 perubahan, '1.1.1.01.0 - Kas Daerah', statuskeperluan, jumlahsp2d, norekbankasal, bankasal, username(request)])
					hasil = 'Simpan SP2D '+jenisnya.upper()+' Berhasil'
			except IntegrityError as e:
				hasil = 'Nomor SPD sudah ada !'

		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("DELETE FROM penatausahaan.SP2DRINCIAN\
							WHERE TAHUN=%s\
							AND KODEURUSAN=%s\
							AND KODESUBURUSAN=%s\
							AND KODEORGANISASI=%s\
							AND KODEUNIT=%s\
							AND NOSP2D=%s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, where_nosp2d])
		
			cursor.execute("DELETE FROM penatausahaan.SP2DPOTONGAN\
							WHERE TAHUN=%s\
							AND KODEURUSAN=%s\
							AND KODESUBURUSAN=%s\
							AND KODEORGANISASI=%s\
							AND KODEUNIT=%s\
							AND NOSP2D=%s",[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi, kd_unit, where_nosp2d])
		
		jumlahperrekening = list(dict.fromkeys(jumlahperrekening))
		print(jumlahperrekening)
		for x in jumlahperrekening:
			objek1 = x.split('^')[0].split('-')[0].split('.')
			objek2 = x.split('^')[0].split('-')[1].split('.')
			sekarang = x.split('^')[1]
			anggaran = x.split('^')[2]
			otorisasi = x.split('^')[3]
			print(objek2)
			# ['0000', '1', '01', '01', '5', '2', '02', '1']
			# ['5', '1', '2', '01', '01', '52']
			if float(sekarang)>0 and otorisasi!='0':
				
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO penatausahaan.SP2DRINCIAN (TAHUN,KODEURUSAN,KODESUBURUSAN,KODEORGANISASI,KODEUNIT,NOSP2D,\
                   			KODEBIDANG,KODEPROGRAM,KODEKEGIATAN,KODESUBKEGIATAN,KODESUBKELUARAN,KODEAKUN,KODEKELOMPOK,KODEJENIS,KODEOBJEK,\
                   			KODERINCIANOBJEK,KODESUBRINCIANOBJEK,TANGGAL,JUMLAH) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),
                   			kd_urusan, kd_suburusan, kd_organisasi, kd_unit, nosp2d, objek1[1]+'.'+objek1[2], objek1[4], objek1[5]+'.'+objek1[6], objek1[7], 0,
                   			objek2[0], objek2[1], objek2[2], objek2[3], objek2[4],objek2[5], tgl_to_db(tgl_sp2d), sekarang])

	return HttpResponse(hasil)
# END HAPUS DAN SIMPAN SP2D GU, TU, GU_NIHIL

# LAPORAN TU, GU, GU_NIHIL
def render_cetak_sp2dgu_tu_nihil(request):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("select id,nama,nip,pangkat, jabatan||' ('||nama||')' AS jabatan1 from master.pejabat_skpkd\
						where tahun=%s and jenissistem=2",[tahun_log(request)])
		hasil_pejabat = dictfetchall(cursor) 
	data = {
		'pejabat':hasil_pejabat,
	}
	return render(request, 'sp2d/modal/laporan_gu.html', data)

def get_sumdan_laporan(request,no_sp2d):
	sumdan = ''
	kode_sumdan = ''
	if no_sp2d!='':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT sumberdana FROM penatausahaan.sp2d WHERE nosp2d = %s",[no_sp2d])
			query = cursor.fetchone()[0]
		if(query==None):
			sumdan = None
		else:
			try:
				kode_sumdan = int(query)
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT urai FROM master.master_sumberdana WHERE kodesumberdana = %s",[query])
					sumdan = cursor.fetchone()[0]
			except ValueError:
				sumdan = query
	return sumdan

def cetak_sp2dgu_tu_nihil(request):
	post 	= request.POST
	lapParm = {}
	skpd 	= post.get('skpd').split('.')
	no_sp2d = post.get('no_sp2d')
	tgl_sp2d = post.get('tgl_sp2d')
	nama = post.get('nama')
	nip = post.get('nip')
	pangkat = post.get('pangkat')
	id_jabatan = post.get('id_jabatan')
	print (id_jabatan) 
	
	lapParm['file'] = 'penatausahaan/sp2d/sp2d.fr3'	
	lapParm['tahun'] = "'"+tahun_log(request)+"'"
	lapParm['nosp2d'] ="'"+no_sp2d+"'"
	lapParm['kodeurusan'] = "'"+skpd[0]+"'"
	lapParm['kodesuburusan'] = "'"+skpd[1]+"'"
	lapParm['kodeorganisasi'] = "'"+skpd[2]+"'"
	lapParm['kodeunit'] = "'"+skpd[3]+"'"
	lapParm['id'] = "'"+id_jabatan+"'"
	lapParm['sumberdana'] = "'"+str(get_sumdan_laporan(request,no_sp2d))+"'"
	lapParm['report_type'] = 'pdf'

	# http://localhost/sipkd_deiyai/report/?tahun=2016&file=spd/SPD.fr3&report_type=pdf&KodeUrusan='1'&KodeSubUrusan='1'&KodeOrganisasi='01'&NOMER='0001/SPD/1/2016'&ID=3

	return HttpResponse(laplink(request, lapParm))
# END LAPORAN TU, GU, GU_NIHIL

def hakakses_user(request, user):
	hasil = ''
	array = []
	hakakses = ''
	kode = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM apbd.fc_angg_view_organisasi_hakakses(%s,%s)",[tahun_log(request), user])
		hasil = dictfetchall(cursor)
	
	for x in range(len(hasil)):
		array.append(str(hasil[x]['output'])) 

	kode = ','.join('\''+dftr+'\'' for dftr in array)

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT HAKAKSES from penatausahaan.pengguna where uname =%s",[user])
		hakakses = cursor.fetchone()[0]

	data = {
		'hakakses':hakakses,
		'kode':kode,
	}
	return data

# JOEL 03 Mei 2019 ==========================================================
# format Uang, Tanggal array ================================================
def ArrayFormater(arrTBL):
	xxaray 	= []
	xyaray 	= []
	esse 	= []
	for dt in arrTBL:
		for key,val in arrTBL[0].items():
			xxaray.append(key)
		for x in xxaray: 
			if x not in esse: esse.append(x)
		for i in range(len(esse)):
			if type(dt[esse[i]]) == decimal.Decimal: dt[esse[i]] = format_rp(dt[esse[i]])
			else: dt[esse[i]] = dt[esse[i]]
			if type(dt[esse[i]]) == datetime.datetime or type(dt[esse[i]]) == datetime.date: dt[esse[i]] = tgl_indo(dt[esse[i]])
			else: dt[esse[i]] = dt[esse[i]]
			dt[esse[i]] = dt[esse[i]] if dt[esse[i]] != None else '0,00'
		xyaray.append(dt)

	return xyaray

# JOEL 06 MEI 2019 ========================================================
# cek LOCK sebelum simpan dan hapus =======================================
def cek_isLocked(tahun_x,nosp2d_x,skpd0,skpd1,skpd2,skpd3):
	with connections[tahun_x].cursor() as cursor:
		cursor.execute("SELECT locked FROM penatausahaan.sp2d WHERE tahun = %s AND nosp2d = %s \
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s  ",
			[tahun_x,nosp2d_x,skpd0,skpd1,skpd2])
		hasil = cursor.fetchone()[0]
def cek_isLocked_sp2b(tahun_x,nosp2b,skpd0,skpd1,skpd2,skpd3):
	with connections[tahun_x].cursor() as cursor:
		cursor.execute("SELECT locked FROM penatausahaan.sp2b WHERE tahun = %s AND nosp2b = %s \
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s  ",
			[tahun_x,nosp2b,skpd0,skpd1,skpd2])
		hasil = cursor.fetchone()[0]

def modal_search_rekening(request):
	data = {
		
	}
	return render(request, 'base/modal/modal_search_rekening.html', data)

# JOEL 09 MEI 2019 =======================================================
# cek STATUS spj_pkd =====================================================
def cek_spj_status(tahun,nospj,skpd0,skpd1,skpd2):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT status FROM penatausahaan.spj_pkd WHERE tahun = %s AND nospj = %s \
			AND kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi = %s", [tahun,nospj,skpd0,skpd1,skpd2])
		hasil = cursor.fetchone()[0]
	return hasil

# JOEL 16 Mei 2019 ======================================================
# cek nomor SKP/SKR
def ck_nomorSKP(tahun, nomorSKP):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT count(nomor) as jml FROM penatausahaan.skp \
			WHERE tahun = %s AND UPPER(nomor) = %s ", [tahun, nomorSKP])
		hasil = dictfetchall(cursor)
	lope = hasil[0]['jml']

	return lope

# JOEL 29 April 2021 ===================================================
# cek otomatis nomer buku kas (KASDA)
def cek_kasda_autoNoKas(request):
	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT hasil FROM kasda.fc_otomatis_kasda(%s)", [tahun_log(request)])
		hasil = cursor.fetchone()

	return hasil

def put_kasda_sumberdana(request):
	hasil = ''
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT urut, kodesumberdana, urai, rekening as norek,\
			case when namarekening is not null then rekening||' ('||namarekening||')' \
			else rekening||' (Nama Rekening Belum Diseting)' end as rekening FROM kasda.KASDA_SUMBERDANAREKENING \
			WHERE KODESUMBERDANA <> 99 ORDER BY KODESUMBERDANA")
		hasil = dictfetchall(cursor)

	return hasil

def cek_noBukti(tahun,nobukti):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT COUNT(nobukti) as jml FROM kasda.kasda_transaksi \
			WHERE tahun = %s AND UPPER(nobukti) = %s ", [tahun, nobukti])
		hasilx = dictfetchall(cursor)
	lope = hasilx[0]['jml']
	return lope
	
def cek_kasda_isLocked(tahun,nobukas,nobukti):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT locked FROM kasda.kasda_transaksi WHERE \
			tahun = %s AND nobukukas = %s AND nobukti = %s", [tahun,nobukas,nobukti])
		hasil = cursor.fetchone()[0]

	return hasil

def convert_datatable(data_db,yg_mau_ditampilkan):
	array = []
	for y in range(len(data_db)):
		array.append([])
		for x in yg_mau_ditampilkan:
			array[y].append(data_db[y][x])
	return array

def cek_NoBuKas(tahun,nobukas):
	with connections[tahun].cursor() as cursor:
		cursor.execute("SELECT COUNT(nobukukas) as jml FROM kasda.kasda_transaksi \
			WHERE tahun = %s AND UPPER(nobukukas) = %s ", [tahun, nobukas])
		hasilx = dictfetchall(cursor)
	lope = hasilx[0]['jml']
	return lope

def generate_no(request, tahun, modul, kodeurusan = None, kodesuburusan = None, kodeorganisasi = None, kodeunit = None, jenis_modul = None, bulan = None):
    x_nomor_spd = ''
    if bulan is None or bulan == '':
        bulan = tanggal(request)['bulan_angka']

    try:
    	kodeurusan = int(kodeurusan)
    except Exception as e:
    	kodeurusan = 0

    try:
    	kodesuburusan = int(kodesuburusan)
    except Exception as e:
    	kodesuburusan = 0

    with connections[tahun_log(request)].cursor() as cursor:
        cursor.execute("SELECT hasil FROM penatausahaan.fc_penomoran_otomatis_spd_spp_spm_sp2d(%s,%s,%s,%s,%s,%s,%s,%s)",[tahun, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, int(bulan), modul, jenis_modul])
        x_nomor_spd = cursor.fetchone()[0]
        
    return x_nomor_spd

def generate_nomor_auto(request):
	modul = request.GET.get('modul')
	kodeurusan = request.GET.get('kodeurusan')
	kodesuburusan = request.GET.get('kodesuburusan')
	kodeorganisasi = request.GET.get('kodeorganisasi')
	kodeunit = request.GET.get('kodeunit')
	jenis_modul = request.GET.get('jenis_modul')
	bulan = request.GET.get('bulan')
	tahun = request.GET.get('tahun')

	data = {'x_nomor_spd':generate_no(request, tahun, modul, kodeurusan, kodesuburusan, kodeorganisasi, kodeunit, jenis_modul, bulan)}

	return JsonResponse(data)