from sipkd.config import *
from django.db import connection,connections
from django.urls import reverse,resolve
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template import RequestContext
import re
import json

def fungsi_del_update(kdsub1,kdsub2,kdsub3):
	array = {}
	if (kdsub1=='') and (kdsub2=='') and (kdsub3==''):
		array = {'tabel':'','field':'','value':'','tabel_insert':'sub1','field_insert':'','value_insert':'','max_insert':'kodesub1','field_insert2':'kodesub1,'}
	elif (kdsub2=='') and (kdsub3==''):
		array = {'tabel':'sub1','field':'and kodesub1 = '+kdsub1+'','value':''+kdsub1+',','tabel_insert':'sub2','field_insert':'and kodesub1 = '+kdsub1+'','value_insert':''+kdsub1+',','max_insert':'kodesub2','field_insert2':'kodesub1,kodesub2,'}
	elif (kdsub3==''):
		array = {'tabel':'sub2','field':'and kodesub1 = '+kdsub1+' and kodesub2 = '+kdsub2+'','value':''+kdsub1+','+kdsub2+',', 'tabel_insert':'sub3','field_insert':'and kodesub1 = '+kdsub1+' and kodesub2 = '+kdsub2+'','value_insert':''+kdsub1+','+kdsub2+',','max_insert':'kodesub3','field_insert2':'kodesub1,kodesub2,kodesub3,'}
	elif (kdsub1!='') and (kdsub2!='') and (kdsub3!=''):
		array = {'tabel':'sub3','field':'and kodesub1 = '+kdsub1+' and kodesub2 = '+kdsub2+' and kodesub3 = '+kdsub3+'','value':''+kdsub1+','+kdsub2+','+kdsub3+',', 'tabel_insert':'','field_insert':'','value_insert':'','max_insert':'','field_insert2':''}
	return array

def function_load_tree(data):
	root={}
	name_to_node = {}
	links = []
# --------------------------------------------
	get_data 	= data.get('data','')
	get_output 	= data.get('output','')
	get_json_output = data.get('json_output','')
# --------------------------------------------
	for x in range(len(get_data)):
		links.append(tuple(get_data[x][z]for z in get_output))
	
	for x in range(len(links)): 
		dic={}
		
		for b in range(len(get_output)):
			dic[get_output[b]]=links[x][b] 

		parent 		= list(dic.values())[0]
		child 		= list(dic.values())[1]
		urai_child 	= list(dic.values())[2]
		urai_parent = list(dic.values())[3]

		parent_node = name_to_node.get(parent)
		if not parent_node:
			name_to_node[parent] = parent_node = {'text': str(parent)+' - '+str(urai_parent)}
			for b in range(len(get_output)):
				parent_node[get_output[b]]=str(links[x][b]) 
			root = {'hasil':[parent_node]}
		name_to_node[child] = child_node = {'text': str(child)+' - '+str(urai_child)}
		for b in range(len(get_output)):
			child_node[get_output[b]]=str(links[x][b]) 
		parent_node.setdefault('nodes', []).append(child_node)
	# print(json.dumps(root, indent=4))
	return json.dumps(root, indent=4) 

def get_sumberdana():
	list_sumberdana = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodesumberdana,urai FROM master.master_sumberdana group by kodesumberdana order by kodesumberdana")
		list_sumberdana = dictfetchall(cursor)
	return list_sumberdana

def get_kepentingan():
	list_kepentingan = ''

	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT kodekepentingan, urai FROM master.master_kepentingan group by kodekepentingan order by kodekepentingan")
		list_kepentingan = dictfetchall(cursor)
	return list_kepentingan

def get_session_link(request):
	return request.session.get('link')

