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

def report_template(request):
	kolom_organisasi = ''
	kolom_peraturan = ''
	kolom_rancangan = ''
	kolom_nomor = ''
	kolom_periode_skpd = ''
	kolom_sesuai = ''
	kolom_belanja_pendapatan = ''
	kolom_realisasi = ''
	kolom_periode = ''
	if (tahun_log(request)):
		skpd = set_organisasi(request)

		kolom_organisasi ='<div class="form-group batas-bawah">'\
						'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-2 batas-atas">Organisasi</div>'\
						'<div class="col-xs-12 col-sm-7 col-md-7 col-lg-8">'\
						'<div class="input-group">'\
						'<input type="text" readonly="readonly" disabled="disabled" class="form-control input-sm" id="kd_org" value="">'\
						'<input type="hidden" id="kd_org2" value=""><input type="hidden" id="kd_org2_urai" value="">'\
						'<span class="input-group-addon btn btn-primary" onclick="showModal(this,\'list_org\')" title="Cari Data" alt="'+reverse('sipkd:list_organisasi')+'" id="cari_data_organisasi">'\
						'<i class="fa fa-binoculars"></i></span>'\
						'</div>'\
						'</div>'\
						'<div class="col-xs-12 col-sm-2 col-md-2 col-lg-2" id="kolom_checkbox">'\
						'<label><input type="checkbox" id="skpkd_checked" onclick="getCekedPPKD(this)" disabled="">&nbsp;IS PPKD'\
						'</label>'\
						'<input type="hidden" class="hidden" name="is_skpkd">'\
						'</div>'\
						'</div>'
		kolom_peraturan = '<div class="kotakan" id="kolom_peraturan">'\
						'<div class="form-group batas-bawah">'\
						'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">Jenis Peraturan</div>'\
						'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">'\
						'<input type="radio" name="radio_peraturan" id="peraturan_daerah" value="0" checked> Peraturan Daerah'\
						'</div>'\
						'<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 batas-atas">'\
						'<input type="radio" name="radio_peraturan" id="peraturan_bupati" value="1"> Peraturan Bupati'\
						'</div>'\
                        '</div></div>'
		kolom_rancangan = '<div class="kotakan" id="kolom_rancangan">'\
					'<div class="form-group batas-bawah">'\
					'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">Jenis Rancangan</div>'\
					'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">'\
					'<input type="radio" name="radio_rancangan" id="rancangan_peraturan" value="0" checked> Rancangan Peraturan'\
					'</div>'\
					'<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 batas-atas">'\
					'<input type="radio" name="radio_rancangan" id="penetapan_peraturan" value="1"> Penetapan Peraturan'\
					'</div>'\
					'</div>'\
					'</div>'
		kolom_nomor = '<div class="form-group form-group-small">'\
					'<span for="nama_pengguna" class="col-xs-12 col-sm-2 col-md-2 col-lg-2 control-label">Nomor</span>'\
					'<div class="col-xs-12 col-sm-10 col-md-4 col-lg-4">'\
					'<input type="text" class="form-control input-sm input-kecil" placeholder="Nomor Peraturan" id="nomor_peraturan" name="nomor_peraturan"></div>'\
					'<span for="peraturan_tgl" class="col-xs-12 col-sm-2 col-md-3 col-lg-3 control-label">Tanggal Peraturan</span>'\
					'<div class="col-xs-5 col-sm-5 col-md-3 col-lg-3" style="padding:0px;">'\
					'<div class="input-group">'\
					'<input type="text" class="form-control input-kecil" value="'+tanggal(request)['tgl_login']+'" placeholder="Tanggal" id="peraturan_tgl" name="peraturan_tgl" style="cursor: pointer;" readonly>'\
					'<label class="input-group-addon addon-kecil" for="peraturan_tgl" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label>'\
					'</div></div></div>'
		kolom_periode_skpd = '<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 batas-atas">'\
							'<div class="col-xs-12 col-sm-12 col-md-2 col-lg-2 batas-atas">Periode</div>'\
							'<div><div class="col-xs-5 col-sm-5 col-md-4 col-lg-4" style="padding:0px;"><div class="input-group">'\
							'<input type="text" class="form-control input-kecil" value="'+tanggal(request)['awal_tahun']+'" placeholder="Tanggal SPM" id="periode_tgl1" name="periode_tgl1" style="cursor: pointer;" readonly>'\
							'<label class="input-group-addon addon-kecil" for="periode_tgl1" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label></div></div>'\
							'<div class="col-xs-2 col-sm-2 col-md-2 col-lg-2 batas-atas" align="center">s/d</div><div class="col-xs-5 col-sm-5 col-md-4 col-lg-4" style="padding:0px;"><div class="input-group">'\
							'<input type="text" class="form-control input-kecil" value="'+tanggal(request)['tgl_login']+'" placeholder="Tanggal SPM" id="periode_tgl2" name="periode_tgl2" style="cursor: pointer;" readonly>'\
							'<label class="input-group-addon addon-kecil" for="periode_tgl2" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label></div></div></div></div>'\
							'<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 batas-atas"><div class="col-xs-12 col-sm-12 col-md-2 col-lg-2 batas-atas">Tanggal Cetak</div><div class="col-xs-12 col-sm-10 col-md-4 col-lg-4">'\
							'<div class="input-group"><input type="text" class="form-control input-kecil" value="'+tanggal(request)['tgl_login']+'" placeholder="Tanggal SPM" id="tanggal_cetak" name="tanggal_cetak" style="cursor: pointer;" readonly> <label class="input-group-addon addon-kecil" for="tanggal_cetak" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label>'\
							'</div></div>'\
							'</div>'
		kolom_sesuai = '<div class="kotakan" id="kolom_sesuai"><div class="form-group batas-bawah"><div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">Sesuai</div>'\
					'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas"><input type="radio" name="radio_sesuai" id="sesuai_sap" value="0" checked> Sesuai SAP </div>'\
					'<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 batas-atas"><input type="radio" name="radio_sesuai" id="sesuai_permen59" value="1"> Sesuai Permen 59</div></div></div>'
		kolom_belanja_pendapatan = '<div class="kotakan" id="kolom_belanja_pendapatan">'\
								'<div class="col-xs-12 col-sm-12 col-md-2 col-lg-2 batas-atas"></div>'\
								'<div class="form-group batas-bawah">'\
								'<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas"><input type="radio" name="radio_belanja_pendapatan" id="belanja" value="0" checked> Belanja </div>'\
								'<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 batas-atas"><input type="radio" name="radio_belanja_pendapatan" id="pendapatan" value="1"> Pendapatan'\
								'</div></div></div>'
		kolom_realisasi = '<div class="kotakan" id="kolom_realisasi"><div class="form-group batas-bawah">'\
			                    '<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas">Realisasi Berdasarkan</div>'\
			                    '<div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 batas-atas"><input type="radio" name="radio_realisasi" id="realisasi_spj" value="0" checked> SPJ </div>'\
								'<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 batas-atas"><input type="radio" name="radio_realisasi" id="realisasi_sp2d" value="1"> SP2D'\
								'</div></div></div>'
		kolom_periode = '<div class="kotakan" id="kolom_periode"><div class="form-group batas-bawah" id="col_periode">'\
        				'<div class="col-xs-12 col-sm-12 col-md-2 col-lg-2 batas-atas">Periode</div><div class="col-xs-12 col-sm-12 col-md-10 col-lg-10"><div>'\
        				'<div class="col-xs-5 col-sm-5 col-md-5 col-lg-5" style="padding:0px;"><div class="input-group">'\
        				'<input type="text" class="form-control input-kecil" value="'+tanggal(request)['awal_tahun']+'" placeholder="Tanggal SPM" id="periode_tgl1" name="periode_tgl1" style="cursor: pointer;" readonly>'\
        				'<label class="input-group-addon addon-kecil" for="periode_tgl1" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label></div></div>'\
        				'<div class="col-xs-2 col-sm-2 col-md-2 col-lg-2 batas-atas" align="center">s/d</div><div class="col-xs-5 col-sm-5 col-md-5 col-lg-5" style="padding:0px;">'\
        				'<div class="input-group"><input type="text" class="form-control input-kecil" value="'+tanggal(request)['tgl_login']+'" placeholder="Tanggal SPM" id="periode_tgl2" name="periode_tgl2" style="cursor: pointer;" readonly>'\
        				'<label class="input-group-addon addon-kecil" for="periode_tgl2" style="cursor: pointer;"><i class="fa fa-calendar-o"></i></label></div></div></div></div></div></div>'            

	return {'report_organisasi':kolom_organisasi,'peraturan':kolom_peraturan,'rancangan':kolom_rancangan,'nomor':kolom_nomor,
			'periode_skpd':kolom_periode_skpd,'sesuai':kolom_sesuai,'belanja_pendapatan':kolom_belanja_pendapatan,
			'realisasi':kolom_realisasi,'periode':kolom_periode}