def print_frm(link,judul,jenis,jenis2,jenis3,request):
	list_sumberdana = get_sumberdana()
	list_kepentingan = get_kepentingan()

	skpd = set_organisasi(request)
	if hakakses(request) != 'OPERATORSKPD':
		buton = '<span class="input-group-addon btn btn-primary" id="search" onclick="showModal(this,\'list_org\')" alt="'+reverse('sipkd:modal_organisasi',args=[0,jenis2])+'">\
				<div title="Cari Data" id="cari_data_organisasi"><i class="fa fa-binoculars"></i></div></span>'
	else:
		buton = '<span class="input-group-addon"><i class="fa fa-binoculars"></i></span>'

	# ---------- LOOPING ----------
	option_sumberdana = '<option value="0.0.0">-- PILIH SUMBERDANA --</option>'
	option_kepentingan = '<option value="0.0.0">-- PILIH KEPENTINGAN --</option>'
	
	for x in list_sumberdana:
		option_sumberdana +='<option value="'+str(x['kodesumberdana'])+'">'+str(x['kodesumberdana'])+' - '+x['urai']+'</option>'
	for x in list_kepentingan:
		option_kepentingan +='<option value="'+str(x['kodekepentingan'])+'">'+str(x['kodekepentingan'])+' - '+x['urai']+'</option>'
	# ---------- END LOOPING ----------

	if (link == 'rkabtlskpd'):
		frm_isian = '<div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
                        <div>Tahun Depan</div>\
                    </div>\
			        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
				        <input type="text" style="text-align:right;" style="display:none;" class="form-control input-sm" placeholder="0,00"\
				        id="tahun_depan" name="tahun_depan" maxlength="50" onfocus="this.value=toAngkaDesimal(this.value)" onblur="this.value=toRp_WithDesimal(this.value)" readonly>\
				    </div>'
	else:
		frm_isian = '<div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
                        <div>Tahun Depan</div>\
                    </div>\
			        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
				        <input type="text" style="text-align:right;" class="form-control input-sm" placeholder="0,00"\
				        id="tahun_depan" name="tahun_depan" maxlength="50" onfocus="this.value=toAngkaDesimal(this.value)" onblur="this.value=toRp_WithDesimal(this.value)" readonly>\
				    </div>'

	form = '<div class="header-konten">\
			    <span style="font-weight:bold;">'+judul+'</span>\
			</div>\
			<div class="isi-konten">\
			    <form action="" method="POST" id="myForm" name="myForm" class="form-horizontal" autocomplete="off">\
			    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="margin-bottom:10px;">\
				<div class="col-xs-12 col-sm-12 col-md-6 col-lg-6" style="padding-left:0px;">\
				<div class="input-group">\
				            <span class="input-group-addon" style="font-weight: bold;font-size: 13px;">Organisasi</span> \
				            <input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="'+skpd["skpd"]+'">\
				            <input type="hidden" id="kd_org2" value="'+skpd["kode"]+'" onchange="pilihOrganisasi(this.value,$(\'#kd_org2_urai\').val(),\''+jenis+'\',\''+jenis2+'\',\''+jenis3+'\')">\
				            <input type="hidden" id="kd_org2_urai" value="'+skpd["urai"]+'">\
				            <input type="hidden" id="jenis" value="'+jenis+'">\
				            <input type="hidden" id="jenis2" value="'+jenis2+'">\
				            <input type="hidden" id="jenis3" value="'+jenis3+'">\
				            <input type="hidden" class="kd_tree" id="kd_tree" value="5 - BELANJA">\
				            '+buton+'\
			            </div>\
			        </div>\
			    </div>\
			    <div style="padding: 0px !important;">\
			    	<input type="hidden" name="count" id="count" value="">\
			        <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4 batas-atas">\
			            <span style="font-weight: bold;">*) Silahkan Klik Kanan Pada Tree Untuk Memunculkan Menu</span>\
			            <div id=scroll_cuy style="background-color: #FFF; width:100%; height:300px; padding:2px 5px; overflow-y: auto; border: 1px solid #E8E8E8;" class="context-menu">\
			                <div id="tree_view"></div>\
			            </div>\
			            <div class="panel-heading" style="background-color:#777; color:#fff; height: 20px; padding: 0;margin-bottom: 5px;">\
                                  <center><b>BELANJA TIDAK LANGSUNG</b></center>\
                      </div>\
                      	<div class="col-xs-12 col-sm-2 col-md-2 col-lg-2 "><b style="font-size: 12px;">Sebelum</b></div>\
                          <div class="col-xs-12 col-sm-3 col-md-2 col-lg-3 "><b style="font-size: 12px;">: Rp</b></div>\
                          <div class="col-xs-12 col-sm-7 col-md-8 col-lg-7 " style="text-align:right;"><b style="font-size: 12px;" id="sebelum">0,00</b></div>\
                          <div class="col-xs-12 col-sm-2 col-md-2 col-lg-2"><b style="font-size: 12px;">Perubahan</b></div>\
                          <div class="col-xs-12 col-sm-3 col-md-1 col-lg-3"><b style="font-size: 12px;">: Rp</b></div>\
                          <div class="col-xs-12 col-sm-7 col-md-7 col-lg-7" style="text-align:right;"> <b style="font-size: 12px;" id="perubahan">0,00</b></div>\
                          <div class="col-xs-12 col-sm-2 col-md-2 col-lg-2"><b style="font-size: 12px;">Selisih</b></div>\
                          <div class="col-xs-12 col-sm-3 col-md-3 col-lg-3"><b style="font-size: 12px;">: Rp</b></div>\
                          <div class="col-xs-12 col-sm-7 col-md-7 col-lg-7" style="text-align:right;"><b style="font-size: 12px;" id="selisih">0,00</b></div>\
			             <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 batas-atas" style="text-align:center; margin-bottom:15px;">\
			                <input type="hidden" onclick="CekShowModal(this,\'tree_btl\')" id="btn_tambah" value="" alt="'+reverse('sipkd:loadmodal_rekening',args=[jenis2])+'">\
			            </div>\
			        </div>\
			        <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8 batas-atas">\
			            <div class="collapse" id="collapseExample">\
			                <div class="form-group inputan">\
			                    <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
			                        <div>Uraian</div>\
			                    </div>\
			                    <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 inputan2">\
			                        <input type="text" class="form-control input-sm" placeholder="Uraian"\
			                        id="uraian" name="uraian" readonly>\
			                    </div>\
			                </div>\
			                <div class="collapse" id="collapseExample2">\
			                    <div class="form-group inputan">\
			                        <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
			                            <div>Volume</div>\
			                        </div>\
			                        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
			                            <input type="text" style="text-align:right;" class="form-control input-sm"\
			                            id="volume" name="volume" maxlength="50" onfocus="this.value=toAngka(this.value)" onblur="this.value=toRp(this.value)" onkeypress="return Angkasaja(event)" oninput="hitungByVolume()">\
			                        </div>\
			                    </div>\
			                    <div class="form-group inputan">\
			                        <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
			                            <div>Satuan</div>\
			                        </div>\
			                        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
			                            <input type="text" class="form-control input-sm"\
			                            id="satuan" name="satuan" maxlength="50">\
			                        </div>\
			                    </div>\
			                    <div class="form-group inputan">\
			                        <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
			                            <div>Harga Satuan</div>\
			                        </div>\
			                        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
			                            <input type="text" style="text-align:right;" class="form-control input-sm"\
			                            id="hrg_satuan" name="hrg_satuan" maxlength="50" onfocus="this.value=toAngkaDesimal(this.value)" onblur="this.value=toRp_WithDesimal(this.value)">\
			                        </div>\
			                    </div>\
			                </div>\
			                <div class="form-group inputan">\
			                    <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">\
			                        <div>Jumlah</div>\
			                    </div>\
			                    <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 inputan2">\
			                        <input type="text" style="text-align:right;" class="form-control input-sm" placeholder="0,00"\
			                        id="jumlah" name="jumlah" maxlength="50" readonly>\
			                    </div>\
			                    <div class="col-xs-1 col-sm-1 col-md-1 col-lg-1">\
			                        <span onclick="klik_kanan(\'update\',\'\')" style="margin-right:5px;"\
			                            class="btn btn-success btn-sm" title="Simpan Data">\
			                            <i class="fa fa-floppy-o"></i>&nbsp;&nbsp;SIMPAN\
			                        </span>\
			                    </div>\
			                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6" id="frm_sumberdana" style="padding-left:20px;">\
			                        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3">\
			                            <div>Sumber Dana</div>\
			                        </div>\
			                        <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">\
			                            <select id="sumberdana" name="sumberdana" style="padding:5px; height:30px; min-width:250px;">\
			                                '+option_sumberdana+'\
			                            </select>\
			                        </div>\
			                    </div>\
			                </div>\
			                <div class="form-group inputan">\
			                    '+frm_isian+'\
			                    <div class="col-xs-1 col-sm-1 col-md-1 col-lg-1"></div>\
			                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6" id="frm_kepentingan" style="padding-left:20px;">\
			                        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3">\
			                            <div>Kepentingan</div>\
			                        </div>\
			                        <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">\
			                            <select id="kepentingan" name="kepentingan" style="padding:5px; height:30px; min-width:250px;">\
			                                '+option_kepentingan+'\
			                            </select>\
			                        </div>\
			                    </div>\
			                </div>\
			            </div>\
			            <table id="tbKodeRekening" class="display responsive nowrap" cellspacing="0" width="100%">\
			                <thead>\
			                    <tr>\
			                        <th rowspan="2" class="rekening">Rekening</th>\
			                        <th rowspan="2" class="uraian-tbl">Urian</th>\
			                        <th colspan="4">Sebelum Perubahan</th>\
			                        <th colspan="4">Setelah Perubahan</th>\
			                        <th rowspan="2">Bertambah/(berkurang)</th>\
			                    </tr>\
			                    <tr>\
			                        <th>Volume</th>\
			                        <th>Satuan</th>\
			                        <th>H.Satuan</th>\
			                        <th>Jumlah</th>\
			                        <th>Volume</th>\
			                        <th>Satuan</th>\
			                        <th class="satuan">H.Satuan</th>\
			                        <th class="jumlah">Jumlah</th>\
			                    </tr>\
			                </thead>\
			                <tbody id="body_table">\
			                </tbody>\
			            </table>\
			        </div>\
			    </div>\
			    </form>\
			</div>'
	return form


def get_data_with_id(tabel,field_id,value,tahun):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM "+tabel+" WHERE "+field_id+"=%s AND tahun = %s",[value,tahun])
		hasil = cursor.fetchone()
	return hasil

def select_max_id(tabel,field_id,tahun):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" WHERE tahun = %s",[tahun])
		hasil = cursor.fetchone()
	return hasil[0]
# tambahan mauludy
def select_max_dana(tabel,field_id):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+"")
		hasil = cursor.fetchone()
	return hasil[0]

def get_data_with_dana(tabel,field_id,value):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM "+tabel+" WHERE "+field_id+"=%s",[value])
		hasil = cursor.fetchone()
	return hasil

def select_jabatan_skpd(tabel,field_id,jenissistem,isskpd):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" WHERE jenissistem='1' and isskpd='0' ",[jenissistem,isskpd])
		hasil = cursor.fetchone()
	return hasil[0]

def select_jabatan_skpkd(tabel,field_id,jenissistem,isskpd):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" where jenissistem='1' and isskpd='1' ",[jenissistem,isskpd])
		hasil = cursor.fetchone()
		print(cursor)
	return hasil[0]

def select_max_suburusan(tabel,field_id,kodeurusan,kodeorganisasi,tahun):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" where kodeurusan =%s AND kodesuburusan<>'0' AND kodeorganisasi='' and tahun = %s ",[kodeurusan,tahun])
		hasil = cursor.fetchone()
	return hasil[0]

def select_max_organisasi(tabel,field_id,kodeurusan,kodesuburusan,kodeorganisasi,tahun):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" where kodeurusan = %s AND kodesuburusan = %s AND kodeorganisasi<>'0' and tahun = %s ",[kodebidang,kodeprogram,kodeorganisasi,tahun])
		hasil = cursor.fetchone()
	return hasil[0]

def select_max_program(tabel,field_id,tahun,kodebidang,kodeprogram):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" WHERE TAHUN =%s AND KODEBIDANG =%s AND KODEPROGRAM = %s AND KODEKEGIATAN ='0'",[tahun,kodebidang,kodeprogram])
		hasil = cursor.fetchone()
	return hasil[0]

def select_max_kegiatan(tabel,field_id,tahun,kodebidang,kodeprogram,kodekegiatan):
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT MAX("+field_id+") FROM "+tabel+" WHERE TAHUN =%s AND KODEBIDANG =%s AND KODEPROGRAM = %s AND KODEKEGIATAN ='0'",[tahun,kodebidang,kodeprogram])
		hasil = cursor.fetchone()
	return hasil[0]
# end tambahan mauludy
def modal_organisasi(request,jenis,jenis2):
	hak_akses = hakakses(request)
	tahun = tahun_log(request)
	uname = username(request)
	list_organisasi = ''
	path=''

	if jenis==0:
		# untuk pra dan rka
		path='modal_listorg.html'
	elif jenis==1:
		# upload
		path='modal_listorgupload.html'


	if jenis2=='skpd':
		if referer(request) not in array_skpd(request):
			return render(request,'base/restricted.html')
		else:
			if hak_akses == 'ADMIN' or hak_akses == 'ADMINANGGARAN':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi, kodeunit, urai FROM master.master_organisasi WHERE tahun = %s and kodeorganisasi <> ''",[tahun])
					list_organisasi = dictfetchall(cursor)
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi, kodeunit, urai FROM view_organisasi_user(%s,%s,%s,1) WHERE pilih=1",[tahun, uname, hak_akses])
					list_organisasi = dictfetchall(cursor)
	elif jenis2=='ppkd':
		if referer(request) not in array_ppkd(request):
			return render(request,'base/restricted.html')
		else:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT kodeurusan,kodesuburusan, LPAD(kodeorganisasi, 2, '0') AS kodeorganisasi, kodeunit, urai FROM master.master_organisasi WHERE tahun = %s and kodeorganisasi <> '' AND skpkd=1",[tahun])
				list_organisasi = dictfetchall(cursor)
	data={
		'list_organisasi':list_organisasi
	}

	return render(request,'base/modal/'+path+'',data)

def cekrekening(request,jenis,jenis2):
	hasil = ''
	status = request.POST.get('status', None)
	action = request.POST.get('action', None)
	
	kdurusan = request.POST.get('kdurusan', None)
	kdsuburusan = request.POST.get('kdsuburusan', None)
	kdorganisasi = request.POST.get('kdorganisasi', None)

	kdakun = request.POST.get('kdakun', None)
	kdkelompok = request.POST.get('kdkelompok', None)
	kdjenis = request.POST.get('kdjenis', None)
	kdobjek = request.POST.get('kdobjek', None)
	kdrincianobjek = request.POST.get('kdrincianobjek', None)	
	kdsub1 = request.POST.get('kdsub1', None)
	kdsub2 = request.POST.get('kdsub2', None)
	kdsub3 = request.POST.get('kdsub3', None)

	sumberdana = request.POST.get('sumberdana', None)
	sumberdana_p = request.POST.get('sumberdana_p', None)
	kodekepentingan = request.POST.get('kodekepentingan', None)

	lock = request.POST.get('lock', None)
	lock_p = request.POST.get('lock_p', None)

	uraian      = request.POST.get('uraian', None)
	urai_tree	= request.POST.get('urai_tree',None)
	volume      = request.POST.get('volume', None)
	satuan      = request.POST.get('satuan', None)
	hrg_satuan  = request.POST.get('hrg_satuan', None)
	jumlah      = request.POST.get('jumlah', None)		
	jumlah_tree = request.POST.get('jumlah_tree', None)
	tahun_depan = request.POST.get('tahun_depan', None)

	tabel_delete = fungsi_del_update(kdsub1,kdsub2,kdsub3)
	nm_tabel = tabel_delete.get('tabel')
	nm_field = tabel_delete.get('field')
	
	nm_tabel_insert = tabel_delete.get('tabel_insert')
	nm_field_insert = tabel_delete.get('field_insert')
	nm_value_insert = tabel_delete.get('value_insert')
	find_max_insert = tabel_delete.get('max_insert')
	nm_field_insert2 = tabel_delete.get('field_insert2')
	status_lock=''
	frm_lanjutan = ''

	if jenis2=='btl':
		lanjutan = ''
		kdbidang=''
		kdprogram=0
		kdkegiatan=0
		l_ra = ''
		l_rea = ''
		l_r1 = ''
		l_re1 = ''
	elif jenis2=='bl':
		lanjutan = request.POST.get('lanjutan', None)
		kdbidang=request.POST.get('kdbidang',None)
		kdprogram=request.POST.get('kdprogram',None)
		kdkegiatan=request.POST.get('kdkegiatan',None)
		l_ra = request.POST.get('jml_lanjutan1','0')
		l_rea = request.POST.get('real_lanjutan1','0')
		l_r1 = request.POST.get('jml_lanjutan2','0')
		l_re1 = request.POST.get('real_lanjutan2','0')

		if lanjutan!='0':
			frm_lanjutan=",L_RA="+l_ra+",L_REA="+l_rea+",L_R1="+l_r1+",L_RE1="+l_re1+""
		else:
			frm_lanjutan=""
# ----------KONDISI UNTUK SCHEMA--------
	schema=''
	if jenis=='bappeda':
		schema='pra_sipkd'
	elif jenis=='angg':
		schema='sipkd'
# ----------KONDISI UNTUK NAMA TABEL----
	nama_tabel=''
	if jenis2=='btl' or jenis2=='bl':
		nama_tabel = jenis+'_belanja'
		
	if perubahananggaran(request) == 1:
		if lock_p=='1':
			status_lock = 'no'
			hasil = 'Tidak diperkenankan menambah, mengedit atau menghapus data, karena sudah disahkan menjadi DPPA. Hubungi Administrator !!!'
		else:
			status_lock = 'yes'
	else:
		if lock=='1':
			status_lock = 'no'
			hasil = 'Tidak diperkenankan menambah, mengedit atau menghapus data, karena sudah disahkan menjadi DPPA. Hubungi Administrator !!!'
		else:
			status_lock = 'yes'

	if status_lock == 'yes':	
		if action=='add':
			if status=='belanja':
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT count(*) as jml FROM "+schema+"."+nama_tabel+" WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodebidang=%s and kodeprogram=%s and kodekegiatan=%s and kodeakun=%s and kodekelompok=%s and kodejenis=%s and kodeobjek=%s and koderincianobjek=%s",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
					jumlah = dictfetchall(cursor)
				for x in jumlah:
					jml = x['jml']
				if jml>=1:
					hasil = 'Kode Rekening Sudah Digunakan !!'
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("INSERT INTO "+schema+"."+nama_tabel+"(tahun, kodeurusan, kodesuburusan, kodeorganisasi,kodebidang,kodeprogram,kodekegiatan,kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, volume, satuan, harga, jumlah, keterangan, volume_p, satuan_p,harga_p, jumlah_p,pengguna) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek,'','',0,0,'','','',0,0,username(request)])
						hasil = 'Data Berhasil Ditambahkan'
				# print(kdurusan+'/'+kdsuburusan+'/'+kdorganisasi+'/'+kdakun+'/'+kdkelompok+'/'+kdjenis+'/'+kdobjek+'/'+kdrincianobjek)
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("SELECT MAX("+find_max_insert+") AS "+find_max_insert+" FROM "+schema+"."+nama_tabel+""+nm_tabel_insert+" WHERE tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodebidang=%s and kodeprogram=%s and kodekegiatan=%s and kodeakun=%s and kodekelompok=%s and kodejenis =%s and kodeobjek =%s and koderincianobjek =%s "+nm_field_insert+"",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
					hasil = dictfetchall(cursor)
				for x in hasil:
					if x[''+find_max_insert+'']==None:
						find_max_insert=1
					else:
						find_max_insert=x[''+find_max_insert+'']+1

				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("INSERT INTO "+schema+"."+nama_tabel+""+nm_tabel_insert+"(tahun, kodeurusan, kodesuburusan, kodeorganisasi,kodebidang,kodeprogram,kodekegiatan,kodeakun, kodekelompok, kodejenis, kodeobjek, koderincianobjek, "+nm_field_insert2+" volume, satuan, harga, jumlah, keterangan, volume_p, satuan_p,harga_p, jumlah_p,urai) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, "+nm_value_insert+" %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek,find_max_insert,0,'',0,0,'','','',0,0,'SUB BARU'])
					hasil = 'Data Berhasil Ditambahkan'	
		elif action=='del':
			# print(action+'/'+status+'/'+kdurusan+'/'+kdsuburusan+'/'+kdorganisasi+'/'+kdakun+'/'+kdkelompok+'/'+kdjenis+'/'+kdobjek+'/'+kdrincianobjek+'/'+kdsub1+'/'+kdsub2+'/'+kdsub3)
			if perubahananggaran(request) == 1:
				if int(jumlah) != 0:
					hasil = 'Tidak diperkenankan menghapus data ! Karena di input sebelum perubahan!'
				else:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("DELETE FROM "+schema+"."+nama_tabel+""+nm_tabel+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s "+nm_field+"",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
						hasil = 'Data Berhasil Dihapus'
			else:
				with connections[tahun_log(request)].cursor() as cursor:
					cursor.execute("DELETE FROM "+schema+"."+nama_tabel+""+nm_tabel+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s "+nm_field+"",[tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
					hasil = 'Data Berhasil Dihapus'
		elif action=='update':
			# print(action+'/'+status+'/'+kdurusan+'/'+kdsuburusan+'/'+kdorganisasi+'/'+kdakun+'/'+kdkelompok+'/'+kdjenis+'/'+kdobjek+'/'+kdrincianobjek+'/'+kdsub1+'/'+kdsub2+'/'+kdsub3+'/'+uraian+'/'+volume+'/'+satuan+'/'+hrg_satuan+'/'+jumlah+'/'+tahun_depan)
			
			if ((kdsub1=='') and (kdsub2=='') and (kdsub3=='')):
				if sumberdana != '' or sumberdana_p != '':
					if perubahananggaran(request)==0:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("UPDATE "+schema+"."+nama_tabel+" SET sumberdana = %s, sumberdana_p = %s, kodekepentingan = %s "+frm_lanjutan+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s",[sumberdana,sumberdana_p,kodekepentingan,tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
							hasil = 'Data Berhasil Diubah'
					elif perubahananggaran(request)==1:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("UPDATE "+schema+"."+nama_tabel+" SET sumberdana_p = %s, kodekepentingan = %s "+frm_lanjutan+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s",[sumberdana_p,kodekepentingan,tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])	
							hasil = 'Data Berhasil Diubah'
				else:
					hasil = 'Sumberdana Tidak Boleh Kosong!'	
			else:
				if perubahananggaran(request)==0:
					with connections[tahun_log(request)].cursor() as cursor:
						cursor.execute("UPDATE "+schema+"."+nama_tabel+""+nm_tabel+" SET volume = %s, satuan = %s, harga = %s, jumlah = %s, volume_p = %s, satuan_p = %s, harga_p = %s, jumlah_p = %s, urai = %s, jumlah_tahun_depan = %s "+frm_lanjutan+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s "+nm_field+"",[volume,satuan,hrg_satuan,jumlah,volume,satuan,hrg_satuan,jumlah,uraian,tahun_depan,tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
						hasil = 'Data Berhasil Diubah'
				elif perubahananggaran(request)==1:
					if ((int(jumlah_tree) != 0) and (urai_tree!=uraian)):
						hasil = 'Tidak diperkenankan merubahan uraian ! Karena di input sebelum perubahan!'
					else:
						with connections[tahun_log(request)].cursor() as cursor:
							cursor.execute("UPDATE "+schema+"."+nama_tabel+""+nm_tabel+" SET volume_p = %s, satuan_p = %s, harga_p = %s, jumlah_p = %s, urai = %s, jumlah_tahun_depan = %s "+frm_lanjutan+" WHERE tahun = %s and kodeurusan = %s and kodesuburusan = %s and kodeorganisasi = %s and kodebidang = %s and kodeprogram = %s and kodekegiatan = %s and kodeakun = %s and kodekelompok = %s and kodejenis = %s and kodeobjek = %s and koderincianobjek = %s "+nm_field+"",[volume,satuan,hrg_satuan,jumlah,uraian,tahun_depan,tahun_log(request),kdurusan,kdsuburusan,kdorganisasi,kdbidang,kdprogram,kdkegiatan,kdakun,kdkelompok,kdjenis,kdobjek,kdrincianobjek])
							hasil = 'Data Berhasil Diubah'
	return HttpResponse(hasil)

def loadmodal_rekening(request,jenis):
	tahun = tahun_log(request)
	list_all = ''

	if jenis=='ppkd':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM sipkd.fc_angg_view_rekening_by_akun(%s) where ( kodeakun = 5 and (kodekelompok in (0,1) and kodejenis not in (1)) ) or (kodeakun=5 and kodekelompok=3)",[tahun])
			list_all = dictfetchall(cursor)
	elif jenis=='skpd':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM sipkd.fc_angg_view_rekening_by_akun(%s) where kodeakun=5 and kodekelompok in (0,1) and kodejenis in (0,1)",[tahun])
			list_all = dictfetchall(cursor)
	elif jenis=='bl':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT * FROM sipkd.fc_angg_view_rekening_by_akun(%s) where kodeakun=5 and kodekelompok in (0,2)",[tahun])
			list_all = dictfetchall(cursor)
	
	data_tree = {'data':list_all,
				 'output':['parent','kode','urai','urai_parent'],
				}
	data = {
		'hasil': function_load_tree(data_tree)
	}
	return render(request, 'base/modal/modal_tree_rekening.html',data)

def modal_shb(request):
	hak_akses = hakakses(request)
	tahun = tahun_log(request)
	uname = username(request)
	list_shb = ''

	if hak_akses == 'ADMIN' or hak_akses == 'ADMINANGGARAN':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT id_shb, jenis_barang, merk, urai, satuan, harga FROM sipkd.ANGG_SHB WHERE tahun = %s ",[tahun])
			list_shb = dictfetchall(cursor)
	else:
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT id_shb, jenis_barang, merk, urai, satuan, harga FROM sipkd.ANGG_SHB WHERE tahun = %s ",[tahun])
			list_shb = dictfetchall(cursor)
	data={
		'list_shb':list_shb
	}
	return render(request,'base/modal/modal_shb.html',data)

def loadtree(request,jenis,jenis2,jenis3):
	kd_urusan = kd_suburusan = kd_organisasi = urai_parent = urai_root = ''
	tahun = tahun_log(request)
	val = request.POST.get('val', None)
	split_val = val.split('.')
	list_all = ''
	schema = ''


	if jenis3=='bappeda':
		schema='pra_sipkd'
	else:
		schema='sipkd'
	for i in range(len(split_val)):
		kd_urusan = split_val[0]
		kd_suburusan = split_val[1]
		kd_organisasi = split_val[2]
	# print(tahun+','+kd_urusan+','+kd_suburusan+','+str(kd_organisasi))
	if jenis=='btl':
		if jenis2=='skpd':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT * FROM "+schema+".fc_"+jenis3+"_view_tree_pra_belanja(%s,%s,%s,%s,0) order by kodeakun",[tahun,kd_urusan,kd_suburusan,str(kd_organisasi)])
				list_all = dictfetchall(cursor)
		elif jenis2=='ppkd':
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("SELECT * FROM "+schema+".fc_"+jenis3+"_view_tree_pra_belanja(%s,%s,%s,%s,1) order by kodeakun",[tahun,kd_urusan,kd_suburusan,str(kd_organisasi)])
				list_all = dictfetchall(cursor)
	
	data_tree = {'data':list_all,
				 'output':['parent','child','urai','urai_parent','jumlah','jumlah_p','selisih','volume','volume_p','satuan','satuan_p','harga','harga_p','sumberdana','kepentingan','tahun_depan','lock','lock_p','xcount'],
				}
	data = {
		'hasil': function_load_tree(data_tree)
	}
	return HttpResponse(data['hasil'])

def loadtabel_upload(request,jenis):
	list_tabel=''
	tr=''
	isitabel_pendapatan = ''
	isitabel_pendapatan_sipkd=''
	isitabel_btl=''
	isitabel_btl_sipkd=''
	isitabel_bl = ''
	isitabel_bl_sipkd=''
	jumlah_pendapatan = 0
	jumlah_pendapatan_sipkd=0
	jumlah_btl=0
	jumlah_btl_sipkd=0
	jumlah_bl = 0
	jumlah_bl_sipkd=0
	
	jml_pendapatan_belum_sah = 0
	jml_btl_belum_sah = 0
	jml_bl_belum_sah = 0
	val = request.POST.get('val', None)
	val2 = val.split('.')
# ----------------------------------
	in_tahun = tahun_log(request)
	in_kodeurusan = val2[0]
	in_kodesuburusan = val2[1]
	in_kodeorganisasi = val2[2]
	if jenis=='skpd':
		in_isskpd = 0
		in_jenis_pendapatan = 1
		in_jenis_btl = 2
	elif jenis=='ppkd':
		in_isskpd = 1
		in_jenis_pendapatan = 4
		in_jenis_btl = 5
# ----------------------------------

# ---------- ISI TABEL BELANJA PENDAPATAN ------------
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kas_pendapatan(%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, in_isskpd]);
		list_tabel_pendapatan = dictfetchall(cursor)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kontrol_sipkd(%s,%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, in_isskpd, in_jenis_pendapatan])
		list_tabel_pendapatan_sipkd = dictfetchall(cursor)
# ---------- ISI TABEL BELANJA TIDAK LANGSUNG ------------
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kas_btl(%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, in_isskpd]);
		list_tabel_btl = dictfetchall(cursor)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kontrol_sipkd(%s,%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, in_isskpd, in_jenis_btl])
		list_tabel_btl_sipkd = dictfetchall(cursor)

# ---------- ISI TABEL BELANJA LANGSUNG ------------
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kas_bl(%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, in_isskpd]);
		list_tabel_bl = dictfetchall(cursor)
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute("SELECT * FROM sipkd.fc_angg_kontrol_sipkd(%s,%s,%s,%s,%s,%s)",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, 0, 3])
		list_tabel_bl_sipkd = dictfetchall(cursor)
	data={
		'list_tabel_pendapatan':list_tabel_pendapatan,
		'list_tabel_pendapatan_sipkd':list_tabel_pendapatan_sipkd,
		'list_tabel_btl':list_tabel_btl,
		'list_tabel_btl_sipkd':list_tabel_btl_sipkd,
		'list_tabel_bl':list_tabel_bl,
		'list_tabel_bl_sipkd':list_tabel_bl_sipkd,
	}
	return JsonResponse(data)

def modalupload(request,jenis):
	tahun = tahun_log(request)
	list_organisasi = ''
	kode = ''
	urai = ''
	skpd = ''
	
	if jenis=='uploadskpd':
		skpd = set_organisasi(request)
		if skpd["kode"] == '': kode = 0
		else: kode = skpd["kode"]

		urai = skpd["urai"]
		skpd = skpd["skpd"]

	elif jenis=='uploadppkd':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("SELECT kodeurusan||'.'||kodesuburusan||'.'||LPAD(kodeorganisasi, 2, '0') AS kode, urai "\
				"FROM master.master_organisasi WHERE tahun = %s and kodeorganisasi <> '' AND skpkd=1",[tahun])
			list_organisasi = dictfetchall(cursor)

		for x in list_organisasi:
			skpd = x["kode"]+" - "+x["urai"]
			urai = x["urai"]
			kode = x["kode"]

	data={'organisasi':skpd,'kd_org':kode,'ur_org':urai}
	
	return render(request,'base/modal/modal_upload_'+jenis+'.html',data)

def render_prog_keg(request):
	kd_org = request.POST.get('val',None)
	jenis = request.POST.get('jenis',None)
	kd_org2 = kd_org.split('.')
	list_program = ''
	isi_drop = '<option value="">Semua Program</option>'
# ----------------------------------
	in_tahun = tahun_log(request)
	in_kodeurusan = kd_org2[0]
	in_kodesuburusan = kd_org2[1]
	in_kodeorganisasi = kd_org2[2]
	in_isskpd = 0
# ----------------------------------
	if jenis == 'prog':
		with connections[tahun_log(request)].cursor() as cursor:
			cursor.execute("select kodebidang||' - '||kodeprogram ||' - '||uraian as xkodeprogram, kodebidang, kodeprogram from sipkd.fc_rka_22_skpd (%s,%s,%s,%s) where kodekegiatan=0",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi])
			list_program = dictfetchall(cursor)
		for x in range(len(list_program)):
			isi_drop += '<option value="'+str(list_program[x]['kodebidang'])+'-'+str(list_program[x]['kodeprogram'])+'">'+list_program[x]['xkodeprogram']+'</option>'
	elif jenis=='keg':
		kdprog = request.POST.get('kdprog',None)
		kdprog2 = kdprog.split('-')
		isi_drop = '<option value="">Semua Kegiatan</option>'

		if kdprog!='':
			kdprog_1 = kdprog2[0].strip()
			kdprog_2 = kdprog2[1].strip()
		
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.execute("select kodekegiatan ||' - '||urai as xkodekegiatan,barulanjutan from sipkd.angg_kegiatan where tahun=%s and kodeurusan=%s and kodesuburusan=%s and kodeorganisasi=%s and kodebidang=%s and kodeprogram=%s and kodekegiatan<>0 order by kodebidang,kodeprogram,kodekegiatan",[in_tahun, in_kodeurusan, in_kodesuburusan, in_kodeorganisasi, kdprog_1, kdprog_2])
				list_program = dictfetchall(cursor)
			for x in range(len(list_program)):
			# print(list_program[0]['xkodekegiatan'])
				isi_drop += '<option value="'+list_program[x]['xkodekegiatan']+'">'+list_program[x]['xkodekegiatan']+'</option>'

	data = {
		'isi_drop': isi_drop,
	}
	return JsonResponse(data)

def upload_praskpd(request):
	combo_org = request.POST.get('organisasi', None)
	cb_jenis = request.POST.getlist('cb_jenis', None)
	pesan = ''
	if combo_org!='--Pilih Organisasi--':
		in_tahun = tahun_log(request)
		in_isskpd = 0
		in_kodeurusan = combo_org.split('.')[0]
		in_kodesuburusan = combo_org.split('.')[1]
		in_kodeorganisasi = str(combo_org.split('.')[2])
		
		if 'cb_pendapatan' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_pendapatan',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		if 'cb_btl' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_btl',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		if 'cb_bl' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_bl',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		pesan = "Upload Data Berhasil"
	else:
		pesan = "Upload Error, Kode Organisasi Kosong !"
	messages.success(request, pesan)
	return redirect('sipkd:index')

def upload_prappkd(request):
	kd_org = request.POST.get('organisasi', None).split('-')[0].strip()
	cb_jenis = request.POST.getlist('cb_jenis', None)
	pesan = ''
	if kd_org!='':
		in_tahun = tahun_log(request)
		in_isskpd = 1
		in_kodeurusan = kd_org.split('.')[0]
		in_kodesuburusan = kd_org.split('.')[1]
		in_kodeorganisasi = str(kd_org.split('.')[2])
		
		if 'cb_pendapatan' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_pendapatan',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		if 'cb_btl' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_btl',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		if 'cb_pembiayaan' in cb_jenis:
			with connections[tahun_log(request)].cursor() as cursor:
				cursor.callproc('pra_sipkd.fc_dump_bappeda_pembiayaan',(in_tahun,in_kodeurusan,in_kodesuburusan,in_kodeorganisasi,in_isskpd))
		pesan = "Upload Data Berhasil"
	else:
		pesan = "Upload Error, Kode Organisasi Kosong !"
	messages.success(request, pesan)
	return redirect('sipkd:index')

def get_pagu_sumberdana(request):
	ret_kode = 0
	ret_pagu = 0
	urai = request.POST.get('urai_sumberdana', '')
	
	kd_urusan = request.POST.get('kd_urusan', '')
	kd_suburusan = request.POST.get('kd_suburusan', '')
	kd_organisasi = request.POST.get('kd_organisasi', '')
	kd_kegiatan = request.POST.get('kd_kegiatan','')

	data = {
		'ret_pagu':hitung_selisih(request,kd_urusan,kd_suburusan,kd_organisasi,kd_kegiatan,urai),
	}
	return JsonResponse(data)

def hitung_selisih(request,kd_urusan,kd_suburusan,kd_organisasi,kd_kegiatan,urai):
	ret_pagu = 0
	with connections[tahun_log(request)].cursor() as cursor:
		cursor.execute('SELECT * FROM sipkd.fc_angg_get_kd_sumberdana(%s,%s,%s,%s,%s,%s)',[tahun_log(request), kd_urusan, kd_suburusan, kd_organisasi,kd_kegiatan, urai])
		ret_pagu = dictfetchall(cursor)
	return ret_pagu